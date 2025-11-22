"""
Retrieval module for fetching evidence from external sources.
Supports Wikipedia, web search, and vector database search.
"""
import os
import requests
from typing import List, Dict, Optional
import wikipedia
from openai import OpenAI


class EvidenceRetriever:
    """Retrieves evidence from various sources to fact-check claims."""
    
    def __init__(self, retrieval_method: str = "wikipedia", openai_api_key: Optional[str] = None):
        """
        Initialize evidence retriever.
        
        Args:
            retrieval_method: "wikipedia", "web", or "vector"
            openai_api_key: OpenAI API key for embeddings (if using vector search)
        """
        self.method = retrieval_method.lower()
        self.openai_client = None
        
        if self.method == "vector" or self.method == "web":
            api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
            if api_key:
                self.openai_client = OpenAI(api_key=api_key)
        
        # Configure Wikipedia
        if self.method == "wikipedia":
            wikipedia.set_lang("en")
            wikipedia.set_rate_limiting(True)
    
    def retrieve(self, claim: str, top_k: int = 5) -> List[Dict[str, str]]:
        """
        Retrieve evidence for a claim.
        
        Args:
            claim: The claim to fact-check
            top_k: Number of evidence snippets to return
            
        Returns:
            List of evidence dictionaries with 'text' and 'source' keys
        """
        if self.method == "wikipedia":
            return self._retrieve_wikipedia(claim, top_k)
        elif self.method == "web":
            return self._retrieve_web(claim, top_k)
        elif self.method == "vector":
            return self._retrieve_vector(claim, top_k)
        else:
            raise ValueError(f"Unknown retrieval method: {self.method}")
    
    def _retrieve_wikipedia(self, claim: str, top_k: int) -> List[Dict[str, str]]:
        """Retrieve evidence from Wikipedia."""
        evidence = []
        
        try:
            # Search for relevant pages
            search_results = wikipedia.search(claim, results=top_k)
            
            for title in search_results[:top_k]:
                try:
                    page = wikipedia.page(title, auto_suggest=False)
                    # Extract relevant sentences (simple approach)
                    sentences = page.content.split('.')[:10]  # First 10 sentences
                    text = '. '.join(sentences) + '.'
                    
                    evidence.append({
                        "text": text,
                        "source": f"Wikipedia: {title}",
                        "url": page.url
                    })
                except wikipedia.exceptions.DisambiguationError:
                    continue
                except wikipedia.exceptions.PageError:
                    continue
                    
        except Exception as e:
            # Fallback: return empty evidence
            print(f"Wikipedia retrieval error: {e}")
        
        return evidence[:top_k]
    
    def _retrieve_web(self, claim: str, top_k: int) -> List[Dict[str, str]]:
        """Retrieve evidence using web search (requires API key)."""
        # This is a placeholder - in production, use Google/Bing API
        # For hackathon, we'll use a simple Wikipedia fallback
        return self._retrieve_wikipedia(claim, top_k)
    
    def _retrieve_vector(self, claim: str, top_k: int) -> List[Dict[str, str]]:
        """Retrieve evidence using vector similarity (placeholder)."""
        # In production, this would search a FAISS/Pinecone database
        # For now, fallback to Wikipedia
        return self._retrieve_wikipedia(claim, top_k)
    
    def get_embeddings(self, text: str) -> List[float]:
        """Get embeddings for text using OpenAI."""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

