#!/usr/bin/env python3
"""
SMB Brute-Force Detection Tool
==============================

Parses Windows Security Event Logs for failed network logons (Event ID 4625,
logon type 3 — the type SMB authentication uses) and flags brute-force patterns:

  * one source IP failing against many distinct accounts  (spray / credential stuffing)
  * one account failing from many distinct source IPs      (targeted brute force)

Two modes:
  * Live  (default): reads the local Security log via PowerShell. Windows + admin.
  * Offline (--csv): analyzes a CSV export, so the logic can be reviewed and
    demoed on any OS. A sample file is included: sample_failed_logons.csv

Examples
--------
  python smb_bruteforce_detector.py                       # live, default thresholds
  python smb_bruteforce_detector.py --csv sample_failed_logons.csv
  python smb_bruteforce_detector.py --threshold 5 --window 10
"""

import argparse
import csv
import io
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta

ASCII_ART = r"""
╔════════════════════════════════════════════════════════╗
║           ███████╗███╗   ███╗██████╗                   ║
║           ██╔════╝████╗ ████║██╔══██╗                  ║
║           ███████╗██╔████╔██║██████╔╝                  ║
║           ╚════██║██║╚██╔╝██║██╔══██╗                  ║
║           ███████║██║ ╚═╝ ██║██████╔╝                  ║
║           ╚══════╝╚═╝     ╚═╝╚═════╝                   ║
║     Brute-Force Detection — SMB Authentication Logs    ║
╚════════════════════════════════════════════════════════╝
"""

# Event 4625 logon types that correspond to SMB / network authentication.
NETWORK_LOGON_TYPES = {"3"}


def check_admin() -> bool:
    """Return True if running with Windows admin rights (always False off-Windows)."""
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def fetch_failed_logins_live(max_events: int) -> list[dict]:
    """Pull failed network logons from the local Windows Security log via PowerShell."""
    powershell_cmd = f"""
    Get-WinEvent -FilterHashtable @{{LogName='Security';ID=4625}} -MaxEvents {max_events} |
    Select-Object TimeCreated,
        @{{Name='Account';Expression={{$_.Properties[5].Value}}}},
        @{{Name='SourceIP';Expression={{$_.Properties[19].Value}}}},
        @{{Name='LogonType';Expression={{$_.Properties[10].Value}}}} |
    ConvertTo-Csv -NoTypeInformation
    """
    try:
        result = subprocess.run(
            ["powershell", "-Command", powershell_cmd],
            capture_output=True, text=True, timeout=30,
        )
    except FileNotFoundError:
        print("[!] PowerShell not found — this mode requires Windows. Try --csv instead.")
        return []
    except Exception as e:  # noqa: BLE001
        print(f"[!] Error retrieving logs: {e}")
        return []
    return _parse_csv_text(result.stdout)


def load_failed_logins_csv(path: str) -> list[dict]:
    """Load failed logons from a CSV export (offline mode)."""
    try:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            return _parse_csv_text(fh.read())
    except FileNotFoundError:
        print(f"[!] CSV file not found: {path}")
        return []


