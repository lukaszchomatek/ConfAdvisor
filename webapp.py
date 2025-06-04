from flask import Flask, request, render_template_string
import markdown
from paper_search import search_by_embedding, list_all_papers

HTML_SEARCH = """
<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>ConfAdvisor</title>
    <link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css\">
  </head>
  <body>
    <div class=\"container py-4\">
      <h1 class=\"mb-4\">ConfAdvisor</h1>
      <ul class=\"nav nav-tabs mb-4\">
        <li class=\"nav-item\"><a class=\"nav-link active\" href=\"/\">Search</a></li>
        <li class=\"nav-item\"><a class=\"nav-link\" href=\"/summary\">Summary</a></li>
      </ul>
      <form method=\"get\" class=\"mb-4\">
        <div class=\"input-group\">
          <input type=\"text\" name=\"q\" class=\"form-control\" placeholder=\"Search\" value=\"{{ query }}\">
          <button class=\"btn btn-primary\" type=\"submit\">Search</button>
        </div>
      </form>
      {% for paper in papers %}
      <div class=\"card mb-3\">
        <div class=\"card-body\">
        {% for key, value in paper.items() %}
          <p><strong>{{ key }}:</strong> {{ value }}</p>
        {% endfor %}
        </div>
      </div>
      {% endfor %}
    </div>
  </body>
</html>
"""

HTML_SUMMARY = """
<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>ConfAdvisor - Summary</title>
    <link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css\">
  </head>
  <body>
    <div class=\"container py-4\">
      <h1 class=\"mb-4\">ConfAdvisor</h1>
      <ul class=\"nav nav-tabs mb-4\">
        <li class=\"nav-item\"><a class=\"nav-link\" href=\"/\">Search</a></li>
        <li class=\"nav-item\"><a class=\"nav-link active\" href=\"/summary\">Summary</a></li>
      </ul>
      <div class="markdown-body">{{ summary|safe }}</div>
    </div>
  </body>
</html>
"""

app = Flask(__name__)

@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    if query:
        papers = [payload for _, payload in search_by_embedding(query, limit=50)]
    else:
        papers = list_all_papers()
    return render_template_string(HTML_SEARCH, papers=papers, query=query)


@app.route("/summary")
def summary():
    try:
        with open("papers_summary.txt", "r", encoding="utf-8") as f:
            content = markdown.markdown(f.read())
    except FileNotFoundError:
        content = "Summary file not found."
    return render_template_string(HTML_SUMMARY, summary=content)

if __name__ == "__main__":
    app.run(debug=True)
