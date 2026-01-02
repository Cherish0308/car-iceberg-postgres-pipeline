#!/bin/bash
# Build Lambda deployment package using Poetry

set -e

echo "Building Lambda package with Poetry..."

# Clean previous builds
rm -rf dist package lambda.zip

# Export dependencies using Poetry
echo "Exporting dependencies..."
poetry export -f requirements.txt --output requirements.txt --without-hashes

# Create package directory
mkdir -p package

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -t package --platform manylinux2014_x86_64 --only-binary=:all: --upgrade || \
pip install -r requirements.txt -t package

# Copy source code
echo "Copying source code..."
cp -r src/* package/
cp config_prod.ini package/

# Create ZIP
echo "Creating lambda.zip..."
cd package && zip -r ../lambda.zip . -q && cd ..

# Show result
echo ""
echo "✅ Lambda package created successfully!"
ls -lh lambda.zip
echo ""
echo "Contents:"
unzip -l lambda.zip | head -20

