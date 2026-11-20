/**
 * HappyMiles Tours — Main JavaScript
 * Animations, Preloader, Lightbox, Theme & Interactions
 */

// Centralized Site Configuration & Fallbacks
window.HAPPYMILES_CONFIG = {
  enquiryFormUrl: 'https://forms.gle/8dFCPRhFAX5Rzg3W7',
  bookingFormUrl: 'https://forms.gle/r97LBQdCx39JAZfQ6',
  whatsappNumber: '918074016910',
  upiId: '7661981338@kotakbank'
};

window.openEnquiryForm = function() {
  window.open(window.HAPPYMILES_CONFIG.enquiryFormUrl, '_blank', 'noopener,noreferrer');
};

window.openBookingForm = function() {
  window.open(window.HAPPYMILES_CONFIG.bookingFormUrl, '_blank', 'noopener,noreferrer');
};

function updateConfiguredLinks() {
  document.querySelectorAll('[data-config-link="enquiryForm"]').forEach(el => {
    el.href = window.HAPPYMILES_CONFIG.enquiryFormUrl;
    el.target = '_blank';
    el.rel = 'noopener noreferrer';
  });

  document.querySelectorAll('[data-config-link="bookingForm"]').forEach(el => {
    el.href = window.HAPPYMILES_CONFIG.bookingFormUrl;
    el.target = '_blank';
    el.rel = 'noopener noreferrer';
  });
}

function initDynamicConfig() {
  updateConfiguredLinks();
  fetch('/api/config')
    .then(r => r.json())
    .then(cfg => {
      if (cfg.enquiry_form_url) window.HAPPYMILES_CONFIG.enquiryFormUrl = cfg.enquiry_form_url;
      if (cfg.booking_form_url) window.HAPPYMILES_CONFIG.bookingFormUrl = cfg.booking_form_url;
      if (cfg.whatsapp_number) window.HAPPYMILES_CONFIG.whatsappNumber = cfg.whatsapp_number;
      if (cfg.upi_id) window.HAPPYMILES_CONFIG.upiId = cfg.upi_id;
      updateConfiguredLinks();
    })
    .catch(err => {
      console.warn('Could not fetch dynamic config from /api/config, fallback in effect:', err);
    });
}

document.addEventListener('DOMContentLoaded', () => {
  initDynamicConfig();
  initPreloader();
  initThemeToggle();
  initNavbarScroll();
  initMobileDrawer();
  initHeroSlider();
  initCursorFollower();
  initStatsCounters();
  initCustomersFilter();
  initLightbox();
  initFaqAccordion();
  initBackToTop();
  initRoadStory();
  initTiltCards();
});

// Toast notification helper
window.showToast = function(msg, icon = '✨') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<span>${icon}</span> <span>${msg}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(15px)';
    setTimeout(() => toast.remove(), 350);
  }, 3200);
};

// 1. Preloader
function initPreloader() {
  const preloader = document.getElementById('preloader');
  const counter = document.getElementById('preloader-counter');
  if (!preloader || !counter) return;

  let count = 0;
  const interval = setInterval(() => {
    count += Math.floor(Math.random() * 8) + 4;
    if (count > 100) count = 100;
    counter.textContent = `${count}%`;
    if (count === 100) {
      clearInterval(interval);
      setTimeout(() => {
        preloader.classList.add('loaded');
        // Trigger GSAP hero animations once preloader finishes
        if (window.gsap) {
          gsap.from('.hero-content > *', {
            y: 30,
            opacity: 0,
            duration: 1,
            stagger: 0.15,
            ease: 'power3.out'
          });
        }
      }, 300);
    }
  }, 40);
}

// 2. Light & Dark Mode Toggle
function initThemeToggle() {
  const toggleBtn = document.getElementById('theme-toggle-btn');
  const storedTheme = localStorage.getItem('happymiles-theme') || 'light';
  document.documentElement.setAttribute('data-theme', storedTheme);

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('happymiles-theme', next);
      showToast(next === 'dark' ? 'Dark mode enabled' : 'Light mode enabled', next === 'dark' ? '🌙' : '☀️');
    });
  }
}

