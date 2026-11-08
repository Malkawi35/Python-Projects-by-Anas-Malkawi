# nmap_port_scanner.py

import nmap3
import json
from datetime import datetime

class NmapPortScanner:
    def port_scan(self, host, vuln: bool = False) -> None:
        """
        Scan the top ports.
        Args:
            host (str): host to scan
            vuln (bool): if True, run nmap's vuln NSE scripts
        """
        nmap = nmap3.Nmap()

        if vuln:

            scan_results = nmap.nmap_version_detection(host, args="--script vuln -Pn")
        else:

            scan_results = nmap.scan_top_ports(host, args= "--top-ports 1024 -Pn")


        print(json.dumps(scan_results, indent=4))

        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_host = host.replace(".", "_").replace("/", "_")
        filename = f"scan_{safe_host}_{ts}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(scan_results, f, indent=4)
        print(f"[+] Results saved to {filename}")


if __name__ == "__main__":
    nmap_scanner = NmapPortScanner()
    Target_IP = input("Enter Target IP: ").strip()
    Vuln = input("Would you like to run nmap's vuln NSE ? (y/n): ").strip().lower()

    use_vuln = (Vuln == "y")


    nmap_scanner.port_scan(Target_IP, use_vuln)
