"""
Auto Debugger - Automatically debugs and fixes errors
"""

import json
import logging
import traceback
from pathlib import Path
from typing import Dict, Any, List, Optional


class AutoDebugger:
    """
    Automatically identifies bugs, analyzes errors, and generates fixes.
    """

    def __init__(self, llm_interface, logger: logging.Logger):
        self.llm = llm_interface
        self.logger = logger

    async def debug_and_fix(self,
                           project_path: Path,
                           test_results: Dict[str, Any],
                           codebase: Dict[str, Any]) -> Dict[str, Any]:
        """
        Debug and fix errors found in test results.

        Returns:
            Dictionary with fixed status and modified files
        """
        self.logger.info("Analyzing errors and attempting fixes...")

        # Extract error information
        errors = self._extract_errors(test_results)

        if not errors:
            return {"fixed": False, "message": "No clear errors to fix"}

        # Analyze each error
        fixes = []
        for error in errors:
            fix = await self._analyze_and_fix_error(error, project_path, codebase)
            if fix:
                fixes.append(fix)

        if not fixes:
            return {"fixed": False, "message": "Could not generate fixes"}

        # Apply fixes
        modified_files = {}
        for fix in fixes:
            for file_path, content in fix.get("files", {}).items():
                modified_files[file_path] = content
                full_path = project_path / file_path
                full_path.write_text(content)
                self.logger.info(f"Applied fix to: {file_path}")

        return {
            "fixed": True,
            "files": modified_files,
            "num_fixes": len(fixes)
        }

    def _extract_errors(self, test_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract error information from test results"""
        errors = []
        output = test_results.get("output", "")

        # Parse output for error messages
        if "FAILED" in output or "ERROR" in output or "Error" in output:
            # Simple extraction - could be made more sophisticated
            lines = output.split("\n")
            current_error = []

            for line in lines:
                if any(marker in line for marker in ["FAILED", "ERROR", "Error:", "Traceback"]):
                    if current_error:
                        errors.append({
                            "message": "\n".join(current_error),
                            "type": "test_failure"
                        })
                        current_error = []
                    current_error.append(line)
                elif current_error:
                    current_error.append(line)

            if current_error:
                errors.append({
                    "message": "\n".join(current_error),
                    "type": "test_failure"
                })

        return errors[:5]  # Limit to first 5 errors

    async def _analyze_and_fix_error(self,
                                     error: Dict[str, Any],
                                     project_path: Path,
                                     codebase: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze a specific error and generate a fix"""
        prompt = f"""
        Analyze this error and generate a fix:

        Error:
        {error.get("message", "")}

        Available codebase files:
        {json.dumps(list(codebase.keys()), indent=2)}

        Tasks:
        1. Identify the root cause of the error
        2. Determine which file(s) need to be modified
        3. Generate the corrected code

        Return as JSON:
        {{
            "analysis": "explanation of the issue",
            "files": {{
                "file_path": "corrected full file content",
                ...
            }},
            "confidence": 0.0-1.0
        }}

        Only include files that need to be changed, with complete corrected content.
        """

        try:
            response = await self.llm.generate(prompt, response_format="json")
            fix = json.loads(response) if isinstance(response, str) else response

            # Only apply if confidence is reasonable
            if fix.get("confidence", 0) > 0.6:
                return fix

        except Exception as e:
            self.logger.error(f"Error generating fix: {e}")

        return None
