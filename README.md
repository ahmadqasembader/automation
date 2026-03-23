# CNCF Automation

This repository contains automation tools and scripts used by the Cloud Native Computing Foundation (CNCF) and its projects. These tools help streamline various tasks and workflows, making it easier to manage and maintain CNCF projects.

## Overview

The CNCF Automation repository provides various tools that help automate repetitive tasks, standardize workflows, and improve efficiency across CNCF projects. These tools are designed to be reusable and configurable for different project needs.

## Tools and Components

### Self-Hosted Runners

Tools and scripts for managing self-hosted GitHub Actions runners on CNCF's infrastructure (e.g., Oracle Cloud Infrastructure). These runners allow CNCF projects to execute their CI/CD workflows in a controlled environment.

For more information, see the [CI documentation](./ci/README.md).

### Project Status Audit

Cross-checks CNCF project lifecycle data from **LFX PCC** against Landscape, CLOMonitor, maintainers CSV, DevStats, and Artwork, and optionally adds **[LFX Insights](https://insights.linuxfoundation.org/)** **Insights Health** (tier) and **Health Score** (number) when `lfx_insights_health.yaml` is present (informational only; not used for anomaly detection).

See [utilities/audit_project_lifecycle_across_tools/README.md](./utilities/audit_project_lifecycle_across_tools/README.md) for workflows, local usage, and file layout.

## Contributing

Contributions to improve these automation tools are welcome! Please see our [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the [Apache License 2.0](LICENSE).