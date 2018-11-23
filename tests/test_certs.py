import io
import sys
import unittest
import certs
from OpenSSL import crypto

class TestCerts(unittest.TestCase):

  def setUp(self):
    self.user_csr = open('./tests/ca/user.csr')
    self.user_key = open('./tests/ca/user.key')
    self.ca_crt_file = open('./tests/ca/ca.crt')
    self.ca_key_file = open('./tests/ca/ca.key')

  def tearDown(self):
    self.user_csr.close()
    self.user_key.close()
    self.ca_crt_file.close()
    self.ca_key_file.close()

  def test_sign_req_invalid_ca_crt(self):
    bad_crt = io.BytesIO()
    bad_crt.write(b'bad_crt')
    bad_crt.seek(0)
    self.assertRaises(certs.InvalidCertificateAuthorityCertificate, certs.sign_req, bad_crt, self.ca_key_file, None, None)

  def test_sign_req_invalid_ca_key(self):
    bad_key = io.BytesIO()
    bad_key.write(b'bad_key')
    bad_key.seek(0)
    self.assertRaises(certs.InvalidCertificateAuthorityPrivateKey, certs.sign_req, self.ca_crt_file, bad_key, None, None)

  def test_sign_req_invalid_req(self):
    bad_req = io.BytesIO()
    bad_req.write(b'bad_req')
    bad_req.seek(0)
    self.assertRaises(certs.InvalidCertificateRequest, certs.sign_req, self.ca_crt_file, self.ca_key_file, bad_req, None)

  def test_sign_req(self):
    cert_file = certs.sign_req(self.ca_crt_file, self.ca_key_file, self.user_csr, 'cluster')
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_file.read())
    self.assertEqual(cert.get_subject().commonName, 'user')
    self.assertEqual(cert.get_subject().organizationalUnitName, 'cluster')

if __name__ == '__main__':
  unittest.main()
