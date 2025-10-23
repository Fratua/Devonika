"""
Project Manager - Manages project state and progress
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class ProjectManager:
    """
    Manages project state, tracks progress, and handles task prioritization.
    """

    def __init__(self, workspace: Path, logger: logging.Logger):
        self.workspace = workspace
        self.logger = logger

    def save_project_plan(self, project_path: Path, plan: Dict[str, Any]) -> None:
        """Save project plan to disk"""
        plan_file = project_path / ".devonika" / "plan.json"
        plan_file.parent.mkdir(parents=True, exist_ok=True)
        plan_file.write_text(json.dumps(plan, indent=2))
        self.logger.debug("Project plan saved")

    def save_architecture(self, project_path: Path, architecture: Dict[str, Any]) -> None:
        """Save architecture to disk"""
        arch_file = project_path / ".devonika" / "architecture.json"
        arch_file.parent.mkdir(parents=True, exist_ok=True)
        arch_file.write_text(json.dumps(architecture, indent=2))
        self.logger.debug("Architecture saved")

    def save_progress(self, project_path: Path, progress: Dict[str, Any]) -> None:
        """Save project progress"""
        progress_file = project_path / ".devonika" / "progress.json"
        progress_file.parent.mkdir(parents=True, exist_ok=True)

        progress["last_updated"] = datetime.now().isoformat()

        progress_file.write_text(json.dumps(progress, indent=2))
        self.logger.debug(f"Progress saved: iteration {progress.get('iteration', 0)}")

    def load_progress(self, project_path: Path) -> Optional[Dict[str, Any]]:
        """Load project progress"""
        progress_file = project_path / ".devonika" / "progress.json"
        if progress_file.exists():
            return json.loads(progress_file.read_text())
        return None

    async def get_next_task(self,
                           project_plan: Dict[str, Any],
                           completion_status: Dict[str, bool]) -> Optional[Dict[str, Any]]:
        """
        Get the next task to work on based on priorities and dependencies.
        """
        tasks = project_plan.get("tasks", [])

        # Filter incomplete tasks
        incomplete_tasks = [
            task for task in tasks
            if not completion_status.get(task.get("component_id"), False)
        ]

        if not incomplete_tasks:
            return None

        # Find task with all prerequisites met
        for task in incomplete_tasks:
            prerequisites = task.get("prerequisites", [])
            prereqs_met = all(
                completion_status.get(prereq, False)
                for prereq in prerequisites
            )

            if prereqs_met:
                return task

        # If no task with met prerequisites, return highest priority task
        return self._select_highest_priority(incomplete_tasks)

    def _select_highest_priority(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Select highest priority task"""
        # Sort by priority and complexity
        priority_map = {"high": 3, "medium": 2, "low": 1}

        tasks_with_scores = []
        for task in tasks:
            priority_score = priority_map.get(task.get("priority", "medium"), 2)
            complexity = task.get("estimated_complexity", 5)
            # Prioritize high-priority, low-complexity tasks first
            score = priority_score * 10 - complexity
            tasks_with_scores.append((score, task))

        tasks_with_scores.sort(reverse=True, key=lambda x: x[0])
        return tasks_with_scores[0][1] if tasks_with_scores else tasks[0]

    def mark_task_complete(self, task: Dict[str, Any]) -> None:
        """Mark a task as completed"""
        self.logger.info(f"Task completed: {task.get('description', 'unknown')}")

    def get_project_status(self, project_path: Path) -> Dict[str, Any]:
        """Get current project status"""
        progress = self.load_progress(project_path)

        if not progress:
            return {"status": "not_started"}

        completion = progress.get("completion_status", {})
        total = len(completion)
        completed = sum(1 for v in completion.values() if v)

        return {
            "status": "in_progress" if completed < total else "completed",
            "completion_percentage": (completed / total * 100) if total > 0 else 0,
            "iteration": progress.get("iteration", 0),
            "last_updated": progress.get("last_updated", "")
        }
