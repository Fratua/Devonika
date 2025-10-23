"""
Main Devonika Engine - Orchestrates all components to build software projects autonomously
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

from devonika.planner.project_planner import ProjectPlanner
from devonika.architect.system_architect import SystemArchitect
from devonika.generator.code_generator import CodeGenerator
from devonika.executor.task_executor import TaskExecutor
from devonika.researcher.tech_researcher import TechResearcher
from devonika.tester.test_runner import TestRunner
from devonika.debugger.auto_debugger import AutoDebugger
from devonika.optimizer.performance_optimizer import PerformanceOptimizer
from devonika.manager.project_manager import ProjectManager
from devonika.intelligence.llm_interface import LLMInterface
from devonika.tools.tool_manager import ToolManager


class DevonikaEngine:
    """
    Main orchestration engine for Devonika AI Software Engineer.

    This engine coordinates all subsystems to autonomously build software projects
    of any scale, handling everything from vague requirements to full implementation.
    """

    def __init__(self, workspace: str = "./workspace", config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Devonika engine.

        Args:
            workspace: Directory where projects will be built
            config: Configuration dictionary for customizing behavior
        """
        self.workspace = Path(workspace)
        self.workspace.mkdir(exist_ok=True, parents=True)

        self.config = config or self._default_config()
        self.logger = self._setup_logging()

        # Initialize LLM interface
        self.llm = LLMInterface(self.config.get("llm", {}))

        # Initialize all subsystems
        self.planner = ProjectPlanner(self.llm, self.logger)
        self.architect = SystemArchitect(self.llm, self.logger)
        self.generator = CodeGenerator(self.llm, self.logger)
        self.executor = TaskExecutor(self.llm, self.logger)
        self.researcher = TechResearcher(self.llm, self.logger)
        self.tester = TestRunner(self.llm, self.logger)
        self.debugger = AutoDebugger(self.llm, self.logger)
        self.optimizer = PerformanceOptimizer(self.llm, self.logger)
        self.manager = ProjectManager(self.workspace, self.logger)
        self.tools = ToolManager(self.logger)

        self.current_project = None
        self.logger.info("Devonika Engine initialized")

    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "max_iterations": 1000,
            "auto_fix_errors": True,
            "auto_test": True,
            "auto_optimize": True,
            "research_enabled": True,
            "verbose": True,
            "llm": {
                "provider": "anthropic",
                "model": "claude-3-5-sonnet-20241022",
                "temperature": 0.7,
            }
        }

    def _setup_logging(self) -> logging.Logger:
        """Setup logging system"""
        log_dir = self.workspace / "logs"
        log_dir.mkdir(exist_ok=True)

        logger = logging.getLogger("Devonika")
        logger.setLevel(logging.DEBUG if self.config.get("verbose") else logging.INFO)

        # File handler
        fh = logging.FileHandler(log_dir / f"devonika_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        fh.setLevel(logging.DEBUG)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    async def build_project(self, description: str, project_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Main entry point to build a project from description.

        This method handles the entire project lifecycle:
        1. Understanding the requirements (even vague ones)
        2. Planning the architecture
        3. Generating code
        4. Testing and debugging
        5. Optimization
        6. Documentation

        Args:
            description: Project description (can be vague)
            project_name: Optional project name (will be generated if not provided)

        Returns:
            Dictionary containing project status and metadata
        """
        self.logger.info(f"Starting new project build: {description[:100]}...")

        try:
            # Step 1: Project Understanding and Planning
            self.logger.info("Phase 1: Understanding project requirements...")
            project_plan = await self._understand_and_plan(description, project_name)

            # Step 2: Architecture Design
            self.logger.info("Phase 2: Designing system architecture...")
            architecture = await self._design_architecture(project_plan)

            # Step 3: Research Required Technologies
            self.logger.info("Phase 3: Researching technologies...")
            tech_knowledge = await self._research_technologies(project_plan, architecture)

            # Step 4: Generate Initial Code
            self.logger.info("Phase 4: Generating initial codebase...")
            codebase = await self._generate_initial_code(project_plan, architecture, tech_knowledge)

            # Step 5: Iterative Development Loop
            self.logger.info("Phase 5: Entering iterative development...")
            final_result = await self._iterative_development_loop(
                project_plan, architecture, codebase
            )

            # Step 6: Final Optimization
            self.logger.info("Phase 6: Optimizing project...")
            await self._optimize_project(final_result)

            # Step 7: Documentation
            self.logger.info("Phase 7: Generating documentation...")
            await self._generate_documentation(final_result)

            self.logger.info("Project build completed successfully!")
            return {
                "status": "success",
                "project": final_result,
                "path": str(self.current_project["path"])
            }

        except Exception as e:
            self.logger.error(f"Error building project: {e}", exc_info=True)
            return {
                "status": "error",
                "error": str(e)
            }

    async def _understand_and_plan(self, description: str, project_name: Optional[str]) -> Dict[str, Any]:
        """
        Understand the project requirements and create a comprehensive plan.
        Handles vague descriptions by asking clarifying questions and making intelligent assumptions.
        """
        # Create project context
        project_context = {
            "description": description,
            "timestamp": datetime.now().isoformat()
        }

        # Use planner to understand and expand requirements
        project_plan = await self.planner.create_comprehensive_plan(description)

        # Generate project name if not provided
        if not project_name:
            project_name = await self.planner.generate_project_name(project_plan)

        project_plan["name"] = project_name

        # Create project directory
        project_path = self.workspace / project_name
        project_path.mkdir(exist_ok=True, parents=True)

        self.current_project = {
            "name": project_name,
            "path": project_path,
            "plan": project_plan,
            "context": project_context
        }

        # Save plan to disk
        self.manager.save_project_plan(project_path, project_plan)

        return project_plan

    async def _design_architecture(self, project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Design the system architecture based on the project plan"""
        architecture = await self.architect.design_architecture(project_plan)

        # Save architecture to disk
        self.manager.save_architecture(self.current_project["path"], architecture)

        return architecture

    async def _research_technologies(self, project_plan: Dict[str, Any],
                                    architecture: Dict[str, Any]) -> Dict[str, Any]:
        """Research required technologies and gather knowledge"""
        if not self.config.get("research_enabled"):
            return {}

        tech_stack = architecture.get("technology_stack", {})
        knowledge = await self.researcher.research_technologies(tech_stack, project_plan)

        return knowledge

    async def _generate_initial_code(self, project_plan: Dict[str, Any],
                                     architecture: Dict[str, Any],
                                     tech_knowledge: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the initial codebase structure and core files"""
        project_path = self.current_project["path"]

        codebase = await self.generator.generate_project_structure(
            project_path,
            project_plan,
            architecture,
            tech_knowledge
        )

        return codebase

    async def _iterative_development_loop(self, project_plan: Dict[str, Any],
                                         architecture: Dict[str, Any],
                                         codebase: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main development loop that iteratively builds, tests, debugs, and improves
        the project until completion.
        """
        project_path = self.current_project["path"]
        max_iterations = self.config.get("max_iterations", 1000)
        iteration = 0

        # Track completion status for each component
        components = project_plan.get("components", [])
        completion_status = {comp["id"]: False for comp in components}

        while iteration < max_iterations:
            iteration += 1
            self.logger.info(f"Development iteration {iteration}/{max_iterations}")

            # Check if all components are complete
            if all(completion_status.values()):
                self.logger.info("All components completed!")
                break

            # Get next task to work on
            next_task = await self.manager.get_next_task(
                project_plan, completion_status
            )

            if not next_task:
                self.logger.info("No more tasks to complete")
                break

            self.logger.info(f"Working on: {next_task['description']}")

            # Execute the task
            task_result = await self.executor.execute_task(
                next_task,
                project_path,
                codebase,
                architecture
            )

            # Update codebase with task results
            codebase.update(task_result.get("files", {}))

            # Test if enabled
            if self.config.get("auto_test"):
                test_results = await self.tester.run_tests(project_path, next_task)

                # Debug and fix if tests fail
                if not test_results.get("passed", False) and self.config.get("auto_fix_errors"):
                    self.logger.info("Tests failed, attempting auto-debug...")
                    debug_result = await self.debugger.debug_and_fix(
                        project_path,
                        test_results,
                        codebase
                    )

                    if debug_result.get("fixed"):
                        codebase.update(debug_result.get("files", {}))
                    else:
                        self.logger.warning(f"Could not auto-fix: {debug_result.get('error')}")

            # Mark task as complete
            if task_result.get("completed"):
                completion_status[next_task["component_id"]] = True
                self.manager.mark_task_complete(next_task)

            # Save progress
            self.manager.save_progress(project_path, {
                "iteration": iteration,
                "completion_status": completion_status,
                "codebase": codebase
            })

        return {
            "codebase": codebase,
            "iterations": iteration,
            "completion_status": completion_status
        }

    async def _optimize_project(self, project_result: Dict[str, Any]) -> None:
        """Optimize the project for performance and best practices"""
        if not self.config.get("auto_optimize"):
            return

        project_path = self.current_project["path"]
        await self.optimizer.optimize(project_path, project_result["codebase"])

    async def _generate_documentation(self, project_result: Dict[str, Any]) -> None:
        """Generate comprehensive documentation for the project"""
        project_path = self.current_project["path"]

        await self.generator.generate_documentation(
            project_path,
            self.current_project["plan"],
            project_result["codebase"]
        )

    def get_project_status(self) -> Dict[str, Any]:
        """Get current project status"""
        if not self.current_project:
            return {"status": "no_active_project"}

        return self.manager.get_project_status(self.current_project["path"])

    def list_projects(self) -> List[str]:
        """List all projects in workspace"""
        return [p.name for p in self.workspace.iterdir() if p.is_dir()]
