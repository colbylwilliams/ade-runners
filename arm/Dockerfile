# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

ARG IMAGE_VERSION=latest

FROM ghcr.io/colbylwilliams/ade-runners/core:${IMAGE_VERSION}
WORKDIR /

ARG IMAGE_VERSION

# Metadata as defined at http://label-schema.org
ARG BUILD_DATE

LABEL maintainer="Microsoft" \
    org.opencontainers.image.created=$BUILD_DATE \
    org.opencontainers.image.url="https://github.com/colbylwilliams/ade-runners" \
    org.opencontainers.image.source="https://github.com/colbylwilliams/ade-runners" \
    org.opencontainers.image.version=$IMAGE_VERSION \
    org.opencontainers.image.vendor="Microsoft" \
    org.opencontainers.image.title="Azure Deployment Environments ARM and Bicep Runner" \
    org.opencontainers.image.description="The Azure Deployment Environments ARM and Bicep runner is used as the runner for environment catalog itmes that reference ARM or Bicep templates." \
    org.opencontainers.image.documentation="https://github.com/colbylwilliams/ade-runners/tree/main/arm" \
    org.opencontainers.image.licenses="MIT" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.vendor="Microsoft" \
    org.label-schema.name="Azure Deployment Environments ARM and Bicep Runner" \
    org.label-schema.version=$IMAGE_VERSION \
    org.label-schema.license="MIT" \
    org.label-schema.description="The Azure Deployment Environments ARM and Bicep runner is used as the runner for environment catalog itmes that reference ARM or Bicep templates." \
    org.label-schema.url="https://github.com/colbylwilliams/ade-runners" \
    org.label-schema.usage="https://github.com/colbylwilliams/ade-runners/tree/main/arm" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.vcs-url="https://github.com/colbylwilliams/ade-runners.git" \
    org.label-schema.docker.cmd="docker run ghcr.io/colbylwilliams/ade-runners/arm:$IMAGE_VERSION"

# install bicep
RUN az bicep install

# Grab all .sh files from actions.d, copy to
# root actions.d, and ake them all executable
COPY actions.d/* /actions.d/
RUN find /actions.d/ -type f -iname "*.sh" -exec chmod +x {} \; \
    && find /actions.d/ -type f -iname "*.py" -exec chmod +x {} \;
