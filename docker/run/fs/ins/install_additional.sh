#!/bin/bash
set -e

# install playwright - moved to install A0
# bash /ins/install_playwright.sh "$@"

# searxng - moved to base image
# bash /ins/install_searxng.sh "$@"

# extra runtime dependencies
apt-get update
apt-get install -y --no-install-recommends sqlite3 libsqlite3-dev
