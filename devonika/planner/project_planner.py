"""
Project Planner - Analyzes requirements and creates comprehensive project plans
"""

import re
import json
from typing import Dict, Any, List, Optional
import logging


class ProjectPlanner:
    """
    Analyzes project descriptions (even vague ones) and creates detailed,
    actionable project plans with components, tasks, and requirements.
    """

    def __init__(self, llm_interface, logger: logging.Logger):
        self.llm = llm_interface
        self.logger = logger

    async def create_comprehensive_plan(self, description: str) -> Dict[str, Any]:
        """
        Create a comprehensive project plan from a description.

        Handles vague descriptions by:
        1. Analyzing keywords and context
        2. Making intelligent assumptions
        3. Expanding requirements based on best practices
        4. Breaking down into manageable components

        Args:
            description: Project description (can be vague)

        Returns:
            Comprehensive project plan dictionary
        """
        self.logger.info("Creating comprehensive project plan...")

        # Step 1: Analyze and expand the description
        expanded_requirements = await self._expand_requirements(description)

        # Step 2: Identify project type and scale
        project_type = await self._identify_project_type(expanded_requirements)

        # Step 3: Generate components and features
        components = await self._generate_components(expanded_requirements, project_type)

        # Step 4: Create task breakdown
        tasks = await self._generate_task_breakdown(components)

        # Step 5: Identify technology stack suggestions
        tech_stack = await self._suggest_tech_stack(project_type, components)

        # Step 6: Estimate complexity and timeline
        estimates = await self._estimate_project(components, tasks)

        plan = {
            "description": description,
            "expanded_requirements": expanded_requirements,
            "project_type": project_type,
            "components": components,
            "tasks": tasks,
            "suggested_tech_stack": tech_stack,
            "estimates": estimates,
            "metadata": {
                "planner_version": "1.0",
                "confidence": self._calculate_confidence(description, expanded_requirements)
            }
        }

        self.logger.info(f"Project plan created with {len(components)} components and {len(tasks)} tasks")
        return plan

    async def _expand_requirements(self, description: str) -> Dict[str, Any]:
        """
        Expand vague requirements into detailed specifications.
        Uses LLM to understand intent and fill gaps.
        """
        prompt = f"""
        Analyze this project description and expand it into detailed requirements.
        Even if the description is vague, infer the most likely intent and expand accordingly.

        Project Description: {description}

        Provide a detailed analysis including:
        1. Core functionality required
        2. Likely user personas
        3. Essential features
        4. Nice-to-have features
        5. Technical considerations
        6. Scalability requirements
        7. Security considerations
        8. Performance requirements

        Format your response as JSON with these keys.
        """

        response = await self.llm.generate(prompt, response_format="json")
        return json.loads(response) if isinstance(response, str) else response

    async def _identify_project_type(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify the type of project (web app, mobile, game, CLI tool, etc.)
        and its characteristics.
        """
        prompt = f"""
        Based on these requirements, identify the project type and characteristics:

        {json.dumps(requirements, indent=2)}

        Classify into:
        1. Primary category (web_app, mobile_app, desktop_app, game, cli_tool, library, api, etc.)
        2. Secondary categories
        3. Scale (small, medium, large, enterprise)
        4. Complexity (simple, moderate, complex, highly_complex)
        5. Architecture pattern (monolith, microservices, serverless, etc.)

        Return as JSON.
        """

        response = await self.llm.generate(prompt, response_format="json")
        return json.loads(response) if isinstance(response, str) else response

    async def _generate_components(self, requirements: Dict[str, Any],
                                   project_type: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate the list of components/modules needed for the project.

        For example, an MMORPG would include:
        - Game server
        - Client application
        - Database layer
        - Authentication system
        - Chat system
        - Inventory system
        - Combat system
        - etc.
        """
        prompt = f"""
        Based on these requirements and project type, generate a complete list of
        components/modules needed to build this project.

        Requirements: {json.dumps(requirements, indent=2)}
        Project Type: {json.dumps(project_type, indent=2)}

        For each component include:
        - id: unique identifier
        - name: component name
        - description: what it does
        - dependencies: which other components it depends on
        - priority: high, medium, low
        - complexity: simple, moderate, complex
        - estimated_files: approximate number of files
        - key_features: list of key features this component handles

        Be comprehensive. For large projects like MMORPGs, include all necessary
        systems (rendering, networking, physics, AI, economy, etc.).

        Return as JSON array.
        """

        response = await self.llm.generate(prompt, response_format="json")
        components = json.loads(response) if isinstance(response, str) else response

        # Ensure each component has a unique ID
        for i, comp in enumerate(components):
            if "id" not in comp:
                comp["id"] = f"component_{i}"

        return components

    async def _generate_task_breakdown(self, components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Break down components into specific, actionable tasks.
        """
        all_tasks = []

        for component in components:
            prompt = f"""
            Break down this component into specific development tasks:

            Component: {json.dumps(component, indent=2)}

            For each task include:
            - id: unique identifier
            - component_id: which component this belongs to
            - description: clear task description
            - prerequisites: which tasks must be completed first
            - estimated_complexity: 1-10 scale
            - type: setup, implementation, testing, documentation

            Return as JSON array.
            """

            response = await self.llm.generate(prompt, response_format="json")
            tasks = json.loads(response) if isinstance(response, str) else response

            # Ensure proper IDs
            for i, task in enumerate(tasks):
                if "id" not in task:
                    task["id"] = f"{component['id']}_task_{i}"
                if "component_id" not in task:
                    task["component_id"] = component["id"]

            all_tasks.extend(tasks)

        return all_tasks

    async def _suggest_tech_stack(self, project_type: Dict[str, Any],
                                  components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Suggest appropriate technology stack based on project requirements.
        """
        prompt = f"""
        Suggest an appropriate technology stack for this project:

        Project Type: {json.dumps(project_type, indent=2)}
        Components: {json.dumps([c["name"] for c in components], indent=2)}

        Suggest:
        - programming_languages: primary and secondary languages
        - frameworks: web frameworks, game engines, etc.
        - databases: SQL, NoSQL, caching
        - infrastructure: cloud providers, containers, orchestration
        - tools: build tools, testing frameworks, CI/CD
        - libraries: key libraries for each component

        Consider best practices, community support, and scalability.

        Return as JSON.
        """

        response = await self.llm.generate(prompt, response_format="json")
        return json.loads(response) if isinstance(response, str) else response

    async def _estimate_project(self, components: List[Dict[str, Any]],
                                tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Estimate project complexity, timeline, and resource requirements.
        """
        total_complexity = sum(
            task.get("estimated_complexity", 5) for task in tasks
        )

        return {
            "total_components": len(components),
            "total_tasks": len(tasks),
            "complexity_score": total_complexity,
            "estimated_iterations": max(10, len(tasks) // 5),
            "size_category": self._categorize_size(len(components), len(tasks)),
        }

    def _categorize_size(self, num_components: int, num_tasks: int) -> str:
        """Categorize project size"""
        if num_components < 5 and num_tasks < 20:
            return "small"
        elif num_components < 15 and num_tasks < 100:
            return "medium"
        elif num_components < 30 and num_tasks < 300:
            return "large"
        else:
            return "enterprise"

    def _calculate_confidence(self, original_desc: str, expanded: Dict[str, Any]) -> float:
        """
        Calculate confidence in the plan based on description clarity.
        More specific descriptions = higher confidence.
        """
        # Simple heuristic based on description length and detail
        word_count = len(original_desc.split())

        if word_count < 10:
            return 0.6
        elif word_count < 30:
            return 0.75
        elif word_count < 100:
            return 0.85
        else:
            return 0.95

    async def generate_project_name(self, project_plan: Dict[str, Any]) -> str:
        """
        Generate an appropriate project name based on the plan.
        """
        description = project_plan.get("description", "")
        project_type = project_plan.get("project_type", {})

        prompt = f"""
        Generate a suitable project name for this project:

        Description: {description}
        Type: {project_type.get("primary_category", "application")}

        The name should be:
        - Memorable and clear
        - Related to the project's purpose
        - Suitable for a code repository
        - lowercase_with_underscores format

        Return only the project name, nothing else.
        """

        name = await self.llm.generate(prompt)
        # Clean and format the name
        name = re.sub(r'[^a-z0-9_]', '', name.lower().replace(' ', '_').replace('-', '_'))

        return name or "unnamed_project"
