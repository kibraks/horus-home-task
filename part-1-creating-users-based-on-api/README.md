### Running in a container
1. Build image:
```
export IMAGE_NAME=<your name of choice>
```
```
docker build -t ${IMAGE_NAME} .
```
2. Run image:
```
docker run --rm ${IMAGE_NAME}
```