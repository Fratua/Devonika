"""
System Architect - Designs comprehensive system architecture
"""

import json
import logging
from typing import Dict, Any, List


class SystemArchitect:
    """
    Designs system architecture including:
    - Directory structure
    - Module organization
    - Data flow
    - API design
    - Database schema
    - Infrastructure requirements
    """

    def __init__(self, llm_interface, logger: logging.Logger):
        self.llm = llm_interface
        self.logger = logger

    async def design_architecture(self, project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Design comprehensive system architecture based on project plan.
        """
        self.logger.info("Designing system architecture...")

        # Design different architectural aspects
        directory_structure = await self._design_directory_structure(project_plan)
        module_architecture = await self._design_module_architecture(project_plan)
        data_architecture = await self._design_data_architecture(project_plan)
        api_design = await self._design_api_architecture(project_plan)
        infrastructure = await self._design_infrastructure(project_plan)

        architecture = {
            "directory_structure": directory_structure,
            "module_architecture": module_architecture,
            "data_architecture": data_architecture,
            "api_design": api_design,
            "infrastructure": infrastructure,
            "technology_stack": project_plan.get("suggested_tech_stack", {}),
            "design_patterns": await self._select_design_patterns(project_plan)
        }

        self.logger.info("System architecture design completed")
        return architecture

    async def _design_directory_structure(self, project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Design the directory/folder structure for the project"""
        project_type = project_plan.get("project_type", {})
        components = project_plan.get("components", [])

        prompt = f"""
        Design a comprehensive directory structure for this project:

        Project Type: {json.dumps(project_type, indent=2)}
        Components: {json.dumps([c["name"] for c in components], indent=2)}

        Create a nested directory structure that:
        - Follows best practices for the project type
        - Organizes code logically
        - Separates concerns appropriately
        - Includes config, tests, docs directories
        - Is scalable and maintainable

        Return as nested JSON where each directory is an object with:
        - name: directory name
        - purpose: what goes here
        - children: nested directories (if any)
        - files: array of file names that should exist here

        Example:
        {{
            "name": "root",
            "children": [
                {{
                    "name": "src",
                    "purpose": "source code",
                    "children": [...]
                }}
            ]
        }}
        """

        response = await self.llm.generate(prompt, response_format="json")
        return json.loads(response) if isinstance(response, str) else response

    async def _design_module_architecture(self, project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Design how modules/components interact with each other"""
        components = project_plan.get("components", [])

        prompt = f"""
        Design the module architecture showing how components interact:

        Components: {json.dumps(components, indent=2)}

        For each component, define:
        - interfaces: public APIs/interfaces it exposes
        - dependencies: what it depends on
        - consumers: what depends on it
        - communication_pattern: how it communicates (REST, events, direct calls, etc.)

        Also define:
        - layers: architectural layers (presentation, business logic, data, etc.)
        - boundaries: clear boundaries between modules
        - data_flow: how data flows through the system

        Return as JSON.
        """

        response = await self.llm.generate(prompt, response_format="json")
        return json.loads(response) if isinstance(response, str) else response

    async def _design_data_architecture(self, project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Design data models, database schema, and data flow"""
        requirements = project_plan.get("expanded_requirements", {})
        components = project_plan.get("components", [])

        prompt = f"""
        Design the data architecture for this project:

        Requirements: {json.dumps(requirements, indent=2)}
        Components: {json.dumps([c["name"] for c in components], indent=2)}

        Include:
        - entities: main data entities/models
        - relationships: how entities relate to each other
        - database_schema: tables/collections design
        - storage_strategy: where different data types are stored
        - caching_strategy: what and how to cache
        - data_flow: how data moves through the system

        Return as JSON.
        """

        response = await self.llm.generate(prompt, response_format="json")
        return json.loads(response) if isinstance(response, str) else response

    async def _design_api_architecture(self, project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Design API endpoints and external interfaces"""
        components = project_plan.get("components", [])
        project_type = project_plan.get("project_type", {})

        prompt = f"""
        Design the API architecture:

        Project Type: {json.dumps(project_type, indent=2)}
        Components: {json.dumps([c["name"] for c in components], indent=2)}

        Define:
        - endpoints: REST/GraphQL endpoints needed
        - authentication: auth strategy
        - authorization: permission model
        - rate_limiting: API rate limits
        - versioning: API versioning strategy
        - documentation_format: OpenAPI/Swagger, etc.

        Return as JSON.
        """

        response = await self.llm.generate(prompt, response_format="json")
        return json.loads(response) if isinstance(response, str) else response

    async def _design_infrastructure(self, project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Design infrastructure and deployment architecture"""
        project_type = project_plan.get("project_type", {})
        scale = project_type.get("scale", "medium")

        prompt = f"""
        Design infrastructure architecture:

        Project Type: {json.dumps(project_type, indent=2)}
        Scale: {scale}

        Include:
        - deployment_strategy: how to deploy (containers, serverless, VMs, etc.)
        - scaling_strategy: horizontal/vertical scaling approach
        - monitoring: what to monitor and how
        - logging: logging strategy
        - backup_strategy: data backup approach
        - ci_cd: CI/CD pipeline design

        Return as JSON.
        """

        response = await self.llm.generate(prompt, response_format="json")
        return json.loads(response) if isinstance(response, str) else response

    async def _select_design_patterns(self, project_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Select appropriate design patterns for the project"""
        project_type = project_plan.get("project_type", {})
        components = project_plan.get("components", [])

        prompt = f"""
        Recommend design patterns for this project:

        Project Type: {json.dumps(project_type, indent=2)}
        Components: {json.dumps([c["name"] for c in components], indent=2)}

        Suggest relevant design patterns like:
        - Creational patterns (Factory, Singleton, Builder, etc.)
        - Structural patterns (Adapter, Decorator, Facade, etc.)
        - Behavioral patterns (Observer, Strategy, Command, etc.)
        - Architectural patterns (MVC, MVVM, Clean Architecture, etc.)

        For each pattern include:
        - name: pattern name
        - where_to_use: which components should use it
        - why: justification
        - example: brief example of implementation

        Return as JSON array.
        """

        response = await self.llm.generate(prompt, response_format="json")
        return json.loads(response) if isinstance(response, str) else response
