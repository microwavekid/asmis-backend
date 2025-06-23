# Project Memory System Migration Summary

**Date:** 2025-06-22

## What Changed
- All project intelligence, memory, and progress tracking files were moved from `backend/` to the project root (`asmis/`).
- The following directories and files are now at the root:
  - `.project_memory/`
  - `track_progress/`
  - `.ai/`
  - `CLAUDE.md`
  - `.cursorrules`
  - `scripts/update_progress.py`
- All scripts, git hooks, and references were updated to use the new root-level paths.
- Tested and confirmed:
  - Git hooks (pre-commit, post-commit) work as expected.
  - `update_progress.py` works for timestamp, task add, and task complete.
  - Session files, memory, and config are accessible and up to date.
  - No broken references remain.

## Why This Matters
- Project memory and intelligence are now project-wide, not backend-specific.
- Easier for all modules (backend, frontend, infra, etc.) to share project intelligence.
- Cleaner, more maintainable repo structure.
- No more confusion about file paths for scripts, hooks, or AI agents.

## How to Use Going Forward
- Always reference project memory, progress, and AI config files from the project root.
- All automation, hooks, and AI tools should use root-relative paths (e.g., `.project_memory/...`). 