import json
import os
from typing import List, Dict

class StorageManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump([], f)
    
    def load(self) -> List[Dict]:
        """Load data from file"""
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save(self, data: List[Dict]):
        """Save data to file"""
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def clear(self):
        """Clear all data"""
        self.save([])