@echo off
echo 🚀 Setting up AI Commerce Chatbot...
echo ================================================

echo 📦 Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Error installing dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully!

if not exist .env (
    echo 📄 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env file and add your TOGETHER_API_KEY
) else (
    echo ✅ .env file already exists
)

echo.
echo ================================================
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your TOGETHER_API_KEY
echo 2. Run: streamlit run chatbot.py
echo.
echo Get your Together AI API key at: https://api.together.xyz/
echo.
pause
