"""
Tech Researcher - Researches technologies and gathers knowledge
"""

import json
import logging
from typing import Dict, Any, List


class TechResearcher:
    """
    Researches technologies, frameworks, and best practices.
    Gathers knowledge to inform implementation decisions.
    """

    def __init__(self, llm_interface, logger: logging.Logger):
        self.llm = llm_interface
        self.logger = logger
        self.knowledge_cache = {}

    async def research_technologies(self,
                                   tech_stack: Dict[str, Any],
                                   project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Research the technologies in the tech stack.

        Returns knowledge about how to use them effectively.
        """
        self.logger.info("Researching technologies...")

        knowledge = {}

        # Research programming languages
        languages = tech_stack.get("programming_languages", {})
        if languages:
            knowledge["languages"] = await self._research_languages(languages, project_plan)

        # Research frameworks
        frameworks = tech_stack.get("frameworks", {})
        if frameworks:
            knowledge["frameworks"] = await self._research_frameworks(frameworks, project_plan)

        # Research databases
        databases = tech_stack.get("databases", {})
        if databases:
            knowledge["databases"] = await self._research_databases(databases, project_plan)

        # Research best practices
        knowledge["best_practices"] = await self._research_best_practices(project_plan)

        self.logger.info("Technology research completed")
        return knowledge

    async def _research_languages(self,
                                 languages: Dict[str, Any],
                                 project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Research programming languages"""
        lang_knowledge = {}

        for lang in languages if isinstance(languages, list) else [languages]:
            if lang in self.knowledge_cache:
                lang_knowledge[lang] = self.knowledge_cache[lang]
                continue

            prompt = f"""
            Provide key information about using {lang} for this type of project:

            Project Type: {json.dumps(project_plan.get("project_type", {}))}

            Include:
            - Key features to use
            - Best practices
            - Common patterns
            - Important libraries
            - Performance considerations
            - Security best practices

            Return as JSON.
            """

            response = await self.llm.generate(prompt, response_format="json")
            knowledge = json.loads(response) if isinstance(response, str) else response

            lang_knowledge[lang] = knowledge
            self.knowledge_cache[lang] = knowledge

        return lang_knowledge

    async def _research_frameworks(self,
                                  frameworks: Dict[str, Any],
                                  project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Research frameworks"""
        framework_knowledge = {}

        for framework in frameworks if isinstance(frameworks, list) else [frameworks]:
            prompt = f"""
            Provide implementation guidance for {framework}:

            Project Type: {json.dumps(project_plan.get("project_type", {}))}

            Include:
            - Setup and configuration
            - Key concepts
            - Best practices
            - Common patterns
            - Integration tips
            - Performance optimization

            Return as JSON.
            """

            response = await self.llm.generate(prompt, response_format="json")
            framework_knowledge[framework] = json.loads(response) if isinstance(response, str) else response

        return framework_knowledge

    async def _research_databases(self,
                                 databases: Dict[str, Any],
                                 project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Research database technologies"""
        db_knowledge = {}

        for db in databases if isinstance(databases, list) else [databases]:
            prompt = f"""
            Provide database implementation guidance for {db}:

            Project Type: {json.dumps(project_plan.get("project_type", {}))}

            Include:
            - Schema design best practices
            - Query optimization
            - Indexing strategies
            - Connection management
            - Scaling considerations
            - Backup strategies

            Return as JSON.
            """

            response = await self.llm.generate(prompt, response_format="json")
            db_knowledge[db] = json.loads(response) if isinstance(response, str) else response

        return db_knowledge

    async def _research_best_practices(self, project_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Research general best practices for the project type"""
        project_type = project_plan.get("project_type", {})

        prompt = f"""
        Provide best practices for this type of project:

        Project Type: {json.dumps(project_type, indent=2)}

        Include:
        - Architecture best practices
        - Code organization
        - Testing strategies
        - Security practices
        - Performance optimization
        - Deployment practices
        - Documentation standards

        Return as JSON.
        """

        response = await self.llm.generate(prompt, response_format="json")
        return json.loads(response) if isinstance(response, str) else response
