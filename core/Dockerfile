# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

FROM mcr.microsoft.com/azure-cli:latest
WORKDIR /

ARG IMAGE_VERSION

# Metadata as defined at http://label-schema.org
ARG BUILD_DATE

# Set an environment variable scripts can use to determine if they are running in a runner container
ENV ADE_RUNNER=1

LABEL maintainer="Microsoft" \
    org.opencontainers.image.created=$BUILD_DATE \
    org.opencontainers.image.url="https://github.com/colbylwilliams/ade-runners" \
    org.opencontainers.image.source="https://github.com/colbylwilliams/ade-runners" \
    org.opencontainers.image.version=$IMAGE_VERSION \
    org.opencontainers.image.vendor="Microsoft" \
    org.opencontainers.image.title="Azure Deployment Environments Core Runner" \
    org.opencontainers.image.description="The Azure Deployment Environments Core runner is used as a base image for all Deployment Environment runner images." \
    org.opencontainers.image.documentation="https://github.com/colbylwilliams/ade-runners/tree/main/core" \
    org.opencontainers.image.licenses="MIT" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.vendor="Microsoft" \
    org.label-schema.name="Azure Deployment Environments Core Runner" \
    org.label-schema.version=$IMAGE_VERSION \
    org.label-schema.license="MIT" \
    org.label-schema.description="The Azure Deployment Environments Core runner is used as a base image for all Deployment Environment runner images." \
    org.label-schema.url="https://github.com/colbylwilliams/ade-runners" \
    org.label-schema.usage="https://github.com/colbylwilliams/ade-runners/tree/main/core" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.vcs-url="https://github.com/colbylwilliams/ade-runners.git" \
    org.label-schema.docker.cmd="docker run ghcr.io/colbylwilliams/ade-runners/core:$IMAGE_VERSION"

COPY actions.d/* /actions.d/
COPY entrypoint.d/* /entrypoint.d/
COPY entrypoint.sh /entrypoint.sh

# Make entrypoint.sh and all sh and py scripts in entrypoint.d and actions.d executable
RUN chmod +x /entrypoint.sh \
    && mkdir -p /actions.d \
    && mkdir -p /entrypoint.d \
    && find /actions.d/ -type f -iname "*.sh" -exec chmod +x {} \; \
    && find /actions.d/ -type f -iname "*.py" -exec chmod +x {} \; \
    && find /entrypoint.d/ -type f -iname "*.sh" -exec chmod +x {} \; \
    && find /entrypoint.d/ -type f -iname "*.py" -exec chmod +x {} \;

# Terminate container on stop
STOPSIGNAL SIGTERM

CMD [ "" ]
ENTRYPOINT [ "/entrypoint.sh" ]