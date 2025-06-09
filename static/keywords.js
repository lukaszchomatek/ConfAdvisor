document.addEventListener('DOMContentLoaded', () => {
  const boxes = document.querySelectorAll('.kw-box');
  const modeSelect = document.getElementById('mode');
  const clearBtn = document.getElementById('clearKeywords');
  const results = document.getElementById('results');

  async function fetchResults() {
    const selected = Array.from(boxes)
      .filter(b => b.checked)
      .map(b => b.value);
    const params = new URLSearchParams();
    selected.forEach(kw => params.append('kw', kw));
    params.set('mode', modeSelect.value);
    if (selected.length === 0) {
      results.innerHTML = '';
      return;
    }
    const resp = await fetch('/api/keywords?' + params.toString());
    const data = await resp.json();
    results.innerHTML = '';
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
  }

  boxes.forEach(b => b.addEventListener('change', fetchResults));
  modeSelect.addEventListener('change', fetchResults);
  clearBtn.addEventListener('click', () => {
    boxes.forEach(b => { b.checked = false; });
    fetchResults();
  });
});
