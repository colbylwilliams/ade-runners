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
    org.opencontainers.image.title="Azure Deployment Environments AZD Runner" \
    org.opencontainers.image.description="The Azure Deployment Environments AZD runner is used as the runner for environment catalog itmes that reference AZD templates." \
    org.opencontainers.image.documentation="https://github.com/colbylwilliams/ade-runners/tree/main/azd" \
    org.opencontainers.image.licenses="MIT" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.vendor="Microsoft" \
    org.label-schema.name="Azure Deployment Environments AZD Runner" \
    org.label-schema.version=$IMAGE_VERSION \
    org.label-schema.license="MIT" \
    org.label-schema.description="The ADE AZD runner is used as the runner for environment catalog itmes that reference AZD templates." \
    org.label-schema.url="https://github.com/colbylwilliams/ade-runners" \
    org.label-schema.usage="https://github.com/colbylwilliams/ade-runners/tree/main/azd" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.vcs-url="https://github.com/colbylwilliams/ade-runners.git" \
    org.label-schema.docker.cmd="docker run ghcr.io/colbylwilliams/ade-runners/azd:$IMAGE_VERSION"

# install terraform
RUN apk add --no-cache terraform --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community

# install azd
# RUN curl https://azure-dev.azureedge.net/azd/standalone/release/azd-linux-amd64.tar.gz
RUN curl -fsSL https://aka.ms/install-azd.sh | bash -s -- --platform "linux" --architecture "amd64" --extension "tar.gz"

# resolve this: https://github.com/golang/go/issues/59304
# with this fix: https://github.com/gohugoio/hugo/issues/10839#issuecomment-1499463944
RUN apk add --no-cache gcompat libc6-compat \
    && ln -s /lib/libc.so.6 /usr/lib/libresolv.so.2

# Grab all .sh files from actions.d, copy to
# root actions.d, and ake them all executable
COPY actions.d/* /actions.d/
RUN find /actions.d/ -type f -iname "*.sh" -exec chmod +x {} \; \
    && find /actions.d/ -type f -iname "*.py" -exec chmod +x {} \;
