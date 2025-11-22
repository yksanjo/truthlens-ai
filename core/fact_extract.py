"""
Fact extraction module - extracts atomic claims from LLM output.
"""
import json
from typing import List, Dict
from .llm import LLMWrapper


class ClaimExtractor:
    """Extracts factual claims from text that can be fact-checked."""
    
    def __init__(self, llm_wrapper: LLMWrapper):
        """
        Initialize claim extractor.
        
        Args:
            llm_wrapper: LLM wrapper instance for extraction
        """
        self.llm = llm_wrapper
    
    def extract_claims(self, text: str) -> List[Dict[str, str]]:
        """
        Extract atomic factual claims from text.
        
        Args:
            text: Text to extract claims from
            
        Returns:
            List of claim dictionaries with 'claim' and 'context' keys
        """
        prompt = f"""Extract all atomic factual claims from the following text. 
A factual claim is a statement that can be verified as true or false.

For each claim, provide:
1. The specific factual statement
2. The context (what it refers to)

Text to analyze:
{text}

Format your response as a JSON array, where each item has:
- "claim": the specific factual statement
- "context": brief context about what this claim refers to

Example format:
[
  {{"claim": "Beethoven met Mozart in Vienna", "context": "Historical meeting between composers"}},
  {{"claim": "The meeting occurred in 1787", "context": "Year of the meeting"}}
]

Return ONLY the JSON array, no other text."""

        try:
            response = self.llm.generate(
                prompt,
                system_prompt="You are a precise fact extraction system. Extract only verifiable factual claims."
            )
            
            # Try to parse JSON from response
            # Sometimes LLM adds markdown formatting
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            claims = json.loads(response)
            
            # Ensure format is correct
            if isinstance(claims, list):
                return [
                    {
                        "claim": item.get("claim", ""),
                        "context": item.get("context", "")
                    }
                    for item in claims
                    if item.get("claim")
                ]
            else:
                return []
                
        except Exception as e:
            print(f"Error extracting claims: {e}")
            # Fallback: simple sentence-based extraction
            return self._fallback_extract(text)
    
    def _fallback_extract(self, text: str) -> List[Dict[str, str]]:
        """Fallback extraction using simple sentence splitting."""
        sentences = text.split('.')
        claims = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 10:  # Filter very short sentences
                # Simple heuristic: if sentence contains dates, names, or numbers
                if any(char.isdigit() for char in sentence):
                    claims.append({
                        "claim": sentence,
                        "context": "Extracted from text"
                    })
        
        return claims[:10]  # Limit to 10 claims

