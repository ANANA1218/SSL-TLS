import ssl
import socket
from OpenSSL import SSL
import nmap

def analyze_ssl_tls(hostname, port=443):
    context = SSL.Context(SSL.SSLv23_METHOD)
    sock = socket.create_connection((hostname, port))
    connection = SSL.Connection(context, sock)
    connection.set_tlsext_host_name(hostname.encode())
    connection.set_connect_state()
    connection.do_handshake()

    cert = connection.get_peer_certificate()
    cipher = connection.get_cipher_name()
    protocol = connection.get_protocol_version_name()

    return {
        "hostname": hostname,
        "port": port,
        "certificate": cert.get_subject().CN,
        "issuer": cert.get_issuer().CN,
        "version": cert.get_version(),
        "cipher": cipher,
        "protocol": protocol
    }

def check_vulnerabilities(result):
    vulnerabilities = []
    
    if result["protocol"] in ["SSLv2", "SSLv3"]:
        vulnerabilities.append("Protocole obsolète détecté")
    
    weak_ciphers = ["RC4", "DES", "MD5"]
    if any(cipher in result["cipher"] for cipher in weak_ciphers):
        vulnerabilities.append("Suite de chiffrement faible détectée")
    
    return vulnerabilities

def generate_report(result, vulnerabilities):
    report = f"""
SSL/TLS Vulnerability Scan Report
---------------------------------
Target: {result['hostname']}:{result['port']}
Certificate: {result['certificate']}
Issuer: {result['issuer']}
Protocol: {result['protocol']}
Cipher Suite: {result['cipher']}

Vulnerabilities:
{chr(10).join('- ' + v for v in vulnerabilities) if vulnerabilities else "Aucune vulnérabilité détectée"}

Recommendations:
- Mettez à jour vers la dernière version de TLS
- Utilisez des suites de chiffrement fortes
- Désactivez les protocoles obsolètes
"""
    return report

def scan_ports(hostname):
    nm = nmap.PortScanner()
    nm.scan(hostname, arguments='-p- --open')
    return nm.all_hosts()

def main():
    hostname = input("Entrez le nom de domaine à scanner : ")
    port = int(input("Entrez le port (443 par défaut) : ") or 443)

    print(f"Analyse de {hostname}:{port}...")
    
    try:
        result = analyze_ssl_tls(hostname, port)
        vulnerabilities = check_vulnerabilities(result)
        report = generate_report(result, vulnerabilities)
        print(report)

        print("Scan des ports ouverts...")
        open_ports = scan_ports(hostname)
        print("Ports ouverts :", open_ports)

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    main()
