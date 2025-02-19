import ssl
import socket
import struct
from OpenSSL import SSL
import nmap
import os

class SSLScanner:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def analyze(self):
        context = SSL.Context(SSL.SSLv23_METHOD)
        sock = socket.create_connection((self.hostname, self.port))
        connection = SSL.Connection(context, sock)
        connection.set_tlsext_host_name(self.hostname.encode())
        connection.set_connect_state()
        connection.do_handshake()

        cert = connection.get_peer_certificate()
        cipher = connection.get_cipher_name()
        protocol = connection.get_protocol_version_name()

        return {
            "hostname": self.hostname,
            "port": self.port,
            "certificate": cert.get_subject().CN,
            "issuer": cert.get_issuer().CN,
            "version": cert.get_version(),
            "cipher": cipher,
            "protocol": protocol
        }

class VulnerabilityChecker:
    def check(self, result):
        vulnerabilities = []
        
        if result["protocol"] in ["SSLv2", "SSLv3"]:
            vulnerabilities.append("Protocole obsolète détecté")
        
        weak_ciphers = ["RC4", "DES", "MD5"]
        if any(cipher in result["cipher"] for cipher in weak_ciphers):
            vulnerabilities.append("Suite de chiffrement faible détectée")
        
        if self.check_heartbleed(result["hostname"], result["port"]):
            vulnerabilities.append("Vulnérabilité Heartbleed détectée")
        
        if self.check_poodle(result["hostname"], result["port"]):
            vulnerabilities.append("Vulnérabilité POODLE détectée")
        
        return vulnerabilities

    def check_heartbleed(self, hostname, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, port))
        s = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1)
        
        hb = b'\x18\x03\x02\x00\x03\x01\x40\x00'
        s.send(hb)
        
        try:
            data = s.recv(1024)
            if len(data) > 3:
                return True
        except:
            pass
        finally:
            s.close()
        return False

    def check_poodle(self, hostname, port):
        context = SSL.Context(SSL.SSLv23_METHOD)
        context.set_options(SSL.OP_NO_SSLv2 | SSL.OP_NO_TLSv1)
        
        s = socket.create_connection((hostname, port))
        connection = SSL.Connection(context, s)
        connection.set_tlsext_host_name(hostname.encode())
        connection.set_connect_state()
        
        try:
            connection.do_handshake()
            return True
        except SSL.Error:
            return False
        finally:
            connection.close()

class Report:
    def generate(self, result, vulnerabilities):
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
- Appliquez les correctifs de sécurité pour Heartbleed et POODLE si détectés
"""
        return report

class PortScanner:
    def scan(self, hostname):
        nm = nmap.PortScanner()
        nm.scan(hostname, arguments='-p- --open')
        open_ports = []
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    open_ports.append(f"{port}/{proto}")
        return open_ports

class SSLVulnerabilityScanner:
    def __init__(self, hostname, port):
        self.ssl_scanner = SSLScanner(hostname, port)
        self.vuln_checker = VulnerabilityChecker()
        self.report_generator = Report()
        self.port_scanner = PortScanner()

    def run(self):
        try:
            print(f"Analyse de {self.ssl_scanner.hostname}:{self.ssl_scanner.port}...")
            ssl_result = self.ssl_scanner.analyze()
            vulnerabilities = self.vuln_checker.check(ssl_result)
            report = self.report_generator.generate(ssl_result, vulnerabilities)
            print(report)

            print("Scan des ports ouverts...")
            open_ports = self.port_scanner.scan(self.ssl_scanner.hostname)
            print("Ports ouverts :")
            for port in open_ports:
                print(f"- {port}")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

def main():
    hostname = os.environ.get('HOSTNAME', 'example.com')
    port = int(os.environ.get('PORT', 443))
    
    scanner = SSLVulnerabilityScanner(hostname, port)
    scanner.run()

if __name__ == "__main__":
    main()
