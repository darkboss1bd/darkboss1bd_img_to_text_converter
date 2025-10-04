#!/bin/bash
echo "Installing DarkBoss1BD Notes Converter on Kali Linux..."

# Update system
echo "Updating system packages..."
sudo apt update

# Install Tesseract OCR
echo "Installing Tesseract OCR..."
sudo apt install -y tesseract-ocr

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install Pillow requests

# Make script executable
chmod +x darkboss_converter.py

echo ""
echo "✅ Installation complete!"
echo "🚀 Run the application with: python3 darkboss_converter.py"
echo ""
echo "📱 Telegram: @darkvaiadmin"
echo "📢 Channel: @windowspremiumkey"
