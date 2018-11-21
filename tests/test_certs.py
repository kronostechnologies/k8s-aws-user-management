import io
import sys
import unittest
import certs
from OpenSSL import crypto

class TestCerts(unittest.TestCase):

  def setUp(self):
    self.ca_crt_file = open('./tests/ca/ca.crt')
    self.ca_key_file = open('./tests/ca/ca.key')

  def tearDown(self):
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
    req_file = certs.create_req('user')
    cert_file = certs.sign_req(self.ca_crt_file, self.ca_key_file, req_file, 'cluster')
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_file.read())
    self.assertEqual(cert.get_subject().organizationName, 'user')
    self.assertEqual(cert.get_subject().organizationalUnitName, 'cluster')

  def test_create_req_with_user(self):
    req_file = certs.create_req('user')
    req = crypto.load_certificate_request(crypto.FILETYPE_PEM, req_file.read())
    self.assertEqual(req.get_subject().organizationName, 'user')
    self.assertFalse(req.get_subject().organizationalUnitName)

if __name__ == '__main__':
  unittest.main()
