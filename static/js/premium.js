document.addEventListener("DOMContentLoaded", function() {
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!prefersReducedMotion) {
        document.documentElement.classList.add("premium-anim");
        const elements = document.querySelectorAll("[data-animate]");
        if ("IntersectionObserver" in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const delay = entry.target.getAttribute("data-delay");
                        if (delay) entry.target.style.transitionDelay = delay + "ms";
                        entry.target.classList.add("is-visible");
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });
            elements.forEach(el => observer.observe(el));
        } else { elements.forEach(el => el.classList.add("is-visible")); }
    }
    const header = document.querySelector('.site-header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 10) header.classList.add('is-scrolled');
            else header.classList.remove('is-scrolled');
        });
    }
    const scrollProgress = document.querySelector('.scroll-progress');
    if (scrollProgress && !prefersReducedMotion) {
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            if (height > 0) scrollProgress.style.width = ((winScroll / height) * 100) + "%";
        });
    }
    const backToTop = document.querySelector('.back-to-top');
    if (backToTop) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 400) backToTop.classList.add('visible');
            else backToTop.classList.remove('visible');
        });
        backToTop.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: prefersReducedMotion ? 'auto' : 'smooth' });
        });
    }
});