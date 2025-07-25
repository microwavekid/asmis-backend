"""
Async Task repositories with proper async/await support.
"""

import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta, UTC

from sqlalchemy import select, and_, or_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from .async_base_repository import AsyncTenantRepository, AsyncBaseRepository
from ..database.task_models import Task, TaskTemplate, TaskExecutionHistory
from ..auth.models import AuthContext

logger = logging.getLogger(__name__)


class AsyncTaskRepository(AsyncTenantRepository[Task]):
    """Async repository for Task operations with tenant isolation."""
    
    def __init__(self):
        """Initialize task repository."""
        super().__init__(Task)
    
    async def get_tasks_by_status(self, session: AsyncSession, status: str, auth: AuthContext, limit: Optional[int] = None) -> List[Task]:
        """Get tasks by status for a tenant.
        
        Args:
            session: Async database session
            status: Task status to filter by
            auth: Authentication context
            limit: Optional limit
            
        Returns:
            List of tasks with the specified status
        """
        try:
            stmt = select(Task).where(
                and_(
                    Task.tenant_id == auth.tenant_id,
                    Task.status == status,
                    Task.is_active.is_(True)
                )
            ).order_by(desc(Task.created_at))
            
            if limit:
                stmt = stmt.limit(limit)
            
            result = await session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting tasks by status {status}: {e}")
            raise
    
    async def get_tasks_by_assignee(self, session: AsyncSession, assignee_id: str, auth: AuthContext, 
                                   include_completed: bool = False, limit: Optional[int] = None) -> List[Task]:
        """Get tasks assigned to a specific user.
        
        Args:
            session: Async database session
            assignee_id: User ID of assignee
            auth: Authentication context
            include_completed: Whether to include completed tasks
            limit: Optional limit
            
        Returns:
            List of assigned tasks
        """
        try:
            conditions = [
                Task.tenant_id == auth.tenant_id,
                Task.assigned_to == assignee_id,
                Task.is_active.is_(True)
            ]
            
            if not include_completed:
                conditions.append(Task.status != "completed")
            
            stmt = select(Task).where(and_(*conditions)).order_by(desc(Task.priority), Task.due_date)
            
            if limit:
                stmt = stmt.limit(limit)
            
            result = await session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting tasks for assignee {assignee_id}: {e}")
            raise
    
    async def get_overdue_tasks(self, session: AsyncSession, auth: AuthContext, limit: Optional[int] = None) -> List[Task]:
        """Get overdue tasks for a tenant.
        
        Args:
            session: Async database session
            auth: Authentication context
            limit: Optional limit
            
        Returns:
            List of overdue tasks
        """
        try:
            now = datetime.now(UTC)
            stmt = select(Task).where(
                and_(
                    Task.tenant_id == auth.tenant_id,
                    Task.due_date < now,
                    Task.status.in_(["pending", "in_progress"]),
                    Task.is_active.is_(True)
                )
            ).order_by(Task.due_date)
            
            if limit:
                stmt = stmt.limit(limit)
            
            result = await session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting overdue tasks: {e}")
            raise
    
    async def search_tasks(self, session: AsyncSession, search_term: str, auth: AuthContext, 
                          filters: Optional[Dict[str, Any]] = None, limit: Optional[int] = None) -> List[Task]:
        """Search tasks by title, description, or notes.
        
        Args:
            session: Async database session
            search_term: Search term to look for
            auth: Authentication context
            filters: Additional filters to apply
            limit: Optional limit
            
        Returns:
            List of matching tasks
        """
        try:
            conditions = [
                Task.tenant_id == auth.tenant_id,
                Task.is_active.is_(True),
                or_(
                    Task.title.ilike(f"%{search_term}%"),
                    Task.description.ilike(f"%{search_term}%"),
                    Task.notes.ilike(f"%{search_term}%")
                )
            ]
            
            # Apply additional filters
            if filters:
                for field, value in filters.items():
                    if hasattr(Task, field):
                        if field.endswith("__ne"):
                            field_name = field[:-4]
                            if hasattr(Task, field_name):
                                conditions.append(getattr(Task, field_name) != value)
                        else:
                            conditions.append(getattr(Task, field) == value)
            
            stmt = select(Task).where(and_(*conditions)).order_by(desc(Task.updated_at))
            
            if limit:
                stmt = stmt.limit(limit)
            
            result = await session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            self.logger.error(f"Error searching tasks: {e}")
            raise
    
    async def assign_task(self, session: AsyncSession, task_id: str, assigned_to: str, auth: AuthContext) -> Optional[Task]:
        """Assign a task to a user.
        
        Args:
            session: Async database session
            task_id: Task ID
            assigned_to: User ID to assign to
            auth: Authentication context
            
        Returns:
            Updated task or None if not found
        """
        try:
            task = await self.get_by_id_with_auth(session, task_id, auth)
            if not task:
                return None
            
            task.assigned_to = assigned_to
            task.updated_at = datetime.now(UTC)
            
            await session.commit()
            await session.refresh(task)
            
            self.logger.info(f"Assigned task {task_id} to user {assigned_to}")
            return task
        except SQLAlchemyError as e:
            await session.rollback()
            self.logger.error(f"Error assigning task {task_id}: {e}")
            raise
    
    async def update_task_status(self, session: AsyncSession, task_id: str, status: str, auth: AuthContext,
                                outcome_status: Optional[str] = None, outcome_notes: Optional[str] = None) -> Optional[Task]:
        """Update task status and optionally outcome details.
        
        Args:
            session: Async database session
            task_id: Task ID
            status: New status
            auth: Authentication context
            outcome_status: Optional outcome status
            outcome_notes: Optional outcome notes
            
        Returns:
            Updated task or None if not found
        """
        try:
            task = await self.get_by_id_with_auth(session, task_id, auth)
            if not task:
                return None
            
            task.status = status
            task.updated_at = datetime.now(UTC)
            
            # Set completion timestamp if completed
            if status == "completed":
                task.completed_at = datetime.now(UTC)
                task.execution_status = "completed"
            
            # Update outcome details if provided
            if outcome_status:
                task.outcome_status = outcome_status
            if outcome_notes:
                task.outcome_notes = outcome_notes
            
            await session.commit()
            await session.refresh(task)
            
            self.logger.info(f"Updated task {task_id} status to {status}")
            return task
        except SQLAlchemyError as e:
            await session.rollback()
            self.logger.error(f"Error updating task status {task_id}: {e}")
            raise
    
    async def get_task_statistics(self, session: AsyncSession, auth: AuthContext, 
                                 date_range: Optional[Tuple[datetime, datetime]] = None) -> Dict[str, Any]:
        """Get task statistics for a tenant.
        
        Args:
            session: Async database session
            auth: Authentication context
            date_range: Optional date range tuple (start, end)
            
        Returns:
            Dictionary containing task statistics
        """
        try:
            conditions = [
                Task.tenant_id == auth.tenant_id,
                Task.is_active.is_(True)
            ]
            
            if date_range:
                start_date, end_date = date_range
                conditions.append(Task.created_at.between(start_date, end_date))
            
            # Get basic counts
            base_stmt = select(Task).where(and_(*conditions))
            
            # Total tasks
            total_result = await session.execute(select(func.count()).select_from(base_stmt.subquery()))
            total_tasks = total_result.scalar()
            
            # Status breakdown
            status_stmt = select(Task.status, func.count(Task.id)).where(and_(*conditions)).group_by(Task.status)
            status_result = await session.execute(status_stmt)
            status_counts = dict(status_result.all())
            
            # Priority breakdown
            priority_stmt = select(Task.priority, func.count(Task.id)).where(and_(*conditions)).group_by(Task.priority)
            priority_result = await session.execute(priority_stmt)
            priority_counts = dict(priority_result.all())
            
            # Execution mode breakdown
            mode_stmt = select(Task.execution_mode, func.count(Task.id)).where(and_(*conditions)).group_by(Task.execution_mode)
            mode_result = await session.execute(mode_stmt)
            mode_counts = dict(mode_result.all())
            
            # Credit usage
            credit_stmt = select(
                func.sum(Task.estimated_credits),
                func.sum(Task.actual_credits_used),
                func.avg(Task.actual_credits_used)
            ).where(and_(*conditions))
            credit_result = await session.execute(credit_stmt)
            estimated_total, used_total, avg_used = credit_result.first()
            
            return {
                "total_tasks": total_tasks,
                "status_breakdown": status_counts,
                "priority_breakdown": priority_counts,
                "execution_mode_breakdown": mode_counts,
                "credit_usage": {
                    "total_estimated": estimated_total or 0,
                    "total_used": used_total or 0,
                    "average_used": round(avg_used or 0, 2),
                    "efficiency": round((used_total or 0) / max(estimated_total or 1, 1) * 100, 2)
                },
                "date_range": date_range
            }
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting task statistics: {e}")
            raise


