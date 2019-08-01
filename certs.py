from OpenSSL import crypto
import datetime
import random
import io
import string

def get_cert_subject(cert_file):
  try:
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_file.read())
  except crypto.Error as e:
    raise InvalidCertificateAuthorityCertificate("Invalid certificate public key: {0}".format(str(e)))
  return cert.get_subject()

def sign_req(ca_crt_file, ca_key_file, req_file, cluster):
  try:
    ca_pub = crypto.load_certificate(crypto.FILETYPE_PEM, ca_crt_file.read())
  except crypto.Error as e:
    raise InvalidCertificateAuthorityCertificate("Invalid certificate public key: {0}".format(str(e)))

  try:
    ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, ca_key_file.read())
  except crypto.Error as e:
    raise InvalidCertificateAuthorityPrivateKey("Invalid certificate authority private key: {0}".format(str(e)))

  try:
    req = crypto.load_certificate_request(crypto.FILETYPE_PEM, req_file.read())
  except crypto.Error as e:
    raise InvalidCertificateRequest("Invalid certificate request: {0}".format(str(e)))

  req.get_subject().organizationalUnitName = cluster

  cert = crypto.X509()
  cert.set_serial_number(random.getrandbits(64))
  cert.gmtime_adj_notBefore(0)
  cert.gmtime_adj_notAfter(94608000) # 3 years
  cert.set_issuer(ca_pub.get_subject())
  cert.set_subject(req.get_subject())
  cert.set_pubkey(req.get_pubkey())
  cert.sign(ca_key, "sha256")
  cert_buffer = io.BytesIO(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
  cert_buffer.seek(0)
  return cert_buffer

class CertsException(Exception):
  pass

class InvalidCertificateRequest(CertsException):
  def __init__(self, message):
    self.message = message

class InvalidCertificateAuthorityCertificate(CertsException):
  def __init__(self, message):
    self.message = message

class InvalidCertificateAuthorityPrivateKey(CertsException):
  def __init__(self, message):
    self.message = message
