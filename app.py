import json

import streamlit as st
from google import genai

MODEL = "gemini-flash-latest"

st.set_page_config(page_title="AI Jargon Decoder", page_icon="🧩")
st.title("AI Jargon Decoder")
st.caption("Paste any AI buzzword. Get back what kind of thing it actually is.")

api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("No API key found. Add GEMINI_API_KEY in this app's Secrets settings.")
    st.stop()

client = genai.Client(api_key=api_key)

PROMPT = """You are explaining the AI ecosystem to a smart professional who is not an engineer.

First, decide whether the input below is a real, recognizable AI/tech term, product,
company, or concept — even a somewhat obscure one is fine. If it is gibberish,
random characters, a typo with no plausible match, or unrelated to AI/tech, it is NOT valid.

If it is NOT valid, return ONLY this JSON:
  {{"is_valid_term": false, "term": "<what they typed>"}}

If it IS valid, classify it into exactly ONE of these categories:
- Model — the brain itself, trained weights that generate output
- Concept or technique — a design pattern or method, not a product
- Framework or library — code developers import to build with
- Platform or SaaS — a product you log into
- Tool or specialist service — a narrow API that does one job well
- Protocol or standard — invisible wiring that lets things talk to each other

Then explain it. No hype, no marketing language. Assume the reader is intelligent
but has never written AI code.

Return ONLY valid JSON. No markdown fences, no commentary before or after.
Use exactly these keys:
  term (string)
  category (string, one of the six above)
  plain_english (string, 2 sentences)
  analogy (string, 1 sentence, from everyday life)
  why_it_matters (string, 2 sentences)
  related_terms (list of exactly 3 strings)
  common_misconception (string)

Term: {term}"""

term = st.text_input(
    "Term",
    placeholder="e.g. RAG, LangGraph, MCP, Mistral, Pinecone, fine-tuning",
)

if st.button("Decode", type="primary") and term.strip():
    with st.spinner("Thinking..."):
        response = client.models.generate_content(
            model=MODEL,
            contents=PROMPT.format(term=term.strip()),
        )
        raw = response.text.strip()

    cleaned = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        st.warning("The model didn't return clean JSON this time. Raw output below.")
        st.code(raw)
    else:
        if not data.get("is_valid_term", True):
            st.error(f"'{data.get('term', term)}' doesn't look like a real AI/tech term. Try something like RAG, MCP, or LangChain.")
        else:
            st.subheader(data["term"])
            st.markdown(f"**Category — {data['category']}**")
            st.write(data["plain_english"])
            st.info(data["analogy"])
            st.markdown("**Why it matters**")
            st.write(data["why_it_matters"])
            st.markdown("**Related terms:** " + ", ".join(data["related_terms"]))
            st.write(data["common_misconception"])

    with st.expander("See the raw model output"):
        st.code(raw)
