# 💬 Conversation History Feature Guide

## Overview

The AI Commerce Chatbot now includes a comprehensive conversation history system that allows users to save, browse, and continue previous conversations.

## Key Features

### 🔄 **Auto-Save** (Default: ON)
- Automatically saves conversations after each AI response
- No manual intervention required
- Can be toggled on/off in the sidebar

### 🆕 **New Chat**
- Start a fresh conversation
- Automatically saves the current chat before starting new one
- Resets the conversation context

### 💾 **Manual Save**
- Save conversations at any time
- Useful for important conversations you want to preserve
- Generates automatic titles from first user message

### 📚 **Browse History**
- View up to 10 most recent conversations
- Shows conversation title and timestamp
- Click to load and continue any conversation

### 🗑️ **Delete Conversations**
- Remove unwanted conversations
- Individual delete buttons for each saved chat
- Permanent deletion (cannot be undone)

## How It Works

### Sidebar Interface
The conversation history is managed through the sidebar with these sections:

1. **💬 Chat History** header
2. **🆕 New Chat** button
3. **🔄 Auto-save** toggle checkbox
4. **💾 Save Current Chat** button
5. **📚 Saved Conversations** list with load/delete buttons

### File Storage
- Conversations are saved in the `conversations/` folder
- Each conversation is a JSON file with timestamp and title
- Format: `YYYYMMDD_HHMMSS_title.json`

### Example Workflow

1. **Start chatting** - Conversation begins normally
2. **Auto-save** - After each response, conversation is automatically saved
3. **Browse history** - Click on any saved conversation in the sidebar
4. **Continue conversation** - Loaded conversation maintains full context
5. **Delete when done** - Remove conversations you no longer need

## Technical Details

### File Structure
```json
{
  "timestamp": "20250627_143022",
  "title": "Looking for a laptop under $800...",
  "messages": [
    {"role": "assistant", "content": "Welcome message"},
    {"role": "user", "content": "User question"},
    {"role": "assistant", "content": "AI response"}
  ],
  "created": "2025-06-27T14:30:22.123456"
}
```

### Memory Management
- When loading a conversation, the AI's context memory is rebuilt
- Full conversation history is maintained
- System prompt is preserved across all conversations

## Benefits

✅ **Never lose important conversations**  
✅ **Resume complex shopping discussions**  
✅ **Reference previous product recommendations**  
✅ **Track shopping decisions over time**  
✅ **Seamless experience across sessions**

## Privacy Note

Conversations are stored locally on your system. To exclude them from git repositories, uncomment the line in `.gitignore`:

```
# conversations/*.json
```

This ensures your conversation history remains private when sharing code.
