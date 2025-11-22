"""
Streamlit UI for the AI Hallucination Meter.
"""
import streamlit as st
import os
from core.hallucination_meter import HallucinationMeter
from core.utils import format_score_display, format_verdict, get_verdict_color


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="AI Hallucination Meter",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 TruthLens AI")
    st.markdown("**Real-Time Truthfulness Score for LLM Output**")
    st.markdown("---")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        llm_provider = st.selectbox(
            "LLM Provider",
            ["openai", "anthropic"],
            help="Choose the LLM provider for generating answers"
        )
        
        retrieval_method = st.selectbox(
            "Retrieval Method",
            ["wikipedia", "web", "vector"],
            help="Method for retrieving evidence"
        )
        
        use_llm_verification = st.checkbox(
            "Use LLM Verification",
            value=True,
            help="Use LLM for claim verification (more accurate but slower)"
        )
        
        st.markdown("---")
        st.markdown("### 📝 API Keys")
        st.markdown("Set these in your environment or enter below:")
        
        if llm_provider == "openai":
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                value=os.getenv("OPENAI_API_KEY", "")
            )
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
        else:
            api_key = st.text_input(
                "Anthropic API Key",
                type="password",
                value=os.getenv("ANTHROPIC_API_KEY", "")
            )
            if api_key:
                os.environ["ANTHROPIC_API_KEY"] = api_key
    
    # Main content area
    tab1, tab2 = st.tabs(["📝 Evaluate Text", "❓ Query & Evaluate"])
    
    with tab1:
        st.header("Evaluate Existing Text")
        st.markdown("Paste any LLM output to check for hallucinations.")
        
        text_input = st.text_area(
            "Text to Evaluate",
            height=200,
            placeholder="Paste LLM output here...\n\nExample: Beethoven met Mozart in Vienna in 1787. They became close friends and collaborated on several compositions."
        )
        
        if st.button("🔍 Evaluate", type="primary"):
            if not text_input.strip():
                st.error("Please enter some text to evaluate.")
            else:
                try:
                    with st.spinner("Analyzing text for hallucinations..."):
                        meter = HallucinationMeter(
                            llm_provider=llm_provider,
                            retrieval_method=retrieval_method,
                            use_llm_verification=use_llm_verification
                        )
                        result = meter.evaluate(text_input)
                    
                    # Display results
                    display_results(result)
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Make sure you have set your API keys in the sidebar.")
    
    with tab2:
        st.header("Query & Evaluate")
        st.markdown("Ask a question and evaluate the AI's answer for truthfulness.")
        
        query = st.text_input(
            "Your Question",
            placeholder="Example: Did Beethoven meet Mozart?"
        )
        
        if st.button("🤖 Generate & Evaluate", type="primary"):
            if not query.strip():
                st.error("Please enter a question.")
            else:
                try:
                    with st.spinner("Generating answer and checking for hallucinations..."):
                        meter = HallucinationMeter(
                            llm_provider=llm_provider,
                            retrieval_method=retrieval_method,
                            use_llm_verification=use_llm_verification
                        )
                        result = meter.evaluate_query(query)
                    
                    # Display query and answer
                    st.subheader("📤 Query")
                    st.write(query)
                    
                    st.subheader("🤖 Generated Answer")
                    st.write(result.get("answer", ""))
                    
                    st.markdown("---")
                    
                    # Display evaluation results
                    display_results(result)
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Make sure you have set your API keys in the sidebar.")


def display_results(result: dict):
    """Display evaluation results in a nice format."""
    # Overall score
    score = result.get("percentage_score", 0.0)
    verdict = result.get("verdict", "unknown")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Truthfulness Score",
            f"{score:.1f}%",
            delta=None
        )
    
    with col2:
        verdict_display = format_verdict(verdict)
        st.markdown(f"**Verdict:** {verdict_display}")
    
    with col3:
        total_claims = result.get("total_claims", 0)
        st.metric("Claims Analyzed", total_claims)
    
    st.markdown("---")
    
    # Detailed claim results
    claim_results = result.get("claim_results", [])
    
    if claim_results:
        st.subheader("📋 Claim-by-Claim Analysis")
        
        for i, claim_result in enumerate(claim_results, 1):
            with st.expander(f"Claim {i}: {claim_result.get('claim', '')[:100]}..."):
                col1, col2 = st.columns(2)
                
                with col1:
                    claim_score = claim_result.get("score", 0.0) * 100
                    st.metric("Score", f"{claim_score:.1f}%")
                    st.markdown(f"**Verdict:** {format_verdict(claim_result.get('verdict', ''))}")
                
                with col2:
                    st.markdown(f"**Context:** {claim_result.get('context', 'N/A')}")
                
                reasoning = claim_result.get("reasoning", "")
                if reasoning:
                    st.markdown(f"**Reasoning:** {reasoning}")
    else:
        st.info("No claims were extracted from the text.")
    
    # Show original text if available
    if "original_text" in result:
        with st.expander("📄 Original Text"):
            st.text(result["original_text"])


if __name__ == "__main__":
    main()

