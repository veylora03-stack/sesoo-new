document.addEventListener("DOMContentLoaded", function() {
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (prefersReducedMotion) {
        document.documentElement.classList.remove("js-anim");
        return;
    }
    document.documentElement.classList.add("js-anim");
    const elements = document.querySelectorAll("[data-animate]");
    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });
        elements.forEach(el => observer.observe(el));
    } else {
        elements.forEach(el => el.classList.add("is-visible"));
    }
});