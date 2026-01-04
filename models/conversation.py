from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Message:
    role: str
    content: str
    timestamp: str
    model: Optional[str] = None
    
    def to_dict(self):
        return {
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp,
            'model': self.model
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)