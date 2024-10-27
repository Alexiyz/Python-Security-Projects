import socket
import sys


def whois(domain: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("whois.iana.org", 43)) # RFC 3912: A WHOIS server listens on TCP port 43 for requests
    s.send(f"{domain}\r\n".encode())
    response = s.recv(4096).decode()
    s.close()
    return response

lookup = "google.com"

if len(sys.argv) > 1:
    target = sys.argv[1]

print(whois(lookup))