#!/bin/bash
# Fix for sentence-transformers and huggingface_hub compatibility issue

echo "Uninstalling conflicting packages..."
pip uninstall -y sentence-transformers huggingface-hub

echo "Installing compatible versions..."
pip install "huggingface-hub>=0.20.0,<1.0.0"
pip install "sentence-transformers>=2.2.0,<3.0.0"

echo "Done! Try running: python test_debug.py"
