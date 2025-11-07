#!/bin/bash

# Variables
GITHUB_USER="ytdl-org"   # GitHub username or organization
REPO="ytdl-nightly"      # Repository name
ASSET_NAME="youtube-dl"  # Asset name to download

# Get the latest release date from the redirect URL
release_date=$(curl -sL -o /dev/null -w %{url_effective} "https://github.com/$GITHUB_USER/$REPO/releases/latest" | grep -oP "(?<=/releases/tag/)[^/]+")

# Check if release date was found
if [ -z "$release_date" ]; then
  echo "Release date not found!"
  exit 1
fi

# Construct the URL of the desired asset
asset_url="https://github.com/$GITHUB_USER/$REPO/releases/download/$release_date/$ASSET_NAME"

# Download the asset
sudo curl -L "$asset_url" -o "/usr/local/bin/$ASSET_NAME"

echo "Asset downloaded: $ASSET_NAME"

