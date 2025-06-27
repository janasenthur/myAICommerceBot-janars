#!/usr/bin/env python3
"""
Setup script for AI Commerce Chatbot
This script helps users set up the environment and dependencies.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages from requirements.txt"""
    try:
        print("📦 Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    env_path = Path(".env")
    example_path = Path(".env.example")
    
    if not env_path.exists() and example_path.exists():
        try:
            with open(example_path, 'r') as f:
                content = f.read()
            
            with open(env_path, 'w') as f:
                f.write(content)
            
            print("📄 Created .env file from .env.example")
            print("⚠️  Please edit .env and add your actual TOGETHER_API_KEY")
            return True
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    elif env_path.exists():
        print("✅ .env file already exists")
        return True
    else:
        print("❌ .env.example file not found")
        return False

def check_api_key():
    """Check if API key is set"""
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r') as f:
            content = f.read()
            if "your_together_ai_api_key_here" in content:
                print("⚠️  Please update your TOGETHER_API_KEY in .env file")
                return False
            elif "TOGETHER_API_KEY=" in content:
                print("✅ API key appears to be set in .env file")
                return True
    return False

def main():
    """Main setup function"""
    print("🚀 Setting up AI Commerce Chatbot...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Check API key
    check_api_key()
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file and add your TOGETHER_API_KEY")
    print("2. Run: streamlit run chatbot.py")
    print("\nGet your Together AI API key at: https://api.together.xyz/")

if __name__ == "__main__":
    main()
