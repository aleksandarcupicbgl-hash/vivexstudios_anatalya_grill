(function () {
  'use strict';

  var doc = document.documentElement;
  var body = document.body;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Intro (einmal pro Sitzung) ---------- */
  var intro = document.getElementById('intro');
  if (intro && !doc.classList.contains('no-intro')) {
    var hideIntro = function () {
      intro.classList.add('is-done');
      doc.classList.remove('intro-lock');
      try { sessionStorage.setItem('ag-intro-seen', '1'); } catch (e) {}
      setTimeout(function () { intro.remove(); }, 800);
    };
    setTimeout(hideIntro, reduceMotion ? 600 : 2100);
    intro.addEventListener('click', hideIntro, { once: true });
  } else {
    doc.classList.remove('intro-lock');
    if (intro) intro.remove();
  }

  /* ---------- Navigation ---------- */
  var nav = document.getElementById('nav');
  var toggle = document.getElementById('nav-toggle');
  var menu = document.getElementById('nav-menu');
  var fab = document.getElementById('fab');

  function setMenu(open) {
    menu.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü öffnen');
  }
  toggle.addEventListener('click', function () { setMenu(!menu.classList.contains('is-open')); });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });

  /* ---------- Scroll: Nav-Hintergrund, Parallax, FAB ---------- */
  var heroMedia = document.getElementById('hero-media');
  var menuSection = document.getElementById('speisekarte');
  var ticking = false;

  function onScroll() {
    var y = window.scrollY;
    nav.classList.toggle('is-scrolled', y > 30);
    if (heroMedia && !reduceMotion && y < window.innerHeight * 1.2) {
      heroMedia.style.transform = 'translate3d(0,' + (y * 0.3).toFixed(1) + 'px,0)';
    }
    if (fab) {
      var r = menuSection.getBoundingClientRect();
      var inMenu = r.top < window.innerHeight * 0.5 && r.bottom > window.innerHeight * 0.5;
      fab.classList.toggle('is-visible', y > window.innerHeight * 0.6 && !inMenu);
    }
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ---------- Aktive Sektion gelb markieren ---------- */
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav__menu a[data-nav]'));
  var sections = Array.prototype.slice.call(document.querySelectorAll('[data-nav-target]'));
  function setActive(key) {
    links.forEach(function (a) {
      var on = a.getAttribute('data-nav') === key;
      a.classList.toggle('is-active', on);
      if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
    });
  }
  if ('IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) setActive(en.target.getAttribute('data-nav-target'));
      });
    }, { rootMargin: '-45% 0px -54% 0px' });
    sections.forEach(function (s) { spy.observe(s); });
  }
  setActive('start');

  /* ---------- Einblenden beim Scrollen ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); ro.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { ro.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- Speisekarte: Kategorie-Filter ---------- */
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.menu-tab'));
  var groupsWrap = document.querySelector('.menu-groups');
  var groups = Array.prototype.slice.call(document.querySelectorAll('.menu-group'));
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      var f = tab.getAttribute('data-filter');
      tabs.forEach(function (t) {
        var on = t === tab;
        t.classList.toggle('is-active', on);
        t.setAttribute('aria-selected', String(on));
      });
      groups.forEach(function (g) {
        g.hidden = f !== 'all' && g.getAttribute('data-cat') !== f;
        g.classList.add('is-in');
      });
      groupsWrap.classList.toggle('is-filtered', f !== 'all');
      tab.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'nearest', inline: 'center' });
      var top = groupsWrap.getBoundingClientRect().top;
      var offset = nav.offsetHeight + document.querySelector('.menu-tabs').offsetHeight + 8;
      if (top < offset) window.scrollTo({ top: window.scrollY + top - offset, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  });

  /* ---------- Jahr im Footer ---------- */
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
