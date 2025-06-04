from flask import Flask, request, render_template_string
from paper_search import search_by_embedding, list_all_papers

HTML_TEMPLATE = """
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

app = Flask(__name__)

@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    if query:
        papers = [payload for _, payload in search_by_embedding(query, limit=50)]
    else:
        papers = list_all_papers()
    return render_template_string(HTML_TEMPLATE, papers=papers, query=query)

if __name__ == "__main__":
    app.run(debug=True)
