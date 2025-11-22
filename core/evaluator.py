"""
Evaluator module - compares claims against evidence and calculates truthfulness scores.
"""
import json
import numpy as np
from typing import List, Dict, Optional
from .retrieval import EvidenceRetriever
from .llm import LLMWrapper


class TruthfulnessEvaluator:
    """Evaluates truthfulness of claims by comparing against evidence."""
    
    def __init__(self, retriever: EvidenceRetriever, llm_wrapper: Optional[LLMWrapper] = None):
        """
        Initialize truthfulness evaluator.
        
        Args:
            retriever: Evidence retriever instance
            llm_wrapper: Optional LLM wrapper for verification (if None, uses embeddings)
        """
        self.retriever = retriever
        self.llm = llm_wrapper
    
    def evaluate_claim(self, claim: str, evidence: List[Dict[str, str]]) -> Dict[str, any]:
        """
        Evaluate a single claim against evidence.
        
        Args:
            claim: The claim to evaluate
            evidence: List of evidence dictionaries
            
        Returns:
            Dictionary with score, verdict, and reasoning
        """
        if not evidence:
            return {
                "score": 0.0,
                "verdict": "no_evidence",
                "reasoning": "No evidence found to verify this claim",
                "confidence": 0.0
            }
        
        # Method 1: Use LLM verification if available
        if self.llm:
            return self._evaluate_with_llm(claim, evidence)
        else:
            # Method 2: Use embedding similarity
            return self._evaluate_with_embeddings(claim, evidence)
    
    def _evaluate_with_llm(self, claim: str, evidence: List[Dict[str, str]]) -> Dict[str, any]:
        """Evaluate using LLM verification."""
        evidence_text = "\n\n".join([
            f"Source: {ev['source']}\n{ev['text']}"
            for ev in evidence[:3]  # Use top 3 evidence snippets
        ])
        
        prompt = f"""Evaluate whether the following claim is supported by the provided evidence.

Claim: {claim}

Evidence:
{evidence_text}

Respond with a JSON object containing:
- "supported": true/false (is the claim supported by evidence?)
- "confidence": 0.0-1.0 (how confident are you?)
- "reasoning": brief explanation
- "contradiction": true/false (does evidence contradict the claim?)

Return ONLY the JSON object, no other text."""

        try:
            response = self.llm.generate(
                prompt,
                system_prompt="You are a fact-checking system. Be precise and objective."
            )
            
            # Parse JSON response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            result = json.loads(response)
            
            supported = result.get("supported", False)
            confidence = float(result.get("confidence", 0.5))
            contradiction = result.get("contradiction", False)
            
            # Calculate score
            if contradiction:
                score = 0.0
                verdict = "contradicted"
            elif supported:
                score = confidence
                verdict = "supported"
            else:
                score = 0.3  # Uncertain
                verdict = "uncertain"
            
            return {
                "score": score,
                "verdict": verdict,
                "reasoning": result.get("reasoning", ""),
                "confidence": confidence
            }
            
        except Exception as e:
            print(f"LLM evaluation error: {e}")
            # Fallback to embedding method
            return self._evaluate_with_embeddings(claim, evidence)
    
    def _evaluate_with_embeddings(self, claim: str, evidence: List[Dict[str, str]]) -> Dict[str, any]:
        """Evaluate using embedding similarity."""
        try:
            claim_embedding = np.array(self.retriever.get_embeddings(claim))
            
            similarities = []
            for ev in evidence:
                ev_embedding = np.array(self.retriever.get_embeddings(ev['text']))
                similarity = self._cosine_similarity(claim_embedding, ev_embedding)
                similarities.append(similarity)
            
            avg_similarity = np.mean(similarities) if similarities else 0.0
            max_similarity = max(similarities) if similarities else 0.0
            
            # Weighted score: 70% max similarity, 30% average
            score = 0.7 * max_similarity + 0.3 * avg_similarity
            
            # Determine verdict
            if score >= 0.75:
                verdict = "supported"
            elif score >= 0.55:
                verdict = "uncertain"
            elif score >= 0.35:
                verdict = "weak_support"
            else:
                verdict = "contradicted"
            
            return {
                "score": float(score),
                "verdict": verdict,
                "reasoning": f"Embedding similarity: {score:.2f}",
                "confidence": float(max_similarity)
            }
            
        except Exception as e:
            print(f"Embedding evaluation error: {e}")
            return {
                "score": 0.0,
                "verdict": "error",
                "reasoning": f"Evaluation error: {str(e)}",
                "confidence": 0.0
            }
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def evaluate_text(self, claims: List[Dict[str, str]], evidence_list: List[List[Dict[str, str]]]) -> Dict[str, any]:
        """
        Evaluate multiple claims and aggregate into overall score.
        
        Args:
            claims: List of claim dictionaries
            evidence_list: List of evidence lists (one per claim)
            
        Returns:
            Overall evaluation result with aggregated score
        """
        if not claims:
            return {
                "overall_score": 0.0,
                "verdict": "no_claims",
                "claim_results": [],
                "total_claims": 0
            }
        
        claim_results = []
        scores = []
        
        for claim_dict, evidence in zip(claims, evidence_list):
            claim = claim_dict.get("claim", "")
            result = self.evaluate_claim(claim, evidence)
            result["claim"] = claim
            result["context"] = claim_dict.get("context", "")
            claim_results.append(result)
            scores.append(result["score"])
        
        # Calculate overall score (weighted average)
        overall_score = np.mean(scores) if scores else 0.0
        
        # Determine overall verdict
        if overall_score >= 0.75:
            verdict = "highly_truthful"
        elif overall_score >= 0.55:
            verdict = "mostly_truthful"
        elif overall_score >= 0.35:
            verdict = "uncertain"
        else:
            verdict = "likely_hallucination"
        
        return {
            "overall_score": float(overall_score),
            "verdict": verdict,
            "claim_results": claim_results,
            "total_claims": len(claims),
            "percentage_score": float(overall_score * 100)
        }

