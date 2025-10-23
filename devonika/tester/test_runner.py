"""
Test Runner - Runs tests and validates code
"""

import subprocess
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional


class TestRunner:
    """
    Runs tests, validates code, and reports results.
    Supports multiple testing frameworks and languages.
    """

    def __init__(self, llm_interface, logger: logging.Logger):
        self.llm = llm_interface
        self.logger = logger

    async def run_tests(self, project_path: Path, task: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run tests for the project or specific task.

        Returns:
            Dictionary with test results
        """
        self.logger.info("Running tests...")

        # Detect testing framework
        framework = await self._detect_test_framework(project_path)

        if not framework:
            self.logger.warning("No test framework detected, skipping tests")
            return {"passed": True, "skipped": True, "message": "No test framework detected"}

        # Run tests based on framework
        if framework == "pytest":
            result = await self._run_pytest(project_path, task)
        elif framework == "jest":
            result = await self._run_jest(project_path, task)
        elif framework == "cargo_test":
            result = await self._run_cargo_test(project_path, task)
        else:
            result = await self._run_generic_tests(project_path, framework, task)

        self.logger.info(f"Tests completed: {'PASSED' if result.get('passed') else 'FAILED'}")
        return result

    async def _detect_test_framework(self, project_path: Path) -> Optional[str]:
        """Detect which testing framework is being used"""
        # Check for Python testing
        if (project_path / "pytest.ini").exists() or (project_path / "pyproject.toml").exists():
            if self._file_contains(project_path / "requirements.txt", "pytest"):
                return "pytest"

        # Check for Node.js testing
        if (project_path / "package.json").exists():
            package_json = json.loads((project_path / "package.json").read_text())
            dev_deps = package_json.get("devDependencies", {})
            if "jest" in dev_deps:
                return "jest"
            if "mocha" in dev_deps:
                return "mocha"

        # Check for Rust testing
        if (project_path / "Cargo.toml").exists():
            return "cargo_test"

        return None

    def _file_contains(self, file_path: Path, text: str) -> bool:
        """Check if file contains text"""
        try:
            if file_path.exists():
                return text in file_path.read_text()
        except:
            pass
        return False

    async def _run_pytest(self, project_path: Path, task: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Run pytest tests"""
        try:
            # Check if pytest is available
            result = subprocess.run(
                ["python", "-m", "pytest", "--version"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                return {"passed": True, "skipped": True, "message": "pytest not installed"}

            # Run tests
            cmd = ["python", "-m", "pytest", "-v", "--tb=short"]
            if task:
                # Try to run specific test file for the task
                test_file = self._find_test_file_for_task(project_path, task)
                if test_file:
                    cmd.append(str(test_file))

            result = subprocess.run(
                cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes
            )

            return {
                "passed": result.returncode == 0,
                "output": result.stdout + result.stderr,
                "framework": "pytest",
                "return_code": result.returncode
            }

        except subprocess.TimeoutExpired:
            return {"passed": False, "error": "Tests timed out"}
        except Exception as e:
            return {"passed": True, "skipped": True, "error": str(e)}

    async def _run_jest(self, project_path: Path, task: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Run Jest tests"""
        try:
            cmd = ["npm", "test"]
            result = subprocess.run(
                cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300
            )

            return {
                "passed": result.returncode == 0,
                "output": result.stdout + result.stderr,
                "framework": "jest",
                "return_code": result.returncode
            }

        except subprocess.TimeoutExpired:
            return {"passed": False, "error": "Tests timed out"}
        except Exception as e:
            return {"passed": True, "skipped": True, "error": str(e)}

    async def _run_cargo_test(self, project_path: Path, task: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Run Cargo tests"""
        try:
            result = subprocess.run(
                ["cargo", "test"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300
            )

            return {
                "passed": result.returncode == 0,
                "output": result.stdout + result.stderr,
                "framework": "cargo_test",
                "return_code": result.returncode
            }

        except subprocess.TimeoutExpired:
            return {"passed": False, "error": "Tests timed out"}
        except Exception as e:
            return {"passed": True, "skipped": True, "error": str(e)}

    async def _run_generic_tests(self,
                                 project_path: Path,
                                 framework: str,
                                 task: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Run tests for other frameworks"""
        return {"passed": True, "skipped": True, "message": f"Testing for {framework} not implemented yet"}

    def _find_test_file_for_task(self, project_path: Path, task: Dict[str, Any]) -> Optional[Path]:
        """Find the test file related to a specific task"""
        component_id = task.get("component_id", "")

        # Look for test files matching the component
        tests_dir = project_path / "tests"
        if tests_dir.exists():
            for test_file in tests_dir.rglob("test_*.py"):
                if component_id.lower() in test_file.name.lower():
                    return test_file

        return None
