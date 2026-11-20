/**
 * HappyMiles Tours — Interactive Booking & Payment Sheet
 * Multi-step form, Server-driven financial calculation, Kotak UPI QR & WhatsApp sync
 */

let currentPackage = null;
let currentBooking = null;
let currentStep = 1;

document.addEventListener('DOMContentLoaded', () => {
  initBookingModal();
});

function initBookingModal() {
  const modal = document.getElementById('booking-modal');
  const closeBtn = document.getElementById('booking-modal-close');
  if (!modal) return;

  if (closeBtn) {
    closeBtn.addEventListener('click', closeBookingModal);
  }

  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeBookingModal();
  });

  // Travelers count buttons (+ and -)
  const minusBtn = document.getElementById('travelers-minus');
  const plusBtn = document.getElementById('travelers-plus');
  const travelersInput = document.getElementById('booking-travelers');

  if (minusBtn && plusBtn && travelersInput) {
    minusBtn.addEventListener('click', () => {
      let val = parseInt(travelersInput.value, 10) || 1;
      if (val > 1) {
        travelersInput.value = val - 1;
        updatePriceSummary();
      }
    });

    plusBtn.addEventListener('click', () => {
      let val = parseInt(travelersInput.value, 10) || 1;
      if (val < 25) {
        travelersInput.value = val + 1;
        updatePriceSummary();
      }
    });

    travelersInput.addEventListener('change', updatePriceSummary);
  }

  // Payment type toggle (Advance vs Full)
  const payAdvanceBtn = document.getElementById('pay-type-advance');
  const payFullBtn = document.getElementById('pay-type-full');

  if (payAdvanceBtn && payFullBtn) {
    payAdvanceBtn.addEventListener('click', () => {
      payAdvanceBtn.classList.add('selected');
      payFullBtn.classList.remove('selected');
      updatePriceSummary();
    });

    payFullBtn.addEventListener('click', () => {
      payFullBtn.classList.add('selected');
      payAdvanceBtn.classList.remove('selected');
      updatePriceSummary();
    });
  }

  // Step Next Buttons
  const step1Next = document.getElementById('btn-step-1-next');
  if (step1Next) {
    step1Next.addEventListener('click', () => {
      const dateInput = document.getElementById('booking-date');
      if (!dateInput.value) {
        window.showToast('Please select your preferred travel date', '📅');
        dateInput.focus();
        return;
      }
      goToStep(2);
    });
  }

  const step2Back = document.getElementById('btn-step-2-back');
  if (step2Back) {
    step2Back.addEventListener('click', () => goToStep(1));
  }

  const step2Submit = document.getElementById('btn-step-2-submit');
  if (step2Submit) {
    step2Submit.addEventListener('click', submitBookingDetails);
  }

  // UTR submission button
  const utrBtn = document.getElementById('btn-submit-utr');
  if (utrBtn) {
    utrBtn.addEventListener('click', submitUTR);
  }

  // Copy helper buttons
  document.querySelectorAll('.copy-trigger').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const text = btn.getAttribute('data-copy');
      if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
          window.showToast(`Copied to clipboard: ${text}`, '📋');
        });
      } else {
        window.showToast(`Copy: ${text}`, '📋');
      }
    });
  });
}

window.openBookingModal = function(packageSlug) {
  const modal = document.getElementById('booking-modal');
  if (!modal) return;

  // Reset steps
  goToStep(1);

  // Fetch package details from API
  fetch(`/api/packages/${packageSlug}`)
    .then(r => r.json())
    .then(pkg => {
      currentPackage = pkg;
      document.getElementById('modal-package-name').textContent = pkg.name;
      document.getElementById('modal-package-tagline').textContent = pkg.tagline || '';
      document.getElementById('modal-package-duration').textContent = pkg.duration;
      
      // Update form
      updatePriceSummary();

      // Ensure modal Google Form link is synced
      const modalGFormLink = document.getElementById('modal-google-form-link');
      if (modalGFormLink && window.HAPPYMILES_CONFIG) {
        modalGFormLink.href = window.HAPPYMILES_CONFIG.bookingFormUrl;
      }

      modal.classList.add('open');
    })
    .catch(err => {
      console.error(err);
      window.showToast('Could not load package details. Please try again.', '⚠️');
    });
};

function closeBookingModal() {
  const modal = document.getElementById('booking-modal');
  if (modal) modal.classList.remove('open');
}

function goToStep(step) {
  currentStep = step;
  document.querySelectorAll('.booking-step-content').forEach(el => el.style.display = 'none');
  const target = document.getElementById(`booking-step-${step}`);
  if (target) target.style.display = 'block';

  // Update indicators
  for (let i = 1; i <= 3; i++) {
    const ind = document.getElementById(`step-indicator-${i}`);
    if (ind) {
      if (i === step) {
        ind.className = 'step-indicator active';
      } else if (i < step) {
        ind.className = 'step-indicator completed';
      } else {
        ind.className = 'step-indicator';
      }
    }
  }
}

function updatePriceSummary() {
  if (!currentPackage) return;

  const travelers = parseInt(document.getElementById('booking-travelers').value, 10) || 1;
  const unitPrice = currentPackage.price;
  const totalPrice = unitPrice * travelers;

  const unitAdvance = currentPackage.advance_price && currentPackage.advance_price > 0
    ? currentPackage.advance_price
    : Math.round(unitPrice * 0.3);
  const totalAdvance = unitAdvance * travelers;

  const isFull = document.getElementById('pay-type-full').classList.contains('selected');
  const dueNow = isFull ? totalPrice : totalAdvance;
  const balanceDue = isFull ? 0 : (totalPrice - totalAdvance);

  document.getElementById('display-advance-amt').textContent = `₹${totalAdvance.toLocaleString()}`;
  document.getElementById('display-full-amt').textContent = `₹${totalPrice.toLocaleString()}`;
  document.getElementById('summary-total-amt').textContent = `₹${totalPrice.toLocaleString()}`;
  document.getElementById('summary-due-now').textContent = `₹${dueNow.toLocaleString()}`;
  document.getElementById('summary-balance').textContent = `₹${balanceDue.toLocaleString()}`;

  // Update pay button text
  const step2Btn = document.getElementById('btn-step-2-submit');
  if (step2Btn) {
    step2Btn.innerHTML = `Proceed to Pay ₹${dueNow.toLocaleString()} <span>→</span>`;
  }
}

