#!/bin/bash

# Script to stop Docker and upgrade to the latest version on Ubuntu

echo "=== Docker Upgrade Script ==="
echo ""

# Step 1: Stop Docker services
echo "Step 1: Stopping Docker services..."
sudo systemctl stop docker.socket
sudo systemctl stop docker.service
sudo systemctl stop containerd.service
echo "✓ Docker services stopped"
echo ""

# Step 2: Check current Docker version
echo "Step 2: Current Docker version:"
docker --version 2>/dev/null || echo "Docker not found or not accessible"
echo ""

# Step 3: Update package index
echo "Step 3: Updating package index..."
sudo apt-get update
echo "✓ Package index updated"
echo ""

# Step 4: Upgrade Docker packages
echo "Step 4: Upgrading Docker packages..."
sudo apt-get install --only-upgrade -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
echo "✓ Docker packages upgraded"
echo ""

# Step 5: Start Docker services
echo "Step 5: Starting Docker services..."
sudo systemctl start docker.service
sudo systemctl enable docker.service
echo "✓ Docker services started"
echo ""

# Step 6: Verify new version
echo "Step 6: New Docker version:"
docker --version
echo ""

# Step 7: Verify Docker is running
echo "Step 7: Checking Docker status..."
sudo systemctl status docker.service --no-pager | head -n 5
echo ""

echo "=== Upgrade Complete ==="
echo ""
echo "You can verify Docker is working by running:"
echo "  sudo docker run hello-world"