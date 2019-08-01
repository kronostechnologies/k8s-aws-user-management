# k8s-aws-user-management

This tool is intended to management certificate for kubernetes user. It assumes two thing : your cluster is managed by kops and it's state is in aws S3.

## Build
```
make
```

## Usage
For development:

```
docker run -i --rm -e AWS_PROFILE -v $(pwd):/code -v $HOME/.aws:/root/.aws k8suser -h
```

For production:
```
./docker-k8suser -h
```

### Certificate Requests Signing
The command below will sign the user certificate request and output the signed certificate on stdout.
```
export AWS_PROFILE=profile # Only needed if you use aws profile for access to your account
# csr via stdin with docker command directly
cat certificate_request.csr | docker run -i --rm -e AWS_PROFILE -v $HOME/.aws:/root/.aws:ro k8suser sign s3-bucket-name kubernetes-cluster-name stdin > out.crt

# csr via command line with bash wrapper script
./docker-k8suser sign s3-bucket-name kubernetes-cluster-name certificate-request.csr
```
> You may add `--group` to add an organization subject when signing a csr

This will automatically download the certificate authtority and it's private key in-memory and sign the certificate requests.

The `s3-bucket-name` must be the bucket name containing your kops' kubernetes state; `kubernetes-cluster-name` is the name of your cluster. To sum it up, you should be able to reach your state via this s3 url : `s3://s3-bucket-name/kubernetes-cluster-name`.

The resulting certificat will have these subjects:
```
CN:username, OU:clustername, O:groupname
```

## Test
```
make test
```
