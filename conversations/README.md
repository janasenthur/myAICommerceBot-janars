# Conversation History

This folder stores saved conversations from the AI Commerce Chatbot.

## Structure

Each conversation is saved as a JSON file with the following structure:

```json
{
  "timestamp": "20250627_143022",
  "title": "Looking for a laptop under $800...",
  "messages": [
    {
      "role": "assistant",
      "content": "Welcome message..."
    },
    {
      "role": "user", 
      "content": "User's question..."
    },
    {
      "role": "assistant",
      "content": "AI's response..."
    }
  ],
  "created": "2025-06-27T14:30:22.123456"
}
```

## Features

- **Auto-save**: Conversations are automatically saved when auto-save is enabled
- **Manual save**: Users can manually save conversations at any time
- **Load & Continue**: Previously saved conversations can be loaded and continued
- **Delete**: Unwanted conversations can be deleted
- **Browse History**: View up to 10 recent conversations in the sidebar

## File Naming

Files are named with the pattern: `YYYYMMDD_HHMMSS_title.json`

Example: `20250627_143022_Looking_for_a_laptop_under_800.json`

## Notes

- Conversations are stored locally in this folder
- Each conversation includes full message history
- Titles are automatically generated from the first user message
- Files are sorted by timestamp (newest first) in the UI
