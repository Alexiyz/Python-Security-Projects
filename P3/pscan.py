import nmap
import socket


nm = nmap.PortScanner()
options = "-sV -sC scan_results"
# Practice website, authorized for port scanning testing
target = "scanme.nmap.org"

def get_ip_address(domain_name):
    try:
        ip_address = socket.gethostbyname(domain_name)
        return ip_address
    except socket.gaierror:
        print("Invalid domain name or DNS lookup failed.")
        exit(1)

ip_address = get_ip_address(target)
print(f"The IP address of {target} is found to be {ip_address}")

nm.scan(target, arguments=options)

for host in nm.all_hosts():
    print("Host: %s (%s)" % (host, nm[host].hostname()))
    print("State: %s" % nm[host].state())
    for protocol in nm[host].all_protocols():
        port_info = nm[host][protocol]
        for port, state in port_info.items():
            print("Port: %s\tState: %s" % (port, state))
