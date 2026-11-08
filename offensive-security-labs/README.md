# Offensive-Security Labs

⚠️ **Authorized lab use only.** These scripts were written for cybersecurity
coursework to demonstrate how common attacker techniques work, so that they can be
detected and defended against. They were run exclusively against virtual machines
and lab hosts that I own or was explicitly authorized to test.

**Do not run these against any system you do not own or have written permission to
test.** Unauthorized scanning, access attempts, or traffic generation against
systems you don't control is illegal in most jurisdictions.

These are published to show understanding of the offensive side of security — the
perspective a SOC analyst or detection engineer needs — not as ready-to-use tools.
Target addresses have been replaced with placeholders that you must set yourself.

## Contents

| Script | Technique demonstrated | Defensive takeaway |
|---|---|---|
| `ssh_bruteforce.py` | Password spraying over SSH | Why key-based auth, rate limiting, and fail2ban matter |
| `scheduled_task_persistence.py` | Persistence via Windows scheduled tasks | Pairs with `defensive-security/scheduled_task_hunter.py`, which detects it |
| `fragmented_packet_firewall_test.py` | IP fragmentation to test firewall reassembly | Why firewalls/IDS must reassemble fragments |
| `icmp_fragment_flood.py` | Fragmented ICMP traffic generation | Why rate limiting and anomaly detection matter |
| `msfvenom_payload_generator.py` | Wrapper around Metasploit's `msfvenom` | Why EDR and application allow-listing matter |

Each script requires a target to be configured before it will do anything. They
ship pointed at placeholder/RFC-5737 documentation addresses, not live hosts.
