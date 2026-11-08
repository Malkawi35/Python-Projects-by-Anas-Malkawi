# Recon & OSINT

Reconnaissance and open-source-intelligence scripts. **Run scanning tools
(`nmap_*`, `shodan_*`) only against hosts you own or are authorized to test.**

| Script | Description | Notes |
|---|---|---|
| `nmap_top_ports_scan.py` | Top-1024 service/version scan of a target host. | Prompts for target |
| `nmap_vuln_scan.py` | Optional nmap vuln NSE scan; saves results to timestamped JSON. | Prompts for target |
| `whois_lookup.py` | WHOIS registration details for a domain/host, saved to JSON. | — |
| `shodan_host_lookup.py` | Pulls host details (geo, ports) from the Shodan API. | Needs a Shodan API key |
| `web_scraper.py` | Fetches a page, parses it with BeautifulSoup, exports fields to CSV. | Sample: `web_scraper_sample_output.csv` |

## Setup

```bash
export SHODAN_API_KEY="your-shodan-key"
```
