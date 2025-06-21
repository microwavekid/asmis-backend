#!/usr/bin/env python3
"""
ASMIS Progress Tracking Update Script

Usage:
    python scripts/update_progress.py "task description"
    python scripts/update_progress.py --mark-complete "Fix client initialization"
    python scripts/update_progress.py --add-task "New feature implementation"
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path

def update_timestamp():
    """Update the timestamp in context_recovery.md"""
    context_file = Path("track_progress/context_recovery.md")
    
    if not context_file.exists():
        print("❌ context_recovery.md not found")
        return False
    
    with open(context_file, 'r') as f:
        content = f.read()
    
    # Update timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_content = re.sub(
        r"Last Updated:.*",
        f"Last Updated: {timestamp}",
        content
    )
    
    with open(context_file, 'w') as f:
        f.write(updated_content)
    
    print(f"✅ Updated timestamp: {timestamp}")
    return True

def mark_task_complete(task_description):
    """Mark a task as complete in todo_tracker.md"""
    todo_file = Path("track_progress/todo_tracker.md")
    
    if not todo_file.exists():
        print("❌ todo_tracker.md not found")
        return False
    
    with open(todo_file, 'r') as f:
        lines = f.readlines()
    
    task_found = False
    for i, line in enumerate(lines):
        if task_description.lower() in line.lower() and "[ ]" in line:
            lines[i] = line.replace("[ ]", "[x]")
            task_found = True
            break
    
    if task_found:
        with open(todo_file, 'w') as f:
            f.writelines(lines)
        print(f"✅ Marked task complete: {task_description}")
        return True
    else:
        print(f"⚠️  Task not found: {task_description}")
        return False

def add_task(task_description):
    """Add a new task to todo_tracker.md"""
    todo_file = Path("track_progress/todo_tracker.md")
    
    if not todo_file.exists():
        print("❌ todo_tracker.md not found")
        return False
    
    with open(todo_file, 'r') as f:
        lines = f.readlines()
    
    # Find the end of the current tasks section
    insert_index = len(lines)
    for i, line in enumerate(lines):
        if "## 🧪 TESTING TASKS" in line:
            insert_index = i + 1
            break
    
    # Add new task
    new_task = f"- [ ] {task_description}\n"
    lines.insert(insert_index, new_task)
    
    with open(todo_file, 'w') as f:
        f.writelines(lines)
    
    print(f"✅ Added new task: {task_description}")
    return True

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1]
    
    if command == "--mark-complete" and len(sys.argv) > 2:
        task_desc = sys.argv[2]
        update_timestamp()
        mark_task_complete(task_desc)
    
    elif command == "--add-task" and len(sys.argv) > 2:
        task_desc = sys.argv[2]
        update_timestamp()
        add_task(task_desc)
    
    elif command == "--timestamp":
        update_timestamp()
    
    else:
        # Default: just update timestamp
        update_timestamp()
        print(f"ℹ️  Use --mark-complete 'task' or --add-task 'task' for more options")

if __name__ == "__main__":
    main() 