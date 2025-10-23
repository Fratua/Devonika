"""
Task Executor - Executes individual development tasks
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List


class TaskExecutor:
    """
    Executes individual development tasks by generating code,
    modifying files, and performing necessary operations.
    """

    def __init__(self, llm_interface, logger: logging.Logger):
        self.llm = llm_interface
        self.logger = logger

    async def execute_task(self,
                          task: Dict[str, Any],
                          project_path: Path,
                          codebase: Dict[str, Any],
                          architecture: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single development task.

        Args:
            task: Task definition with description and requirements
            project_path: Path to project directory
            codebase: Current codebase state
            architecture: Project architecture

        Returns:
            Dictionary with task results including modified files
        """
        self.logger.info(f"Executing task: {task.get('description', 'unnamed')}")

        task_type = task.get("type", "implementation")

        if task_type == "setup":
            result = await self._execute_setup_task(task, project_path, architecture)
        elif task_type == "implementation":
            result = await self._execute_implementation_task(task, project_path, codebase, architecture)
        elif task_type == "testing":
            result = await self._execute_testing_task(task, project_path, codebase)
        elif task_type == "documentation":
            result = await self._execute_documentation_task(task, project_path, codebase)
        else:
            result = await self._execute_generic_task(task, project_path, codebase, architecture)

        return result

    async def _execute_setup_task(self,
                                  task: Dict[str, Any],
                                  project_path: Path,
                                  architecture: Dict[str, Any]) -> Dict[str, Any]:
        """Execute setup tasks (environment setup, dependencies, etc.)"""
        prompt = f"""
        Execute this setup task:

        Task: {json.dumps(task, indent=2)}
        Architecture: {json.dumps(architecture, indent=2)}

        Generate:
        1. Setup scripts or configuration files needed
        2. Instructions for what needs to be installed or configured
        3. Any initialization code

        Return as JSON:
        {{
            "files": {{"file_path": "content", ...}},
            "commands": ["command1", "command2", ...],
            "completed": true/false,
            "notes": "any important notes"
        }}
        """

        response = await self.llm.generate(prompt, response_format="json")
        result = json.loads(response) if isinstance(response, str) else response

        # Write files if any
        for file_path, content in result.get("files", {}).items():
            full_path = project_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)

        return result

    async def _execute_implementation_task(self,
                                          task: Dict[str, Any],
                                          project_path: Path,
                                          codebase: Dict[str, Any],
                                          architecture: Dict[str, Any]) -> Dict[str, Any]:
        """Execute implementation tasks (writing actual code)"""
        # Get relevant context from codebase
        relevant_files = await self._identify_relevant_files(task, codebase, architecture)

        prompt = f"""
        Implement this development task:

        Task: {json.dumps(task, indent=2)}
        Architecture: {json.dumps(architecture.get("module_architecture", {}), indent=2)}

        Relevant existing files:
        {json.dumps(relevant_files, indent=2)}

        Generate complete, production-ready code that:
        - Implements the task requirements fully
        - Integrates with existing code
        - Follows best practices and design patterns
        - Includes proper error handling
        - Is well-documented with docstrings/comments
        - Is efficient and maintainable

        Return as JSON:
        {{
            "files": {{
                "file_path": "complete file content",
                ...
            }},
            "completed": true/false,
            "dependencies": ["any new dependencies needed"],
            "notes": "implementation notes"
        }}

        For each file, provide the COMPLETE file content, not just changes.
        """

        response = await self.llm.generate(prompt, response_format="json")
        result = json.loads(response) if isinstance(response, str) else response

        # Write files
        for file_path, content in result.get("files", {}).items():
            full_path = project_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
            self.logger.debug(f"Updated: {file_path}")

        return result

    async def _execute_testing_task(self,
                                    task: Dict[str, Any],
                                    project_path: Path,
                                    codebase: Dict[str, Any]) -> Dict[str, Any]:
        """Execute testing tasks (writing tests)"""
        prompt = f"""
        Create tests for this task:

        Task: {json.dumps(task, indent=2)}
        Related code files: {json.dumps(list(codebase.keys())[:10], indent=2)}

        Generate comprehensive tests including:
        - Unit tests for individual functions/methods
        - Integration tests for component interactions
        - Edge case tests
        - Error handling tests

        Return as JSON:
        {{
            "files": {{"test_file_path": "test content", ...}},
            "completed": true,
            "notes": "testing notes"
        }}
        """

        response = await self.llm.generate(prompt, response_format="json")
        result = json.loads(response) if isinstance(response, str) else response

        # Write test files
        for file_path, content in result.get("files", {}).items():
            full_path = project_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)

        return result

    async def _execute_documentation_task(self,
                                         task: Dict[str, Any],
                                         project_path: Path,
                                         codebase: Dict[str, Any]) -> Dict[str, Any]:
        """Execute documentation tasks"""
        prompt = f"""
        Create documentation for this task:

        Task: {json.dumps(task, indent=2)}
        Code files: {json.dumps(list(codebase.keys())[:10], indent=2)}

        Generate clear, comprehensive documentation.

        Return as JSON:
        {{
            "files": {{"doc_file_path": "content", ...}},
            "completed": true
        }}
        """

        response = await self.llm.generate(prompt, response_format="json")
        result = json.loads(response) if isinstance(response, str) else response

        # Write documentation files
        for file_path, content in result.get("files", {}).items():
            full_path = project_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)

        return result

    async def _execute_generic_task(self,
                                    task: Dict[str, Any],
                                    project_path: Path,
                                    codebase: Dict[str, Any],
                                    architecture: Dict[str, Any]) -> Dict[str, Any]:
        """Execute generic/other tasks"""
        return await self._execute_implementation_task(task, project_path, codebase, architecture)

    async def _identify_relevant_files(self,
                                      task: Dict[str, Any],
                                      codebase: Dict[str, Any],
                                      architecture: Dict[str, Any]) -> Dict[str, str]:
        """Identify files relevant to the current task"""
        # Simple heuristic: find files related to the task's component
        component_id = task.get("component_id", "")
        relevant = {}

        for file_path, content in codebase.items():
            # Check if file is related to the component
            if component_id.lower() in file_path.lower():
                relevant[file_path] = content[:1000]  # First 1000 chars for context

        return relevant
