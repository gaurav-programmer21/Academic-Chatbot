import json
from datetime import datetime
from typing import List, Dict, Optional
from utils.storage import StorageManager

class KnowledgeService:
    def __init__(self):
        self.storage = StorageManager('data/knowledge_base.json')
        self.knowledge = self.storage.load()
    
    def add_knowledge(self, knowledge_entry: Dict):
        """Add new knowledge entry"""
        knowledge_entry['timestamp'] = datetime.now().isoformat()
        self.knowledge.append(knowledge_entry)
        self.storage.save(self.knowledge)
    
    def get_all_knowledge(self) -> List[Dict]:
        """Get all knowledge entries"""
        return self.knowledge
    
    def extract_knowledge(self, question: str, answer: str) -> Optional[Dict]:
        """Extract knowledge from Q&A pair"""
        keywords = ['explain', 'what is', 'define', 'describe', 'how does', 'why']
        
        # Check if question contains learning keywords
        if any(keyword in question.lower() for keyword in keywords):
            if len(answer) > 50:
                return {
                    'topic': question[:100],
                    'content': answer[:300],
                    'question': question,
                    'answer': answer
                }
        return None
    
    def clear_knowledge(self):
        """Clear all knowledge entries"""
        self.knowledge = []
        self.storage.save(self.knowledge)
    
    def search_knowledge(self, query: str) -> List[Dict]:
        """Search knowledge base"""
        query_lower = query.lower()
        results = []
        
        for entry in self.knowledge:
            if (query_lower in entry.get('topic', '').lower() or 
                query_lower in entry.get('content', '').lower()):
                results.append(entry)
        
        return results