function submitBookingDetails() {
  const name = document.getElementById('booking-name').value.trim();
  const phone = document.getElementById('booking-phone').value.trim();
  const email = document.getElementById('booking-email').value.trim();
  const date = document.getElementById('booking-date').value;
  const travelers = parseInt(document.getElementById('booking-travelers').value, 10) || 1;
  const isFull = document.getElementById('pay-type-full').classList.contains('selected');
  const payType = isFull ? 'full' : 'advance';
  const pickup = document.getElementById('booking-pickup').value;
  const notes = document.getElementById('booking-notes').value.trim();

  // Gentle validation
  if (!name || name.length < 2) {
    window.showToast('Oops, could you please enter your full name?', '✍️');
    document.getElementById('booking-name').focus();
    return;
  }

  if (!phone || phone.length < 10) {
    window.showToast('Please provide a valid 10-digit WhatsApp/phone number', '📱');
    document.getElementById('booking-phone').focus();
    return;
  }

  const payload = {
    package_slug: currentPackage.slug,
    customer_name: name,
    phone: phone,
    email: email || null,
    travel_date: date,
    travelers: travelers,
    pay_type: payType,
    pickup_point: pickup || null,
    notes: notes || null
  };

  const btn = document.getElementById('btn-step-2-submit');
  btn.disabled = true;
  btn.textContent = 'Securing your booking...';

  fetch('/api/bookings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
    .then(r => {
      if (!r.ok) return r.json().then(e => { throw new Error(e.detail || 'Booking failed'); });
      return r.json();
    })
    .then(booking => {
      currentBooking = booking;
      btn.disabled = false;
      renderPaymentSheet(booking);
      goToStep(3);
    })
    .catch(err => {
      btn.disabled = false;
      btn.innerHTML = `Try Again <span>→</span>`;
      window.showToast(err.message, '⚠️');
    });
}

function renderPaymentSheet(booking) {
  document.getElementById('pay-sheet-ref').textContent = booking.ref;
  const dueNow = booking.pay_type === 'advance' ? booking.advance_amount : booking.total_amount;
  document.getElementById('pay-sheet-amount').textContent = `₹${dueNow.toLocaleString()}`;

  // Configure Deep Link UPI button
  const upiUrl = `upi://pay?pa=7661981338@kotakbank&pn=HappyMiles%20Tours&am=${dueNow}&cu=INR&tn=Trip-${booking.ref}`;
  const upiLinkBtn = document.getElementById('upi-deep-link');
  if (upiLinkBtn) {
    upiLinkBtn.href = upiUrl;
  }
}

function submitUTR() {
  if (!currentBooking) return;
  const utrInput = document.getElementById('booking-utr');
  const utrVal = utrInput.value.trim();

  if (!utrVal || utrVal.length < 6) {
    window.showToast('Please enter the 12-digit UPI / Bank Reference (UTR) number', '🔢');
    utrInput.focus();
    return;
  }

  const btn = document.getElementById('btn-submit-utr');
  btn.disabled = true;
  btn.textContent = 'Verifying reference...';

  fetch(`/api/bookings/${currentBooking.ref}/utr`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ utr: utrVal })
  })
    .then(r => {
      if (!r.ok) return r.json().then(e => { throw new Error(e.detail || 'Verification error'); });
      return r.json();
    })
    .then(updated => {
      btn.disabled = false;
      showSuccessScreen(updated);
    })
    .catch(err => {
      btn.disabled = false;
      btn.textContent = 'Submit UTR';
      window.showToast(err.message, '⚠️');
    });
}

function showSuccessScreen(booking) {
  // Hide step 3, show success container
  document.getElementById('booking-step-3').style.display = 'none';
  const successContainer = document.getElementById('booking-success-screen');
  successContainer.style.display = 'block';

  document.getElementById('success-booking-ref').textContent = booking.ref;
  const amountPaid = booking.pay_type === 'advance' ? booking.advance_amount : booking.total_amount;

  // Craft polite WhatsApp notification message
  const msg = `Hello HappyMiles Tours! 🎒✨\n\nI have just booked a trip on your website.\n\n` +
    `*Booking Ref:* ${booking.ref}\n` +
    `*Destination:* ${booking.package_name}\n` +
    `*Travel Date:* ${booking.travel_date}\n` +
    `*Travelers:* ${booking.travelers}\n` +
    `*Payment Mode:* ${booking.pay_type.toUpperCase()} (₹${amountPaid.toLocaleString()})\n` +
    `*UTR / Ref No.:* ${booking.utr}\n` +
    `*Name:* ${booking.customer_name}\n` +
    `*Phone:* ${booking.phone}\n\n` +
    `Please confirm my booking and share trip captain details. Thank you!`;

  const waBtn = document.getElementById('btn-whatsapp-confirm');
  if (waBtn) {
    waBtn.href = `https://wa.me/918074016910?text=${encodeURIComponent(msg)}`;
  }

  // Confetti effect if library loaded
  if (window.confetti) {
    window.confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
  }
}
