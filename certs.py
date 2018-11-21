from OpenSSL import crypto
import datetime
import random

def sign_req(ca_pub_file, ca_key_file, req):
  ca_pub_file.seek(0)
  ca_key_file.seek(0)
  ca_pub = crypto.load_certificate(crypto.FILETYPE_PEM, ca_pub_file.read())
  ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, ca_key_file.read())

  cert = crypto.X509()
  cert.set_serial_number(random.getrandbits(64))
  cert.gmtime_adj_notBefore(0)
  cert.gmtime_adj_notAfter(315360000) # 10 years
  cert.set_issuer(ca_pub.get_subject())
  cert.set_subject(req.get_subject())
  cert.set_pubkey(req.get_pubkey())
  cert.sign(ca_key, "sha256")
  return crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
  
def create_req(username, cluster):
  pkey = crypto.PKey()
  pkey.generate_key(crypto.TYPE_RSA, 4096)
  
  req = crypto.X509Req()
  req.get_subject().countryName = "CA"
  req.get_subject().stateOrProvinceName = "QC"
  req.get_subject().localityName = "Québec"
  req.get_subject().organizationName = cluster
  req.get_subject().commonName = username
  req.set_pubkey(pkey)
  req.sign(pkey, "sha256")
  return req
