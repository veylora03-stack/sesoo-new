document.addEventListener("DOMContentLoaded", function() {
    const menuToggle = document.querySelector('[data-menu-toggle]');
    const siteNav = document.querySelector('[data-menu]');
    if (menuToggle && siteNav) {
        menuToggle.addEventListener('click', function() {
            const isOpen = siteNav.classList.toggle('is-open');
            menuToggle.setAttribute('aria-expanded', isOpen);
        });
        const menuLinks = siteNav.querySelectorAll('a');
        menuLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (siteNav.classList.contains('is-open')) {
                    siteNav.classList.remove('is-open');
                    menuToggle.setAttribute('aria-expanded', 'false');
                }
            });
        });
    }
});