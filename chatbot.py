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
import json
import datetime
from dotenv import load_dotenv
from PIL import Image

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

# Conversation History Functions
def save_conversation(conversation_data, title=None):
    """Save the current conversation to a file"""
    if not os.path.exists("conversations"):
        os.makedirs("conversations")
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if not title:
        # Generate title from first user message
        first_user_msg = next((msg["content"][:50] for msg in conversation_data if msg["role"] == "user"), "New Conversation")
        title = first_user_msg.replace("/", "_").replace("\\", "_")[:30] + "..."
    
    filename = f"conversations/{timestamp}_{title.replace(' ', '_')}.json"
    
    conversation_info = {
        "timestamp": timestamp,
        "title": title,
        "messages": conversation_data,
        "created": datetime.datetime.now().isoformat()
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(conversation_info, f, indent=2, ensure_ascii=False)
        return filename
    except Exception as e:
        st.error(f"Error saving conversation: {str(e)}")
        return None

def load_conversations():
    """Load all saved conversations"""
    conversations = []
    if not os.path.exists("conversations"):
        return conversations
    
    try:
        for filename in os.listdir("conversations"):
            if filename.endswith(".json"):
                with open(f"conversations/{filename}", 'r', encoding='utf-8') as f:
                    conversation = json.load(f)
                    conversation["filename"] = filename
                    conversations.append(conversation)
        
        # Sort by timestamp (newest first)
        conversations.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    except Exception as e:
        st.error(f"Error loading conversations: {str(e)}")
    
    return conversations

def load_conversation(filename):
    """Load a specific conversation"""
    try:
        with open(f"conversations/{filename}", 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading conversation: {str(e)}")
        return None

def delete_conversation(filename):
    """Delete a conversation file"""
    try:
        os.remove(f"conversations/{filename}")
        return True
    except Exception as e:
        st.error(f"Error deleting conversation: {str(e)}")
        return False

def format_conversation_title(conversation):
    """Format conversation title for display"""
    title = conversation.get("title", "Untitled")
    timestamp = conversation.get("timestamp", "")
    if timestamp:
        try:
            dt = datetime.datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
            date_str = dt.strftime("%m/%d %H:%M")
            return f"{title} ({date_str})"
        except:
            pass
    return title

# Initialize session state variables
if 'current_conversation_file' not in st.session_state:
    st.session_state.current_conversation_file = None

if 'auto_save' not in st.session_state:
    st.session_state.auto_save = True
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

# Create user interface with logo
def display_sidebar_logo():
    """Display the company logo in the sidebar if it exists"""
    # Try different logo file formats
    logo_files = ["assets/logo.png", "assets/logo.jpg", "assets/logo.jpeg", "assets/logo.gif"]
    
    logo_found = False
    for logo_path in logo_files:
        if os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path)
                st.image(logo, width=150)
                logo_found = True
                break
            except Exception as e:
                st.warning(f"Could not load logo from {logo_path}: {str(e)}")
    
    if not logo_found:
        # If no logo file, show text-based logo in sidebar
        st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <h1 style="color: #00c851; font-size: 2em; margin: 0;">🛒</h1>
            <p style="color: #fff; margin: 5px; font-size: 0.8em;">Commerce Bot</p>
        </div>
        """, unsafe_allow_html=True)

def get_title_logo():
    """Get logo for title or return default icon"""
    logo_files = ["assets/logo.png", "assets/logo.jpg", "assets/logo.jpeg", "assets/logo.gif"]
    
    for logo_path in logo_files:
        if os.path.exists(logo_path):
            return logo_path
    return None

# Set dark theme with enhanced styling
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: #fafafa;
}
.stSidebar {
    background-color: #262730;
}
.stButton > button {
    background-color: #00c851;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    width: 100%;
    padding: 0.5rem 1rem;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    background-color: #00a844;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 200, 81, 0.3);
}
.stChatInputContainer {
    background-color: #262730;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #fafafa;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
}
.stAlert {
    background-color: #262730;
    color: #fafafa;
}
/* Custom scrollbar for dark theme */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #262730;
}
::-webkit-scrollbar-thumb {
    background: #00c851;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #00a844;
}
/* Reduce top spacing */
.main .block-container {
    padding-top: 2rem;
}
</style>""", unsafe_allow_html=True)

# Create title with logo or icon
title_logo = get_title_logo()
if title_logo:
    # Display title with small logo
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        logo = Image.open(title_logo)
        st.image(logo, width=50)
    with col2:
        st.markdown("# AI Commerce Assistant")
        st.markdown("### 🤖 Your intelligent shopping companion powered by AI")
