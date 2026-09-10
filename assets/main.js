document.addEventListener('DOMContentLoaded', () => {
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Header scroll shadow
  const headerEl = document.querySelector('header');
  if (headerEl) {
    window.addEventListener('scroll', () => {
      headerEl.classList.toggle('scrolled', window.scrollY > 8);
    }, { passive: true });
  }

  // Scroll-in reveal
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

  // Stat count-up
  const statsBar = document.getElementById('statsBar');
  if (statsBar) {
    const countUp = () => {
      statsBar.querySelectorAll('[data-count]').forEach(el => {
        const target = parseInt(el.getAttribute('data-count'), 10);
        const suffix = el.getAttribute('data-suffix') || '';
        const duration = 1200;
        const start = performance.now();
        function tick(now) {
          const progress = Math.min((now - start) / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          const value = Math.round(target * eased);
          el.textContent = value.toLocaleString() + suffix;
          if (progress < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
      });
    };
    const statsObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) { countUp(); statsObserver.disconnect(); }
      });
    }, { threshold: 0.4 });
    statsObserver.observe(statsBar);
  }

  // Mobile menu toggle
  const menuBtn = document.getElementById('menuBtn');
  const mobileMenu = document.getElementById('mobileMenu');
  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener('click', () => mobileMenu.classList.toggle('open'));
    mobileMenu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => mobileMenu.classList.remove('open')));
  }

  // Accordion (FAQ)
  document.querySelectorAll('.accordion-item').forEach(item => {
    const trigger = item.querySelector('.accordion-trigger');
    const panel = item.querySelector('.accordion-panel');
    if (!trigger || !panel) return;
    trigger.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.accordion-item.open').forEach(openItem => {
        openItem.classList.remove('open');
        const openPanel = openItem.querySelector('.accordion-panel');
        if (openPanel) openPanel.style.maxHeight = null;
      });
      if (!isOpen) {
        item.classList.add('open');
        panel.style.maxHeight = panel.scrollHeight + 'px';
      }
    });
  });

  // Before/After slider (only present on pages with a portfolio section)
  const baSlider = document.getElementById('baSlider');
  const baAfter = document.getElementById('baAfter');
  const baHandle = document.getElementById('baHandle');
  if (baSlider && baAfter && baHandle) {
    let dragging = false;
    function setSlider(clientX) {
      const rect = baSlider.getBoundingClientRect();
      let pct = ((clientX - rect.left) / rect.width) * 100;
      pct = Math.max(0, Math.min(100, pct));
      baAfter.style.clipPath = `inset(0 0 0 ${pct}%)`;
      baHandle.style.left = pct + '%';
    }
    baSlider.addEventListener('mousedown', e => { dragging = true; setSlider(e.clientX); });
    window.addEventListener('mousemove', e => { if (dragging) setSlider(e.clientX); });
    window.addEventListener('mouseup', () => dragging = false);
    baSlider.addEventListener('touchstart', e => { dragging = true; setSlider(e.touches[0].clientX); });
    baSlider.addEventListener('touchmove', e => { if (dragging) setSlider(e.touches[0].clientX); });
    window.addEventListener('touchend', () => dragging = false);
  }

  // Contact form (static demo — GHL endpoint not wired up yet)
  const form = document.getElementById('estimateForm');
  const formSuccess = document.getElementById('formSuccess');
  if (form && formSuccess) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      formSuccess.classList.add('show');
      form.reset();
    });
  }
});
