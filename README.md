# ConfAdvisor

## Running the web application

Install dependencies and start the server:

```bash
pip install flask qdrant-client openai markdown
python webapp.py
```

The application connects to a local Qdrant instance and requires `key.txt` with an OpenAI API key.
Results on the search page are fetched via JavaScript from `/api/search`.
Templates live in the `templates/` directory and client scripts in `static/`.

## Preparing visualization data

Generate a file with 2‑D coordinates for all paper embeddings:

```bash
pip install scikit-learn
python prepare_viz.py
```

The resulting `viz_data.json` is used by the visualization tab in the web interface.
