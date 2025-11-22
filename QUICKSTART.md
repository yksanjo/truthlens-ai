# 🚀 Quick Start Guide

Get the AI Hallucination Meter running in 5 minutes!

## Step 1: Install Dependencies

```bash
cd ai-hallucination-meter
pip install -r requirements.txt
```

## Step 2: Set API Key

Choose one:

**Option A: Environment variable**
```bash
export OPENAI_API_KEY="your-key-here"
```

**Option B: Create .env file**
```bash
cp .env.example .env
# Then edit .env and add your API key
```

## Step 3: Run the App

**Streamlit UI (Recommended):**
```bash
streamlit run app/ui.py
```

Or use the quick script:
```bash
./run_streamlit.sh
```

**FastAPI Server:**
```bash
python app/api.py
```

Or:
```bash
./run_api.sh
```

## Step 4: Test It!

1. Open the Streamlit UI (usually at http://localhost:8501)
2. Go to "Evaluate Text" tab
3. Paste: "Beethoven met Mozart in Vienna in 1787."
4. Click "Evaluate"
5. See the truthfulness score! 🎉

## Example API Call

```bash
curl -X POST "http://localhost:8000/check" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The capital of France is Paris.",
    "llm_provider": "openai",
    "retrieval_method": "wikipedia"
  }'
```

## Troubleshooting

**"No API key found"**
- Make sure you've set OPENAI_API_KEY or ANTHROPIC_API_KEY
- Check that .env file is in the project root

**"Module not found"**
- Make sure you're in the project directory
- Run `pip install -r requirements.txt` again

**Wikipedia rate limiting**
- This is normal - Wikipedia has rate limits
- Wait a few seconds between requests

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Try the test script: `python test_example.py`
- Check out the API docs at http://localhost:8000/docs

Happy fact-checking! 🔍

