document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('themeToggle');
  if (!toggle) return;
  function updateText(theme) {
    toggle.textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
  }
  let theme = document.documentElement.getAttribute('data-bs-theme') || 'light';
  updateText(theme);
  toggle.addEventListener('click', () => {
    theme = theme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem('theme', theme);
    updateText(theme);
  });
});
