"""
Tool Manager - Manages external tools and integrations
"""

import subprocess
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional


class ToolManager:
    """
    Manages external tools like git, package managers, databases, etc.
    """

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    # Git Operations
    def git_init(self, project_path: Path) -> bool:
        """Initialize git repository"""
        try:
            subprocess.run(["git", "init"], cwd=project_path, check=True, capture_output=True)
            self.logger.info("Git repository initialized")
            return True
        except Exception as e:
            self.logger.error(f"Error initializing git: {e}")
            return False

    def git_add_all(self, project_path: Path) -> bool:
        """Git add all files"""
        try:
            subprocess.run(["git", "add", "."], cwd=project_path, check=True, capture_output=True)
            return True
        except Exception as e:
            self.logger.error(f"Error adding files to git: {e}")
            return False

    def git_commit(self, project_path: Path, message: str) -> bool:
        """Git commit"""
        try:
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=project_path,
                check=True,
                capture_output=True
            )
            self.logger.info(f"Git commit: {message}")
            return True
        except Exception as e:
            self.logger.error(f"Error committing to git: {e}")
            return False

    # Package Management
    def install_python_dependencies(self, project_path: Path) -> bool:
        """Install Python dependencies from requirements.txt"""
        requirements_file = project_path / "requirements.txt"
        if not requirements_file.exists():
            return True

        try:
            self.logger.info("Installing Python dependencies...")
            subprocess.run(
                ["pip", "install", "-r", "requirements.txt"],
                cwd=project_path,
                check=True,
                capture_output=True,
                timeout=300
            )
            self.logger.info("Python dependencies installed")
            return True
        except Exception as e:
            self.logger.error(f"Error installing Python dependencies: {e}")
            return False

    def install_node_dependencies(self, project_path: Path) -> bool:
        """Install Node.js dependencies from package.json"""
        package_json = project_path / "package.json"
        if not package_json.exists():
            return True

        try:
            self.logger.info("Installing Node.js dependencies...")
            subprocess.run(
                ["npm", "install"],
                cwd=project_path,
                check=True,
                capture_output=True,
                timeout=300
            )
            self.logger.info("Node.js dependencies installed")
            return True
        except Exception as e:
            self.logger.error(f"Error installing Node.js dependencies: {e}")
            return False

    def install_cargo_dependencies(self, project_path: Path) -> bool:
        """Install Rust dependencies"""
        cargo_toml = project_path / "Cargo.toml"
        if not cargo_toml.exists():
            return True

        try:
            self.logger.info("Installing Rust dependencies...")
            subprocess.run(
                ["cargo", "build"],
                cwd=project_path,
                check=True,
                capture_output=True,
                timeout=300
            )
            self.logger.info("Rust dependencies installed")
            return True
        except Exception as e:
            self.logger.error(f"Error installing Rust dependencies: {e}")
            return False

    # Build Operations
    def build_project(self, project_path: Path, build_command: str) -> bool:
        """Run project build command"""
        try:
            self.logger.info(f"Building project with: {build_command}")
            result = subprocess.run(
                build_command.split(),
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=600
            )

            if result.returncode == 0:
                self.logger.info("Build successful")
                return True
            else:
                self.logger.error(f"Build failed: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Error building project: {e}")
            return False

    # Database Operations
    def setup_database(self, db_type: str, config: Dict[str, Any]) -> bool:
        """Setup database based on type"""
        self.logger.info(f"Database setup for {db_type} (placeholder)")
        # This would be implemented based on specific database requirements
        return True

    # Docker Operations
    def create_dockerfile(self, project_path: Path, project_type: Dict[str, Any]) -> bool:
        """Create Dockerfile for the project"""
        # Simple Dockerfile generation
        dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
"""
        try:
            dockerfile = project_path / "Dockerfile"
            dockerfile.write_text(dockerfile_content)
            self.logger.info("Dockerfile created")
            return True
        except Exception as e:
            self.logger.error(f"Error creating Dockerfile: {e}")
            return False

    def run_command(self, command: str, cwd: Path, timeout: int = 60) -> Dict[str, Any]:
        """Run arbitrary command"""
        try:
            result = subprocess.run(
                command.split(),
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }

        except Exception as e:
            self.logger.error(f"Error running command: {e}")
            return {
                "success": False,
                "error": str(e)
            }
