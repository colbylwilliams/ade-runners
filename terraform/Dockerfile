# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

ARG IMAGE_VERSION=latest

FROM jarewert.azurecr.io/core:${IMAGE_VERSION}
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
    org.opencontainers.image.title="Dev Center Terraform Runner" \
    org.opencontainers.image.description="The Dev Center Terraform runner is used as a base image for Dev Center deployments in Azure." \
    org.opencontainers.image.documentation="https://github.com/Azure/Fidalgo-Runners/tree/main/terraform" \
    org.opencontainers.image.licenses="MIT" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.vendor="Microsoft" \
    org.label-schema.name="Dev Center Terraform Runner" \
    org.label-schema.version=$IMAGE_VERSION \
    org.label-schema.license="MIT" \
    org.label-schema.description="The Dev Center Terraform runner is used as a base image for Dev Center deployments in Azure." \
    org.label-schema.url="https://github.com/Azure/Fidalgo-Runners" \
    org.label-schema.usage="https://github.com/Azure/Fidalgo-Runners/tree/main/terraform" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.vcs-url="https://github.com/Azure/Fidalgo-Runners.git" \
    org.label-schema.docker.cmd="docker run ghcr.io/azure/fidalgo/terraform:$IMAGE_VERSION"


# install terraform
RUN apk add --no-cache terraform --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community

# Grab all .sh files from actions.d, copy to
# root actions.d, and make them all executable
COPY actions.d/* /actions.d/
RUN find /actions.d/ -type f -iname "*.sh" -exec chmod +x {} \;
