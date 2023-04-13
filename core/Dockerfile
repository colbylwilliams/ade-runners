# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

FROM mcr.microsoft.com/azure-cli:latest
WORKDIR /

ARG IMAGE_VERSION

# Metadata as defined at http://label-schema.org
ARG BUILD_DATE

LABEL maintainer="Microsoft" \
    org.opencontainers.image.created=$BUILD_DATE \
    org.opencontainers.image.url="https://github.com/Azure/Fidalgo-Runners" \
    org.opencontainers.image.source="https://github.com/Azure/Fidalgo-Runners.git" \
    org.opencontainers.image.version=$IMAGE_VERSION \
    org.opencontainers.image.vendor="Microsoft" \
    org.opencontainers.image.title="Fidalgo Core" \
    org.opencontainers.image.description="The Fidalgo Core runner is used as a base image for Fidalgo deployments in Azure." \
    org.opencontainers.image.documentation="https://github.com/Azure/Fidalgo-Runners/tree/main/core" \
    org.opencontainers.image.licenses="MIT" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.vendor="Microsoft" \
    org.label-schema.name="Fidalgo Core Runner" \
    org.label-schema.version=$IMAGE_VERSION \
    org.label-schema.license="MIT" \
    org.label-schema.description="The Fidalgo Core runner is used as a base image for Fidalgo deployments in Azure." \
    org.label-schema.url="https://github.com/Azure/Fidalgo-Runners" \
    org.label-schema.usage="https://github.com/Azure/Fidalgo-Runners/tree/main/core" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.vcs-url="https://github.com/Azure/Fidalgo-Runners.git" \
    org.label-schema.docker.cmd="docker run ghcr.io/azure/fidalgo/core:$IMAGE_VERSION"

# Add jq for parsing JSON
RUN apk add jq

COPY entrypoint.d/* /entrypoint.d/
COPY entrypoint.sh /entrypoint.sh
COPY actions.d/* /actions.d/

RUN chmod +x /entrypoint.sh \
    && mkdir -p /entrypoint.d && find /entrypoint.d/ -type f -iname "*.sh" -exec chmod +x {} \; \
    && mkdir -p /actions.d && find /actions.d/ -type f -iname "*.sh" -exec chmod +x {} \;

# Terminate container on stop
STOPSIGNAL SIGTERM

CMD [ "" ]
ENTRYPOINT [ "/entrypoint.sh" ]