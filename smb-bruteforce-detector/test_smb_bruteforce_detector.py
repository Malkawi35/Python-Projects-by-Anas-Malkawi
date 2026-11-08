"""Unit tests for the SMB brute-force detector. Run: python -m pytest  (or python test_...py)."""
import smb_bruteforce_detector as d


def _events(pairs, logon_type="3", t="2025-11-01 09:00:00"):
    return [{"time": t, "account": a, "source_ip": ip, "logon_type": logon_type}
            for a, ip in pairs]


def test_ip_spray_flagged():
    # One IP against 3 distinct accounts should trip the default threshold.
    events = _events([("a", "203.0.113.50"), ("b", "203.0.113.50"), ("c", "203.0.113.50")])
    findings = d.detect_brute_force(events, threshold=3)
    assert any(f["type"] == "IP_ATTACK" and f["count"] == 3 for f in findings)


def test_distinct_counting_not_volume():
    # 5 failures but only 2 distinct accounts -> below threshold 3 (regression guard:
    # the earlier version counted raw attempts and would have false-flagged this).
    events = _events([("a", "203.0.113.50")] * 4 + [("b", "203.0.113.50")])
    assert d.detect_brute_force(events, threshold=3) == []


def test_account_from_many_ips_flagged():
    events = _events([("admin", "198.51.100.7"), ("admin", "198.51.100.8"),
                      ("admin", "198.51.100.9")])
    findings = d.detect_brute_force(events, threshold=3)
    assert any(f["type"] == "USER_ATTACK" and f["indicator"] == "admin" for f in findings)


def test_non_network_logons_filtered_out():
    events = _events([("a", "1.1.1.1"), ("b", "1.1.1.1"), ("c", "1.1.1.1")], logon_type="2")
    assert d.filter_events(events, window_minutes=None) == []


def test_sample_csv_end_to_end():
    events = d.load_failed_logins_csv("sample_failed_logons.csv")
    smb = d.filter_events(events, window_minutes=None)
    findings = d.detect_brute_force(smb, threshold=3)
    kinds = {f["type"] for f in findings}
    assert "IP_ATTACK" in kinds    # 203.0.113.50 sprays several accounts
    assert "USER_ATTACK" in kinds  # administrator hit from several IPs


if __name__ == "__main__":
    import sys
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except AssertionError:
            failed += 1
            print(f"FAIL {fn.__name__}")
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
