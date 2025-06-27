# � AI Commerce Chatbot

An intelligent AI-powered commerce assistant built with Streamlit and LangChain, specialized in e-commerce support and powered by Meta's Llama 3.2 model via Together AI. This chatbot provides personalized shopping assistance, product recommendations, order support, and comprehensive e-commerce customer service.

## ✨ Features

- **🛍️ Smart Product Recommendations**: AI-powered product suggestions based on customer preferences and needs
- **📦 Order Support**: Comprehensive assistance with order tracking, returns, and customer service
- **💰 Deal Finder**: Intelligent deal discovery and price comparison capabilities
- **🔍 Product Search & Compare**: Advanced product search and detailed comparison features
- **💬 Interactive Chat Interface**: Modern, user-friendly chat UI optimized for shopping experiences
- **🧠 Conversation Memory**: Maintains shopping context across conversations for personalized assistance
- **💾 Conversation History**: Save, browse, and continue previous conversations with full history management
- **⚡ Real-time Responses**: Fast, accurate responses powered by Meta Llama 3.2-90B-Vision-Instruct-Turbo
- **🎯 Quick Actions**: Pre-built buttons for common shopping tasks and inquiries
- **🎨 Custom Branding**: Support for company logos and brand customization

## 🎯 AI Commerce Capabilities

### **Product & Shopping Support:**
- Personalized product recommendations
- Feature comparisons and specifications
- Inventory availability and restocking information
- Price matching and deal identification
- Shopping cart optimization

### **Customer Service:**
- Order tracking and status updates
- Returns, exchanges, and refund guidance
- Account management assistance
- Shipping and delivery information
- Payment and billing support

### **Shopping Experience:**
- Gift recommendations and seasonal suggestions
- Bulk order assistance
- Technical compatibility guidance
- Customer review analysis
- Trend identification and recommendations

### **Conversation Management:**
- **Auto-save conversations**: Automatically saves chat history for future reference
- **Browse conversation history**: Access up to 10 recent conversations from the sidebar
- **Load and continue**: Resume any previous conversation from where you left off
- **Manual save**: Save important conversations with custom titles
- **Delete conversations**: Remove unwanted conversation history
- **New chat**: Start fresh conversations while preserving history

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Together AI API key ([Get one here](https://api.together.xyz/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/myAICommerceBot-janars.git
   cd myAICommerceBot-janars
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Together AI API key
   # TOGETHER_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run chatbot.py
   ```

5. **Start shopping with AI assistance!**
   - Use the sidebar quick action buttons for common tasks
   - Ask about specific products or categories
   - Request price comparisons and recommendations
   - Get help with orders and customer service

## 🔧 Configuration

### Environment Variables

The application requires the following environment variable:

- `TOGETHER_API_KEY`: Your Together AI API key

You can set this in multiple ways:

1. **Using .env file** (recommended for local development)
2. **Using Streamlit secrets** (for Streamlit Cloud deployment)
3. **Using system environment variables**

### Streamlit Secrets (for deployment)

If deploying to Streamlit Cloud, add your API key to `.streamlit/secrets.toml`:

```toml
TOGETHER_API_KEY = "your_api_key_here"
```

## 🛠️ Customization

### Adding Your Company Logo & Dark Theme

Customize the chatbot with professional dark theme and company branding:

1. **Save your logo** as `logo.png` in the `assets/` folder
2. **Supported formats**: PNG, JPG, JPEG, GIF
3. **Recommended size**: 300x150 pixels (landscape orientation)
4. **Logo appears in two locations**:
   - **Sidebar**: Large logo above Quick Actions menu
   - **Main title**: Small logo replacing the cart icon

```
assets/
└── logo.png  # Your company logo here
```

**🌙 Dark Theme Features:**
- Professional dark background (#0e1117)
- Optimized contrast for readability
- Green accent color (#00c851) for branding
- Enhanced button styling with hover effects

If no logo is provided, stylized icons will be shown instead.

### Changing the AI Model

You can easily switch between different models by modifying the `llm` initialization in `chatbot.py`:

```python
# For OpenAI GPT models
llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key="your_openai_key")

# For Google Gemini
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="your_google_key")

# Current: Meta Llama via Together AI
llm = ChatOpenAI(
    model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
    openai_api_key=TOGETHER_API_KEY,
    openai_api_base="https://api.together.xyz/v1"
)
```

### Adjusting Memory Settings

Modify the conversation memory window size for better shopping context retention:

```python
st.session_state.buffer_memory = ConversationBufferWindowMemory(k=5, return_messages=True)
```

### Customizing Commerce Categories

You can customize the shopping categories and quick actions by modifying the sidebar section in `chatbot.py`:

```python
# Add custom quick action buttons
if st.button("🎮 Gaming Products"):
    st.session_state.messages.append({"role": "user", "content": "Show me the latest gaming products and deals."})
    st.rerun()
```

### Adding Product Integration

To integrate with real product databases or APIs, modify the system prompt and add API connections:

```python
# Example: Add product API integration
COMMERCE_SYSTEM_PROMPT += """
Access to real-time product database for:
- Live inventory checking
- Current pricing information  
- Product availability
- Customer reviews and ratings
"""
```

## 📦 Dependencies

- `streamlit`: Web application framework
- `streamlit-chat`: Chat UI components
- `langchain`: LLM application framework
- `langchain-openai`: OpenAI integration for LangChain
- `python-dotenv`: Environment variable management

## 🚀 Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add your `TOGETHER_API_KEY` to the secrets in Streamlit Cloud
4. Deploy and start helping customers shop with AI!

### E-commerce Integration

For production e-commerce integration:

1. **Product Database Connection**: Connect to your product catalog API
2. **Order Management**: Integrate with your order management system
3. **Customer Authentication**: Add user authentication for personalized experiences
4. **Analytics**: Implement conversation analytics for customer insights
5. **Multi-language Support**: Add internationalization for global customers

### Local Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "chatbot.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/myAICommerceBot-janars/issues) page
2. Create a new issue if your problem isn't already reported
3. Provide detailed information about the error and your environment

## 🏗️ Built With

- [Streamlit](https://streamlit.io/) - The web framework used
- [LangChain](https://langchain.com/) - LLM application framework
- [Together AI](https://together.ai/) - AI model hosting platform
- [Meta Llama](https://llama.meta.com/) - The AI model powering the chatbot

---

⭐ If you found this project helpful, please give it a star!