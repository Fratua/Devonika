"""
Tests for DEVONIKA System Prompts
"""

import pytest
from pathlib import Path

from devonika.system_prompts import (
    SystemPromptManager,
    OperationalMode,
    WorkflowPhase,
    get_devonika_prompt,
)


class TestSystemPromptManager:
    """Test SystemPromptManager functionality"""

    def setup_method(self):
        """Setup for each test"""
        self.manager = SystemPromptManager()

    def test_initialization(self):
        """Test manager initializes correctly"""
        assert self.manager.prompts_dir is not None
        assert self.manager.components_dir.exists()
        assert self.manager.workflows_dir.exists()

    def test_load_component(self):
        """Test loading individual components"""
        identity = self.manager._load_component("core_identity")
        assert identity is not None
        assert len(identity) > 0
        assert "DEVONIKA" in identity

    def test_load_workflow(self):
        """Test loading workflow phases"""
        discovery = self.manager._load_workflow(WorkflowPhase.DISCOVERY)
        assert discovery is not None
        assert len(discovery) > 0
        assert "DISCOVERY" in discovery or "discovery" in discovery.lower()

    def test_get_system_prompt_full(self):
        """Test getting full system prompt"""
        prompt = self.manager.get_system_prompt(mode=OperationalMode.FULL)
        assert prompt is not None
        assert len(prompt) > 1000  # Should be comprehensive
        assert "DEVONIKA" in prompt
        assert "capabilities" in prompt.lower() or "CAPABILITIES" in prompt

    def test_get_system_prompt_autonomous(self):
        """Test getting autonomous mode prompt"""
        prompt = self.manager.get_system_prompt(mode=OperationalMode.AUTONOMOUS)
        assert prompt is not None
        assert "DEVONIKA" in prompt
        assert "autonomous" in prompt.lower()

    def test_get_phase_specific_prompt(self):
        """Test getting phase-specific prompts"""
        for phase in WorkflowPhase:
            prompt = self.manager.get_phase_specific_prompt(phase)
            assert prompt is not None
            assert len(prompt) > 100
            assert "DEVONIKA" in prompt

    def test_get_minimal_prompt(self):
        """Test getting minimal prompt"""
        prompt = self.manager.get_minimal_prompt()
        assert prompt is not None
        assert "DEVONIKA" in prompt
        # Should be shorter than full prompt
        full_prompt = self.manager.get_system_prompt(mode=OperationalMode.FULL)
        assert len(prompt) < len(full_prompt)

    def test_custom_additions(self):
        """Test adding custom instructions"""
        custom = "Must use PostgreSQL database"
        prompt = self.manager.get_system_prompt(
            mode=OperationalMode.FULL,
            custom_additions=custom
        )
        assert custom in prompt

    def test_get_available_components(self):
        """Test listing available components"""
        components = self.manager.get_available_components()
        assert len(components) > 0
        assert "core_identity" in components
        assert "capabilities" in components

    def test_get_available_workflows(self):
        """Test listing available workflows"""
        workflows = self.manager.get_available_workflows()
        assert len(workflows) > 0
        assert any("discovery" in w.lower() for w in workflows)


class TestConvenienceFunction:
    """Test the convenience function"""

    def test_get_devonika_prompt_default(self):
        """Test default prompt generation"""
        prompt = get_devonika_prompt()
        assert prompt is not None
        assert "DEVONIKA" in prompt

    def test_get_devonika_prompt_with_mode(self):
        """Test prompt generation with specific mode"""
        prompt = get_devonika_prompt(mode=OperationalMode.AUTONOMOUS)
        assert prompt is not None
        assert "autonomous" in prompt.lower()

    def test_get_devonika_prompt_with_phase(self):
        """Test prompt generation with specific phase"""
        prompt = get_devonika_prompt(phase=WorkflowPhase.DISCOVERY)
        assert prompt is not None
        assert "discovery" in prompt.lower()


class TestOperationalMode:
    """Test OperationalMode enum"""

    def test_operational_modes_exist(self):
        """Test all operational modes are defined"""
        assert OperationalMode.FULL is not None
        assert OperationalMode.AUTONOMOUS is not None
        assert OperationalMode.GUIDED is not None
        assert OperationalMode.DISCOVERY is not None
        assert OperationalMode.IMPLEMENTATION is not None

    def test_operational_mode_values(self):
        """Test operational mode values"""
        assert OperationalMode.FULL.value == "full"
        assert OperationalMode.AUTONOMOUS.value == "autonomous"
        assert OperationalMode.GUIDED.value == "guided"


class TestWorkflowPhase:
    """Test WorkflowPhase enum"""

    def test_workflow_phases_exist(self):
        """Test all workflow phases are defined"""
        assert WorkflowPhase.DISCOVERY is not None
        assert WorkflowPhase.ARCHITECTURE is not None
        assert WorkflowPhase.IMPLEMENTATION is not None
        assert WorkflowPhase.VERIFICATION is not None
        assert WorkflowPhase.DEPLOYMENT is not None

    def test_workflow_phase_values(self):
        """Test workflow phase values"""
        assert WorkflowPhase.DISCOVERY.value == "discovery"
        assert WorkflowPhase.ARCHITECTURE.value == "architecture"
        assert WorkflowPhase.IMPLEMENTATION.value == "implementation"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
