"""
Simple test script to verify the hallucination meter works.
"""
import os
from core.hallucination_meter import HallucinationMeter


def test_basic_evaluation():
    """Test basic text evaluation."""
    print("🧪 Testing AI Hallucination Meter...")
    print("")
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: No API key found!")
        print("   Please set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
        return
    
    # Initialize meter
    print("📦 Initializing Hallucination Meter...")
    try:
        meter = HallucinationMeter(
            llm_provider="openai" if os.getenv("OPENAI_API_KEY") else "anthropic",
            retrieval_method="wikipedia",
            use_llm_verification=True
        )
        print("✅ Initialized successfully!")
        print("")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return
    
    # Test 1: Evaluate a known fact
    print("Test 1: Evaluating a factual statement...")
    test_text = "The capital of France is Paris."
    print(f"   Text: {test_text}")
    
    try:
        result = meter.evaluate(test_text)
        print(f"   ✅ Score: {result['percentage_score']:.1f}%")
        print(f"   ✅ Verdict: {result['verdict']}")
        print(f"   ✅ Claims analyzed: {result['total_claims']}")
        print("")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("")
    
    # Test 2: Evaluate a potentially false statement
    print("Test 2: Evaluating a potentially false statement...")
    test_text = "Beethoven met Mozart in Vienna in 1787 and they became best friends."
    print(f"   Text: {test_text}")
    
    try:
        result = meter.evaluate(test_text)
        print(f"   ✅ Score: {result['percentage_score']:.1f}%")
        print(f"   ✅ Verdict: {result['verdict']}")
        print(f"   ✅ Claims analyzed: {result['total_claims']}")
        print("")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("")
    
    # Test 3: Query and evaluate
    print("Test 3: Query and evaluate...")
    query = "What is the capital of France?"
    print(f"   Query: {query}")
    
    try:
        result = meter.evaluate_query(query)
        print(f"   ✅ Answer: {result.get('answer', 'N/A')[:100]}...")
        print(f"   ✅ Score: {result['percentage_score']:.1f}%")
        print(f"   ✅ Verdict: {result['verdict']}")
        print("")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("")
    
    print("🎉 Tests completed!")


if __name__ == "__main__":
    test_basic_evaluation()

