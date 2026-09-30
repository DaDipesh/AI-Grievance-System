(() => {
  const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  async function refreshReminders() {
    try {
      const notes = await SG_API.notifications();
      let panel = document.querySelector('#officerReminderPanel');
      if (!panel) {
        panel = document.createElement('section');
        panel.id = 'officerReminderPanel';
        panel.className = 'bg-dark rounded-4 p-3 mb-4';
        panel.innerHTML = '<h5>Citizen reminders</h5><div class="small" id="officerReminderList"></div>';
        document.querySelector('#message')?.after(panel);
      }
      const reminders = notes.filter(note => ['Citizen reminder', 'नागरिक का अनुस्मारक'].includes(note.title)).slice(0, 12);
      panel.querySelector('#officerReminderList').innerHTML = reminders.length
        ? reminders.map(note => `<div style="padding:9px 0;border-bottom:1px solid #274760"><b>${escapeHtml(note.title)}</b> · ${escapeHtml(note.message)}<small class="d-block text-secondary">${new Date(note.created_at).toLocaleString()}</small></div>`).join('')
        : 'No citizen reminders yet.';
    } catch {}
  }
  refreshReminders();
  setInterval(() => { if (document.visibilityState === 'visible') refreshReminders(); }, 5000);
})();
