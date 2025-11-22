"""
Main entry point for the AI Hallucination Meter.
Run this to start the Streamlit UI.
"""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import streamlit.web.cli as stcli
    
    # Run Streamlit
    sys.argv = ["streamlit", "run", "app/ui.py"]
    sys.exit(stcli.main())

