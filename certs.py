from OpenSSL import crypto
import datetime
import random
import io

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
  cert_buffer = io.BytesIO()
  cert_buffer.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
  cert_buffer.seek(0)
  return cert_buffer

def create_req(username):
  pkey = crypto.PKey()
  pkey.generate_key(crypto.TYPE_RSA, 4096)
  
  req = crypto.X509Req()
  req.get_subject().countryName = "CA"
  req.get_subject().stateOrProvinceName = "QC"
  req.get_subject().localityName = "Quebec"
  req.get_subject().organizationName = username
  req.get_subject().commonName = username
  req.set_pubkey(pkey)
  req.sign(pkey, "sha256")
  req_buffer = io.BytesIO()
  req_buffer.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, req))
  req_buffer.seek(0)
  return req_buffer

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
