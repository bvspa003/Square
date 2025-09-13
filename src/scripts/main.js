/**
 * Square Transport Website - Main JavaScript
 * Handles navigation, interactions, and core functionality
 * Swedish design principles with accessibility focus
 */

class SquareWebsite {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupNavigation();
        this.setupScrollEffects();
        this.setupContactForm();
        this.setupSmoothScrolling();
        this.loadCompanyData();
        this.setupCounterAnimations();
        
        // Initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.onDOMReady();
            });
        } else {
            this.onDOMReady();
        }
    }
    
    onDOMReady() {
        console.log('🚀 Square Transport Website initialized');
        this.setupScrollReveal();
        this.setupPerformanceOptimizations();
    }
    
    setupNavigation() {
        const navToggle = document.getElementById('nav-toggle');
        const navMobile = document.getElementById('nav-mobile');
        const nav = document.getElementById('main-nav');
        
        if (navToggle && navMobile) {
            navToggle.addEventListener('click', () => {
                const isOpen = navToggle.classList.toggle('nav__toggle--active');
                navMobile.classList.toggle('nav__menu--open');
                navToggle.setAttribute('aria-expanded', isOpen);
                
                // Prevent body scroll when menu is open
                document.body.style.overflow = isOpen ? 'hidden' : '';
            });
            
            // Close mobile menu when clicking on links
            navMobile.querySelectorAll('a').forEach(link => {
                link.addEventListener('click', () => {
                    navToggle.classList.remove('nav__toggle--active');
                    navMobile.classList.remove('nav__menu--open');
                    navToggle.setAttribute('aria-expanded', 'false');
                    document.body.style.overflow = '';
                });
            });
        }
        
        // Navigation scroll effect
        if (nav) {
            const handleScroll = () => {
                if (window.scrollY > 100) {
                    nav.classList.add('nav--scrolled');
                } else {
                    nav.classList.remove('nav--scrolled');
                }
            };
            
            window.addEventListener('scroll', this.throttle(handleScroll, 100));
        }
        
        // Active navigation highlighting
        this.updateActiveNavigation();
    }
    
    updateActiveNavigation() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav__link');
        
        navLinks.forEach(link => {
            link.classList.remove('nav__link--active');
            link.removeAttribute('aria-current');
            
            const linkPath = new URL(link.href).pathname;
            if (linkPath === currentPath || (currentPath === '/' && linkPath === '/')) {
                link.classList.add('nav__link--active');
                link.setAttribute('aria-current', 'page');
            }
        });
    }
    
    setupScrollEffects() {
        // Parallax effect for hero background
        const hero = document.getElementById('hero');
        if (hero) {
            const handleParallax = () => {
                const scrolled = window.scrollY;
                const heroHeight = hero.offsetHeight;
                const rate = scrolled * -0.5;
                
                if (scrolled < heroHeight) {
                    hero.style.transform = `translateY(${rate}px)`;
                }
            };
            
            window.addEventListener('scroll', this.throttle(handleParallax, 16));
        }
    }
    
    setupScrollReveal() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('scroll-reveal--visible');
                    
                    // Add stagger delay for multiple elements
                    const staggerDelay = entry.target.dataset.stagger || 0;
                    if (staggerDelay > 0) {
                        entry.target.style.transitionDelay = `${staggerDelay * 0.1}s`;
                    }
                }
            });
        }, observerOptions);
        
        // Observe all scroll reveal elements
        document.querySelectorAll('.scroll-reveal').forEach(el => {
            observer.observe(el);
        });
    }
    
    setupSmoothScrolling() {
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = anchor.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    const navHeight = document.getElementById('main-nav')?.offsetHeight || 0;
                    const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - navHeight;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
    
    setupContactForm() {
        const contactForms = document.querySelectorAll('form[data-contact]');
        
        contactForms.forEach(form => {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const submitButton = form.querySelector('[type="submit"]');
                const originalText = submitButton.textContent;
                
                // Show loading state
                submitButton.textContent = 'Sending...';
                submitButton.disabled = true;
                submitButton.classList.add('btn--loading');
                
                try {
                    // Simulate form submission (replace with actual endpoint)
                    await new Promise(resolve => setTimeout(resolve, 2000));
                    
                    // Show success message
                    this.showNotification('Message sent successfully! We\'ll get back to you soon.', 'success');
                    form.reset();
                    
                } catch (error) {
                    this.showNotification('Failed to send message. Please try again.', 'error');
                } finally {
                    // Reset button state
                    submitButton.textContent = originalText;
                    submitButton.disabled = false;
                    submitButton.classList.remove('btn--loading');
                }
            });
        });
    }
    
    async loadCompanyData() {
        try {
            const response = await fetch('/api/company-data');
            if (response.ok) {
                const data = await response.json();
                this.populateCompanyData(data);
            }
        } catch (error) {
            console.warn('Could not load company data:', error);
        }
    }
    
    populateCompanyData(data) {
        // Update dynamic content with company data
        if (data.achievements) {
            this.updateAchievements(data.achievements);
        }
        
        if (data.benefits) {
            this.updateBenefits(data.benefits);
        }
        
        if (data.market_data) {
            this.updateMarketData(data.market_data);
        }
    }
    
    updateAchievements(achievements) {
        // Update achievements section if exists
        const achievementsSection = document.querySelector('[data-achievements]');
        if (achievementsSection && achievements.length > 0) {
            const firstAchievement = achievements[0];
            const badge = achievementsSection.querySelector('.badge');
            if (badge) {
                badge.textContent = firstAchievement.title;
            }
        }
    }
    
    updateBenefits(benefits) {
        // Update benefits with real data
        const costElement = document.querySelector('[data-benefit="cost"]');
        const energyElement = document.querySelector('[data-benefit="energy"]');
        const carbonElement = document.querySelector('[data-benefit="carbon"]');
        
        if (costElement && benefits.cost_reduction) {
            costElement.textContent = benefits.cost_reduction;
        }
        if (energyElement && benefits.energy_reduction) {
            energyElement.textContent = benefits.energy_reduction;
        }
        if (carbonElement && benefits.carbon_reduction) {
            carbonElement.textContent = benefits.carbon_reduction;
        }
    }
    
    updateMarketData(marketData) {
        // Update market size statistics
        const tamElement = document.querySelector('[data-market="tam"]');
        const samElement = document.querySelector('[data-market="sam"]');
        const somElement = document.querySelector('[data-market="som"]');
        
        if (tamElement && marketData.total_addressable_market) {
            tamElement.textContent = marketData.total_addressable_market;
        }
        if (samElement && marketData.serviceable_addressable_market) {
            samElement.textContent = marketData.serviceable_addressable_market;
        }
        if (somElement && marketData.serviceable_obtainable_market) {
            somElement.textContent = marketData.serviceable_obtainable_market;
        }
    }
    
    setupPerformanceOptimizations() {
        // Lazy load images
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
        
        // Preload critical assets
        this.preloadCriticalAssets();
    }
    
    preloadCriticalAssets() {
        // Preload critical CSS and fonts
        const criticalAssets = [
            '/styles/main.css',
            'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap'
        ];
        
        criticalAssets.forEach(asset => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = asset.includes('.css') ? 'style' : 'font';
            link.href = asset;
            if (asset.includes('font')) {
                link.crossOrigin = 'anonymous';
            }
            document.head.appendChild(link);
        });
    }
    
    showNotification(message, type = 'info') {
        // Create and show notification toast
        const notification = document.createElement('div');
        notification.className = `notification notification--${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? 'var(--color-success)' : 'var(--color-error)'};
            color: white;
            padding: var(--spacing-4) var(--spacing-6);
            border-radius: var(--border-radius-base);
            box-shadow: var(--shadow-lg);
            z-index: var(--z-toast);
            animation: slideInRight 0.3s ease-out;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove after 5 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-in forwards';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 5000);
    }
    
    // Utility function for throttling
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }
    
    setupCounterAnimations() {
        const counters = document.querySelectorAll('[data-target]');
        
        const startCounter = (counter) => {
            const target = parseInt(counter.getAttribute('data-target'));
            const increment = target / 60; // 60 frames for smooth animation
            let current = 0;
            
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                
                if (counter.textContent.includes('%')) {
                    counter.textContent = Math.floor(current) + '%';
                } else if (counter.textContent.includes('M')) {
                    counter.textContent = '$' + Math.floor(current) + 'M';
                } else {
                    counter.textContent = Math.floor(current);
                }
            }, 50);
        };
        
        // Start counters after page load
        window.addEventListener('load', () => {
            setTimeout(() => {
                counters.forEach(counter => startCounter(counter));
            }, 500); // Delay to let animations settle
        });
    }
    
    // Utility function for debouncing
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Initialize the website when script loads
const squareWebsite = new SquareWebsite();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SquareWebsite;
}

// Global error handling
window.addEventListener('error', (e) => {
    console.error('Square Website Error:', e.error);
});

// Performance monitoring
window.addEventListener('load', () => {
    // Log performance metrics
    if ('performance' in window && 'measure' in performance) {
        setTimeout(() => {
            const navigation = performance.getEntriesByType('navigation')[0];
            const loadTime = navigation.loadEventEnd - navigation.loadEventStart;
            console.log(`🚀 Square Website loaded in ${loadTime}ms`);
        }, 0);
    }
});

// Add CSS animations dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .notification {
        transition: all 0.3s ease;
    }
`;
document.head.appendChild(style);
