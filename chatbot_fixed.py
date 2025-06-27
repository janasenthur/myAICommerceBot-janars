# -*- coding: utf-8 -*-
import streamlit as st
from streamlit_chat import message
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_core.messages import SystemMessage

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure API key from environment variables or Streamlit secrets
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY") or st.secrets.get("TOGETHER_API_KEY")

# AI Commerce Chatbot System Prompt
COMMERCE_SYSTEM_PROMPT = """You are an AI Commerce Assistant specialized in helping customers with online shopping, product recommendations, and e-commerce support. Your role is to:

🛍️ **Core Responsibilities:**
- Provide expert product recommendations based on customer needs and preferences
- Assist with order inquiries, tracking, and returns/exchanges
- Answer questions about product features, specifications, and comparisons
- Help customers navigate the shopping experience and find the best deals
- Provide information about shipping, delivery, and payment options
- Assist with account management and customer service issues

💡 **Expertise Areas:**
- Product discovery and personalized recommendations
- Price comparisons and deal identification
- Inventory availability and restocking information
- Technical product specifications and compatibility
- Customer reviews and ratings analysis
- Shopping cart optimization and checkout assistance
- Post-purchase support and satisfaction

🎯 **Communication Style:**
- Be friendly, helpful, and professional
- Ask clarifying questions to better understand customer needs
- Provide detailed but concise product information
- Use emojis appropriately to enhance the shopping experience
- Offer multiple options when possible
- Be proactive in suggesting complementary products
- Always prioritize customer satisfaction

🔧 **Guidelines:**
- If you don't have specific product information, acknowledge this and suggest how the customer can find it
- For order-specific issues, direct customers to contact customer service with their order number
- Maintain customer privacy and never ask for sensitive information like passwords or full credit card numbers
- Stay updated on current trends and seasonal shopping patterns
- Provide honest assessments of products, including potential drawbacks

Remember: Your goal is to make the customer's shopping experience as smooth and satisfying as possible while helping them find exactly what they need."""

# Initialize session state variables
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=5, return_messages=True)

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "🛍️ Welcome to your AI Commerce Assistant! I'm here to help you with product recommendations, shopping questions, order support, and finding the best deals. What can I help you shop for today?"}
    ]

# Initialize ChatOpenAI and ConversationChain
if not TOGETHER_API_KEY:
    st.error("❌ TOGETHER_API_KEY not found! Please set it in your environment variables or Streamlit secrets.")
    st.stop()

try:
    # llm = ChatOpenAI(model_name="gpt-4o-mini")
    # llm = ChatGoogleGenerativeAI(model = "gemini-pro")
    llm = ChatOpenAI(
        model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
        openai_api_key=TOGETHER_API_KEY,
        openai_api_base="https://api.together.xyz/v1"
    )
    
    # Create conversation chain with system prompt
    conversation = ConversationChain(
        memory=st.session_state.buffer_memory, 
        llm=llm
    )
    
    # Add system message to set the AI's role (this will be included in the conversation context)
    if not hasattr(st.session_state, 'system_prompt_added'):
        st.session_state.buffer_memory.chat_memory.add_message(SystemMessage(content=COMMERCE_SYSTEM_PROMPT))
        st.session_state.system_prompt_added = True
        
except Exception as e:
    st.error(f"❌ Error initializing chatbot: {str(e)}")
    st.stop()

# Create user interface
st.title("🛒 AI Commerce Assistant")
st.subheader("🤖 Your intelligent shopping companion powered by AI")

# Add helpful sidebar with commerce features
with st.sidebar:
    st.header("🛍️ Quick Actions")
    
    if st.button("🔍 Product Search"):
        st.session_state.messages.append({"role": "user", "content": "I'm looking for product recommendations. Can you help me find something specific?"})
        st.rerun()
    
    if st.button("📦 Order Support"):
        st.session_state.messages.append({"role": "user", "content": "I need help with my order status or tracking information."})
        st.rerun()
    
    if st.button("💰 Find Deals"):
        st.session_state.messages.append({"role": "user", "content": "What are the best deals and discounts available right now?"})
        st.rerun()
    
    if st.button("⭐ Product Compare"):
        st.session_state.messages.append({"role": "user", "content": "I want to compare different products. Can you help me?"})
        st.rerun()
    
    if st.button("🔄 Returns & Exchanges"):
        st.session_state.messages.append({"role": "user", "content": "I need information about returns, exchanges, or refund policies."})
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 💡 Tips:")
    st.markdown("• Be specific about your needs")
    st.markdown("• Mention your budget range")
    st.markdown("• Ask about product features")
    st.markdown("• Request comparisons")
    st.markdown("• Check for current deals")

# Main chat interface

if prompt := st.chat_input("Ask me about products, orders, deals, or any shopping questions..."): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("🛍️ Finding the best solution for you..."):
            try:
                response = conversation.predict(input=prompt)
                st.write(response)
                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)  # Add response to message history
            except Exception as e:
                st.error(f"❌ Error generating response: {str(e)}")
                error_message = {"role": "assistant", "content": "🛒 I apologize, but I'm having trouble processing your request right now. Please try again, and I'll be happy to assist you with your shopping needs!"}
                st.session_state.messages.append(error_message)

# Footer with additional commerce information
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🛍️ Shopping Categories")
    st.markdown("• Electronics & Tech")
    st.markdown("• Fashion & Apparel") 
    st.markdown("• Home & Garden")
    st.markdown("• Sports & Outdoors")

with col2:
    st.markdown("### 🎯 Special Services")
    st.markdown("• Personal Shopping")
    st.markdown("• Price Matching")
    st.markdown("• Gift Recommendations")
    st.markdown("• Bulk Orders")

with col3:
    st.markdown("### 📞 Support Options")
    st.markdown("• 24/7 Chat Support")
    st.markdown("• Order Tracking")
    st.markdown("• Easy Returns")
    st.markdown("• Warranty Info")

# Clear chat button
if st.button("🗑️ Clear Chat History"):
    st.session_state.messages = [
        {"role": "assistant", "content": "🛍️ Welcome back! I'm here to help you with product recommendations, shopping questions, order support, and finding the best deals. What can I help you shop for today?"}
    ]
    st.session_state.buffer_memory.clear()
    # Re-add system prompt
    st.session_state.buffer_memory.chat_memory.add_message(SystemMessage(content=COMMERCE_SYSTEM_PROMPT))
    st.rerun()
