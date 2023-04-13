# ade-runners

[![Images](https://github.com/colbylwilliams/ade-runners/actions/workflows/images.yml/badge.svg)](https://github.com/colbylwilliams/ade-runners/actions/workflows/images.yml)

| Image                      | Description                                                                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| [core][pkg-core]           | The Azure Deployment Environments Core runner is used as a base image for all Deployment Environment runner images.                               |
| [arm][pkg-arm]             | The Azure Deployment Environments ARM and Bicep runner is used as the runner for environment catalog itmes that reference ARM or Bicep templates. |
| [azd][pkg-azd]             | The Azure Deployment Environments AZD runner is used as the runner for environment catalog itmes that reference AZD templates.                    |
| [terraform][pkg-terraform] | The Azure Deployment Environments Terraform runner is used as the runner for environment catalog itmes that reference Terraform templates.        |

[pkg-core]: https://github.com/colbylwilliams/ade-runners/pkgs/container/ade-runners%2Fcore
[pkg-arm]: https://github.com/colbylwilliams/ade-runners/pkgs/container/ade-runners%2Farm
[pkg-azd]: https://github.com/colbylwilliams/ade-runners/pkgs/container/ade-runners%2Fazd
[pkg-terraform]: https://github.com/colbylwilliams/ade-runners/pkgs/container/ade-runners%2Fterraform
