#!/usr/bin/env python3

import os.path
import select
import sys
import boto3
import botocore
import argparse
import re
import tempfile
import s3
import certs

def req(args):
  username = args.USERNAME

  req  = certs.create_req(username)
  print(req.decode('utf8'))

def ca(args):
  ca_parser.print_help()

def ca_sign(args):
  bucket = args.BUCKET
  cluster = args.CLUSTER
  req_parameter = args.REQ

  if req_parameter == 'stdin':
    if select.select([sys.stdin,],[],[],0.0)[0]:
      req_file = sys.stdin
    else:
      raise ValueError('There is not data on stdin')
  elif os.path.isfile(req_parameter):
    req_file = open(req_parameter, 'r')

  try:
    key_file = s3.download_key_file(bucket, cluster)
    cert_file = s3.download_cert_file(bucket, cluster)
    cert = certs.sign_req(cert_file, key_file, req_file, cluster)
    print(cert.decode('utf8'))
  except (certs.InvalidCertificateRequest, s3.BucketNotFound, s3.S3FileNotFound) as e:
    raise e

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="AWS Kubernetes user management certificate")
  subparsers = parser.add_subparsers()
  
  req_parser = subparsers.add_parser('req', help='Certificate request commands')
  req_parser.set_defaults(func=req)
  req_parser.add_argument('USERNAME', help='The username for your certificate request')
  
  ca_parser = subparsers.add_parser('ca', help='Certificate authority related commands')
  ca_parser.set_defaults(func=ca)
  ca_subparsers = ca_parser.add_subparsers()
  ca_sign_parser = ca_subparsers.add_parser('sign', help='Certificate authority signing related commands')
  ca_sign_parser.set_defaults(func=ca_sign)
  ca_sign_parser.add_argument('BUCKET', help='The S3 bucket containing cluster information')
  ca_sign_parser.add_argument('CLUSTER', help='Cluster name for which you want to sign the certificate against')
  ca_sign_parser.add_argument('REQ', help='Certificate request file. Pass -- for stdin')

  args = parser.parse_args()
  if hasattr(args, 'func'):
    try:
      args.func(args)
    except (certs.CertsException, s3.S3Exception) as e:
      sys.stderr.write(e.args[0])
      sys.exit(1)
  else:
    parser.print_help()

  sys.exit(0)
