"""
LLM wrapper for generating and processing text with various providers.
"""
import os
from typing import Optional
from openai import OpenAI
import anthropic


class LLMWrapper:
    """Wrapper for different LLM providers (OpenAI, Anthropic)."""
    
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        """
        Initialize LLM wrapper.
        
        Args:
            provider: "openai" or "anthropic"
            api_key: API key (if None, reads from environment)
        """
        self.provider = provider.lower()
        
        if self.provider == "openai":
            api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-4o-mini"  # Cost-effective default
            
        elif self.provider == "anthropic":
            api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment")
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model = "claude-3-haiku-20240307"  # Fast default
            
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            Generated text
        """
        if self.provider == "openai":
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
            
        elif self.provider == "anthropic":
            system = system_prompt or ""
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
    
    def generate_answer(self, query: str) -> str:
        """
        Generate an answer to a query (convenience method).
        
        Args:
            query: User question
            
        Returns:
            Answer text
        """
        return self.generate(query)

