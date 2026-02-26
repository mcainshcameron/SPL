/**
 * SPL v2 - Main JavaScript
 */

// Format currency
function formatCurrency(value) {
    if (value >= 1000000) {
        return `€${(value / 1000000).toFixed(1)}M`;
    }
    return `€${(value / 1000).toFixed(0)}K`;
}

// Format percentage
function formatPercent(value) {
    return `${value.toFixed(1)}%`;
}

// Debounce function
function debounce(func, wait) {
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

// Add loading state to elements
function showLoading(element) {
    element.classList.add('loading');
}

function hideLoading(element) {
    element.classList.remove('loading');
}

// Toast notification system
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Table sorting
function sortTable(table, column, ascending = true) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    rows.sort((a, b) => {
        const aValue = a.children[column].textContent.trim();
        const bValue = b.children[column].textContent.trim();
        
        // Try to parse as number
        const aNum = parseFloat(aValue.replace(/[^0-9.-]/g, ''));
        const bNum = parseFloat(bValue.replace(/[^0-9.-]/g, ''));
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return ascending ? aNum - bNum : bNum - aNum;
        }
        
        // Fall back to string comparison
        return ascending 
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
    });
    
    // Re-append rows
    rows.forEach(row => tbody.appendChild(row));
}

// Add sortable headers
document.addEventListener('DOMContentLoaded', function() {
    const sortableHeaders = document.querySelectorAll('th[data-sortable]');
    
    sortableHeaders.forEach(header => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            const table = this.closest('table');
            const column = Array.from(this.parentElement.children).indexOf(this);
            const isAscending = !this.classList.contains('sorted-asc');
            
            // Remove sorted class from all headers
            table.querySelectorAll('th').forEach(th => {
                th.classList.remove('sorted-asc', 'sorted-desc');
            });
            
            // Add sorted class to current header
            this.classList.add(isAscending ? 'sorted-asc' : 'sorted-desc');
            
            sortTable(table, column, isAscending);
        });
    });
});

// Lazy loading for images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    document.addEventListener('DOMContentLoaded', function() {
        const lazyImages = document.querySelectorAll('img.lazy');
        lazyImages.forEach(img => imageObserver.observe(img));
    });
}

// Handle external links
document.addEventListener('DOMContentLoaded', function() {
    const externalLinks = document.querySelectorAll('a[href^="http"]');
    externalLinks.forEach(link => {
        if (!link.href.includes(window.location.hostname)) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });
});

// Mobile menu toggle (if needed in future)
function toggleMobileMenu() {
    const menu = document.querySelector('.nav-mobile');
    menu.classList.toggle('open');
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Escape key to close modals/dropdowns
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal, .dropdown').forEach(el => {
            el.classList.remove('open');
        });
    }
});

// Copy to clipboard helper
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copiato negli appunti!', 'success');
        }).catch(() => {
            showToast('Errore durante la copia', 'error');
        });
    }
}

// Animated number counters
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = Math.round(target);
            clearInterval(timer);
        } else {
            element.textContent = Math.round(current);
        }
    }, 16);
}

// Initialize counters on page load
document.addEventListener('DOMContentLoaded', function() {
    const counters = document.querySelectorAll('.stat-value[data-count]');
    
    counters.forEach(counter => {
        const target = parseInt(counter.dataset.count);
        if (!isNaN(target)) {
            counter.textContent = '0';
            setTimeout(() => {
                animateCounter(counter, target);
            }, 300);
        }
    });
});

// Card entrance animations using IntersectionObserver
if ('IntersectionObserver' in window) {
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '50px'
    });
    
    document.addEventListener('DOMContentLoaded', function() {
        const cards = document.querySelectorAll('.game-card, .market-card, .championship-card, .roster-card');
        cards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            cardObserver.observe(card);
        });
    });
}

// Auto-expand roster card when linked from standings
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.hash) {
        const targetId = window.location.hash.substring(1);
        const targetElement = document.getElementById(targetId);
        if (targetElement && targetElement.tagName === 'DETAILS') {
            targetElement.open = true;
            setTimeout(() => {
                targetElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);
        }
    }
});

// Export utilities
window.SPL = {
    formatCurrency,
    formatPercent,
    showToast,
    copyToClipboard,
    debounce,
    animateCounter
};
