/*
 * Small enhancements. Without JavaScript the site still shows everything:
 * all three focus areas are listed one after the other.
 *
 * 1. Focus areas as tabs. A link like  .../de/?fokus=kontakte  opens the page with
 *    "Kontakte" selected and highlights the matching experience. Useful in applications.
 * 2. Mobile menu closes after choosing a section.
 * 3. Image gallery with a lightbox on experience pages.
 */
(function () {
  'use strict';

  // ---------- 1. focus areas ----------
  var lens = document.querySelector('[data-lens]');
  if (lens) {
    var tablist = lens.querySelector('[role="tablist"]');
    var tabs = Array.prototype.slice.call(lens.querySelectorAll('[role="tab"]'));
    var panels = Array.prototype.slice.call(lens.querySelectorAll('[role="tabpanel"]'));
    var ids = tabs.map(function (tab) { return tab.getAttribute('data-area'); });
    var aliases = {
      contacts: 'kontakte', contatti: 'kontakte', bd: 'kontakte', sales: 'kontakte', vertrieb: 'kontakte',
      coordination: 'koordination', coordinamento: 'koordination', projekte: 'koordination', projects: 'koordination', progetti: 'koordination', pm: 'koordination',
      contenuti: 'content', kommunikation: 'content', communication: 'content', comunicazione: 'content'
    };
    var entries = Array.prototype.slice.call(document.querySelectorAll('[data-areas]'));

    var normalise = function (value) {
      if (!value) return null;
      value = String(value).toLowerCase().replace(/^fokus-|^focus-/, '');
      if (ids.indexOf(value) !== -1) return value;
      return aliases[value] && ids.indexOf(aliases[value]) !== -1 ? aliases[value] : null;
    };

    var highlight = function (id) {
      entries.forEach(function (entry) {
        var areas = (entry.getAttribute('data-areas') || '').split(/\s+/);
        var match = id && areas.indexOf(id) !== -1;
        entry.classList.toggle('is-match', Boolean(match));
        Array.prototype.forEach.call(entry.querySelectorAll('[data-area]'), function (tag) {
          tag.classList.toggle('is-on', Boolean(match) && tag.getAttribute('data-area') === id);
        });
      });
    };

    var select = function (id, options) {
      options = options || {};
      tabs.forEach(function (tab) {
        var on = tab.getAttribute('data-area') === id;
        tab.setAttribute('aria-selected', on ? 'true' : 'false');
        tab.tabIndex = on ? 0 : -1;
      });
      panels.forEach(function (panel) {
        var on = panel.getAttribute('data-panel') === id;
        panel.hidden = !on;
        if (on && options.animate) {
          panel.classList.remove('is-entering');
          void panel.offsetWidth;
          panel.classList.add('is-entering');
        }
      });
      if (options.explicit) {
        highlight(id);
        try {
          var url = new URL(window.location.href);
          url.searchParams.delete('focus');
          url.searchParams.delete('ambito');
          url.searchParams.set('fokus', id);
          url.hash = '';
          window.history.replaceState(null, '', url.toString());
        } catch (error) {
          /* the address bar simply stays as it is */
        }
      }
    };

    if (tablist && tabs.length) {
      tablist.hidden = false;
      lens.classList.add('has-tabs');
      var params = new URLSearchParams(window.location.search);
      var wanted = normalise(params.get('fokus') || params.get('focus') || params.get('ambito')) || normalise(window.location.hash.slice(1));
      select(wanted || ids[0], { explicit: Boolean(wanted) });

      tabs.forEach(function (tab, index) {
        tab.addEventListener('click', function () {
          select(tab.getAttribute('data-area'), { explicit: true, animate: true });
        });
        tab.addEventListener('keydown', function (event) {
          var next = null;
          if (event.key === 'ArrowRight') next = tabs[(index + 1) % tabs.length];
          if (event.key === 'ArrowLeft') next = tabs[(index - 1 + tabs.length) % tabs.length];
          if (event.key === 'Home') next = tabs[0];
          if (event.key === 'End') next = tabs[tabs.length - 1];
          if (next) {
            event.preventDefault();
            next.focus();
            select(next.getAttribute('data-area'), { explicit: true, animate: true });
          }
        });
      });

      // The three big words at the top open their focus area.
      Array.prototype.forEach.call(document.querySelectorAll('[data-focus-link]'), function (link) {
        link.addEventListener('click', function (event) {
          var id = link.getAttribute('data-focus-link');
          if (ids.indexOf(id) === -1) return;
          event.preventDefault();
          select(id, { explicit: true, animate: true });
          var section = document.getElementById('focus');
          if (section) {
            var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
            section.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
          }
          var tab = document.getElementById('tab-' + id);
          if (tab) tab.focus({ preventScroll: true });
        });
      });
    }
  }

  // ---------- 2. mobile menu ----------
  Array.prototype.forEach.call(document.querySelectorAll('details.menu'), function (menu) {
    var close = function () { menu.removeAttribute('open'); };
    Array.prototype.forEach.call(menu.querySelectorAll('a'), function (link) {
      link.addEventListener('click', close);
    });
    document.addEventListener('click', function (event) {
      if (menu.hasAttribute('open') && !menu.contains(event.target)) close();
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') close();
    });
  });

  // ---------- 3. gallery ----------
  Array.prototype.forEach.call(document.querySelectorAll('[data-gallery]'), function (gallery) {
    var dialog = gallery.querySelector('dialog');
    var image = gallery.querySelector('[data-lightbox-img]');
    var caption = gallery.querySelector('[data-lightbox-caption]');
    var buttons = Array.prototype.slice.call(gallery.querySelectorAll('button[data-full]'));
    if (!dialog || !image || !caption || !buttons.length || typeof dialog.showModal !== 'function') return;
    var current = 0;
    var show = function (index) {
      current = (index + buttons.length) % buttons.length;
      var button = buttons[current];
      image.src = button.getAttribute('data-full');
      image.alt = button.getAttribute('data-alt') || '';
      caption.textContent = button.getAttribute('data-caption') || '';
    };
    buttons.forEach(function (button, index) {
      button.addEventListener('click', function () {
        show(index);
        dialog.showModal();
      });
    });
    var prev = gallery.querySelector('[data-prev]');
    var next = gallery.querySelector('[data-next]');
    var closeButton = gallery.querySelector('[data-close]');
    if (prev) prev.addEventListener('click', function () { show(current - 1); });
    if (next) next.addEventListener('click', function () { show(current + 1); });
    if (closeButton) closeButton.addEventListener('click', function () { dialog.close(); });
    dialog.addEventListener('click', function (event) {
      if (event.target === dialog) dialog.close();
    });
    dialog.addEventListener('keydown', function (event) {
      if (event.key === 'ArrowLeft') show(current - 1);
      if (event.key === 'ArrowRight') show(current + 1);
    });
  });
})();
