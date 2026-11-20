/**
 * HappyMiles Tours — Admin Dashboard Script
 * Authentication, Bookings Management, UTR Verification, Package CRUD
 */

let adminAuthHeader = localStorage.getItem('happymiles_admin_auth') || '';
let currentBookings = [];
let currentPackages = [];

document.addEventListener('DOMContentLoaded', () => {
  if (!adminAuthHeader) {
    promptLogin();
  } else {
    loadDashboard();
  }

  // Filter tabs
  document.querySelectorAll('.status-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.status-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      filterBookingsTable();
    });
  });

  // Search input
  const searchInput = document.getElementById('admin-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', filterBookingsTable);
  }

  // Export CSV
  const exportBtn = document.getElementById('btn-export-csv');
  if (exportBtn) {
    exportBtn.addEventListener('click', () => {
      window.location.href = '/api/admin/bookings/export';
    });
  }

  // Logout button
  const logoutBtn = document.getElementById('btn-admin-logout');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('happymiles_admin_auth');
      window.location.reload();
    });
  }
});

function promptLogin() {
  const user = prompt('Enter Admin Username (default: admin):', 'admin');
  const pass = prompt('Enter Admin Password (default: happymiles2026):', 'happymiles2026');
  if (user && pass) {
    adminAuthHeader = 'Basic ' + btoa(`${user}:${pass}`);
    localStorage.setItem('happymiles_admin_auth', adminAuthHeader);
    loadDashboard();
  } else {
    document.body.innerHTML = '<div style="padding:4rem;text-align:center;"><h2>Access Restricted</h2><p>Please reload and provide admin credentials.</p></div>';
  }
}

function adminFetch(url, options = {}) {
  options.headers = options.headers || {};
  options.headers['Authorization'] = adminAuthHeader;
  return fetch(url, options).then(res => {
    if (res.status === 401) {
      localStorage.removeItem('happymiles_admin_auth');
      alert('Invalid admin credentials. Please try again.');
      window.location.reload();
      throw new Error('Unauthorized');
    }
    return res;
  });
}

function loadDashboard() {
  loadStats();
  loadBookings();
  loadPackages();
}

function loadStats() {
  adminFetch('/api/admin/stats')
    .then(r => r.json())
    .then(stats => {
      document.getElementById('stat-total-bookings').textContent = stats.total_bookings;
      document.getElementById('stat-pending-utr').textContent = stats.payment_submitted;
      document.getElementById('stat-confirmed').textContent = stats.confirmed;
      document.getElementById('stat-revenue').textContent = `₹${stats.total_revenue.toLocaleString()}`;
    })
    .catch(console.error);
}

function loadBookings() {
  adminFetch('/api/admin/bookings')
    .then(r => r.json())
    .then(bookings => {
      currentBookings = bookings;
      filterBookingsTable();
    })
    .catch(console.error);
}

function filterBookingsTable() {
  const activeTab = document.querySelector('.status-tab.active');
  const statusFilter = activeTab ? activeTab.getAttribute('data-status') : 'all';
  const query = (document.getElementById('admin-search-input')?.value || '').toLowerCase().trim();

  let filtered = currentBookings;
  if (statusFilter !== 'all') {
    filtered = filtered.filter(b => b.status === statusFilter);
  }
  if (query) {
    filtered = filtered.filter(b =>
      b.ref.toLowerCase().includes(query) ||
      b.customer_name.toLowerCase().includes(query) ||
      b.phone.includes(query) ||
      (b.utr && b.utr.toLowerCase().includes(query)) ||
      b.package_name.toLowerCase().includes(query)
    );
  }

  renderBookingsTable(filtered);
}

