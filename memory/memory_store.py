import json
import os

MEMORY_FILE = "memory/memory.jsonl"


def save_to_memory(record: dict):
    os.makedirs("memory", exist_ok=True)
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def find_similar_by_topic(topic: str, limit: int = 3):
    results = []

    if not os.path.exists(MEMORY_FILE):
        return results

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
                parsed = record.get("parsed_problem", {})
                if parsed.get("topic") == topic:
                    results.append(record)
            except json.JSONDecodeError:
                continue

    return results[-limit:]
