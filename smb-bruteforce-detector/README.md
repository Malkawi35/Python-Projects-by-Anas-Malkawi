# SMB Brute-Force Detection Tool

A defensive tool that parses Windows Security Event Logs for failed SMB
authentication and flags brute-force patterns. Built for cybersecurity coursework.

## What it detects

It looks at **Event ID 4625** failed logons of **logon type 3** (network logons —
the type SMB uses) and raises an alert when either:

- **IP spray:** one source IP fails against *N or more distinct accounts*, or
- **Targeted brute force:** one account fails from *N or more distinct source IPs*.

"Distinct" matters: the tool counts unique counterparts, not raw attempt volume, so
a user fat-fingering their own password 10 times doesn't look like an attack.

## Two ways to run

**Offline (any OS, no admin)** — great for trying it out:

```bash
python smb_bruteforce_detector.py --csv sample_failed_logons.csv
```

**Live (Windows, elevated)** — reads the real Security log:

```bash
python smb_bruteforce_detector.py --window 15 --threshold 5
```

| Flag | Meaning | Default |
|---|---|---|
| `--csv PATH` | Analyze a CSV export instead of the live log | live mode |
| `--threshold N` | Distinct accounts/IPs before flagging | 3 |
| `--window MINUTES` | Only consider the last N minutes of activity | all |
| `--max-events N` | Max events to pull in live mode | 200 |

Exit code is `0` when clear, `2` when threats are found — handy for scripting/alerting.

## Sample output

```
[*] SMB (network) failed-logon events analyzed: 9
[*] Threshold: 3 distinct counterparts

[!] Status: ALERT — 2 suspicious pattern(s) detected!

  [THREAT] Source IP 203.0.113.50 failed against 4 distinct accounts
           Accounts: administrator, backup_svc, jsmith, mjones

  [THREAT] Account 'administrator' failed from 4 distinct source IPs
           Sources: 198.51.100.23, 198.51.100.7, 198.51.100.88, 203.0.113.50
```

## Tests

```bash
python test_smb_bruteforce_detector.py   # or: python -m pytest
```

Covers distinct-counting, logon-type filtering, both detection directions, and an
end-to-end run over the sample CSV.

## How it maps to real defense

This is the logic behind a basic SIEM correlation rule. In production you'd feed
4625 events into a SIEM and alert on the same thresholds; this project demonstrates
the detection reasoning from first principles.
