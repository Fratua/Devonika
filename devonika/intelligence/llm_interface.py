"""
LLM Interface - Handles interactions with Large Language Models
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List

from devonika.system_prompts import (
    SystemPromptManager,
    OperationalMode,
    WorkflowPhase,
    get_devonika_prompt
)


class LLMInterface:
    """
    Interface for interacting with various LLM providers (Anthropic, OpenAI, etc.)
    Handles prompt engineering, context management, and response parsing.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = config.get("provider", "anthropic")
        self.model = config.get("model", "claude-3-5-sonnet-20241022")
        self.temperature = config.get("temperature", 0.7)

        # Initialize client based on provider
        self.client = self._init_client()

        # Context management
        self.context_window = []
        self.max_context_messages = 10

        # DEVONIKA system prompt management
        self.system_prompt_manager = SystemPromptManager()
        self.operational_mode = OperationalMode(
            config.get("operational_mode", "full")
        )
        self.current_phase = None
        self.use_devonika_prompt = config.get("use_devonika_prompt", True)

    def _init_client(self):
        """Initialize the LLM client"""
        if self.provider == "anthropic":
            try:
                import anthropic
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    raise ValueError("ANTHROPIC_API_KEY environment variable not set")
                return anthropic.Anthropic(api_key=api_key)
            except ImportError:
                raise ImportError("anthropic package not installed. Install with: pip install anthropic")

        elif self.provider == "openai":
            try:
                import openai
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY environment variable not set")
                openai.api_key = api_key
                return openai
            except ImportError:
                raise ImportError("openai package not installed. Install with: pip install openai")

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    async def generate(self,
                      prompt: str,
                      system_prompt: Optional[str] = None,
                      response_format: Optional[str] = None,
                      max_tokens: int = 4096) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            response_format: Optional format hint ("json", "code", etc.)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response
        """
        # Add format instructions if specified
        if response_format == "json":
            prompt += "\n\nIMPORTANT: Respond with valid JSON only, no markdown code blocks."

        # Use provider-specific API
        if self.provider == "anthropic":
            return await self._generate_anthropic(prompt, system_prompt, max_tokens)
        elif self.provider == "openai":
            return await self._generate_openai(prompt, system_prompt, max_tokens)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    async def _generate_anthropic(self,
                                  prompt: str,
                                  system_prompt: Optional[str],
                                  max_tokens: int) -> str:
        """Generate using Anthropic's Claude"""
        messages = [{"role": "user", "content": prompt}]

        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": self.temperature,
            "messages": messages
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        try:
            # Synchronous call - in production, use async client
            response = self.client.messages.create(**kwargs)
            return response.content[0].text

        except Exception as e:
            logging.error(f"Error generating with Anthropic: {e}")
            raise

    async def _generate_openai(self,
                              prompt: str,
                              system_prompt: Optional[str],
                              max_tokens: int) -> str:
        """Generate using OpenAI's GPT"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content

        except Exception as e:
            logging.error(f"Error generating with OpenAI: {e}")
            raise

    def add_to_context(self, role: str, content: str) -> None:
        """Add a message to the context window"""
        self.context_window.append({"role": role, "content": content})

        # Trim context if too large
        if len(self.context_window) > self.max_context_messages:
            self.context_window = self.context_window[-self.max_context_messages:]

    def clear_context(self) -> None:
        """Clear the context window"""
        self.context_window = []

    def get_context(self) -> List[Dict[str, str]]:
        """Get current context"""
        return self.context_window.copy()

    def set_operational_mode(self, mode: OperationalMode) -> None:
        """
        Set the operational mode for DEVONIKA.

        Args:
            mode: The operational mode to use
        """
        self.operational_mode = mode

    def set_workflow_phase(self, phase: Optional[WorkflowPhase]) -> None:
        """
        Set the current workflow phase.

        Args:
            phase: The workflow phase to focus on (None to clear)
        """
        self.current_phase = phase

    def get_devonika_system_prompt(
        self,
        custom_additions: Optional[str] = None
    ) -> str:
        """
        Get the DEVONIKA system prompt based on current settings.

        Args:
            custom_additions: Additional custom instructions to append

        Returns:
            Complete DEVONIKA system prompt
        """
        if self.current_phase:
            return self.system_prompt_manager.get_phase_specific_prompt(
                self.current_phase
            )
        else:
            return self.system_prompt_manager.get_system_prompt(
                mode=self.operational_mode,
                custom_additions=custom_additions
            )

    async def generate_with_devonika(
        self,
        prompt: str,
        response_format: Optional[str] = None,
        max_tokens: int = 4096,
        custom_system_additions: Optional[str] = None
    ) -> str:
        """
        Generate a response using DEVONIKA system prompt.

        Args:
            prompt: The user prompt
            response_format: Optional format hint ("json", "code", etc.)
            max_tokens: Maximum tokens to generate
            custom_system_additions: Additional custom system instructions

        Returns:
            Generated text response
        """
        system_prompt = self.get_devonika_system_prompt(custom_system_additions)
        return await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            response_format=response_format,
            max_tokens=max_tokens
        )
