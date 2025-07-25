"""
Enhanced Task API Router with AI features and tenant isolation.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta, UTC
import logging

from ..database.connection import get_async_db_session
from ..database.task_models import Task, TaskTemplate, TaskExecutionHistory
from ..database.models import User
from ..schemas.task_schemas import (
    TaskResponse, TaskCreate, TaskUpdate, TaskListResponse,
    TaskAssignment, TaskCompletion, TaskApproval,
    TaskTemplateResponse, TaskTemplateCreate, TaskTemplateUpdate,
    TaskExecutionHistoryResponse,
    BulkTaskCreate, BulkTaskResponse,
    TaskSuggestionRequest, TaskSuggestionsResponse,
    CreditEstimationRequest, CreditEstimationResponse,
    TemplateRecommendationRequest, TemplateRecommendationResponse,
    TaskStatus, TaskPriority, ExecutionMode
)
from ..repositories.async_task_repository import (
    AsyncTaskRepository, AsyncTaskTemplateRepository, AsyncTaskExecutionHistoryRepository
)
from ..auth.models import AuthContext
from .router_config import get_auth_dependency

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

# Initialize repositories
task_repo = AsyncTaskRepository()
template_repo = AsyncTaskTemplateRepository()
history_repo = AsyncTaskExecutionHistoryRepository()


# Task CRUD Endpoints

@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    execution_mode: Optional[ExecutionMode] = Query(None, description="Filter by execution mode"),
    assigned_to: Optional[str] = Query(None, description="Filter by assigned user ID"),
    deal_id: Optional[str] = Query(None, description="Filter by deal ID"),
    account_id: Optional[str] = Query(None, description="Filter by account ID"),
    stakeholder_id: Optional[str] = Query(None, description="Filter by stakeholder ID"),
    include_completed: bool = Query(True, description="Include completed tasks"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search in title, description, notes"),
    db: AsyncSession = Depends(get_async_db_session),
    auth: AuthContext = Depends(get_auth_dependency())
):
    """List tasks with filtering and pagination."""
    try:
        # Build filters
        filters = {}
        if status:
            filters["status"] = status.value
        if priority:
            filters["priority"] = priority.value
        if execution_mode:
            filters["execution_mode"] = execution_mode.value
        if assigned_to:
            filters["assigned_to"] = assigned_to
        if deal_id:
            filters["deal_id"] = deal_id
        if account_id:
            filters["account_id"] = account_id
        if stakeholder_id:
            filters["stakeholder_id"] = stakeholder_id
        
        # Apply completed filter
        if not include_completed:
            filters["status__ne"] = "completed"
        
        # Get tasks
        if search:
            tasks = await task_repo.search_tasks(db, search, auth, filters, per_page)
        else:
            # Get all tasks with basic filtering
            all_tasks = await task_repo.get_all_with_auth(db, auth)
            
            # Apply filters manually (in production, this would be done in the query)
            filtered_tasks = []
            for task in all_tasks:
                match = True
                if status and task.status != status.value:
                    match = False
                if priority and task.priority != priority.value:
                    match = False
                if execution_mode and task.execution_mode != execution_mode.value:
                    match = False
                if assigned_to and task.assigned_to != assigned_to:
                    match = False
                if deal_id and task.deal_id != deal_id:
                    match = False
                if account_id and task.account_id != account_id:
                    match = False
                if stakeholder_id and task.stakeholder_id != stakeholder_id:
                    match = False
                if not include_completed and task.status == "completed":
                    match = False
                    
                if match:
                    filtered_tasks.append(task)
            
            # Simple pagination
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            tasks = filtered_tasks[start_idx:end_idx]
        
        total = len(tasks)  # Simplified for now
        
        return TaskListResponse(
            tasks=[TaskResponse.from_orm(task) for task in tasks],
            total=total,
            page=page,
            per_page=per_page,
            has_next=len(tasks) == per_page,
            has_prev=page > 1
        )
        
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks"
        )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    db: AsyncSession = Depends(get_async_db_session),
    auth: AuthContext = Depends(get_auth_dependency())
):
    """Get a specific task by ID."""
    try:
        task = await task_repo.get_by_id_with_auth(db, task_id, auth)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return TaskResponse.from_orm(task)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task"
        )


@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_async_db_session),
    auth: AuthContext = Depends(get_auth_dependency())
):
    """Create a new task."""
    try:
        # Prepare task data
        task_dict = {
            "title": task_data.title,
            "description": task_data.description,
            "status": task_data.status.value,
            "due_date": task_data.due_date,
            "priority": task_data.priority.value,
            "assigned_to": task_data.assigned_to,
            "deal_id": task_data.deal_id,
            "account_id": task_data.account_id,
            "stakeholder_id": task_data.stakeholder_id,
            "task_type": task_data.task_type.value,
            "execution_mode": task_data.execution_mode.value,
            "source": task_data.source,
            "template_id": task_data.template_id,
            "template_parameters": task_data.template_parameters,
            "smart_capture_id": task_data.smart_capture_id,
            "transcript_segments": task_data.transcript_segments,
            "tags": task_data.tags,
            "notes": task_data.notes,
            "user_id": auth.user_id,
            "estimated_credits": 0,
            "actual_credits_used": 0,
            "complexity_tier": "simple",
            "execution_status": "not_started",
            "execution_method": "manual",
            "requires_approval": False
        }
        
        # Create task using repository
        task = await task_repo.create_with_auth(db, auth, **task_dict)
        
        # If created from template, increment usage count
        if task_data.template_id:
            await template_repo.increment_template_usage(db, task_data.template_id, auth)
        
        # Log creation in execution history
        await history_repo.create_execution_record(
            db, task.id, "human", auth.user_id, "task_created",
            {"source": task_data.source, "template_used": bool(task_data.template_id)},
            "success", auth, 0
        )
        
        return TaskResponse.from_orm(task)
        
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_async_db_session),
    auth: AuthContext = Depends(get_auth_dependency())
):
    """Update a task."""
    try:
        task = await task_repo.get_by_id_with_auth(db, task_id, auth)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Track changes for history
        changes = {}
        if task_data.title is not None and task_data.title != task.title:
            changes["title"] = {"from": task.title, "to": task_data.title}
            task.title = task_data.title
        
        if task_data.description is not None and task_data.description != task.description:
            changes["description"] = {"from": task.description, "to": task_data.description}
            task.description = task_data.description
            
        if task_data.status is not None and task_data.status.value != task.status:
            changes["status"] = {"from": task.status, "to": task_data.status.value}
            task.status = task_data.status.value
            
            # Auto-set completed_at if status changed to completed
            if task_data.status.value == "completed" and not task.completed_at:
                task.completed_at = datetime.now(UTC)
        
        if task_data.due_date is not None and task_data.due_date != task.due_date:
            changes["due_date"] = {"from": task.due_date, "to": task_data.due_date}
            task.due_date = task_data.due_date
            
        if task_data.priority is not None and task_data.priority.value != task.priority:
            changes["priority"] = {"from": task.priority, "to": task_data.priority.value}
            task.priority = task_data.priority.value
            
        if task_data.assigned_to is not None and task_data.assigned_to != task.assigned_to:
            changes["assigned_to"] = {"from": task.assigned_to, "to": task_data.assigned_to}
            task.assigned_to = task_data.assigned_to
        
        if task_data.execution_mode is not None and task_data.execution_mode.value != task.execution_mode:
            changes["execution_mode"] = {"from": task.execution_mode, "to": task_data.execution_mode.value}
            task.execution_mode = task_data.execution_mode.value
        
        if task_data.execution_status is not None and task_data.execution_status != task.execution_status:
            changes["execution_status"] = {"from": task.execution_status, "to": task_data.execution_status}
            task.execution_status = task_data.execution_status
        
        if task_data.outcome_status is not None and task_data.outcome_status != task.outcome_status:
            changes["outcome_status"] = {"from": task.outcome_status, "to": task_data.outcome_status}
            task.outcome_status = task_data.outcome_status
            
        if task_data.outcome_notes is not None and task_data.outcome_notes != task.outcome_notes:
            task.outcome_notes = task_data.outcome_notes
        
        if task_data.tags is not None:
            task.tags = task_data.tags
            
        if task_data.notes is not None:
            task.notes = task_data.notes
        
        task.updated_at = datetime.now(UTC)
        await db.commit()
        
        # Log update in execution history if there were changes
        if changes:
            await history_repo.create_execution_record(
                db, task.id, "human", auth.user_id, "task_updated",
                {"changes": changes}, "success", auth, 0
            )
        
        return TaskResponse.from_orm(task)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )


@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    db: AsyncSession = Depends(get_async_db_session),
    auth: AuthContext = Depends(get_auth_dependency())
):
    """Soft delete a task."""
    try:
        task = await task_repo.get_by_id_with_auth(db, task_id, auth)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Soft delete
        task.is_active = False
        task.updated_at = datetime.now(UTC)
        await db.commit()
        
        # Log deletion in execution history
        await history_repo.create_execution_record(
            db, task.id, "human", auth.user_id, "task_deleted",
            {"reason": "user_request"}, "success", auth, 0
        )
        
        return {"message": "Task deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )


# Specialized Task Operations

@router.post("/{task_id}/assign", response_model=TaskResponse)
async def assign_task(
    task_id: str,
    assignment_data: TaskAssignment,
    db: AsyncSession = Depends(get_async_db_session),
    auth: AuthContext = Depends(get_auth_dependency())
):
    """Assign a task to a user."""
    try:
        task = await task_repo.assign_task(db, task_id, assignment_data.assigned_to, auth)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Log assignment in execution history
        await history_repo.create_execution_record(
            db, task.id, "human", auth.user_id, "task_assigned",
            {
                "assigned_to": assignment_data.assigned_to,
                "notes": assignment_data.notes
            },
            "success", auth, 0
        )
        
        return TaskResponse.from_orm(task)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assigning task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to assign task"
        )


@router.post("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: str,
    completion_data: TaskCompletion,
    db: AsyncSession = Depends(get_async_db_session),
    auth: AuthContext = Depends(get_auth_dependency())
):
    """Mark a task as completed."""
    try:
        task = await task_repo.update_task_status(
            db, task_id, "completed", auth,
            completion_data.outcome_status,
            completion_data.outcome_notes
        )
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Update outcome metrics if provided
        if completion_data.outcome_metrics:
            task.outcome_metrics = completion_data.outcome_metrics
            await db.commit()
        
        # Log completion in execution history
        await history_repo.create_execution_record(
            db, task.id, "human", auth.user_id, "task_completed",
            {
                "outcome_status": completion_data.outcome_status,
                "outcome_notes": completion_data.outcome_notes
            },
            "success", auth, 0
        )
        
        return TaskResponse.from_orm(task)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error completing task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete task"
        )


# Task History and Analytics

@router.get("/{task_id}/history", response_model=List[TaskExecutionHistoryResponse])
async def get_task_history(
    task_id: str,
    limit: int = Query(50, ge=1, le=100, description="Limit number of history records"),
    db: AsyncSession = Depends(get_async_db_session),
    auth: AuthContext = Depends(get_auth_dependency())
):
    """Get execution history for a task."""
    try:
        history = await history_repo.get_history_for_task(db, task_id, auth, limit)
        return [TaskExecutionHistoryResponse.from_orm(record) for record in history]
        
    except Exception as e:
        logger.error(f"Error getting task history {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task history"
        )


@router.get("/analytics/statistics", response_model=Dict[str, Any])
async def get_task_statistics(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: AsyncSession = Depends(get_async_db_session),
    auth: AuthContext = Depends(get_auth_dependency())
):
    """Get task analytics and statistics."""
    try:
        end_date = datetime.now(UTC)
        start_date = end_date - timedelta(days=days)
        
        stats = await task_repo.get_task_statistics(db, auth, (start_date, end_date))
        return stats
        
    except Exception as e:
        logger.error(f"Error getting task statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task statistics"
        )


# Convenience Endpoints

@router.get("/my", response_model=List[TaskResponse])
async def get_my_tasks(
    include_completed: bool = Query(False, description="Include completed tasks"),
    limit: int = Query(50, ge=1, le=100, description="Limit number of tasks"),
    db: AsyncSession = Depends(get_async_db_session),
    auth: AuthContext = Depends(get_auth_dependency())
):
    """Get tasks assigned to the current user."""
    try:
        tasks = await task_repo.get_tasks_by_assignee(
            db, auth.user_id, auth, include_completed, limit
        )
        return [TaskResponse.from_orm(task) for task in tasks]
        
    except Exception as e:
        logger.error(f"Error getting my tasks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve your tasks"
        )


@router.get("/overdue", response_model=List[TaskResponse])
async def get_overdue_tasks(
    limit: int = Query(50, ge=1, le=100, description="Limit number of tasks"),
    db: AsyncSession = Depends(get_async_db_session),
    auth: AuthContext = Depends(get_auth_dependency())
):
    """Get overdue tasks."""
    try:
        tasks = await task_repo.get_overdue_tasks(db, auth, limit)
        return [TaskResponse.from_orm(task) for task in tasks]
        
    except Exception as e:
        logger.error(f"Error getting overdue tasks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve overdue tasks"
        )