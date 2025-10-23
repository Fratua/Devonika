"""
Tests for LLM Integration with DEVONIKA System Prompts
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from devonika.intelligence.llm_interface import LLMInterface
from devonika.system_prompts import OperationalMode, WorkflowPhase


class TestLLMIntegration:
    """Test LLM integration with DEVONIKA prompts"""

    @pytest.fixture
    def llm_config(self):
        """Fixture for LLM configuration"""
        return {
            "provider": "anthropic",
            "model": "claude-3-5-sonnet-20241022",
            "temperature": 0.7,
            "operational_mode": "full",
            "use_devonika_prompt": True
        }

    @pytest.fixture
    def mock_anthropic_client(self):
        """Mock Anthropic client"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock(text="Test response")]
        mock_client.messages.create.return_value = mock_response
        return mock_client

    def test_llm_initialization_with_devonika(self, llm_config):
        """Test LLM initializes with DEVONIKA support"""
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            with patch("anthropic.Anthropic"):
                llm = LLMInterface(llm_config)
                assert llm.use_devonika_prompt is True
                assert llm.operational_mode == OperationalMode.FULL
                assert llm.system_prompt_manager is not None

    def test_set_operational_mode(self, llm_config):
        """Test setting operational mode"""
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            with patch("anthropic.Anthropic"):
                llm = LLMInterface(llm_config)
                llm.set_operational_mode(OperationalMode.AUTONOMOUS)
                assert llm.operational_mode == OperationalMode.AUTONOMOUS

    def test_set_workflow_phase(self, llm_config):
        """Test setting workflow phase"""
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            with patch("anthropic.Anthropic"):
                llm = LLMInterface(llm_config)
                llm.set_workflow_phase(WorkflowPhase.DISCOVERY)
                assert llm.current_phase == WorkflowPhase.DISCOVERY

    def test_get_devonika_system_prompt(self, llm_config):
        """Test getting DEVONIKA system prompt"""
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            with patch("anthropic.Anthropic"):
                llm = LLMInterface(llm_config)
                prompt = llm.get_devonika_system_prompt()
                assert prompt is not None
                assert "DEVONIKA" in prompt

    def test_get_devonika_system_prompt_with_phase(self, llm_config):
        """Test getting phase-specific prompt"""
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            with patch("anthropic.Anthropic"):
                llm = LLMInterface(llm_config)
                llm.set_workflow_phase(WorkflowPhase.ARCHITECTURE)
                prompt = llm.get_devonika_system_prompt()
                assert "architecture" in prompt.lower()

    @pytest.mark.asyncio
    async def test_generate_with_devonika(self, llm_config, mock_anthropic_client):
        """Test generating response with DEVONIKA prompt"""
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            with patch("anthropic.Anthropic", return_value=mock_anthropic_client):
                llm = LLMInterface(llm_config)
                response = await llm.generate_with_devonika(
                    prompt="Build a todo app"
                )
                assert response == "Test response"
                # Verify that system prompt was used
                mock_anthropic_client.messages.create.assert_called_once()
                call_args = mock_anthropic_client.messages.create.call_args
                assert "system" in call_args[1]
                assert "DEVONIKA" in call_args[1]["system"]

    def test_custom_system_additions(self, llm_config):
        """Test adding custom system instructions"""
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            with patch("anthropic.Anthropic"):
                llm = LLMInterface(llm_config)
                custom = "Use PostgreSQL only"
                prompt = llm.get_devonika_system_prompt(custom_additions=custom)
                assert custom in prompt


class TestLLMConfigurationModes:
    """Test different LLM configuration modes"""

    def test_autonomous_mode_config(self):
        """Test autonomous mode configuration"""
        config = {
            "provider": "anthropic",
            "operational_mode": "autonomous",
            "use_devonika_prompt": True
        }
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            with patch("anthropic.Anthropic"):
                llm = LLMInterface(config)
                assert llm.operational_mode == OperationalMode.AUTONOMOUS

    def test_guided_mode_config(self):
        """Test guided mode configuration"""
        config = {
            "provider": "anthropic",
            "operational_mode": "guided",
            "use_devonika_prompt": True
        }
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            with patch("anthropic.Anthropic"):
                llm = LLMInterface(config)
                assert llm.operational_mode == OperationalMode.GUIDED

    def test_discovery_mode_config(self):
        """Test discovery mode configuration"""
        config = {
            "provider": "anthropic",
            "operational_mode": "discovery",
            "use_devonika_prompt": True
        }
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            with patch("anthropic.Anthropic"):
                llm = LLMInterface(config)
                assert llm.operational_mode == OperationalMode.DISCOVERY


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
