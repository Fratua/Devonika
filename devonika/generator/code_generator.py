"""
Code Generator - Generates actual source code for projects
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional


class CodeGenerator:
    """
    Generates source code files based on architecture and requirements.
    Supports multiple programming languages and frameworks.
    """

    def __init__(self, llm_interface, logger: logging.Logger):
        self.llm = llm_interface
        self.logger = logger

    async def generate_project_structure(self,
                                        project_path: Path,
                                        project_plan: Dict[str, Any],
                                        architecture: Dict[str, Any],
                                        tech_knowledge: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate the complete initial project structure with all files.

        Returns:
            Dictionary mapping file paths to their content
        """
        self.logger.info("Generating project structure...")

        # Create directory structure
        await self._create_directories(project_path, architecture["directory_structure"])

        # Generate configuration files
        config_files = await self._generate_config_files(project_plan, architecture)

        # Generate core application files
        core_files = await self._generate_core_files(project_plan, architecture, tech_knowledge)

        # Generate component files
        component_files = await self._generate_component_files(project_plan, architecture)

        # Generate test files
        test_files = await self._generate_test_files(project_plan, architecture)

        # Generate utility files
        utility_files = await self._generate_utility_files(project_plan, architecture)

        # Combine all files
        all_files = {
            **config_files,
            **core_files,
            **component_files,
            **test_files,
            **utility_files
        }

        # Write files to disk
        for file_path, content in all_files.items():
            full_path = project_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
            self.logger.debug(f"Created: {file_path}")

        self.logger.info(f"Generated {len(all_files)} files")
        return all_files

    async def _create_directories(self, project_path: Path, dir_structure: Dict[str, Any]) -> None:
        """Recursively create directory structure"""

        def create_recursive(base_path: Path, structure: Dict[str, Any]):
            name = structure.get("name", "")
            if name and name != "root":
                base_path = base_path / name

            base_path.mkdir(parents=True, exist_ok=True)

            for child in structure.get("children", []):
                create_recursive(base_path, child)

        create_recursive(project_path, dir_structure)

    async def _generate_config_files(self, project_plan: Dict[str, Any],
                                     architecture: Dict[str, Any]) -> Dict[str, str]:
        """Generate configuration files (package.json, requirements.txt, etc.)"""
        tech_stack = architecture.get("technology_stack", {})
        languages = tech_stack.get("programming_languages", {})

        files = {}

        # Generate language-specific config files
        if "python" in str(languages).lower():
            files.update(await self._generate_python_configs(project_plan, architecture))

        if "javascript" in str(languages).lower() or "typescript" in str(languages).lower():
            files.update(await self._generate_nodejs_configs(project_plan, architecture))

        if "rust" in str(languages).lower():
            files.update(await self._generate_rust_configs(project_plan, architecture))

        # Generate common config files
        files["README.md"] = await self._generate_readme(project_plan, architecture)
        files[".gitignore"] = await self._generate_gitignore(tech_stack)

        return files

    async def _generate_python_configs(self, project_plan: Dict[str, Any],
                                       architecture: Dict[str, Any]) -> Dict[str, str]:
        """Generate Python-specific configuration files"""
        files = {}

        # requirements.txt
        prompt = f"""
        Generate a requirements.txt file for this Python project:

        Project: {project_plan.get("description")}
        Architecture: {json.dumps(architecture.get("technology_stack", {}), indent=2)}

        Include all necessary packages with appropriate versions.
        Use semantic versioning (e.g., package>=1.0.0,<2.0.0)
        """

        files["requirements.txt"] = await self.llm.generate(prompt)

        # setup.py
        prompt = f"""
        Generate a setup.py file for this Python project:

        Project Name: {project_plan.get("name", "project")}
        Description: {project_plan.get("description")}

        Include proper metadata, dependencies, and entry points.
        """

        files["setup.py"] = await self.llm.generate(prompt)

        # pyproject.toml
        files["pyproject.toml"] = await self._generate_pyproject_toml(project_plan)

        return files

    async def _generate_nodejs_configs(self, project_plan: Dict[str, Any],
                                       architecture: Dict[str, Any]) -> Dict[str, str]:
        """Generate Node.js/TypeScript configuration files"""
        files = {}

        # package.json
        prompt = f"""
        Generate a package.json file for this Node.js project:

        Project: {project_plan.get("description")}
        Architecture: {json.dumps(architecture.get("technology_stack", {}), indent=2)}

        Include scripts for build, test, start, etc.
        Return valid JSON only.
        """

        files["package.json"] = await self.llm.generate(prompt, response_format="json")

        # tsconfig.json if TypeScript
        if "typescript" in str(architecture.get("technology_stack", {})).lower():
            files["tsconfig.json"] = await self._generate_tsconfig(project_plan)

        return files

    async def _generate_rust_configs(self, project_plan: Dict[str, Any],
                                     architecture: Dict[str, Any]) -> Dict[str, str]:
        """Generate Rust configuration files"""
        files = {}

        # Cargo.toml
        prompt = f"""
        Generate a Cargo.toml file for this Rust project:

        Project Name: {project_plan.get("name", "project")}
        Description: {project_plan.get("description")}
        Architecture: {json.dumps(architecture.get("technology_stack", {}), indent=2)}

        Include necessary dependencies.
        """

        files["Cargo.toml"] = await self.llm.generate(prompt)

        return files

    async def _generate_core_files(self, project_plan: Dict[str, Any],
                                   architecture: Dict[str, Any],
                                   tech_knowledge: Dict[str, Any]) -> Dict[str, str]:
        """Generate core application files (main entry points, app setup, etc.)"""
        files = {}
        tech_stack = architecture.get("technology_stack", {})

        prompt = f"""
        Generate the main entry point file for this project:

        Project: {json.dumps(project_plan.get("description"))}
        Type: {json.dumps(project_plan.get("project_type", {}))}
        Tech Stack: {json.dumps(tech_stack, indent=2)}
        Architecture: {json.dumps(architecture.get("module_architecture", {}), indent=2)}

        Create a complete, working entry point that:
        - Initializes the application
        - Sets up necessary configurations
        - Includes proper error handling
        - Follows best practices for the chosen language/framework

        Include the file path (relative to project root) and complete code.
        Return as JSON: {{"file_path": "...", "content": "..."}}
        """

        response = await self.llm.generate(prompt, response_format="json")
        entry_point = json.loads(response) if isinstance(response, str) else response

        files[entry_point["file_path"]] = entry_point["content"]

        return files

    async def _generate_component_files(self, project_plan: Dict[str, Any],
                                        architecture: Dict[str, Any]) -> Dict[str, str]:
        """Generate files for each component in the project"""
        files = {}
        components = project_plan.get("components", [])

        for component in components:
            self.logger.debug(f"Generating files for component: {component['name']}")

            prompt = f"""
            Generate implementation files for this component:

            Component: {json.dumps(component, indent=2)}
            Architecture: {json.dumps(architecture.get("module_architecture", {}), indent=2)}
            Tech Stack: {json.dumps(architecture.get("technology_stack", {}), indent=2)}

            Generate complete, production-ready code that:
            - Implements all component features
            - Follows SOLID principles
            - Includes proper error handling
            - Has clear documentation
            - Is well-structured and maintainable

            Return as JSON array of files: [{{"file_path": "...", "content": "..."}}, ...]
            Generate all necessary files for this component (implementation, interfaces, types, etc.)
            """

            response = await self.llm.generate(prompt, response_format="json")
            component_files = json.loads(response) if isinstance(response, str) else response

            for file_info in component_files:
                files[file_info["file_path"]] = file_info["content"]

        return files

    async def _generate_test_files(self, project_plan: Dict[str, Any],
                                   architecture: Dict[str, Any]) -> Dict[str, str]:
        """Generate test files for components"""
        files = {}
        components = project_plan.get("components", [])[:5]  # Start with first 5 for efficiency

        for component in components:
            prompt = f"""
            Generate test files for this component:

            Component: {json.dumps(component, indent=2)}
            Tech Stack: {json.dumps(architecture.get("technology_stack", {}), indent=2)}

            Include:
            - Unit tests
            - Integration tests (if applicable)
            - Mock/fixture data
            - Test utilities

            Return as JSON array: [{{"file_path": "...", "content": "..."}}]
            """

            response = await self.llm.generate(prompt, response_format="json")
            test_files = json.loads(response) if isinstance(response, str) else response

            for file_info in test_files:
                files[file_info["file_path"]] = file_info["content"]

        return files

    async def _generate_utility_files(self, project_plan: Dict[str, Any],
                                      architecture: Dict[str, Any]) -> Dict[str, str]:
        """Generate utility and helper files"""
        files = {}

        prompt = f"""
        Generate common utility files for this project:

        Project Type: {json.dumps(project_plan.get("project_type", {}))}
        Tech Stack: {json.dumps(architecture.get("technology_stack", {}), indent=2)}

        Include files for:
        - Configuration management
        - Logging setup
        - Error handling utilities
        - Common helpers
        - Constants

        Return as JSON array: [{{"file_path": "...", "content": "..."}}]
        """

        response = await self.llm.generate(prompt, response_format="json")
        utility_files = json.loads(response) if isinstance(response, str) else response

        for file_info in utility_files:
            files[file_info["file_path"]] = file_info["content"]

        return files

    async def _generate_readme(self, project_plan: Dict[str, Any],
                              architecture: Dict[str, Any]) -> str:
        """Generate comprehensive README.md"""
        prompt = f"""
        Generate a comprehensive README.md for this project:

        Project: {project_plan.get("description")}
        Name: {project_plan.get("name")}
        Type: {json.dumps(project_plan.get("project_type", {}))}
        Components: {json.dumps([c["name"] for c in project_plan.get("components", [])], indent=2)}

        Include:
        - Project title and description
        - Features
        - Installation instructions
        - Usage examples
        - Architecture overview
        - Development setup
        - Testing instructions
        - Contributing guidelines
        - License

        Make it professional and comprehensive.
        """

        return await self.llm.generate(prompt)

    async def _generate_gitignore(self, tech_stack: Dict[str, Any]) -> str:
        """Generate .gitignore file"""
        languages = tech_stack.get("programming_languages", {})

        ignores = ["# Devonika generated .gitignore", ""]

        if "python" in str(languages).lower():
            ignores.extend([
                "# Python",
                "__pycache__/",
                "*.py[cod]",
                "*$py.class",
                "*.so",
                ".Python",
                "env/",
                "venv/",
                ".venv/",
                "pip-log.txt",
                ".pytest_cache/",
                "*.egg-info/",
                ""
            ])

        if any(lang in str(languages).lower() for lang in ["javascript", "typescript", "node"]):
            ignores.extend([
                "# Node.js",
                "node_modules/",
                "npm-debug.log*",
                "yarn-debug.log*",
                "yarn-error.log*",
                ".npm",
                "dist/",
                "build/",
                ""
            ])

        ignores.extend([
            "# IDEs",
            ".vscode/",
            ".idea/",
            "*.swp",
            "*.swo",
            "",
            "# OS",
            ".DS_Store",
            "Thumbs.db",
            "",
            "# Environment",
            ".env",
            ".env.local",
            ""
        ])

        return "\n".join(ignores)

    async def _generate_pyproject_toml(self, project_plan: Dict[str, Any]) -> str:
        """Generate pyproject.toml for Python projects"""
        return f"""[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_plan.get('name', 'project')}"
version = "0.1.0"
description = "{project_plan.get('description', '')[:100]}"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]

[tool.black]
line-length = 100
target-version = ['py38']
"""

    async def _generate_tsconfig(self, project_plan: Dict[str, Any]) -> str:
        """Generate tsconfig.json for TypeScript projects"""
        return json.dumps({
            "compilerOptions": {
                "target": "ES2020",
                "module": "commonjs",
                "lib": ["ES2020"],
                "outDir": "./dist",
                "rootDir": "./src",
                "strict": True,
                "esModuleInterop": True,
                "skipLibCheck": True,
                "forceConsistentCasingInFileNames": True,
                "resolveJsonModule": True,
                "declaration": True,
                "declarationMap": True,
                "sourceMap": True
            },
            "include": ["src/**/*"],
            "exclude": ["node_modules", "dist", "tests"]
        }, indent=2)

    async def generate_documentation(self, project_path: Path,
                                    project_plan: Dict[str, Any],
                                    codebase: Dict[str, Any]) -> None:
        """Generate comprehensive documentation for the project"""
        self.logger.info("Generating documentation...")

        docs_dir = project_path / "docs"
        docs_dir.mkdir(exist_ok=True)

        # Generate architecture documentation
        arch_doc = await self._generate_architecture_doc(project_plan)
        (docs_dir / "ARCHITECTURE.md").write_text(arch_doc)

        # Generate API documentation
        api_doc = await self._generate_api_doc(project_plan)
        (docs_dir / "API.md").write_text(api_doc)

        # Generate development guide
        dev_guide = await self._generate_dev_guide(project_plan)
        (docs_dir / "DEVELOPMENT.md").write_text(dev_guide)

        self.logger.info("Documentation generated")

    async def _generate_architecture_doc(self, project_plan: Dict[str, Any]) -> str:
        """Generate architecture documentation"""
        prompt = f"""
        Generate comprehensive architecture documentation for this project:

        Project: {project_plan.get("description")}
        Components: {json.dumps(project_plan.get("components", []), indent=2)}

        Include:
        - System overview
        - Component descriptions
        - Data flow diagrams (as text/ASCII)
        - Design decisions and rationale
        - Technology choices
        """

        return await self.llm.generate(prompt)

    async def _generate_api_doc(self, project_plan: Dict[str, Any]) -> str:
        """Generate API documentation"""
        prompt = f"""
        Generate API documentation for this project:

        Project: {project_plan.get("description")}

        Document all public APIs, endpoints, functions, and interfaces.
        Include request/response examples where applicable.
        """

        return await self.llm.generate(prompt)

    async def _generate_dev_guide(self, project_plan: Dict[str, Any]) -> str:
        """Generate development guide"""
        prompt = f"""
        Generate a development guide for this project:

        Project: {project_plan.get("description")}

        Include:
        - Getting started
        - Development workflow
        - Code style guidelines
        - Testing guidelines
        - Contribution guidelines
        - Troubleshooting
        """

        return await self.llm.generate(prompt)
