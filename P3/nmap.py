import socket
import sys

target = "www.google.com"

if len(sys.argv) > 1:
    target = sys.argv[1]

def get_ip_address(domain_name):
    try:
        ip_addr = socket.gethostbyname(domain_name)
        return ip_addr
    except socket.gaierror:
        raise "Invalid domain name or DNS lookup failed."

ip_address = get_ip_address(target)
print(f"The IP address of {target} is: {ip_address}")