function renderBookingsTable(bookings) {
  const tbody = document.getElementById('bookings-tbody');
  if (!tbody) return;

  if (bookings.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;padding:2rem;color:#888;">No bookings found matching criteria.</td></tr>`;
    return;
  }

  tbody.innerHTML = bookings.map(b => {
    const statusClass = `status-${b.status}`;
    const paidAmt = b.pay_type === 'advance' ? b.advance_amount : b.total_amount;
    const utrHtml = b.utr
      ? `<span class="utr-code">${b.utr}</span>`
      : `<span style="color:#aaa;font-size:0.8rem;">None yet</span>`;

    return `
      <tr>
        <td><strong>${b.ref}</strong><br><small style="color:#888;">${new Date(b.created_at).toLocaleDateString()}</small></td>
        <td><strong>${b.customer_name}</strong><br><small style="color:#666;">📞 ${b.phone}</small></td>
        <td>${b.package_name}<br><small style="color:#888;">📅 ${b.travel_date} (${b.travelers} pax)</small></td>
        <td>
          <strong>₹${paidAmt.toLocaleString()}</strong> 
          <small style="color:#0b8a8f;">(${b.pay_type})</small>
          <br><small style="color:#888;">Total: ₹${b.total_amount.toLocaleString()}</small>
        </td>
        <td>${utrHtml}</td>
        <td><span class="badge-status ${statusClass}">${b.status.replace('_', ' ')}</span></td>
        <td>
          <select class="action-select" onchange="updateBookingStatus('${b.ref}', this.value)">
            <option value="pending" ${b.status === 'pending' ? 'selected' : ''}>Pending</option>
            <option value="payment_submitted" ${b.status === 'payment_submitted' ? 'selected' : ''}>Payment Submitted</option>
            <option value="paid" ${b.status === 'paid' ? 'selected' : ''}>Paid (Verified)</option>
            <option value="confirmed" ${b.status === 'confirmed' ? 'selected' : ''}>Confirmed</option>
            <option value="cancelled" ${b.status === 'cancelled' ? 'selected' : ''}>Cancelled</option>
          </select>
        </td>
      </tr>
    `;
  }).join('');
}

window.updateBookingStatus = function(ref, newStatus) {
  adminFetch(`/api/admin/bookings/${ref}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: newStatus })
  })
    .then(r => r.json())
    .then(updated => {
      alert(`Booking ${ref} updated to ${newStatus.toUpperCase()}`);
      loadDashboard();
    })
    .catch(err => alert('Failed to update status: ' + err.message));
};

function loadPackages() {
  fetch('/api/packages?active_only=false')
    .then(r => r.json())
    .then(pkgs => {
      currentPackages = pkgs;
      renderPackagesList(pkgs);
    })
    .catch(console.error);
}

function renderPackagesList(pkgs) {
  const container = document.getElementById('packages-admin-grid');
  if (!container) return;

  container.innerHTML = pkgs.map(p => `
    <div style="background:#fff;border-radius:12px;padding:1.2rem;border:1px solid #e2e8f0;display:flex;align-items:center;justify-content:space-between;gap:1rem;">
      <div>
        <h4 style="margin:0 0 4px;">${p.name}</h4>
        <p style="margin:0;font-size:0.85rem;color:#64748b;">Duration: ${p.duration} | Price: ₹${p.price.toLocaleString()} | Advance: ₹${(p.advance_price || p.price * 0.3).toLocaleString()}</p>
        <span style="display:inline-block;margin-top:6px;font-size:0.75rem;padding:2px 8px;border-radius:4px;background:${p.active ? '#dcfce7' : '#fee2e2'};color:${p.active ? '#15803d' : '#991b1b'};font-weight:600;">
          ${p.active ? 'ACTIVE' : 'HIDDEN'}
        </span>
      </div>
      <div style="display:flex;gap:8px;">
        <button onclick="togglePackageActive(${p.id}, ${!p.active})" style="padding:6px 12px;border-radius:6px;background:#f1f5f9;border:1px solid #cbd5e1;cursor:pointer;font-size:0.85rem;">
          ${p.active ? 'Hide' : 'Activate'}
        </button>
      </div>
    </div>
  `).join('');
}

window.togglePackageActive = function(id, newState) {
  adminFetch(`/api/admin/packages/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ active: newState })
  })
    .then(() => loadPackages())
    .catch(err => alert('Error: ' + err.message));
};
