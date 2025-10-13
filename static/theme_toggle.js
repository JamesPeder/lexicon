function toggleDarkMode() {
  const body = document.body;
  body.classList.toggle('dark');
  const isDark = body.classList.contains('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  document.getElementById('darkToggle').textContent = isDark ? '☀️ Light' : '🌙 Dark';
}

// Apply saved preference on load
(function () {
  const saved = localStorage.getItem('theme');
  if (saved === 'dark') {
    document.body.classList.add('dark');
    const btn = document.getElementById('darkToggle');
    if (btn) btn.textContent = '☀️ Light';
  }
})();