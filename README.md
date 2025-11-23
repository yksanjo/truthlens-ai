# 🔍 TruthLens AI

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) [![GitHub stars](https://img.shields.io/github/stars/yksanjo/truthlens-ai?style=social)](https://github.com/yksanjo/truthlens-ai/stargazers) [![GitHub forks](https://img.shields.io/github/forks/yksanjo/truthlens-ai.svg)](https://github.com/yksanjo/truthlens-ai/network/members) [![GitHub issues](https://img.shields.io/github/issues/yksanjo/truthlens-ai.svg)](https://github.com/yksanjo/truthlens-ai/issues)
[![Last commit](https://img.shields.io/github/last-commit/yksanjo/truthlens-ai.svg)](https://github.com/yksanjo/truthlens-ai/commits/main)


**Real-Time Truthfulness Score for LLM Output**

A hackathon-ready tool that evaluates LLM (Large Language Model) outputs for hallucinations by checking claims against external evidence sources. Built for measuring how "responsible" AI models are.

## ✨ Features

- **Real-Time Evaluation**: Check any LLM output for factual accuracy
- **Claim Extraction**: Automatically identifies verifiable claims from text
- **Evidence Retrieval**: Fetches evidence from Wikipedia and other sources
- **Truthfulness Scoring**: Provides a 0-100% truthfulness score
- **Multiple LLM Support**: Works with OpenAI and Anthropic models
- **Beautiful UI**: Streamlit-based web interface
- **API Endpoint**: FastAPI backend for Chrome extension integration

> **TruthLens AI** - See through the hallucinations. Verify the truth.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key OR Anthropic API key

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd ai-hallucination-meter
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys:**
   
   Option A: Environment variables
   ```bash
   export OPENAI_API_KEY="your-key-here"
   # OR
   export ANTHROPIC_API_KEY="your-key-here"
   ```
   
   Option B: Create a `.env` file
   ```
   OPENAI_API_KEY=your-key-here
   ANTHROPIC_API_KEY=your-key-here
   ```

### Running the Application

#### Option 1: Streamlit UI (Recommended for demos)

```bash
streamlit run app/ui.py
```

Then open your browser to `http://localhost:8501`

#### Option 2: FastAPI Server (For API/Chrome extension)

```bash
python app/api.py
```

Or with uvicorn:
```bash
uvicorn app.api:app --reload
```

API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## 📖 Usage

### Using the Streamlit UI

1. **Evaluate Existing Text:**
   - Paste any LLM output in the text area
   - Click "Evaluate"
   - View truthfulness score and claim-by-claim analysis

2. **Query & Evaluate:**
   - Enter a question
   - Click "Generate & Evaluate"
   - See the generated answer and its truthfulness score

### Using the API

#### Evaluate Text

```bash
curl -X POST "http://localhost:8000/check" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Beethoven met Mozart in Vienna in 1787.",
    "llm_provider": "openai",
    "retrieval_method": "wikipedia",
    "use_llm_verification": true
  }'
```

#### Query & Evaluate

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Did Beethoven meet Mozart?",
    "llm_provider": "openai",
    "retrieval_method": "wikipedia"
  }'
```

### Using as a Python Library

```python
from core.hallucination_meter import HallucinationMeter

# Initialize
meter = HallucinationMeter(
    llm_provider="openai",
    retrieval_method="wikipedia",
    use_llm_verification=True
)

# Evaluate text
result = meter.evaluate("Beethoven met Mozart in Vienna in 1787.")
print(f"Truthfulness Score: {result['percentage_score']:.1f}%")
print(f"Verdict: {result['verdict']}")

# Or query and evaluate
result = meter.evaluate_query("Did Beethoven meet Mozart?")
print(f"Answer: {result['answer']}")
print(f"Score: {result['percentage_score']:.1f}%")
```

## 🏗️ Architecture

```
User Input → LLM Output → Claim Extractor → Evidence Retriever → 
Evaluator → Truthfulness Score → UI/API
```

### Components

- **LLMWrapper**: Handles OpenAI and Anthropic API calls
- **ClaimExtractor**: Extracts atomic factual claims from text
- **EvidenceRetriever**: Fetches evidence from Wikipedia/web/vector DB
- **TruthfulnessEvaluator**: Compares claims against evidence
- **HallucinationMeter**: Main orchestrator combining all components

## 🎯 How It Works

1. **Claim Extraction**: Uses LLM to identify verifiable factual claims
2. **Evidence Retrieval**: Searches Wikipedia (or other sources) for relevant information
3. **Comparison**: Uses embedding similarity or LLM verification to compare claims vs evidence
4. **Scoring**: Aggregates individual claim scores into overall truthfulness score
5. **Visualization**: Displays results with color-coded verdicts and detailed breakdowns

## 📊 Scoring System

- **75-100%**: ✅ Highly Truthful
- **55-74%**: ⚠️ Mostly Truthful
- **35-54%**: ❓ Uncertain
- **0-34%**: ❌ Likely Hallucination

## 🔧 Configuration

### LLM Providers
- `openai`: Uses GPT-4o-mini (cost-effective)
- `anthropic`: Uses Claude 3 Haiku (fast)

### Retrieval Methods
- `wikipedia`: Wikipedia API (default, no API key needed)
- `web`: Web search (requires search API)
- `vector`: Vector database search (requires setup)

### Verification Methods
- **LLM Verification**: More accurate, uses LLM to verify claims
- **Embedding Similarity**: Faster, uses cosine similarity of embeddings

## 🎨 Chrome Extension (Future)

The API is designed to support a Chrome extension that can:
- Highlight AI output on any webpage
- Right-click → "Check Hallucinations"
- Show truthfulness score in a popup

## 📝 Example Output

```
Truthfulness Score: 42.0%
Verdict: ❌ Likely Hallucination

Claims Analyzed: 3

Claim-by-Claim Analysis:
  Claim 1: Beethoven met Mozart in Vienna
    Score: 85.0%
    Verdict: ✅ Supported
    
  Claim 2: The meeting occurred in 1787
    Score: 15.0%
    Verdict: ❌ Contradicted
    Reasoning: Evidence suggests 1787 is uncertain
    
  Claim 3: They became close friends
    Score: 25.0%
    Verdict: ❓ Uncertain
```

## 🛠️ Development

### Project Structure

```
ai-hallucination-meter/
├── core/
│   ├── llm.py              # LLM wrapper
│   ├── retrieval.py        # Evidence retrieval
│   ├── fact_extract.py     # Claim extraction
│   ├── evaluator.py        # Truthfulness evaluation
│   ├── hallucination_meter.py  # Main orchestrator
│   └── utils.py            # Utilities
├── app/
│   ├── ui.py               # Streamlit UI
│   └── api.py              # FastAPI endpoint
├── data/
│   └── sample_queries.json # Sample queries
├── requirements.txt
└── README.md
```

### Adding New Retrieval Methods

Extend `EvidenceRetriever` in `core/retrieval.py`:

```python
def _retrieve_custom(self, claim: str, top_k: int):
    # Your custom retrieval logic
    return evidence_list
```

### Adding New Evaluation Methods

Extend `TruthfulnessEvaluator` in `core/evaluator.py`:

```python
def _evaluate_custom(self, claim: str, evidence: List[Dict]):
    # Your custom evaluation logic
    return result
```

## 🤝 Contributing

This is a hackathon project! Feel free to:
- Add more retrieval sources
- Improve claim extraction
- Add bias detection
- Create Chrome extension
- Add more evaluation metrics

## 📄 License

MIT License - feel free to use for hackathons and projects!

## 🙏 Acknowledgments

Built for TREA-AI / Responsible AI hackathons. Inspired by:
- EleutherAI Evals
- TruthfulQA benchmarks
- Model evaluation frameworks

## 🐛 Known Limitations

- Wikipedia retrieval may be rate-limited
- Claim extraction depends on LLM quality
- Scoring is heuristic-based
- No real-time fact-checking database integration

## 🚀 Future Enhancements

- [ ] Vector database integration (FAISS/Pinecone)
- [ ] Real-time web search (Google/Bing API)
- [ ] Chrome extension
- [ ] Batch evaluation
- [ ] Custom fact-checking databases
- [ ] Bias detection
- [ ] Citation accuracy checking

---

**Built with ❤️ for Responsible AI**

