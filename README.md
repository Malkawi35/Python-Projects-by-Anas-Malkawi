# Python for Cybersecurity — Project Portfolio

**Anas Malkawi** · CompTIA Security+ (SY0-701) · A.A.S. Cybersecurity, Harper College

A collection of Python projects built while studying cybersecurity, ranging from
defensive log analysis and DFIR tooling to supervised recon and authorized
offensive-security lab exercises. Each project is self-contained and documented.

> All offensive tooling here was written for coursework and runs only against lab
> machines I own or was explicitly authorized to test. See the ethics note below.

---

## Featured project — SMB Brute-Force Detection Tool

A defensive tool that parses Windows Security Event Logs, isolates failed SMB
network logons, and flags brute-force patterns (one source hitting many accounts,
or one account hit from many sources) inside a configurable time window.

- **What it shows:** Windows Event Log analysis, detection logic, threat modeling
- **Tech:** Python, `Get-WinEvent`, Event ID 4625 (logon type 3)
- **Runs offline too:** ships with a sample CSV and a `--csv` mode, so a reviewer
  can see it work without a Windows box or admin rights.

→ [`smb-bruteforce-detector/`](smb-bruteforce-detector/)

---

## Projects by area

### 🛡️ Defensive security & DFIR — [`defensive-security/`](defensive-security/)
| Project | What it does |
|---|---|
| `scheduled_task_hunter.py` | Flags suspicious Windows scheduled tasks against an allow-list of trusted publishers |
| `process_inspector.py` | Enumerates running processes and their metadata with `psutil` |
| `dfir_file_integrity_checker.py` | Generates and compares SHA-256 fingerprints to detect file tampering |
| `virustotal_lookup.py` | Queries the VirusTotal API to reputation-check a hash or IP |
| `cti_breach_report.py` | Pulls recent breaches from the Have I Been Pwned API into a PDF CTI brief |
| `file_metadata_extractor.py` | Extracts metadata from PDF, Word, and Excel files |
| `phishing_url_classifier.py` | Trains a Random Forest model on URL features to classify phishing vs. legitimate |

### 🔎 Recon & OSINT — [`recon-osint/`](recon-osint/)
| Project | What it does |
|---|---|
| `nmap_top_ports_scan.py` | Top-ports service/version scan via the nmap library |
| `nmap_vuln_scan.py` | Optional vuln NSE scan, results saved to timestamped JSON |
| `whois_lookup.py` | WHOIS registration lookup for a domain or host |
| `shodan_host_lookup.py` | Pulls host details from the Shodan API |
| `web_scraper.py` | Parses a page with BeautifulSoup and exports fields to CSV |

### ⚠️ Offensive-security labs — [`offensive-security-labs/`](offensive-security-labs/)
Coursework demonstrating attacker techniques for defenders to understand.
**Authorized lab use only.** See [`offensive-security-labs/README.md`](offensive-security-labs/README.md).

### 🐍 Python fundamentals — [`python-fundamentals/`](python-fundamentals/)
Early coursework: a calculator and pseudocode design exercises.

---

## Running the projects

```bash
git clone https://github.com/Malkawi35/python-projects-by-anas-malkawi.git
cd python-projects-by-anas-malkawi
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Several defensive tools (Event Log, process inspection) are Windows-specific and
may need an elevated prompt. Each project folder has its own README with specifics.

---

## Ethics & scope

These projects were built for academic coursework in a controlled lab. Anything
that interacts with a network or a remote host — recon, scanning, and especially
the offensive-security labs — was only ever run against systems I own or had
written authorization to test. Running these tools against systems you do not own
or have permission to test is illegal and unethical. They are published here to
demonstrate learning, not to be pointed at live targets.

## About me

Cybersecurity student focused on defensive security, SOC analysis, and detection
engineering. CompTIA Security+ certified.
📫 [LinkedIn](https://linkedin.com/in/anas-malkawi-47am)
