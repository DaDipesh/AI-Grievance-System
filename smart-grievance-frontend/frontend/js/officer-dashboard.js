(() => {
  const $ = selector => document.querySelector(selector);
  const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const statusLabels = {pending:'pending', in_progress:'in progress', resolved:'resolved', rejected:'rejected', closed:'closed'};
  let loading = false;

  const showMessage = (message, success = false) => {
    const box = $('#message');
    box.textContent = message;
    box.className = `alert ${success ? 'alert-success' : 'alert-danger'}`;
  };

  async function start() {
    if (!localStorage.getItem('sg_access_token')) return location.replace('login.html');
    const user = await SG_API.me();
    if (!['officer', 'admin'].includes(user.role)) return location.replace('index.html');
    $('#officerMeta').textContent = `${user.name || 'Officer'} • ${user.department || 'All departments'} • ${user.mobile || ''}`;
    $('#logout').onclick = () => { SG_API.clearSession(); location.replace('login.html'); };

    async function load() {
      if (loading || document.activeElement?.matches('.statusSelect')) return;
      loading = true;
      try {
        const complaints = await SG_API.officerComplaints();
        $('#total').textContent = complaints.length;
        $('#pending').textContent = complaints.filter(item => item.status === 'pending').length;
        $('#progress').textContent = complaints.filter(item => item.status === 'in_progress').length;
        $('#resolved').textContent = complaints.filter(item => ['resolved', 'closed'].includes(item.status)).length;

        $('#rows').innerHTML = complaints.map(item => {
          const currentStatus = item.status || 'pending';
          const choices = Object.entries(statusLabels).filter(([value]) => value !== currentStatus)
            .map(([value, label]) => `<option value="${value}">${label}</option>`).join('');
          const photo = item.evidence_path
            ? `<button type="button" class="btn btn-sm btn-outline-info view-evidence" data-evidence="${escapeHtml(item.evidence_path)}">View photo</button>`
            : '—';
          return `<tr>
            <td><b>#${item.id}</b><br><small>${escapeHtml(item.ticket_number)}</small></td>
            <td><b>${escapeHtml(item.citizen_name || `Citizen #${item.citizen_id}`)}</b><br><small>${escapeHtml(item.citizen_mobile || '')}</small></td>
            <td style="min-width:240px">${escapeHtml(item.complaint_text)}<br><small>${escapeHtml(item.category_predicted || '—')} • ${escapeHtml(item.priority || '—')} • ${escapeHtml(item.severity || '—')}</small></td>
            <td>${photo}</td>
            <td>${escapeHtml(item.city || '—')}${item.area ? `, ${escapeHtml(item.area)}` : ''}</td>
            <td>${escapeHtml(item.department || '—')}<br>${item.assigned_officer_id ? 'Assigned to you' : 'Department queue'}</td>
            <td><span class="badge bg-secondary">${escapeHtml(currentStatus.replaceAll('_', ' '))}</span></td>
            <td><select class="form-select form-select-sm statusSelect" data-id="${item.id}" aria-label="Choose a new complaint status"><option value="">Choose status…</option>${choices}</select><button class="btn btn-primary btn-sm mt-2 updateBtn" data-id="${item.id}" disabled>Update</button></td>
          </tr>`;
        }).join('') || '<tr><td colspan="8">No complaints assigned to this department.</td></tr>';

        document.querySelectorAll('.view-evidence').forEach(button => {
          button.onclick = () => SG_API.viewEvidence(button.dataset.evidence).catch(error => showMessage(error.message));
        });
        document.querySelectorAll('.statusSelect').forEach(select => {
          select.onchange = () => {
            const update = document.querySelector(`.updateBtn[data-id="${select.dataset.id}"]`);
            if (update) update.disabled = !select.value;
          };
        });
        document.querySelectorAll('.updateBtn').forEach(button => {
          button.onclick = async () => {
            const select = document.querySelector(`.statusSelect[data-id="${button.dataset.id}"]`);
            if (!select?.value) return;
            button.disabled = true;
            try {
              await SG_API.updateStatus(button.dataset.id, select.value);
              showMessage('Complaint status updated.', true);
              await load();
            } catch (error) {
              showMessage(error.message);
              button.disabled = false;
            }
          };
        });
      } catch (error) {
        if (error.status === 401) {
          SG_API.clearSession();
          location.replace('login.html');
        } else showMessage(error.message);
      } finally {
        loading = false;
      }
    }

    await load();
    setInterval(() => {
      if (document.visibilityState === 'visible') load();
    }, 5000);
  }

  start().catch(error => {
    if (error.status === 401) {
      SG_API.clearSession();
      location.replace('login.html');
    } else showMessage(error.message);
  });
})();
