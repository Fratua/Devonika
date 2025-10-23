"""
DEVONIKA System Prompts Module

This module manages the DEVONIKA system prompts, which define the AI's
identity, capabilities, and operational workflows.
"""

from .system_prompt_manager import (
    SystemPromptManager,
    OperationalMode,
    WorkflowPhase,
    get_devonika_prompt,
)

__all__ = [
    "SystemPromptManager",
    "OperationalMode",
    "WorkflowPhase",
    "get_devonika_prompt",
]
