/**
 * SPL v3 — shared site behaviour
 * - count-up numbers on [data-count]
 * - reveal-on-scroll for [data-reveal] (with a safety net: content never stays hidden)
 * - query-string helpers for filter deep links (SPL.setParams)
 * - open a <details> targeted by the URL hash (FantaSPL rosters)
 */
(function () {
    'use strict';

    const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function formatCurrency(value) {
        const v = Math.abs(value), sign = value < 0 ? '-' : '';
        return v >= 1e6 ? sign + '€' + (v / 1e6).toFixed(1) + 'M' : sign + '€' + (v / 1e3).toFixed(0) + 'K';
    }

    // Same output as the builder's `num` filter: 2399 -> "2.399"
    function formatNumber(n) {
        return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    }

    function countUp(el) {
        const target = parseFloat(el.dataset.count);
        if (isNaN(target) || reduceMotion) return;
        const start = performance.now(), duration = 1400;
        function step(now) {
            const p = Math.min((now - start) / duration, 1);
            el.textContent = formatNumber(target * (1 - Math.pow(1 - p, 4)));
            if (p < 1) requestAnimationFrame(step);
        }
        el.textContent = '0';
        requestAnimationFrame(step);
    }

    function setupReveal() {
        const els = Array.from(document.querySelectorAll('[data-reveal]'));
        if (!els.length || reduceMotion || !('IntersectionObserver' in window)) return;

        // stagger siblings inside the same grid
        els.forEach(el => {
            const siblings = Array.from(el.parentElement.children).filter(c => c.hasAttribute('data-reveal'));
            el.style.setProperty('--i', Math.min(siblings.indexOf(el), 8));
        });
        document.documentElement.classList.add('reveal-ready');

        const io = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-in');
                    io.unobserve(entry.target);
                }
            });
        }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
        els.forEach(el => io.observe(el));

        // Safety net: never leave anything invisible (print, screenshots, odd browsers)
        setTimeout(() => els.forEach(el => el.classList.add('is-in')), 2200);
    }

    function setParams(updates) {
        const url = new URL(location.href);
        Object.entries(updates).forEach(([k, v]) => {
            if (v === null || v === undefined || v === '') url.searchParams.delete(k);
            else url.searchParams.set(k, String(v).replace(/^Stagione /, ''));
        });
        history.replaceState(null, '', url.pathname + url.search + url.hash);
    }

    function openHashTarget() {
        if (!location.hash) return;
        let target = null;
        try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch (e) { return; }
        if (target && target.tagName === 'DETAILS') {
            target.open = true;
            setTimeout(() => target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'center' }), 80);
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('[data-count]').forEach(countUp);
        setupReveal();
        openHashTarget();
    });
    window.addEventListener('hashchange', openHashTarget);

    window.SPL = { formatCurrency, formatNumber, setParams };
})();
