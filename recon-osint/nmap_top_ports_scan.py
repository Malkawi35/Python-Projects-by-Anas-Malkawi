import nmap3
import json
class NmapPortScanner:
    def port_scan(self, host) -> None:
        """
         Scan the top ports.
         Args:
        host (str): host to scan
        """
        nmap = nmap3.Nmap()
# Perform nmap's top ports scan. By default the number is set to 10 which can be increased adding a parameter
# "default=<number", where <number> is the number of top ports you want to scan.
        scan_results = nmap.nmap_version_detection(host, args="--top-ports 1024 -Pn")
        print(json.dumps(scan_results, indent=4))
if __name__ == "__main__":
    nmap_scanner = NmapPortScanner()
    target = input('Enter target IP/host (must be authorized): ').strip()
    nmap_scanner.port_scan(target)
