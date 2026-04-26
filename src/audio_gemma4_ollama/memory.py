import json
import os
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

def append_memory(record: Dict[str, Any], path: str = "data/memory/memory.jsonl"):
    """
    Append a memory record to a JSONL file.
    Validates required fields: id, kind, text, source.
    """
    required_fields = ["id", "kind", "text", "source"]
    for field in required_fields:
        if field not in record:
            raise ValueError(f"Missing required field: {field}")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Set default values if missing
    if "created_at" not in record:
        record["created_at"] = datetime.now(timezone.utc).isoformat()
    if "tags" not in record:
        record["tags"] = []
    if "confidence" not in record:
        record["confidence"] = 1.0
    if "metadata" not in record:
        record["metadata"] = {}

    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

def read_memories(path: str = "data/memory/memory.jsonl") -> List[Dict[str, Any]]:
    """
    Read all memories from a JSONL file.
    """
    if not os.path.exists(path):
        return []
    
    memories = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                memories.append(json.loads(line))
    return memories