class AsyncTaskTemplateRepository(AsyncTenantRepository[TaskTemplate]):
    """Async repository for TaskTemplate operations with tenant isolation."""
    
    def __init__(self):
        """Initialize task template repository."""
        super().__init__(TaskTemplate)
    
    async def get_templates_by_category(self, session: AsyncSession, category: str, auth: AuthContext, 
                                       limit: Optional[int] = None) -> List[TaskTemplate]:
        """Get templates by category for a tenant.
        
        Args:
            session: Async database session
            category: Template category
            auth: Authentication context
            limit: Optional limit
            
        Returns:
            List of templates in the category
        """
        try:
            stmt = select(TaskTemplate).where(
                and_(
                    TaskTemplate.tenant_id == auth.tenant_id,
                    TaskTemplate.category == category,
                    TaskTemplate.is_active.is_(True)
                )
            ).order_by(desc(TaskTemplate.usage_count))
            
            if limit:
                stmt = stmt.limit(limit)
            
            result = await session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting templates by category {category}: {e}")
            raise
    
    async def increment_template_usage(self, session: AsyncSession, template_id: str, auth: AuthContext) -> Optional[TaskTemplate]:
        """Increment the usage count for a template.
        
        Args:
            session: Async database session
            template_id: Template ID
            auth: Authentication context
            
        Returns:
            Updated template or None if not found
        """
        try:
            template = await self.get_by_id_with_auth(session, template_id, auth)
            if not template:
                return None
            
            template.usage_count += 1
            template.last_used_at = datetime.now(UTC)
            template.updated_at = datetime.now(UTC)
            
            await session.commit()
            await session.refresh(template)
            
            self.logger.info(f"Incremented usage count for template {template_id}")
            return template
        except SQLAlchemyError as e:
            await session.rollback()
            self.logger.error(f"Error incrementing template usage {template_id}: {e}")
            raise


