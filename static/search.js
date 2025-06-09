document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('searchForm');
  const results = document.getElementById('results');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const q = document.getElementById('query').value;
    results.innerHTML = '';
    if (!q.trim()) return;
    const resp = await fetch('/api/search?q=' + encodeURIComponent(q));
    const data = await resp.json();
    data.forEach(paper => {
      const card = document.createElement('div');
      card.className = 'card mb-3';
      const body = document.createElement('div');
      body.className = 'card-body';
      Object.entries(paper).forEach(([k, v]) => {
        const p = document.createElement('p');
        p.innerHTML = `<strong>${k}:</strong> ${v}`;
        body.appendChild(p);
      });
      card.appendChild(body);
      results.appendChild(card);
    });
  });
});
