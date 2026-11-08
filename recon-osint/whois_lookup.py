# whois_script.py

import whois as ws
import json
class WhoisInfo:
    def print_whois_info(self, host):

        """
            host: Host that you want the whois details for.

        """

        whois_info = ws.whois(host)
        with open('whois.json', 'w', encoding='utf-8') as f:
            json.dump(whois_info, f, indent=4, ensure_ascii=False, default=str)
        print(json.dumps(whois_info, indent=4, ensure_ascii=False, default=str))
if __name__ == "__main__":
    target = input("Enter the host you want the whois details for: ").strip()
    whois_info = WhoisInfo()
    whois_info.print_whois_info(target)
