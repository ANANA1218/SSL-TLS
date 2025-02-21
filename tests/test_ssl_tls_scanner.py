import unittest
from unittest.mock import patch, MagicMock
from ssl_tls_scanner import analyze_ssl_tls, check_vulnerabilities, generate_report, scan_ports

class TestSSLTLSScanner(unittest.TestCase):
    @patch('ssl_tls_scanner.socket.create_connection')
    @patch('ssl_tls_scanner.SSL.Connection')
    def test_analyze_ssl_tls(self, mock_connection, mock_socket):
        mock_socket.return_value = MagicMock()
        mock_connection.return_value = MagicMock()

        mock_connection.return_value.get_peer_certificate.return_value.get_subject.return_value.CN = 'example.com'
        mock_connection.return_value.get_peer_certificate.return_value.get_issuer.return_value.CN = 'CA Authority'
        mock_connection.return_value.get_peer_certificate.return_value.get_version.return_value = 3
        mock_connection.return_value.get_cipher_name.return_value = 'AES256-SHA'
        mock_connection.return_value.get_protocol_version_name.return_value = 'TLSv1.2'

        result = analyze_ssl_tls('example.com', 443)
        self.assertEqual(result['certificate'], 'example.com')
        self.assertEqual(result['issuer'], 'CA Authority')
        self.assertEqual(result['cipher'], 'AES256-SHA')
        self.assertEqual(result['protocol'], 'TLSv1.2')

    def test_check_vulnerabilities(self):
        result = {'protocol': 'SSLv3', 'cipher': 'RC4-MD5'}
        vulnerabilities = check_vulnerabilities(result)
        self.assertIn('Protocole obsolète détecté', vulnerabilities)
        self.assertIn('Suite de chiffrement faible détectée', vulnerabilities)

    def test_generate_report(self):
        result = {'hostname': 'example.com', 'port': 443, 'certificate': 'example.com',
                  'issuer': 'CA Authority', 'protocol': 'TLSv1.2', 'cipher': 'AES256-SHA'}
        vulnerabilities = ['Protocole obsolète détecté']
        report = generate_report(result, vulnerabilities)
        self.assertIn('example.com', report)
        self.assertIn('TLSv1.2', report)
        self.assertIn('Protocole obsolète détecté', report)

    @patch('ssl_tls_scanner.nmap.PortScanner')
    def test_scan_ports(self, mock_nmap):
        mock_nmap_instance = mock_nmap.return_value
        mock_nmap_instance.scan.return_value = None
        mock_nmap_instance.all_hosts.return_value = ['127.0.0.1']

        result = scan_ports('127.0.0.1')
        self.assertEqual(result, ['127.0.0.1'])
