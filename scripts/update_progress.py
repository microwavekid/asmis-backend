#!/usr/bin/env python3
"""
ASMIS Progress Tracking Update Script

Usage:
    python scripts/update_progress.py "task description"
    python scripts/update_progress.py --mark-complete "Fix client initialization"
    python scripts/update_progress.py --add-task "New feature implementation"
    python scripts/update_progress.py --ai-update "Task description" "completion notes"
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path

def update_timestamp():
    """Update the timestamp in context_recovery.md"""
    context_file = Path(".project_memory/progress/context_recovery.md")
    
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
    todo_file = Path(".project_memory/progress/todo_tracker.md")
    
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
    todo_file = Path(".project_memory/progress/todo_tracker.md")
    
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

def ai_update_task(task_description, completion_notes=""):
    """
    AI-friendly function to update todo_tracker.md with completion details.
    
    Args:
        task_description: Description of the completed task
        completion_notes: Optional notes about the completion
    """
    todo_file = Path(".project_memory/progress/todo_tracker.md")
    
    if not todo_file.exists():
        print("❌ todo_tracker.md not found")
        return False
    
    with open(todo_file, 'r') as f:
        content = f.read()
    
    # Update timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Mark task as complete
    task_pattern = rf"(- \[ \].*{re.escape(task_description)}.*)"
    replacement = rf"\1  - ✅ Completed: {timestamp}"
    if completion_notes:
        replacement += f" - Notes: {completion_notes}"
    
    updated_content = re.sub(task_pattern, replacement, content, flags=re.IGNORECASE)
    
    # Update last updated timestamp
    updated_content = re.sub(
        r"Last Updated:.*",
        f"Last Updated: {timestamp}",
        updated_content
    )
    
    with open(todo_file, 'w') as f:
        f.write(updated_content)
    
    print(f"✅ AI updated task: {task_description}")
    print(f"   Timestamp: {timestamp}")
    if completion_notes:
        print(f"   Notes: {completion_notes}")
    
    return True

def get_current_status():
    """Get current status summary for AI agents."""
    todo_file = Path(".project_memory/progress/todo_tracker.md")
    
    if not todo_file.exists():
        return "todo_tracker.md not found"
    
    with open(todo_file, 'r') as f:
        content = f.read()
    
    # Count tasks
    total_tasks = len(re.findall(r"- \[[ x]\]", content))
    completed_tasks = len(re.findall(r"- \[x\]", content))
    pending_tasks = total_tasks - completed_tasks
    
    # Get last updated
    last_updated_match = re.search(r"Last Updated: (.*)", content)
    last_updated = last_updated_match.group(1) if last_updated_match else "Unknown"
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "completion_rate": f"{(completed_tasks/total_tasks*100):.1f}%" if total_tasks > 0 else "0%",
        "last_updated": last_updated
    }

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
    
    elif command == "--ai-update" and len(sys.argv) > 2:
        task_desc = sys.argv[2]
        completion_notes = sys.argv[3] if len(sys.argv) > 3 else ""
        ai_update_task(task_desc, completion_notes)
    
    elif command == "--status":
        status = get_current_status()
        print("📊 Current Status:")
        for key, value in status.items():
            print(f"   {key}: {value}")
    
    elif command == "--timestamp":
        update_timestamp()
    
    else:
        # Default: just update timestamp
        update_timestamp()
        print(f"ℹ️  Use --mark-complete 'task' or --add-task 'task' for more options")

if __name__ == "__main__":
    main() 