"""
Performance Optimizer - Optimizes code for performance
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List


class PerformanceOptimizer:
    """
    Analyzes code and applies performance optimizations.
    """

    def __init__(self, llm_interface, logger: logging.Logger):
        self.llm = llm_interface
        self.logger = logger

    async def optimize(self, project_path: Path, codebase: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize the project for performance.

        Returns:
            Dictionary with optimization results
        """
        self.logger.info("Analyzing code for optimization opportunities...")

        # Identify optimization opportunities
        opportunities = await self._identify_opportunities(codebase)

        if not opportunities:
            self.logger.info("No clear optimization opportunities found")
            return {"optimized": False, "message": "Code is already well-optimized"}

        # Apply optimizations
        optimizations_applied = []
        for opportunity in opportunities[:10]:  # Limit to top 10
            result = await self._apply_optimization(opportunity, project_path, codebase)
            if result.get("success"):
                optimizations_applied.append(result)

        self.logger.info(f"Applied {len(optimizations_applied)} optimizations")
        return {
            "optimized": True,
            "count": len(optimizations_applied),
            "optimizations": optimizations_applied
        }

    async def _identify_opportunities(self, codebase: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify optimization opportunities"""
        opportunities = []

        # Sample a few files for analysis
        sample_files = dict(list(codebase.items())[:10])

        prompt = f"""
        Analyze this code for performance optimization opportunities:

        Files:
        {json.dumps({k: v[:500] for k, v in sample_files.items()}, indent=2)}

        Identify:
        - Algorithmic improvements (O(n²) -> O(n log n), etc.)
        - Database query optimization
        - Caching opportunities
        - Memory optimization
        - Async/parallel processing opportunities
        - Resource leak prevention

        For each opportunity include:
        - file_path: which file
        - issue: what's suboptimal
        - fix: how to fix it
        - impact: expected performance impact (low/medium/high)
        - priority: priority (1-10)

        Return as JSON array.
        """

        try:
            response = await self.llm.generate(prompt, response_format="json")
            opportunities = json.loads(response) if isinstance(response, str) else response

            # Sort by priority
            opportunities.sort(key=lambda x: x.get("priority", 0), reverse=True)

        except Exception as e:
            self.logger.error(f"Error identifying opportunities: {e}")

        return opportunities

    async def _apply_optimization(self,
                                  opportunity: Dict[str, Any],
                                  project_path: Path,
                                  codebase: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a specific optimization"""
        file_path = opportunity.get("file_path", "")
        if not file_path or file_path not in codebase:
            return {"success": False, "error": "File not found"}

        current_content = codebase[file_path]

        prompt = f"""
        Apply this optimization:

        Opportunity: {json.dumps(opportunity, indent=2)}

        Current file content:
        {current_content}

        Generate the optimized version of this file.
        Ensure:
        - Functionality remains the same
        - Code is still readable and maintainable
        - Comments explain optimizations made
        - No bugs are introduced

        Return as JSON:
        {{
            "content": "optimized file content",
            "explanation": "what was changed and why"
        }}
        """

        try:
            response = await self.llm.generate(prompt, response_format="json")
            result = json.loads(response) if isinstance(response, str) else response

            # Write optimized file
            full_path = project_path / file_path
            full_path.write_text(result["content"])

            return {
                "success": True,
                "file": file_path,
                "explanation": result.get("explanation", "")
            }

        except Exception as e:
            self.logger.error(f"Error applying optimization: {e}")
            return {"success": False, "error": str(e)}
