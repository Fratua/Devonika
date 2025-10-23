"""
System Prompt Manager - Assembles and manages DEVONIKA system prompts
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from enum import Enum


class OperationalMode(Enum):
    """Operational modes for DEVONIKA"""
    GUIDED = "guided"  # Step-by-step with user checkpoints
    AUTONOMOUS = "autonomous"  # Full autonomy with minimal intervention
    DISCOVERY = "discovery"  # Focus on discovery and planning phase
    IMPLEMENTATION = "implementation"  # Focus on implementation phase
    FULL = "full"  # All capabilities and workflows


class WorkflowPhase(Enum):
    """Workflow phases"""
    DISCOVERY = "discovery"
    ARCHITECTURE = "architecture"
    IMPLEMENTATION = "implementation"
    VERIFICATION = "verification"
    DEPLOYMENT = "deployment"


class SystemPromptManager:
    """
    Manages the assembly and delivery of DEVONIKA system prompts.
    Supports dynamic prompt construction based on operational mode and context.
    """

    def __init__(self, prompts_dir: Optional[Path] = None):
        """
        Initialize the SystemPromptManager.

        Args:
            prompts_dir: Directory containing prompt components (defaults to package location)
        """
        if prompts_dir is None:
            prompts_dir = Path(__file__).parent

        self.prompts_dir = prompts_dir
        self.components_dir = prompts_dir / "components"
        self.workflows_dir = prompts_dir / "workflows"

        # Validate directories exist
        if not self.components_dir.exists():
            raise FileNotFoundError(f"Components directory not found: {self.components_dir}")
        if not self.workflows_dir.exists():
            raise FileNotFoundError(f"Workflows directory not found: {self.workflows_dir}")

    def _load_component(self, component_name: str) -> str:
        """Load a component file and return its content"""
        component_path = self.components_dir / f"{component_name}.txt"
        if not component_path.exists():
            raise FileNotFoundError(f"Component not found: {component_path}")

        with open(component_path, 'r', encoding='utf-8') as f:
            return f.read().strip()

    def _load_workflow(self, phase: WorkflowPhase) -> str:
        """Load a workflow phase file and return its content"""
        workflow_map = {
            WorkflowPhase.DISCOVERY: "phase1_discovery",
            WorkflowPhase.ARCHITECTURE: "phase2_architecture",
            WorkflowPhase.IMPLEMENTATION: "phase3_implementation",
            WorkflowPhase.VERIFICATION: "phase4_verification",
            WorkflowPhase.DEPLOYMENT: "phase5_deployment",
        }

        workflow_file = workflow_map.get(phase)
        if not workflow_file:
            raise ValueError(f"Unknown workflow phase: {phase}")

        workflow_path = self.workflows_dir / f"{workflow_file}.txt"
        if not workflow_path.exists():
            raise FileNotFoundError(f"Workflow not found: {workflow_path}")

        with open(workflow_path, 'r', encoding='utf-8') as f:
            return f.read().strip()

    def get_system_prompt(
        self,
        mode: OperationalMode = OperationalMode.FULL,
        include_workflows: Optional[List[WorkflowPhase]] = None,
        custom_additions: Optional[str] = None
    ) -> str:
        """
        Assemble and return the complete system prompt based on parameters.

        Args:
            mode: Operational mode for DEVONIKA
            include_workflows: Specific workflow phases to include (None = all)
            custom_additions: Additional custom instructions to append

        Returns:
            Complete system prompt as a string
        """
        sections = []

        # Core components (always included)
        sections.append(self._load_component("core_identity"))
        sections.append(self._load_component("capabilities"))
        sections.append(self._load_component("operating_principles"))

        # Add workflows based on mode and parameters
        if mode == OperationalMode.FULL or include_workflows:
            sections.append("\n=== WORKFLOW METHODOLOGY ===\n")

            phases_to_include = include_workflows or list(WorkflowPhase)
            for phase in phases_to_include:
                sections.append(self._load_workflow(phase))

        # Context management (always useful)
        sections.append(self._load_component("context_management"))

        # Communication protocol
        sections.append(self._load_component("communication_protocol"))

        # Mode-specific components
        if mode == OperationalMode.AUTONOMOUS:
            sections.append(self._load_component("autonomous_mode"))

        # Success metrics and final directives (always included)
        sections.append(self._load_component("success_metrics"))
        sections.append(self._load_component("final_directives"))

        # Custom additions if provided
        if custom_additions:
            sections.append("\n=== CUSTOM INSTRUCTIONS ===\n")
            sections.append(custom_additions)

        # Assemble all sections
        return "\n\n".join(sections)

    def get_phase_specific_prompt(self, phase: WorkflowPhase) -> str:
        """
        Get a prompt focused on a specific workflow phase.

        Args:
            phase: The workflow phase to focus on

        Returns:
            System prompt focused on the specified phase
        """
        sections = [
            self._load_component("core_identity"),
            self._load_component("capabilities"),
            self._load_component("operating_principles"),
            f"\n=== CURRENT PHASE: {phase.value.upper()} ===\n",
            self._load_workflow(phase),
            self._load_component("communication_protocol"),
            self._load_component("success_metrics"),
        ]

        return "\n\n".join(sections)

    def get_minimal_prompt(self) -> str:
        """
        Get a minimal system prompt with just core identity and principles.

        Returns:
            Minimal system prompt
        """
        sections = [
            self._load_component("core_identity"),
            self._load_component("capabilities"),
            self._load_component("operating_principles"),
            self._load_component("final_directives"),
        ]

        return "\n\n".join(sections)

    def get_available_components(self) -> List[str]:
        """Get list of available component files"""
        return [f.stem for f in self.components_dir.glob("*.txt")]

    def get_available_workflows(self) -> List[str]:
        """Get list of available workflow files"""
        return [f.stem for f in self.workflows_dir.glob("*.txt")]


# Convenience function for quick access
def get_devonika_prompt(
    mode: OperationalMode = OperationalMode.FULL,
    phase: Optional[WorkflowPhase] = None
) -> str:
    """
    Convenience function to get DEVONIKA system prompt.

    Args:
        mode: Operational mode
        phase: Specific phase to focus on (if any)

    Returns:
        System prompt string
    """
    manager = SystemPromptManager()

    if phase:
        return manager.get_phase_specific_prompt(phase)
    else:
        return manager.get_system_prompt(mode=mode)
