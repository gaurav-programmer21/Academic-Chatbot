from dataclasses import dataclass
from datetime import datetime

@dataclass
class KnowledgeEntry:
    topic: str
    content: str
    question: str
    answer: str
    timestamp: str
    
    def to_dict(self):
        return {
            'topic': self.topic,
            'content': self.content,
            'question': self.question,
            'answer': self.answer,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)