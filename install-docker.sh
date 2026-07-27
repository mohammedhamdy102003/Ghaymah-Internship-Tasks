#!/bin/bash
set -e

echo ">>> Updating packages..."
sudo apt update

echo ">>> Installing prerequisites..."
sudo apt install -y ca-certificates curl gnupg

echo ">>> Setting up Docker keyring..."
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo ">>> Adding Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo ">>> Installing Docker..."
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo ">>> Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

echo ">>> Adding current user to docker group..."
sudo usermod -aG docker $USER

echo ""
echo "=========================================="
echo "Docker installed successfully."
echo "IMPORTANT: run 'newgrp docker' OR log out/in"
echo "then run: docker --version"
echo "=========================================="