class AsyncTaskExecutionHistoryRepository(AsyncBaseRepository[TaskExecutionHistory]):
    """Async repository for TaskExecutionHistory operations with tenant isolation via task relationship."""
    
    def __init__(self):
        """Initialize task execution history repository."""
        super().__init__(TaskExecutionHistory)
    
    async def create_execution_record(
        self, 
        session: AsyncSession, 
        task_id: str,
        executor_type: str,
        executor_id: str,
        action_type: str,
        action_details: Dict[str, Any],
        result_status: str,
        auth: AuthContext,
        credits_consumed: int = 0,
        **kwargs
    ) -> TaskExecutionHistory:
        """Create a new execution history record.
        
        Args:
            session: Async database session
            task_id: Task ID
            executor_type: Type of executor (human, ai_assisted, ai_autonomous)
            executor_id: ID of executor
            action_type: Type of action performed
            action_details: Details of the action
            result_status: Result status
            auth: Authentication context
            credits_consumed: Credits consumed
            **kwargs: Additional fields
            
        Returns:
            Created execution history record
        """
        try:
            record_data = {
                "task_id": task_id,
                "execution_timestamp": datetime.now(UTC),
                "executor_type": executor_type,
                "executor_id": executor_id,
                "action_type": action_type,
                "action_details": action_details,
                "result_status": result_status,
                "credits_consumed": credits_consumed,
                **kwargs
            }
            
            return await self.create(session, **record_data)
        except SQLAlchemyError as e:
            self.logger.error(f"Error creating execution record: {e}")
            raise
    
    async def get_history_for_task(self, session: AsyncSession, task_id: str, auth: AuthContext, 
                                  limit: Optional[int] = None) -> List[TaskExecutionHistory]:
        """Get execution history for a task with tenant isolation.
        
        Args:
            session: Async database session
            task_id: Task ID
            auth: Authentication context
            limit: Optional limit
            
        Returns:
            List of execution history records
        """
        try:
            # Join with tasks table to ensure tenant isolation
            stmt = select(TaskExecutionHistory).join(Task).where(
                and_(
                    TaskExecutionHistory.task_id == task_id,
                    Task.tenant_id == auth.tenant_id,
                    Task.is_active.is_(True)
                )
            ).order_by(desc(TaskExecutionHistory.execution_timestamp))
            
            if limit:
                stmt = stmt.limit(limit)
            
            result = await session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting history for task {task_id}: {e}")
            raise