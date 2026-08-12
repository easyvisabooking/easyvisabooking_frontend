/* ==========================================================================
   Easy Visa Booking: Blog System JS
   --------------------------------------------------------------------------
   Progressive enhancement only. Every page must remain fully readable and
   fully crawlable with JavaScript disabled:
     - FAQ accordions are native <details>, so they need no JS at all.
     - The blog hub renders every card in static HTML; the filter below only
       hides cards that are already in the DOM.

   Loaded on /blog/ and every /blog/<post>/ page. Safe to load on both;
   each block no-ops when its markup is absent.
   ========================================================================== */
(function () {
    'use strict';

    /* ----------------------------------------------------------------------
       1. Reading progress bar (post pages)
       ---------------------------------------------------------------------- */
    function initReadingProgress() {
        var bar = document.querySelector('.reading-progress');
        // .post-body is the current shell; .blog-article article is the legacy one
        var article = document.querySelector('.post-body') || document.querySelector('.blog-article article');
        if (!bar || !article) return;

        var ticking = false;

        function update() {
            var rect = article.getBoundingClientRect();
            var total = rect.height - window.innerHeight;
            var scrolled = -rect.top;
            var pct = total <= 0 ? 0 : (scrolled / total) * 100;
            bar.style.width = Math.min(100, Math.max(0, pct)) + '%';
            ticking = false;
        }

        window.addEventListener('scroll', function () {
            if (!ticking) {
                window.requestAnimationFrame(update);
                ticking = true;
            }
        }, { passive: true });

        window.addEventListener('resize', update, { passive: true });
        update();
    }

    /* ----------------------------------------------------------------------
       2. Table-of-contents scrollspy (post pages)
       Highlights the section currently in view. The TOC itself is authored
       in static HTML so it works without JS.
       ---------------------------------------------------------------------- */
    function initTocSpy() {
        var toc = document.querySelector('.toc');
        if (!toc || !('IntersectionObserver' in window)) return;

        var links = Array.prototype.slice.call(toc.querySelectorAll('a[href^="#"]'));
        if (!links.length) return;

        var map = {};
        var targets = [];

        links.forEach(function (link) {
            var id = link.getAttribute('href').slice(1);
            var el = document.getElementById(id);
            if (el) {
                map[id] = link;
                targets.push(el);
            }
        });

        if (!targets.length) return;

        var visible = {};

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                visible[entry.target.id] = entry.isIntersecting;
            });

            var currentId = null;
            for (var i = 0; i < targets.length; i++) {
                if (visible[targets[i].id]) {
                    currentId = targets[i].id;
                    break;
                }
            }

            links.forEach(function (link) { link.classList.remove('is-current'); });
            if (currentId && map[currentId]) map[currentId].classList.add('is-current');
        }, { rootMargin: '-88px 0px -70% 0px', threshold: 0 });

        targets.forEach(function (el) { observer.observe(el); });
    }

    /* ----------------------------------------------------------------------
       3. Category filter (blog hub)
       Filters the static card grid client-side. No URLs are created, so no
       thin category pages and no crawlable duplicates.
       ---------------------------------------------------------------------- */
    function initHubFilter() {
        var bar = document.querySelector('.hub-filters');
        if (!bar) return;

        var buttons = Array.prototype.slice.call(bar.querySelectorAll('.hub-filter'));
        var cards = Array.prototype.slice.call(document.querySelectorAll('.post-card[data-category]'));
        var featured = document.querySelector('.featured[data-category]');
        var featuredLabel = document.querySelector('[data-role="featured-label"]');
        var empty = document.querySelector('.hub-empty');
        if (!buttons.length || !cards.length) return;

        function apply(category) {
            var shown = 0;

            cards.forEach(function (card) {
                var match = category === 'all' || card.getAttribute('data-category') === category;
                card.classList.toggle('is-hidden', !match);
                if (match) shown++;
            });

            if (featured) {
                var fMatch = category === 'all' || featured.getAttribute('data-category') === category;
                featured.style.display = fMatch ? '' : 'none';
                if (featuredLabel) featuredLabel.style.display = fMatch ? '' : 'none';
                if (fMatch) shown++;
            }

            if (empty) empty.style.display = shown === 0 ? 'block' : 'none';

            buttons.forEach(function (btn) {
                btn.setAttribute('aria-pressed', String(btn.getAttribute('data-filter') === category));
            });
        }

        buttons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                apply(btn.getAttribute('data-filter'));
            });
        });

        apply('all');
    }

    /* ----------------------------------------------------------------------
       4. Boot
       ---------------------------------------------------------------------- */
    function boot() {
        initReadingProgress();
        initTocSpy();
        initHubFilter();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
