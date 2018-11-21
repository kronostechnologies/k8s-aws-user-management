# k8s-aws-user-management

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
docker run -i --rm -e AWS_PROFILE -v $HOME/.aws:/root/.aws k8suser -h
```

## Test
```
make test
```
