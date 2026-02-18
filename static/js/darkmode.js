// Enhanced Dark Mode Toggle with smooth transitions
document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const htmlElement = document.documentElement;

    if (!darkModeToggle) return;

    // Check for saved dark mode preference or default to off
    const isDarkMode = localStorage.getItem('darkMode') === 'true';

    // Set initial dark mode state
    if (isDarkMode) {
        htmlElement.setAttribute('data-theme', 'dark');
        updateToggleIcon();
    }

    // Toggle dark mode on button click with animation
    darkModeToggle.addEventListener('click', () => {
        // Add click animation
        darkModeToggle.style.transform = 'scale(0.9)';
        setTimeout(() => {
            darkModeToggle.style.transform = 'scale(1)';
        }, 150);
        
        const currentTheme = htmlElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        // Smooth transition
        htmlElement.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        htmlElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('darkMode', newTheme === 'dark');
        updateToggleIcon();
        
        // Remove transition after animation
        setTimeout(() => {
            htmlElement.style.transition = '';
        }, 300);
    });

    function updateToggleIcon() {
        const icon = darkModeToggle.querySelector('.toggle-icon');
        if (!icon) return;
        const isDark = htmlElement.getAttribute('data-theme') === 'dark';
        icon.textContent = isDark ? '☀️' : '🌙';
        icon.style.transition = 'transform 0.3s ease';
        icon.style.transform = 'rotate(360deg)';
        setTimeout(() => {
            icon.style.transform = 'rotate(0deg)';
        }, 300);
    }
    
    // Add hover effect
    darkModeToggle.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1)';
    });
    
    darkModeToggle.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
});
