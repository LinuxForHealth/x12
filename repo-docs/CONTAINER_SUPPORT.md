# LinuxForHealth X12 Container Support

## Building the Image

The LinuxForHealth X12 image build accepts a single build argument, `X12_SEM_VER`. This argument should align
with the current `linuxforhealth.x12.__version__` attribute value. 'X12_SEM_VER' should also align with the image
tag, for consistency.

```shell
docker build --build-arg X12_SEM_VER=0.57.0 -t x12:0.57.0 .
```

## Run Container Image

The LinuxForHealth X12 container is stored within the GitHub Container Registry. 
The following command launches the X12 container mapping the host port `5000` to the container port `5000`.

```shell
docker run --name lfh-x12 --rm -d -p 5000:5000 ghcr.io/linuxforhealth/x12:latest
```

To access the Open API UI, browse to http://localhost:5000/docs

To stop and remove the container:
```shell
docker stop lfh-x12
```
