# Docker / CKAN upstream

OpenImperia uses the official CKAN Docker Compose project as its infrastructure
base.

- https://github.com/ckan/ckan-docker
- https://github.com/ckan/ckan-docker-base

The upstream Docker project is not vendored in v0.1, keeping this repository
small and making CKAN upgrades easier. A later release can vendor a pinned
snapshot while preserving upstream attribution and licensing.
