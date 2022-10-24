# Builds the LinuxForHealth X12 API container using a multi-stage build

# build stage
FROM python:slim-buster AS builder

# the full semantic version number, used to match to the generated wheel file in dist/
ARG X12_SEM_VER

# OS library updates and build tooling
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
     build-essential \
     gcc

# copy source and build files
WORKDIR /tmp/lfh-x12
COPY setup.cfg .
COPY pyproject.toml .
COPY ../src src/

# build the service
RUN python -m venv /tmp/lfh-x12/venv
ENV PATH="/tmp/lfh-x12/venv/bin:$PATH"
RUN python -m pip install --upgrade pip setuptools wheel build
RUN python -m build
RUN python -m pip install dist/linuxforhealth_x12-"$X12_SEM_VER"-py3-none-any.whl[api]

# main image
FROM python:3.10-slim-buster

# container build arguments
# lfh user id and group ids
ARG LFH_USER_ID=1000
ARG LFH_GROUP_ID=1000

# create service user and group
RUN groupadd -g $LFH_GROUP_ID lfh && \
    useradd -m -u $LFH_USER_ID -g lfh lfh
USER lfh
WORKDIR /home/lfh

# configure and execute application
COPY --from=builder /tmp/lfh-x12/venv ./venv
# set venv executables first in path
ENV PATH="/home/lfh/venv/bin:$PATH"
# listening address for application
ENV X12_UVICORN_HOST=0.0.0.0
EXPOSE 5000
CMD ["python", "-m", "linuxforhealth.x12.api"]
