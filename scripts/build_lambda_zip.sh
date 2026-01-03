#!/bin/bash

set -e

echo "=============================================================================="
echo "Building Lambda Package with Poetry"
echo "=============================================================================="
echo ""

if ! command -v poetry &> /dev/null; then
    echo "❌ Error: Poetry is not installed or not in PATH"
    echo "Install Poetry: https://python-poetry.org/docs/#installation"
    exit 1
fi

echo "✅ Poetry version: $(poetry --version)"
echo ""

echo "🧹 Cleaning previous builds..."
rm -rf dist build lambda.zip lambda_package/

echo ""
echo "📦 Building with Poetry..."

mkdir -p lambda_package

echo "📥 Exporting production dependencies..."
poetry export --format requirements.txt --output lambda_package/requirements.txt --without dev --without-hashes

echo ""
echo "📚 Installing dependencies..."

pip install \
    --target lambda_package \
    --platform manylinux2014_x86_64 \
    --only-binary=:all: \
    --upgrade \
    -r lambda_package/requirements.txt \
    2>&1 | grep -E "Successfully|Collecting|Downloading" || true

if [ $? -ne 0 ]; then
    echo "⚠️  x86_64 build had issues, retrying without platform flag..."
    pip install \
        --target lambda_package \
        --only-binary=:all: \
        --upgrade \
        -r lambda_package/requirements.txt
fi

echo ""
echo "📂 Copying application code..."

if [ -d "src" ]; then
    echo "  Copying src/ directory..."
    cp -r src/* lambda_package/
else
    echo "  ⚠️  src/ directory not found, trying package/..."
    cp -r package/* lambda_package/ 2>/dev/null || true
fi

echo "  Copying config_prod.ini..."
cp config_prod.ini lambda_package/

if [ -f "lambda_handler.py" ]; then
    echo "  Copying lambda_handler.py..."
    cp lambda_handler.py lambda_package/
fi

echo ""
echo "📦 Creating Lambda ZIP archive..."

cd lambda_package
zip -r ../lambda.zip . -q
cd ..

echo ""
echo "=============================================================================="
echo "✅ Lambda package created successfully!"
echo "=============================================================================="
echo ""
echo "📊 Package Details:"
echo "   Size: $(ls -lh lambda.zip | awk '{print $5}')"
echo "   Location: $(pwd)/lambda.zip"
echo ""
echo "📋 Package Contents (top 20 items):"
unzip -l lambda.zip | head -25
echo ""
echo "🚀 Deployment:"
echo "   1. Update configuration in lambda_package/config_prod.ini"
echo "   2. Upload lambda.zip to AWS Lambda"
echo "   3. Set environment variable: ENV=prod"
echo "   4. Set handler: main.lambda_handler"
echo ""
echo "Dependencies included:"
poetry export --format requirements.txt --without dev --without-hashes 2>/dev/null | wc -l | awk '{print "  Total: " $1 - 1 " packages"}'
echo ""
echo "=============================================================================="