// 3. Navbar scroll and auto-hide
function initNavbarScroll() {
  const navWrapper = document.querySelector('.navbar-wrapper');
  if (!navWrapper) return;

  let lastScroll = 0;
  window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    if (currentScroll > 60) {
      navWrapper.classList.add('scrolled');
    } else {
      navWrapper.classList.remove('scrolled');
    }

    if (currentScroll > 300 && currentScroll > lastScroll) {
      navWrapper.classList.add('hidden');
    } else {
      navWrapper.classList.remove('hidden');
    }
    lastScroll = currentScroll;
  }, { passive: true });
}

// 4. Mobile Drawer Menu
function initMobileDrawer() {
  const btn = document.getElementById('mobile-menu-btn');
  const drawer = document.getElementById('mobile-drawer');
  const closeBtn = document.getElementById('mobile-drawer-close');
  if (!btn || !drawer) return;

  btn.addEventListener('click', () => drawer.classList.toggle('open'));
  if (closeBtn) closeBtn.addEventListener('click', () => drawer.classList.remove('open'));

  // Close when clicking any nav link
  drawer.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => drawer.classList.remove('open'));
  });
}

// 5. Hero Background Slideshow with Ken Burns
function initHeroSlider() {
  const slides = document.querySelectorAll('.hero-slide');
  if (slides.length <= 1) return;

  let current = 0;
  setInterval(() => {
    slides[current].classList.remove('active');
    current = (current + 1) % slides.length;
    slides[current].classList.add('active');
  }, 6000);
}

// 6. Desktop Cursor Follower
function initCursorFollower() {
  const dot = document.querySelector('.cursor-dot');
  const circle = document.querySelector('.cursor-circle');
  if (!dot || !circle) return;

  let mouseX = window.innerWidth / 2;
  let mouseY = window.innerHeight / 2;
  let circleX = mouseX;
  let circleY = mouseY;

  window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    dot.style.transform = `translate(${mouseX}px, ${mouseY}px)`;
  });

  function renderCircle() {
    circleX += (mouseX - circleX) * 0.15;
    circleY += (mouseY - circleY) * 0.15;
    circle.style.transform = `translate(${circleX}px, ${circleY}px)`;
    requestAnimationFrame(renderCircle);
  }
  renderCircle();

  // Hover effect over interactive elements
  document.querySelectorAll('a, button, .customer-card, .package-card, .bento-item').forEach(el => {
    el.addEventListener('mouseenter', () => {
      circle.style.width = '55px';
      circle.style.height = '55px';
      circle.style.borderColor = 'var(--color-accent)';
    });
    el.addEventListener('mouseleave', () => {
      circle.style.width = '36px';
      circle.style.height = '36px';
      circle.style.borderColor = 'var(--color-primary)';
    });
  });
}

// 7. Animated Number Counters
function initStatsCounters() {
  const counters = document.querySelectorAll('.counter-val');
  if (!counters.length) return;

  let animated = false;
  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && !animated) {
      animated = true;
      counters.forEach(counter => {
        const target = +counter.getAttribute('data-target');
        const duration = 1800;
        const step = target / (duration / 25);
        let curr = 0;
        const timer = setInterval(() => {
          curr += step;
          if (curr >= target) {
            counter.textContent = target.toLocaleString();
            clearInterval(timer);
          } else {
            counter.textContent = Math.floor(curr).toLocaleString();
          }
        }, 25);
      });
    }
  }, { threshold: 0.3 });

  const statsSection = document.querySelector('.stats-section');
  if (statsSection) observer.observe(statsSection);
}

