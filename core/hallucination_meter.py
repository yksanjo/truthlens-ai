"""
Main orchestrator for the AI Hallucination Meter.
Combines all components to evaluate LLM output.
"""
from typing import Dict, Optional
from .llm import LLMWrapper
from .retrieval import EvidenceRetriever
from .fact_extract import ClaimExtractor
from .evaluator import TruthfulnessEvaluator


class HallucinationMeter:
    """Main class that orchestrates the hallucination detection pipeline."""
    
    def __init__(
        self,
        llm_provider: str = "openai",
        retrieval_method: str = "wikipedia",
        use_llm_verification: bool = True
    ):
        """
        Initialize the hallucination meter.
        
        Args:
            llm_provider: "openai" or "anthropic"
            retrieval_method: "wikipedia", "web", or "vector"
            use_llm_verification: Whether to use LLM for verification (vs embeddings)
        """
        # Initialize components
        self.llm = LLMWrapper(provider=llm_provider)
        self.retriever = EvidenceRetriever(retrieval_method=retrieval_method)
        self.extractor = ClaimExtractor(self.llm)
        self.evaluator = TruthfulnessEvaluator(
            self.retriever,
            llm_wrapper=self.llm if use_llm_verification else None
        )
    
    def evaluate(self, text: str) -> Dict:
        """
        Evaluate text for hallucinations.
        
        Args:
            text: Text to evaluate (LLM output)
            
        Returns:
            Dictionary with evaluation results
        """
        # Step 1: Extract claims
        claims = self.extractor.extract_claims(text)
        
        if not claims:
            return {
                "overall_score": 0.0,
                "verdict": "no_claims",
                "percentage_score": 0.0,
                "claim_results": [],
                "total_claims": 0,
                "original_text": text
            }
        
        # Step 2: Retrieve evidence for each claim
        evidence_list = []
        for claim_dict in claims:
            claim = claim_dict.get("claim", "")
            evidence = self.retriever.retrieve(claim, top_k=3)
            evidence_list.append(evidence)
        
        # Step 3: Evaluate claims against evidence
        result = self.evaluator.evaluate_text(claims, evidence_list)
        result["original_text"] = text
        result["claims"] = claims
        
        return result
    
    def evaluate_query(self, query: str) -> Dict:
        """
        Generate answer to query and evaluate it.
        
        Args:
            query: User query
            
        Returns:
            Dictionary with answer and evaluation results
        """
        # Generate answer
        answer = self.llm.generate_answer(query)
        
        # Evaluate the answer
        evaluation = self.evaluate(answer)
        evaluation["query"] = query
        evaluation["answer"] = answer
        
        return evaluation

