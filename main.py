#!/usr/bin/env python3

import sys
import boto3
import botocore
import argparse
import re
import tempfile
import s3
import certs

parser = argparse.ArgumentParser(description="AWS Kubernetes user management certificate")
parser.add_argument("--bucket", dest="bucket", metavar="BUCKET", type=str, help="Bucket name holding kops state")
parser.add_argument("--cluster", dest="cluster", metavar="CLUSTER", type=str, help="cluster name for which you want to add a user")
parser.add_argument("--username", dest="username", metavar="USERNAME", type=str, help="Username for which we want to create a new certificate")

args = parser.parse_args()
try:
  key_file = s3.download_key_file(args.bucket, args.cluster)
  cert_file = s3.download_cert_file(args.bucket, args.cluster)
  req  = certs.create_req(args.username, args.cluster)
  cert = certs.sign_req(cert_file, key_file, req)
  print(cert)
except s3.BucketNotFound as e1:
  print(e1.message)
  sys.exit()
except s3.S3FileNotFound as e2:
  print(e2.message)
  sys.exit()