// 8. Happy Customers Filter Tabs
function initCustomersFilter() {
  const tabs = document.querySelectorAll('.filter-tab-btn');
  const cards = document.querySelectorAll('.customer-card');
  if (!tabs.length || !cards.length) return;

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const filter = tab.getAttribute('data-filter');

      cards.forEach(card => {
        const categories = card.getAttribute('data-category') || '';
        if (filter === 'all' || categories.includes(filter)) {
          card.style.display = 'block';
          if (window.gsap) {
            gsap.fromTo(card, { opacity: 0, scale: 0.95 }, { opacity: 1, scale: 1, duration: 0.4 });
          }
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

// 9. Fullscreen Lightbox Modal (Swipe, Keyboard, Zoom)
let lightboxImages = [];
let currentLightboxIdx = 0;

function initLightbox() {
  const modal = document.getElementById('lightbox-modal');
  if (!modal) return;

  const imgEl = document.getElementById('lightbox-img');
  const captionEl = document.getElementById('lightbox-caption');
  const closeBtn = document.getElementById('lightbox-close');
  const prevBtn = document.getElementById('lightbox-prev');
  const nextBtn = document.getElementById('lightbox-next');

  function openLightbox(idx) {
    currentLightboxIdx = idx;
    const item = lightboxImages[idx];
    if (!item) return;
    imgEl.src = item.src;
    imgEl.alt = item.alt || '';
    if (captionEl) captionEl.textContent = item.caption || item.alt || '';
    modal.classList.add('open');
  }

  function closeLightbox() {
    modal.classList.remove('open');
  }

  function nextLightbox() {
    currentLightboxIdx = (currentLightboxIdx + 1) % lightboxImages.length;
    openLightbox(currentLightboxIdx);
  }

  function prevLightbox() {
    currentLightboxIdx = (currentLightboxIdx - 1 + lightboxImages.length) % lightboxImages.length;
    openLightbox(currentLightboxIdx);
  }

  // Bind clicks on all zoomable elements
  document.querySelectorAll('[data-lightbox-src]').forEach((el) => {
    const src = el.getAttribute('data-lightbox-src');
    const caption = el.getAttribute('data-lightbox-caption') || el.getAttribute('alt') || '';
    const idx = lightboxImages.length;
    lightboxImages.push({ src, caption });

    el.addEventListener('click', (e) => {
      e.preventDefault();
      openLightbox(idx);
    });
  });

  if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
  if (nextBtn) nextBtn.addEventListener('click', nextLightbox);
  if (prevBtn) prevBtn.addEventListener('click', prevLightbox);

  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeLightbox();
  });

  // Keyboard navigation
  window.addEventListener('keydown', (e) => {
    if (!modal.classList.contains('open')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowRight') nextLightbox();
    if (e.key === 'ArrowLeft') prevLightbox();
  });

  // Touch Swipe for mobile
  let touchStartX = 0;
  modal.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });
  modal.addEventListener('touchend', (e) => {
    const touchEndX = e.changedTouches[0].screenX;
    if (touchStartX - touchEndX > 50) nextLightbox();
    if (touchEndX - touchStartX > 50) prevLightbox();
  }, { passive: true });
}

// 10. FAQ Accordion
function initFaqAccordion() {
  const items = document.querySelectorAll('.faq-item');
  items.forEach(item => {
    const btn = item.querySelector('.faq-question');
    const answer = item.querySelector('.faq-answer');
    if (!btn || !answer) return;

    btn.addEventListener('click', () => {
      const isOpen = item.classList.contains('active');
      items.forEach(i => {
        i.classList.remove('active');
        const a = i.querySelector('.faq-answer');
        if (a) a.style.maxHeight = null;
      });
      if (!isOpen) {
        item.classList.add('active');
        answer.style.maxHeight = answer.scrollHeight + 30 + 'px';
      }
    });
  });
}

// 11. Back to Top Button
function initBackToTop() {
  const btn = document.getElementById('back-to-top-btn');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    if (window.pageYOffset > 500) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }, { passive: true });

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// 12. Road Storyline Vehicle Scroll Tracking
function initRoadStory() {
  const roadCar = document.getElementById('road-vehicle');
  const roadSection = document.getElementById('story-road');
  if (!roadCar || !roadSection) return;

  window.addEventListener('scroll', () => {
    const rect = roadSection.getBoundingClientRect();
    const windowH = window.innerHeight;
    if (rect.top < windowH && rect.bottom > 0) {
      const progress = (windowH - rect.top) / (rect.height + windowH);
      const clampProg = Math.max(0, Math.min(1, progress));
      roadCar.style.top = `${clampProg * 90}%`;
    }
  }, { passive: true });
}

// 13. 3D Tilt Card effect for desktop
function initTiltCards() {
  if (window.matchMedia('(pointer: coarse)').matches) return;
  const cards = document.querySelectorAll('.package-card');
  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const midX = rect.width / 2;
      const midY = rect.height / 2;
      const rotateX = ((y - midY) / midY) * -7;
      const rotateY = ((x - midX) / midX) * 7;
      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
    });
  });
}
