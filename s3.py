import boto3
import botocore
import re
import tempfile


s3 = boto3.resource("s3")

def download_key_file(bucket_name, cluster_name):
  return __download_file(bucket_name, "^{0}/pki/private/ca/[0-9]+\.key$".format(cluster_name))

def download_cert_file(bucket_name, cluster_name):
  return __download_file(bucket_name, "^{0}/pki/issued/ca/[0-9]+\.crt$".format(cluster_name))


def __download_file(bucket_name, pattern):
  try:
    s3.meta.client.head_bucket(Bucket=bucket_name)
  except botocore.exceptions.ClientError as e:
    raise BucketNotFound(bucket_name)

  bucket = s3.Bucket(bucket_name)
  regex = re.compile(pattern)
  for s3_object in bucket.objects.all():
    if regex.match(s3_object.key):
      s3_file = tempfile.TemporaryFile()
      bucket.download_fileobj(s3_object.key, s3_file)
      s3_file.seek(0)
      return s3_file

  raise S3FileNotFound(pattern)

class S3Exception(Exception):
  pass

class BucketNotFound(S3Exception):
  def __init__(self, bucket):
    self.message = "Bucket {0} does not exists".format(bucket)
    self.bucket = bucket

class S3FileNotFound(S3Exception):
  def __init__(self, pattern):
    self.message = "No file were found matching the pattern '{0}'".format(pattern)
    self.pattern = pattern
