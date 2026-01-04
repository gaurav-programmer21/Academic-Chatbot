from datetime import datetime
from typing import List, Dict
from utils.storage import StorageManager

class MemoryService:
    def __init__(self):
        self.storage = StorageManager('data/conversations.json')
        self.history = self.storage.load()
    
    def add_message(self, role: str, content: str):
        """Add message to history"""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        self.history.append(message)
        self.storage.save(self.history)
    
    def get_recent_history(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        return self.history[-limit:] if self.history else []
    
    def get_all_history(self) -> List[Dict]:
        """Get all conversation history"""
        return self.history
    
    def clear_history(self):
        """Clear all history"""
        self.history = []
        self.storage.save(self.history)
    
    def get_conversation_summary(self) -> Dict:
        """Get conversation statistics"""
        user_messages = sum(1 for msg in self.history if msg['role'] == 'user')
        assistant_messages = sum(1 for msg in self.history if msg['role'] == 'assistant')
        
        return {
            'total_messages': len(self.history),
            'user_messages': user_messages,
            'assistant_messages': assistant_messages
        }