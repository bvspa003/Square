/**
 * Square Transport Website - GSAP Animations
 * High-performance animations with Swedish design aesthetics
 */

class SquareAnimations {
    constructor() {
        this.initGSAP();
        this.setupAnimations();
    }
    
    initGSAP() {
        // Register GSAP plugins
        if (typeof gsap !== 'undefined') {
            gsap.registerPlugin(ScrollTrigger);
            
            // Set animation defaults for consistency
            gsap.defaults({
                duration: 0.6,
                ease: "power2.out"
            });
            
            console.log('🎬 GSAP animations initialized');
        } else {
            console.warn('GSAP not loaded - falling back to CSS animations');
            return;
        }
    }
    
    setupAnimations() {
        if (typeof gsap === 'undefined') return;
        
        this.animateHero();
        this.animateScrollElements();
        this.animateStats();
        this.animateCards();
        this.setupPageTransitions();
        this.setupHoverAnimations();
    }
    
    animateHero() {
        const hero = document.querySelector('.hero--landing');
        if (!hero) return;
        
        const tl = gsap.timeline();
        
        // Animate hero content on load
        tl.from('.hero__title--landing', {
            y: 60,
            opacity: 0,
            duration: 1,
            ease: "power3.out"
        })
        .from('.hero__subtitle--landing', {
            y: 40,
            opacity: 0,
            duration: 0.8,
            ease: "power3.out"
        }, "-=0.6")
        .from('.hero__buttons--landing .btn', {
            y: 30,
            opacity: 0,
            duration: 0.6,
            stagger: 0.2,
            ease: "back.out(1.7)"
        }, "-=0.4")
        .from('.hero__stat--landing', {
            y: 30,
            opacity: 0,
            scale: 0.8,
            duration: 0.6,
            stagger: 0.15,
            ease: "back.out(1.7)"
        }, "-=0.2");
        
        // Floating animation for hero stats
        gsap.to('.hero__stat--landing', {
            y: -10,
            duration: 2,
            ease: "sine.inOut",
            yoyo: true,
            repeat: -1,
            stagger: 0.3
        });
    }
    
    animateScrollElements() {
        // Problem section animation
        this.animateSection('.problem-section', {
            '.problem__title': { y: 50, opacity: 0 },
            '.problem__description': { y: 30, opacity: 0 },
            '.problem__highlight': { y: 40, opacity: 0, scale: 0.9 }
        });
        
        // Solution section animation
        this.animateSection('.solution-section', {
            '.solution__title': { x: -50, opacity: 0 },
            '.solution__description': { x: -30, opacity: 0 },
            '.solution__feature': { x: -20, opacity: 0 },
            '.solution__visual': { x: 50, opacity: 0, scale: 0.95 }
        });
        
        // Benefits section animation
        this.animateSection('.benefits-section', {
            '.benefits__title': { y: 50, opacity: 0 },
            '.benefit': { y: 60, opacity: 0, scale: 0.9 }
        });
    }
    
    animateSection(sectionSelector, animations) {
        const section = document.querySelector(sectionSelector);
        if (!section) return;
        
        Object.entries(animations).forEach(([selector, fromProps]) => {
            const elements = section.querySelectorAll(selector);
            if (elements.length === 0) return;
            
            gsap.fromTo(elements, fromProps, {
                y: 0,
                x: 0,
                opacity: 1,
                scale: 1,
                duration: 0.8,
                stagger: 0.2,
                ease: "power3.out",
                scrollTrigger: {
                    trigger: elements[0],
                    start: "top 80%",
                    end: "bottom 20%",
                    toggleActions: "play none none reverse"
                }
            });
        });
    }
    
    animateStats() {
        const stats = document.querySelectorAll('.stat__number, .hero__stat-number--landing, .benefit__number');
        
        stats.forEach(stat => {
            const endValue = stat.textContent;
            
            // Handle different stat formats
            if (endValue.includes('%')) {
                // Percentage values like "70%", "90%"
                const numericValue = parseInt(endValue.replace('%', ''));
                if (isNaN(numericValue)) return;
                
                gsap.fromTo(stat, 
                    { textContent: 0 },
                    {
                        textContent: numericValue,
                        duration: 2,
                        ease: "power2.out",
                        snap: { textContent: 1 },
                        delay: 0.5, // Start after page loads
                        onUpdate: function() {
                            const currentValue = Math.round(this.targets()[0].textContent);
                            stat.textContent = currentValue + '%';
                        }
                    }
                );
            } else if (endValue.includes('$')) {
                // Currency values like "$500M"
                const numericPart = endValue.replace(/[^0-9]/g, '');
                const numericValue = parseInt(numericPart);
                
                if (isNaN(numericValue)) return;
                
                gsap.fromTo(stat, 
                    { textContent: 0 },
                    {
                        textContent: numericValue,
                        duration: 2,
                        ease: "power2.out",
                        snap: { textContent: 1 },
                        delay: 0.7, // Stagger the start times
                        onUpdate: function() {
                            const currentValue = Math.round(this.targets()[0].textContent);
                            stat.textContent = '$' + currentValue + 'M';
                        }
                    }
                );
            } else {
                // Regular numeric values
                const numericValue = parseInt(endValue.replace(/[^0-9]/g, ''));
                if (isNaN(numericValue)) return;
                
                gsap.fromTo(stat, 
                    { textContent: 0 },
                    {
                        textContent: numericValue,
                        duration: 2,
                        ease: "power2.out",
                        snap: { textContent: 1 },
                        delay: 0.3
                    }
                );
            }
        });
    }
    