else:
    # Use default cart icon
    st.title("🛒 AI Commerce Assistant")
    st.subheader("🤖 Your intelligent shopping companion powered by AI")

# Add helpful sidebar with commerce features
with st.sidebar:
    # Display logo at top of sidebar
    display_sidebar_logo()
    
    st.markdown("---")  # Separator line
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
    
    # Conversation History Section
    st.header("💬 Chat History")
    
    # New conversation button
    if st.button("🆕 New Chat"):
        # Save current conversation if it has messages
        if len(st.session_state.messages) > 1:  # More than just welcome message
            save_conversation(st.session_state.messages)
        
        # Reset to new conversation
        st.session_state.messages = [
            {"role": "assistant", "content": "🛍️ Welcome to your AI Commerce Assistant! I'm here to help you with product recommendations, shopping questions, order support, and finding the best deals. What can I help you shop for today?"}
        ]
        st.session_state.buffer_memory.clear()
        st.session_state.buffer_memory.chat_memory.add_message(SystemMessage(content=COMMERCE_SYSTEM_PROMPT))
        st.session_state.current_conversation_file = None
        st.rerun()
    
    # Auto-save toggle
    st.session_state.auto_save = st.checkbox("🔄 Auto-save conversations", value=st.session_state.auto_save)
    
    # Save current conversation manually
    if st.button("💾 Save Current Chat"):
        if len(st.session_state.messages) > 1:
            filename = save_conversation(st.session_state.messages)
            if filename:
                st.session_state.current_conversation_file = filename
                st.success("💾 Conversation saved!")
        else:
            st.warning("No conversation to save!")
    
    # Load conversations
    conversations = load_conversations()
    
    if conversations:
        st.markdown("**📚 Saved Conversations:**")
        
        for i, conv in enumerate(conversations[:10]):  # Show last 10 conversations
            col1, col2 = st.columns([3, 1])
            
            with col1:
                conv_title = format_conversation_title(conv)
                if st.button(f"💬 {conv_title}", key=f"load_conv_{i}"):
                    # Load the selected conversation
                    loaded_conv = load_conversation(conv["filename"])
                    if loaded_conv:
                        st.session_state.messages = loaded_conv["messages"]
                        st.session_state.current_conversation_file = conv["filename"]
                        # Reset memory and rebuild from loaded messages
                        st.session_state.buffer_memory.clear()
                        st.session_state.buffer_memory.chat_memory.add_message(SystemMessage(content=COMMERCE_SYSTEM_PROMPT))
                        st.success(f"💬 Loaded: {conv['title']}")
                        st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"del_conv_{i}", help="Delete conversation"):
                    if delete_conversation(conv["filename"]):
                        st.success("🗑️ Deleted!")
                        st.rerun()
        
        if len(conversations) > 10:
            st.markdown(f"*... and {len(conversations) - 10} more conversations*")
    else:
        st.markdown("*No saved conversations yet*")
    
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
                
                # Auto-save conversation if enabled
                if st.session_state.auto_save and len(st.session_state.messages) > 2:
                    if st.session_state.current_conversation_file:
                        # Update existing conversation
                        save_conversation(st.session_state.messages, 
                                        st.session_state.current_conversation_file.split('_', 1)[1].replace('.json', ''))
                    else:
                        # Save new conversation
                        filename = save_conversation(st.session_state.messages)
                        if filename:
                            st.session_state.current_conversation_file = filename
                            
            except Exception as e:
                st.error(f"❌ Error generating response: {str(e)}")
                error_message = {"role": "assistant", "content": "🛒 I apologize, but I'm having trouble processing your request right now. Please try again, and I'll be happy to assist you with your shopping needs!"}
                st.session_state.messages.append(error_message)

# Clear chat button
if st.button("🗑️ Clear Chat History"):
    # Save current conversation before clearing if it has content
    if len(st.session_state.messages) > 1 and st.session_state.auto_save:
        save_conversation(st.session_state.messages)
    
    st.session_state.messages = [
        {"role": "assistant", "content": "🛍️ Welcome back! I'm here to help you with product recommendations, shopping questions, order support, and finding the best deals. What can I help you shop for today?"}
    ]
    st.session_state.buffer_memory.clear()
    st.session_state.current_conversation_file = None
    # Re-add system prompt
    st.session_state.buffer_memory.chat_memory.add_message(SystemMessage(content=COMMERCE_SYSTEM_PROMPT))
    st.rerun()