def _parse_csv_text(text: str) -> list[dict]:
    """Normalize CSV text (from PowerShell or a file) into a list of event dicts."""
    rows: list[dict] = []
    reader = csv.DictReader(io.StringIO(text.strip()))
    for row in reader:
        # Tolerate differing header casing/whitespace.
        norm = {(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}
        account = norm.get("account", "")
        source_ip = norm.get("sourceip", "")
        if not account or not source_ip or source_ip == "-":
            continue
        rows.append({
            "time": norm.get("timecreated", ""),
            "account": account,
            "source_ip": source_ip,
            "logon_type": norm.get("logontype", "3"),
        })
    return rows


def _parse_time(value: str) -> datetime | None:
    for fmt in ("%Y-%m-%d %H:%M:%S", "%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y %H:%M:%S"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def filter_events(events: list[dict], window_minutes: int | None) -> list[dict]:
    """Keep only SMB/network logons, optionally within the last `window_minutes`."""
    smb = [e for e in events if e["logon_type"] in NETWORK_LOGON_TYPES]
    if not window_minutes:
        return smb
    newest = max((t for e in smb if (t := _parse_time(e["time"]))), default=None)
    if newest is None:
        return smb  # timestamps unparseable; skip windowing rather than drop everything
    cutoff = newest - timedelta(minutes=window_minutes)
    windowed = []
    for e in smb:
        t = _parse_time(e["time"])
        if t is None or t >= cutoff:
            windowed.append(e)
    return windowed


def detect_brute_force(events: list[dict], threshold: int) -> list[dict]:
    """Flag IPs/accounts whose count of *distinct* counterparts meets the threshold."""
    ip_to_accounts: dict[str, set] = defaultdict(set)
    account_to_ips: dict[str, set] = defaultdict(set)

    for e in events:
        ip_to_accounts[e["source_ip"]].add(e["account"])
        account_to_ips[e["account"]].add(e["source_ip"])

    findings = []
    for source_ip, accounts in ip_to_accounts.items():
        if len(accounts) >= threshold:
            findings.append({
                "type": "IP_ATTACK", "indicator": source_ip,
                "count": len(accounts), "details": ", ".join(sorted(accounts)),
            })
    for account, ips in account_to_ips.items():
        if len(ips) >= threshold:
            findings.append({
                "type": "USER_ATTACK", "indicator": account,
                "count": len(ips), "details": ", ".join(sorted(ips)),
            })
    return sorted(findings, key=lambda f: f["count"], reverse=True)


def display_results(findings: list[dict], total: int, threshold: int) -> None:
    print("=" * 70)
    print("[*] SMB BRUTE-FORCE DETECTION REPORT")
    print("=" * 70)
    print(f"[*] SMB (network) failed-logon events analyzed: {total}")
    print(f"[*] Threshold: {threshold} distinct counterparts\n")

    if not findings:
        print("[✓] Status: CLEAR — no brute-force patterns detected")
        print("=" * 70)
        return

    print(f"[!] Status: ALERT — {len(findings)} suspicious pattern(s) detected!\n")
    for f in findings:
        if f["type"] == "IP_ATTACK":
            print(f"  [THREAT] Source IP {f['indicator']} failed against "
                  f"{f['count']} distinct accounts")
            print(f"           Accounts: {f['details']}\n")
        else:
            print(f"  [THREAT] Account '{f['indicator']}' failed from "
                  f"{f['count']} distinct source IPs")
            print(f"           Sources: {f['details']}\n")
    print("=" * 70)
    print("[!] RISK LEVEL: HIGH")
    print("[*] Recommend: enable account lockout, review affected accounts,")
    print("    and block/monitor the flagged source IPs.")
    print("=" * 70)


def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Detect SMB brute-force attacks in Windows Event Logs.")
    p.add_argument("--csv", metavar="PATH",
                   help="analyze a CSV export instead of the live log (works on any OS)")
    p.add_argument("--threshold", type=int, default=3,
                   help="distinct accounts/IPs before flagging (default: 3)")
    p.add_argument("--window", type=int, default=None, metavar="MINUTES",
                   help="only consider events within the last N minutes of activity")
    p.add_argument("--max-events", type=int, default=200,
                   help="max events to pull in live mode (default: 200)")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    print(ASCII_ART)

    if args.csv:
        print(f"[*] Offline mode — reading {args.csv}\n")
        events = load_failed_logins_csv(args.csv)
    else:
        if not check_admin():
            print("[!] Live mode needs Windows administrator privileges.")
            print("[*] Run elevated, or try: --csv sample_failed_logons.csv\n")
            return 1
        print("[✓] Administrator privileges verified")
        print("[*] Scanning Security log for Event ID 4625 (failed logons)...\n")
        events = fetch_failed_logins_live(args.max_events)

    if not events:
        print("[*] No failed-logon events to analyze.")
        return 0

    smb_events = filter_events(events, args.window)
    findings = detect_brute_force(smb_events, args.threshold)
    display_results(findings, len(smb_events), args.threshold)
    return 2 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
