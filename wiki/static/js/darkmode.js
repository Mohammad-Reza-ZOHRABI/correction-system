// Dark Mode Toggle - Persistent across all pages
(function() {
    'use strict';

    // Initialize dark mode from localStorage or system preference
    function initDarkMode() {
        const darkMode = localStorage.getItem('darkMode');
        if (darkMode === 'true' ||
            (darkMode === null && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        }
    }

    // Toggle dark mode
    function toggleDarkMode() {
        const html = document.documentElement;
        const isDark = html.classList.toggle('dark');
        localStorage.setItem('darkMode', isDark);

        // Update button icon
        updateDarkModeButton(isDark);
    }

    // Update button icon based on current mode
    function updateDarkModeButton(isDark) {
        const sunIcon = document.getElementById('sun-icon');
        const moonIcon = document.getElementById('moon-icon');

        if (sunIcon && moonIcon) {
            if (isDark) {
                sunIcon.classList.remove('hidden');
                moonIcon.classList.add('hidden');
            } else {
                sunIcon.classList.add('hidden');
                moonIcon.classList.remove('hidden');
            }
        }
    }

    // Initialize on page load
    initDarkMode();

    // Setup toggle button when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        const darkModeToggle = document.getElementById('dark-mode-toggle');
        if (darkModeToggle) {
            darkModeToggle.addEventListener('click', toggleDarkMode);

            // Set initial icon state
            const isDark = document.documentElement.classList.contains('dark');
            updateDarkModeButton(isDark);
        }
    });
})();