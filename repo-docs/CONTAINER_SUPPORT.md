# LinuxForHealth X12 Container Support

The LinuxForHealth X12 API component supports a containerized execution environment. This guide provides an overview of
how to build and run the image.

## Image Build

### Supported Build Arguments


| Build Argument | Description                                    | Default Value |
|----------------|------------------------------------------------|---------------|
| X12_SEM_VER    | The current X12 library sematic version number | None          |
| LFH_USER_ID    | The user id used for the LFH container user    | 1000          |
| LFH_GROUP_ID   | The group id used for the LFH container group  | 1000          |

The `X12_SEM_VER`. This argument should align with the current `linuxforhealth.x12.__version__` attribute value and the
desired image tag.

```shell
docker build --build-arg X12_SEM_VER=0.57.0 -t x12:0.57.0 .
```

## Run Container

### Supported Environment Configurations

| Build Argument   | Description                       | Default Value |
|------------------|-----------------------------------|---------------|
| X12_UVICORN_HOST | The container's listening address | 0.0.0.0       |


The following command launches the LinuxForHealth X12 container:
```shell
docker run --name lfh-x12 --rm -d -p 5000:5000 ghcr.io/linuxforhealth/x12:latest
```

To access the Open API UI, browse to http://localhost:5000/docs

Finally, to stop and remove the container:
```shell
docker stop lfh-x12
```