    animateCards() {
        const cards = document.querySelectorAll('.card, .benefit, .achievement, .team-member, .spec-card');
        
        cards.forEach(card => {
            // Entrance animation
            gsap.fromTo(card, 
                { y: 40, opacity: 0, scale: 0.95 },
                {
                    y: 0,
                    opacity: 1,
                    scale: 1,
                    duration: 0.6,
                    ease: "back.out(1.7)",
                    scrollTrigger: {
                        trigger: card,
                        start: "top 85%",
                        toggleActions: "play none none reverse"
                    }
                }
            );
            
            // Hover animations
            card.addEventListener('mouseenter', () => {
                gsap.to(card, {
                    y: -8,
                    scale: 1.02,
                    duration: 0.3,
                    ease: "power2.out"
                });
            });
            
            card.addEventListener('mouseleave', () => {
                gsap.to(card, {
                    y: 0,
                    scale: 1,
                    duration: 0.3,
                    ease: "power2.out"
                });
            });
        });
    }
    
    setupPageTransitions() {
        // Page transition animation
        const links = document.querySelectorAll('a[href^="/"]');
        
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                if (link.hostname !== window.location.hostname) return;
                
                e.preventDefault();
                
                // Fade out current page
                gsap.to('main', {
                    opacity: 0,
                    scale: 0.95,
                    duration: 0.4,
                    ease: "power2.in",
                    onComplete: () => {
                        window.location.href = link.href;
                    }
                });
            });
        });
        
        // Fade in on page load
        gsap.fromTo('main', 
            { opacity: 0, scale: 0.95 },
            { 
                opacity: 1, 
                scale: 1, 
                duration: 0.6, 
                ease: "power2.out",
                delay: 0.1
            }
        );
    }
    
    setupHoverAnimations() {
        // Button hover animations
        const buttons = document.querySelectorAll('.btn');
        
        buttons.forEach(btn => {
            btn.addEventListener('mouseenter', () => {
                gsap.to(btn, {
                    scale: 1.05,
                    duration: 0.2,
                    ease: "power2.out"
                });
                
                // Special animation for CTA buttons
                if (btn.classList.contains('btn--cta')) {
                    gsap.to(btn, {
                        boxShadow: "0 20px 40px rgba(30, 64, 175, 0.3)",
                        duration: 0.3
                    });
                }
            });
            
            btn.addEventListener('mouseleave', () => {
                gsap.to(btn, {
                    scale: 1,
                    boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
                    duration: 0.2,
                    ease: "power2.out"
                });
            });
        });
        
        // Navigation link animations
        const navLinks = document.querySelectorAll('.nav__link');
        
        navLinks.forEach(link => {
            link.addEventListener('mouseenter', () => {
                gsap.to(link, {
                    scale: 1.05,
                    duration: 0.2,
                    ease: "power2.out"
                });
            });
            
            link.addEventListener('mouseleave', () => {
                gsap.to(link, {
                    scale: 1,
                    duration: 0.2,
                    ease: "power2.out"
                });
            });
        });
    }
    
    // Utility methods for specific animations
    pulseElement(element, options = {}) {
        const defaults = {
            scale: 1.1,
            duration: 1,
            repeat: -1,
            yoyo: true,
            ease: "power2.inOut"
        };
        
        gsap.to(element, { ...defaults, ...options });
    }
    
    floatElement(element, options = {}) {
        const defaults = {
            y: -15,
            duration: 2,
            repeat: -1,
            yoyo: true,
            ease: "sine.inOut"
        };
        
        gsap.to(element, { ...defaults, ...options });
    }
    
    slideInElement(element, direction = 'up', options = {}) {
        const directions = {
            up: { y: 50 },
            down: { y: -50 },
            left: { x: -50 },
            right: { x: 50 }
        };
        
        const defaults = {
            duration: 0.8,
            ease: "power3.out",
            ...directions[direction],
            opacity: 0
        };
        
        gsap.fromTo(element, defaults, {
            x: 0,
            y: 0,
            opacity: 1,
            duration: defaults.duration,
            ease: defaults.ease,
            ...options
        });
    }
    
    // Method to create staggered animations
    staggerAnimation(elements, animation, staggerAmount = 0.2) {
        gsap.fromTo(elements, animation.from, {
            ...animation.to,
            stagger: staggerAmount
        });
    }
    
    // Method to create timeline animations
    createTimeline(animations, options = {}) {
        const tl = gsap.timeline(options);
        
        animations.forEach(anim => {
            if (anim.method === 'to') {
                tl.to(anim.target, anim.vars, anim.position);
            } else if (anim.method === 'from') {
                tl.from(anim.target, anim.vars, anim.position);
            } else if (anim.method === 'fromTo') {
                tl.fromTo(anim.target, anim.from, anim.to, anim.position);
            }
        });
        
        return tl;
    }
    
    // Performance optimization - pause animations when tab is not visible
    setupPerformanceOptimizations() {
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                gsap.globalTimeline.pause();
            } else {
                gsap.globalTimeline.resume();
            }
        });
    }
    
    // Accessibility - respect prefers-reduced-motion
    setupAccessibility() {
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        
        if (prefersReducedMotion.matches) {
            // Disable all animations
            gsap.set("*", { duration: 0.01 });
            ScrollTrigger.config({ limitCallbacks: true });
        }
        
        // Listen for changes
        prefersReducedMotion.addEventListener('change', () => {
            if (prefersReducedMotion.matches) {
                gsap.set("*", { duration: 0.01 });
            } else {
                gsap.set("*", { duration: 0.6 });
            }
        });
    }
    
    // Clean up method
    destroy() {
        ScrollTrigger.getAll().forEach(trigger => trigger.kill());
        gsap.killTweensOf("*");
    }
}

// Initialize animations when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const squareAnimations = new SquareAnimations();
    squareAnimations.setupPerformanceOptimizations();
    squareAnimations.setupAccessibility();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SquareAnimations;
}
