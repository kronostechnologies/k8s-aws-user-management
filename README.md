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

### Certificate Requests
Certificate request can be generated for a user as follow :
```
./docker-k8suser req $USER
```
Usually, this command would be run by a user that wants an access to your kubernetes cluster.

### Certificate Requests Signing
The command below will sign the user certificate request and output the signed certificate on stdout.
```
export AWS_PROFILE=profile # Only needed if you use aws profile for access to your account
./docker-k8suser ca sign s3-bucket-name kubernetes-cluster-name certificate-request.csr
```
This will automatically download the certificate authtority and it's private key in-memory and sign the certificate requests.

The `s3-bucket-name` must be the bucket name containing your kops' kubernetes state; `kubernetes-cluster-name` is the name of your cluster. To sum it up, you should be able to reach your state via this s3 url : `s3://s3-bucket-name/kubernetes-cluster-name`.

## Test
```
make test
```
