# Defensive Security & DFIR

Tools for detection, incident response, and threat intelligence.

| Script | Description | Notes |
|---|---|---|
| `scheduled_task_hunter.py` | Inspects Windows scheduled tasks and flags ones whose creator isn't on a trusted publisher allow-list and that launch executables from outside `System32`. | Windows |
| `process_inspector.py` | Enumerates running processes and prints detailed metadata (owner, path, command line, parent, CPU/memory). | Sample output in `process_inspector_sample_output.txt` |
| `dfir_file_integrity_checker.py` | Generates SHA-256 fingerprints of Python files in a directory, then re-checks them later to detect tampering. | Cross-platform |
| `virustotal_lookup.py` | Reputation-checks a file hash or IP via the VirusTotal API v3. | Needs a free VirusTotal API key |
| `cti_breach_report.py` | Fetches breaches added to Have I Been Pwned in the last 7 days and writes a PDF CTI brief. | Sample: `cti_breach_report_sample.pdf` |
| `file_metadata_extractor.py` | Extracts embedded metadata from PDF, Word, and Excel files. | Useful for OSINT / document forensics |
| `phishing_url_classifier.py` | Extracts lexical features from URLs and trains a Random Forest to classify phishing vs. legitimate. | Dataset: UCI PhiUSIIL |

## Setup

API keys are read from environment variables rather than hard-coded. Set them
before running the relevant script:

```bash
export VT_API_KEY="your-virustotal-key"
```
