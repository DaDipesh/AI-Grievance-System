/* Connects the existing Nivaran UI to the real FastAPI + AI backend. */
(() => {
  const $ = s => document.querySelector(s);
  const lang = () => localStorage.getItem('sg_lang') || 'en';
  const hi = () => lang() === 'hi';
  const t = (en, h) => hi() ? h : en;
  const esc = value => String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const token = () => localStorage.getItem('sg_access_token');
  const user = () => { try { return JSON.parse(localStorage.getItem('sg_user') || '{}'); } catch { return {}; } };
  if (!window.SG_API) return;
  if (!token()) { location.replace('login.html'); return; }

  function toast(msg) { window.showToast ? window.showToast(msg) : alert(msg); }
  function statusText(s) { return esc((s || '').replaceAll('_',' ')); }
  function ensureSubmitButton() {
    if ($('#submitComplaintBackendBtn')) return $('#submitComplaintBackendBtn');
    const b = document.createElement('button');
    b.id='submitComplaintBackendBtn'; b.type='button'; b.className='btn-main w-100 mt-3'; b.disabled=true;
    b.innerHTML='<i class="bi bi-send-fill"></i> '+t('Submit Complaint','शिकायत दर्ज करें')+' <i class="bi bi-arrow-right"></i>';
    $('#analyzeComplaintBtn')?.insertAdjacentElement('afterend',b); return b;
  }
  const submitBtn = ensureSubmitButton();
  let previewPayload=null, uploadedEvidence='';

  $('#complaintImage')?.addEventListener('change',()=>{
    uploadedEvidence=''; previewPayload=null; submitBtn.disabled=true;
  });
  ['#complaintText','#complaintLocation'].forEach(selector=>$(selector)?.addEventListener('input',()=>{
    previewPayload=null; submitBtn.disabled=true;
  }));

  async function uploadEvidenceIfNeeded() {
    const input=$('#complaintImage'), file=input?.files?.[0];
    if(!file) return '';
    if(file.size>5*1024*1024) throw new Error(t('Image must be 5 MB or smaller.','फोटो 5 MB या उससे छोटी होनी चाहिए।'));
    if(uploadedEvidence) return uploadedEvidence;
    const result=await SG_API.uploadEvidence(file); uploadedEvidence=result.file_id; return uploadedEvidence;
  }

  function locationPayload() {
    const profile=JSON.parse(localStorage.getItem('sg_profile')||'{}');
    const locations=window.grievanceLocations||{};
    const point=locations.problem||locations.current||null;
    return {
      city: user().city || profile.city || '', district: profile.district || '', state: user().state || profile.state || '',
      area: $('#complaintLocation')?.value.trim() || profile.village || '',
      latitude: point?.latitude ?? null, longitude: point?.longitude ?? null,
      location_source: locations.problem ? 'MAP_PIN' : (locations.current ? 'CURRENT' : null)
    };
  }

  async function runPreview(event) {
    event.preventDefault(); event.stopImmediatePropagation();
    const text=$('#complaintText')?.value.trim();
    if(!text){toast(t('Please enter a complaint first.','पहले शिकायत लिखें।'));$('#complaintText')?.focus();return;}
    const loc=locationPayload();
    if(!loc.area && (loc.latitude==null || loc.longitude==null)){toast(t('Enter an area or choose a location pin.','क्षेत्र दर्ज करें या स्थान पिन चुनें।'));return;}
    const btn=$('#analyzeComplaintBtn'); btn.disabled=true; btn.innerHTML='<span class="spinner-border spinner-border-sm"></span> '+t('Analyzing with AI…','AI से विश्लेषण हो रहा है…');
    try {
      const evidence=await uploadEvidenceIfNeeded();
      const payload={complaint_text:text,...loc,evidence_file_id:evidence||null};
      const result=await SG_API.previewComplaint(payload); previewPayload={...payload,preview_token:result.preview_token};
      $('#resultEmpty')?.classList.add('d-none'); $('#aiResult')?.classList.remove('d-none'); $('#resultState').textContent=t('ANALYZED','विश्लेषित');
      $('#resultTicket').textContent=result.ticket_number; $('#resultCategory').textContent=result.category_predicted||'-'; $('#resultPriority').textContent=result.priority||'-';
      $('#resultSentiment').textContent=t('Detected by AI','AI द्वारा निर्धारित'); $('#resultImpact').textContent=result.duplicate_flag?t('Possible duplicate','संभावित डुप्लीकेट'):(result.severity||'-');
      $('#resultDepartment').textContent=result.department||'-'; $('#resultEta').textContent=result.estimated_resolution_hours!=null?`${result.estimated_resolution_hours} ${t('hours','घंटे')}`:'-';
      $('#resultEmergency').textContent=result.severity==='Critical'||result.priority==='Urgent'?t('Critical/Urgent','गंभीर/तत्काल'):t('Not critical','सामान्य');
      $('#resultSentiment').textContent=result.severity||'-';
      $('#resultImpact').textContent=result.estimated_resolution_hours==null?'-':`${result.estimated_resolution_hours} h`;
      $('#previewLocation').textContent=[loc.area,loc.city,loc.district,loc.state].filter(Boolean).join(', ')||t('Location pin selected','स्थान पिन चुना गया');
      $('#previewComplaintText').textContent=result.response?`${text}\n\n${result.response}`:text;
      submitBtn.disabled=false;
      if(result.response) toast(result.response); else toast(t('AI analysis completed. Review the result and submit.','AI विश्लेषण पूरा हुआ। परिणाम देखकर शिकायत दर्ज करें।'));
      window.lastAIResult=result;
    } catch(e) { toast(e.message); submitBtn.disabled=true; }
    finally { btn.disabled=false; btn.innerHTML='<i class="bi bi-stars"></i> '+t('Analyze Complaint with AI','AI से शिकायत का विश्लेषण करें')+' <i class="bi bi-arrow-right"></i>'; }
  }

  document.addEventListener('click', e => {
    if(e.target.closest('#analyzeComplaintBtn')) runPreview(e);
  }, true);

  submitBtn?.addEventListener('click', async()=>{
    if(!previewPayload) return;
    submitBtn.disabled=true; submitBtn.innerHTML='<span class="spinner-border spinner-border-sm"></span> '+t('Submitting…','जमा किया जा रहा है…');
    try {
      const complaint=await SG_API.createComplaint(previewPayload);
      previewPayload=null;
      uploadedEvidence=''; if($('#complaintImage'))$('#complaintImage').value='';
      localStorage.setItem('sg_last_complaint_id',String(complaint.id)); localStorage.setItem('sg_last_ticket',complaint.ticket_number);
      toast(lang()==='hi'?`\u0936\u093f\u0915\u093e\u092f\u0924 ${complaint.ticket_number} \u0938\u092b\u0932\u0924\u093e\u092a\u0942\u0930\u094d\u0935\u0915 \u0926\u0930\u094d\u091c \u0939\u094b \u0917\u0908 \u0939\u0948\u0964`:`Report successfully registered. Ticket: ${complaint.ticket_number}`);
      renderComplaintResult(complaint); await refreshCitizenData();
    } catch(e) { toast(e.message); }
    finally { submitBtn.disabled=!previewPayload; submitBtn.innerHTML='<i class="bi bi-send-fill"></i> '+t('Submit Complaint','शिकायत दर्ज करें')+' <i class="bi bi-arrow-right"></i>'; }
  });

  function renderComplaintResult(c){
    $('#resultTicket').textContent=c.ticket_number; $('#resultCategory').textContent=c.category_predicted||'-'; $('#resultPriority').textContent=c.priority||'-';
    $('#resultDepartment').textContent=c.department||'-'; $('#resultEta').textContent=c.estimated_resolution_hours!=null?`${c.estimated_resolution_hours} ${t('hours','घंटे')}`:'-';
    $('#resultEmergency').textContent=c.status==='resolved'?t('Resolved','समाधान हो गया'):t('Pending','लंबित'); $('#resultState').textContent=t('SUBMITTED','दर्ज');
  }

  async function refreshCitizenData(){
    try{
      const [complaints,notes]=await Promise.all([SG_API.complaints(),SG_API.notifications()]);
      const feedbackRows=await Promise.all(complaints.filter(c=>['resolved','rejected','closed'].includes(c.status)).map(async c=>[c.id,await SG_API.getFeedback(c.id).catch(()=>null)]));
      window.sgFeedbackState=Object.fromEntries(feedbackRows.filter(([,feedback])=>feedback).map(([id])=>[id,true]));
      window.sgComplaints=complaints; window.sgNotifications=notes;
      renderNotifications(notes); renderCitizenStats(complaints); renderCitizenDashboard(complaints); renderCitizenMap(complaints);
    }catch(e){ if(e.status===401) logout(); }
  }
  function renderNotifications(notes){
    let box=$('#sgNotificationsPanel'); if(!box){box=document.createElement('div');box.id='sgNotificationsPanel';box.style.cssText='position:fixed;right:18px;bottom:18px;width:min(380px,calc(100vw - 36px));max-height:55vh;overflow:auto;background:#0b1628;color:#fff;padding:16px;border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,.35);z-index:2000;display:none';document.body.appendChild(box)}
    box.innerHTML=`<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px"><strong>${t('Notifications','सूचनाएँ')}</strong><button id="closeSgNotifications" class="btn btn-sm btn-outline-light">×</button></div>`+(notes.length?notes.slice(0,20).map(n=>`<div data-notification-id="${n.id}" style="padding:10px;border-bottom:1px solid rgba(255,255,255,.1);opacity:${n.is_read ? .6 : 1}"><b>${n.title}</b><div style="font-size:13px;margin-top:4px">${n.message}</div></div>`).join(''):`<div style="opacity:.7">${t('No notifications yet.','अभी कोई सूचना नहीं है।')}</div>`);
    $('#closeSgNotifications').onclick=()=>box.style.display='none';
  }
  function renderCitizenStats(complaints){
    const total=complaints.length,resolved=complaints.filter(c=>['resolved','closed'].includes(c.status)).length,pending=complaints.filter(c=>c.status==='pending').length,progress=complaints.filter(c=>c.status==='in_progress').length;
    const nodes=document.querySelectorAll('[data-sg-stat]'); nodes.forEach(n=>{const k=n.dataset.sgStat;n.textContent=k==='total'?total:k==='resolved'?resolved:k==='pending'?pending:k==='progress'?progress:0});
  }
  function renderCitizenDashboard(complaints){
    const section=$('#dashboard'), body=section?.querySelector('.container'); if(!body)return;
    $('#citizenDashboardLoading')?.remove();
    body.querySelectorAll(':scope > .row').forEach(row=>row.remove());
    let panel=$('#citizenComplaintList'); if(!panel){panel=document.createElement('div');panel.id='citizenComplaintList';panel.className='dash-panel mt-4';body.appendChild(panel);}
    const feedbackState=window.sgFeedbackState||{};
    const rows=complaints.map(c=>{const status=(c.status||'pending').toLowerCase(),statusClass=['pending','in_progress','resolved','rejected','reopened','closed'].includes(status)?status.replace('_','-'):'pending',photo=c.evidence_path?`<button type="button" class="btn btn-sm btn-outline-info view-evidence" data-evidence="${esc(c.evidence_path)}">View photo</button>`:'-',action=['pending','in_progress'].includes(status)?`<button type="button" class="btn btn-sm btn-outline-warning complaint-reminder" data-id="${c.id}">Reminder</button>`:['resolved','rejected','closed'].includes(status)?(feedbackState[c.id]?'Feedback sent':`<button type="button" class="btn btn-sm btn-outline-success complaint-feedback" data-id="${c.id}">Feedback</button>`):'—';return `<tr><td><a href="#track" data-track-ticket="${esc(c.ticket_number)}">${esc(c.ticket_number)}</a></td><td>${esc(c.category_predicted||'-')}</td><td>${esc(c.priority||'-')} / ${esc(c.severity||'-')}</td><td>${esc(c.department||'-')}</td><td>${esc(c.city||'-')}${c.area?', '+esc(c.area):''}</td><td>${photo}</td><td><span class="complaint-status status-${statusClass}">${statusText(status)}</span></td><td>${action}</td><td>${c.estimated_resolution_hours==null?'-':`${esc(c.estimated_resolution_hours)} h`}</td><td>${esc(new Date(c.created_at).toLocaleDateString())}</td></tr>`}).join('');
    panel.innerHTML=`<h3>My complaints</h3><div class="table-responsive"><table class="table table-dark table-hover"><thead><tr><th>Ticket</th><th>Category</th><th>Priority / Severity</th><th>Department</th><th>Location</th><th>Photo</th><th>Status</th><th>Action</th><th>Est. resolution</th><th>Created</th></tr></thead><tbody>${rows||'<tr><td colspan="10">No complaints submitted yet.</td></tr>'}</tbody></table></div>`;
    panel.querySelectorAll('.view-evidence').forEach(button=>button.addEventListener('click',()=>SG_API.viewEvidence(button.dataset.evidence).catch(error=>toast(error.message))));
    panel.querySelectorAll('.complaint-reminder').forEach(button=>button.addEventListener('click',async()=>{button.disabled=true;try{await SG_API.reminder(button.dataset.id);toast(t('Reminder sent to the officer.','अधिकारी को अनुस्मारक भेज दिया गया है।'));}catch(error){toast(error.message)}finally{button.disabled=false}}));
    panel.querySelectorAll('.complaint-feedback').forEach(button=>button.addEventListener('click',()=>openFeedbackDialog(button.dataset.id)));
  }
  function openFeedbackDialog(id){
    let dialog=$('#sgFeedbackDialog');if(!dialog){dialog=document.createElement('dialog');dialog.id='sgFeedbackDialog';dialog.style.cssText='width:min(480px,calc(100% - 24px));border:1px solid #37617d;border-radius:18px;padding:22px;background:#0c2035;color:#eaf4ff';dialog.innerHTML='<form method="dialog"><div style="display:flex;justify-content:space-between;align-items:center"><h3>Complaint feedback</h3><button class="btn btn-sm btn-outline-light" value="cancel">×</button></div><label>Rating</label><select id="sgFeedbackRating" class="form-select my-2"><option value="5">5 - Excellent</option><option value="4">4 - Good</option><option value="3">3 - Average</option><option value="2">2 - Poor</option><option value="1">1 - Very poor</option></select><label for="sgFeedbackComment">Comment (optional)</label><textarea id="sgFeedbackComment" class="form-control my-2" rows="3" maxlength="1000"></textarea><button id="sgSubmitFeedback" type="button" class="btn btn-success mt-2">Submit feedback</button></form>';document.body.appendChild(dialog)}
    dialog.showModal();dialog.querySelector('#sgSubmitFeedback').onclick=async()=>{const submit=dialog.querySelector('#sgSubmitFeedback');submit.disabled=true;try{await SG_API.feedback(id,Number(dialog.querySelector('#sgFeedbackRating').value),dialog.querySelector('#sgFeedbackComment').value.trim());dialog.close();window.sgFeedbackState=window.sgFeedbackState||{};window.sgFeedbackState[id]=true;toast(t('Feedback sent to the administration.','प्रतिक्रिया प्रशासन को भेज दी गई है।'));renderCitizenDashboard(window.sgComplaints||[])}catch(error){toast(error.message)}finally{submit.disabled=false}};
  }
  function renderCitizenMap(complaints){
    const map=window.grievanceMap; if(!map||!window.L)return;
    if(window.sgComplaintMarkers) window.sgComplaintMarkers.forEach(marker=>map.removeLayer(marker));
    window.sgComplaintMarkers=[];
    complaints.filter(c=>Number.isFinite(c.latitude)&&Number.isFinite(c.longitude)).forEach(c=>{
      const marker=window.L.marker([c.latitude,c.longitude]).addTo(map);
      const popup=document.createElement('span'); popup.textContent=`${c.ticket_number} · ${c.category_predicted||''} · ${statusText(c.status)}`;
      marker.bindPopup(popup); window.sgComplaintMarkers.push(marker);
    });
  }
  function logout(){SG_API.clearSession();location.href='login.html'}

  $('#logoutBtn')?.addEventListener('click',e=>{e.preventDefault();logout()});
  // Track by ticket number OR numeric complaint ID.
  document.addEventListener('click', async e=>{
    if(!e.target.closest('#trackButton')) return;
    e.preventDefault();e.stopImmediatePropagation();
    const value=$('#trackingId')?.value.trim(); if(!value){toast(t('Enter a ticket number.','टिकट नंबर दर्ज करें।'));return}
    try{
      const c=await SG_API.complaintByTicket(value.toUpperCase()).catch(async err=>{if(err.status!==404)throw err;const complaints=await SG_API.complaints();return complaints.find(x=>String(x.id)===value)||null});
      if(!c) throw new Error(t('Complaint not found.','शिकायत नहीं मिली।'));
      const history=await SG_API.history(c.id); const box=$('#trackingResult'); box?.classList.remove('d-none');
      if(box){box.innerHTML=`<div class="ticket-summary"><div><small>TICKET</small><b>${c.ticket_number}</b></div><span>${statusText(c.status).toUpperCase()}</span></div><div style="margin-top:14px"><b>${c.category_predicted||'-'}</b> • ${c.priority||'-'} • ${c.department||'-'}<br><small>${c.city||''}${c.area?', '+c.area:''}</small></div><div style="margin-top:12px">${history.map(h=>`<div style="padding:6px 0;border-bottom:1px solid rgba(148,163,184,.12)"><b>${statusText(h.new_status)}</b><small style="display:block">${h.note||''}</small></div>`).join('')}</div>`}
      toast(t('Complaint status loaded.','शिकायत की स्थिति लोड हो गई।'));
    }catch(e){toast(e.message)}
  },true);

  // Notification button is added without changing the existing navigation.
  const nav=document.querySelector('.navbar-nav'); if(nav && !$('#sgNotificationBtn')){const li=document.createElement('li');li.className='ms-lg-2';li.innerHTML='<button id="sgNotificationBtn" class="theme-toggle" type="button" title="Notifications"><i class="bi bi-bell"></i></button>';nav.insertBefore(li,nav.lastElementChild);$('#sgNotificationBtn').onclick=()=>{const p=$('#sgNotificationsPanel');if(p){p.style.display=p.style.display==='none'?'block':'none'}}}
  refreshCitizenData();
  setInterval(()=>{if(document.visibilityState==='visible')refreshCitizenData()},5000);
  SG_API.me().then(u=>{localStorage.setItem('sg_user',JSON.stringify(u));localStorage.setItem('sg_lang',u.preferred_language||lang());if(u.role!=='citizen')location.replace(u.role==='officer'?'officer.html':'admin.html');}).catch(e=>{if(e.status===401){SG_API.clearSession();location.replace('login.html');}});
})();
