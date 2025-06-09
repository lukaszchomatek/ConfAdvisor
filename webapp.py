from flask import Flask, request, jsonify, render_template
import markdown
import json
from paper_search import (
    search_by_embedding,
    list_all_papers,
    list_all_keywords,
    search_by_keywords,
)

app = Flask(__name__)

@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    if query:
        papers = [payload for _, payload in search_by_embedding(query, limit=50)]
    else:
        papers = list_all_papers()
    return render_template("index.html", papers=papers, query=query, active="search")

@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").strip()
    if query:
        papers = [payload for _, payload in search_by_embedding(query, limit=50)]
    else:
        papers = list_all_papers()
    return jsonify(papers)

@app.route("/summary")
def summary():
    try:
        with open("papers_summary.txt", "r", encoding="utf-8") as f:
            content = markdown.markdown(f.read())
    except FileNotFoundError:
        content = "Summary file not found."
    return render_template("summary.html", summary=content, active="summary")

@app.route("/similar")
def similar():
    try:
        with open("viz_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    return render_template("similar.html", data=json.dumps(data), active="similar")

@app.route("/affiliations")
def affiliations():
    query = request.args.get("q", "").strip().lower()
    try:
        with open("affiliations.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    if query:
        data = {k: v for k, v in data.items() if query in k.lower()}
    return render_template("affiliations.html", data=data, query=query, active="affiliations")

@app.route("/authors")
def authors():
    query = request.args.get("q", "").strip().lower()
    try:
        with open("authors.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    if query:
        data = {k: v for k, v in data.items() if query in k.lower()}
    return render_template("authors.html", data=data, query=query, active="authors")


@app.route("/keywords")
def keywords_page():
    selected = request.args.getlist("kw")
    mode = request.args.get("mode", "AND").upper()
    keywords = list_all_keywords()
    papers = search_by_keywords(selected, mode, limit=50) if selected else []
    return render_template(
        "keywords.html",
        keywords=keywords,
        papers=papers,
        selected=selected,
        mode=mode,
        active="keywords",
    )


@app.route("/api/keywords")
def api_keywords():
    selected = request.args.getlist("kw")
    mode = request.args.get("mode", "AND").upper()
    papers = search_by_keywords(selected, mode, limit=50) if selected else []
    return jsonify(papers)

if __name__ == "__main__":
    app.run(debug=True)
