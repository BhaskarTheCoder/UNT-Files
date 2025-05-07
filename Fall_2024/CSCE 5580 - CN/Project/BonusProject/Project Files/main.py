# main.py
import socket
import sys
from multithreading_programming_example import run_a_thread, run_threads
from socket_programming_example_client import socket_example_client
from socket_programming_example_server import socket_example_server
from tcp_syn_flood_attack import tcp_syn_flood_attack
from http_flood_attack import start_http_flood_attack

def main():
    # 1. Hello World example
    print("Hello World!")

    # 2. Multi-thread programming examples in Python
    """
    run_a_thread()  # Run a single thread
    run_threads()   # Run multiple threads
    """

    # 3. Socket Programming examples
    # Please use an independent terminal to run main_server.py to start the socket server first.
    #socket_example_server()  # Server side
    #socket_example_client()  # Client side

    # 4. TCP syn flood attack examples
    # Please use an independent terminal to run main_server.py to start the socket server first.
    """
    disPort = 65525
    num_requests = 100000
    disIP = '127.0.0.1'
    tcp_syn_flood_attack(disIP, disPort, num_requests)
    """

    # 5. HTTP flood attack example
    
    start_http_flood_attack()
    

if __name__ == '__main__':
    main()