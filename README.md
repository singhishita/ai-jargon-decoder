# AI Jargon Decoder

Paste an AI buzzword — get back what *category* of thing it actually is,
explained in plain English.

**Live app:** https://ai-jargon-decoder.streamlit.app

## Why I built it

The hardest part of learning the AI ecosystem isn't the technical depth — it's
that every term sounds like the same kind of thing. RAG, LangChain, Mistral and
MCP are a technique, a library, a model and a protocol, and nothing about the
names tells you that. This classifies the term first, then explains it.

## How it works

1. Streamlit takes the term from a text box
2. A prompt asks Gemini to classify it into one of six categories and return strict JSON
3. The app parses the JSON and renders it — with a fallback if the model returns something malformed

## Stack

Python · Streamlit · Google Gemini API · deployed on Streamlit Community Cloud

## Run it yourself

```
pip install -r requirements.txt
streamlit run app.py
```

Add your Gemini key to `.streamlit/secrets.toml`:

```
GEMINI_API_KEY = "your-key"
```

## What I'd do next

- Cache repeated lookups so the same term doesn't cost a second API call
- Let users compare two terms side by side
- Add a confidence signal for terms that genuinely straddle two categories
