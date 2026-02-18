// Dark Mode Toggle
const darkModeToggle = document.getElementById('darkModeToggle');
const htmlElement = document.documentElement;

// Check for saved dark mode preference or default to off
const isDarkMode = localStorage.getItem('darkMode') === 'true';

// Set initial dark mode state
if (isDarkMode) {
    htmlElement.setAttribute('data-theme', 'dark');
    updateToggleIcon();
}

// Toggle dark mode on button click
darkModeToggle.addEventListener('click', () => {
    const currentTheme = htmlElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    htmlElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('darkMode', newTheme === 'dark');
    updateToggleIcon();
});

function updateToggleIcon() {
    const icon = darkModeToggle.querySelector('.toggle-icon');
    const isDark = htmlElement.getAttribute('data-theme') === 'dark';
    icon.textContent = isDark ? '☀️' : '🌙';
}
