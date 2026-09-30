/* Nivaran API client - connected to FastAPI backend. */
(() => {
  // Set <meta name="sg-api-base" content="..."> or window.SG_API_BASE_URL
  // when the frontend is hosted separately. Backend-hosted pages use same origin.
  // A page opened directly from disk has an opaque `null` origin and an empty
  // hostname. It still needs to call the local API explicitly.
  const isFileFrontend = window.location.protocol === 'file:';
  const isLocalFrontend = isFileFrontend || (['localhost','127.0.0.1'].includes(window.location.hostname) && window.location.port !== '8765');
  const localApiOrigin = `http://${window.location.hostname === 'localhost' ? 'localhost' : '127.0.0.1'}:8765`;
  const sameOrigin = window.location.origin;
  const configuredBase = window.SG_API_BASE_URL || document.querySelector('meta[name="sg-api-base"]')?.content || `${isLocalFrontend ? localApiOrigin : sameOrigin}/api/v1`;
  const API_BASE = configuredBase.replace(/\/$/, '');
  const getToken = () => localStorage.getItem('sg_access_token') || '';
  const jsonHeaders = () => ({'Content-Type':'application/json', ...(getToken()?{'Authorization':`Bearer ${getToken()}`}:{})});
  async function request(path, options={}) {
    const headers = {...(options.body instanceof FormData ? {} : {'Content-Type':'application/json'}), ...(getToken()?{'Authorization':`Bearer ${getToken()}`}:{}) , ...(options.headers||{})};
    let r;
    try { r = await fetch(`${API_BASE}${path}`, {...options, cache:'no-store', headers}); }
    catch (cause) { const e=new Error(`Could not connect to Nivaran backend at ${API_BASE}. Start the “Nivaran API (FastAPI)” task, then retry.`); e.cause=cause; throw e; }
    let data=null; try { data=await r.json(); } catch {}
    if (!r.ok) { const language=localStorage.getItem('sg_lang')||'en'; const friendly={401:language==='hi'?'कृपया फिर से लॉगिन करें।':'Please log in again.',403:language==='hi'?'आपको इसकी अनुमति नहीं है।':'You are not authorized to do that.',404:language==='hi'?'जानकारी नहीं मिली।':'The requested information was not found.',409:language==='hi'?'यह बदलाव पहले ही हो चुका है या संभव नहीं है।':'This change was already made or conflicts with the current state.',422:language==='hi'?'कृपया दर्ज की गई जानकारी जाँचें।':'Please check the information you entered.',429:language==='hi'?'बहुत अधिक अनुरोध हुए। थोड़ी देर बाद प्रयास करें।':'Too many requests. Please try again shortly.',500:language==='hi'?'सर्वर में समस्या है। कृपया बाद में प्रयास करें।':'The server encountered a problem. Please try again later.',503:language==='hi'?'SMS सेवा उपलब्ध नहीं है। सहायता से संपर्क करें।':'SMS delivery is unavailable. Please contact support.'}; const detail=data?.detail; let message;if(Array.isArray(detail)){const emailError=detail.some(item=>Array.isArray(item.loc)&&item.loc.includes('email'));message=emailError?(language==='hi'?'कृपया सही ईमेल पता दर्ज करें, जैसे name@example.com।':'Enter a valid email address, for example name@example.com.'):friendly[r.status]||friendly[500]}else if(!detail||String(detail).includes('Traceback'))message=friendly[r.status]||friendly[500];else message=detail; const e=new Error(message); e.status=r.status; e.data=data; throw e; }
    return data;
  }
  window.SG_API = {
    base: API_BASE,
    async register(mobile,password,confirm_password,language,role='citizen',special_id='',department='') { return request('/auth/register',{method:'POST',body:JSON.stringify({mobile,password,confirm_password,language,role,special_id:special_id||null,department:department||null})}); },
    async login(mobile,password,language) { return request('/auth/login',{method:'POST',body:JSON.stringify({mobile,password,language})}); },
    async me() { return request('/auth/me'); },
    async profilePhoto() { return request('/users/me/photo'); },
    async updateLanguage(language) { return request('/users/me/language',{method:'PUT',body:JSON.stringify({language})}); },
    async updateProfile(payload) { return request('/users/me/profile',{method:'PUT',body:JSON.stringify(payload)}); },
    async updateStaffProfile(payload) { return request('/users/me/staff-profile',{method:'PUT',body:JSON.stringify(payload)}); },
    async uploadEvidence(file) { const fd=new FormData(); fd.append('file',file); return request('/complaints/evidence',{method:'POST',body:fd}); },
    async viewEvidence(fileId) { const r=await fetch(`${API_BASE}/complaints/evidence/${encodeURIComponent(fileId)}`,{cache:'no-store',headers:getToken()?{'Authorization':`Bearer ${getToken()}`}:{}}); if(!r.ok)throw new Error(r.status===401?'Please log in again.':'Evidence is unavailable.'); const url=URL.createObjectURL(await r.blob());let modal=document.querySelector('#sgPhotoViewer');if(!modal){modal=document.createElement('div');modal.id='sgPhotoViewer';modal.innerHTML='<button type="button" aria-label="Close photo">×</button><img alt="Complaint evidence">';modal.style.cssText='position:fixed;inset:0;background:#020817ed;z-index:10000;display:none;align-items:center;justify-content:center;padding:5vh 5vw';const close=()=>{modal.style.display='none';modal.querySelector("img").src='';if(modal.dataset.url)URL.revokeObjectURL(modal.dataset.url);modal.dataset.url=''};modal.querySelector('button').onclick=close;modal.onclick=e=>{if(e.target===modal)close()};modal.querySelector('button').style.cssText='position:absolute;right:24px;top:20px;border:1px solid #fff;border-radius:50%;width:44px;height:44px;background:#102b43;color:white;font-size:30px;line-height:1;cursor:pointer';modal.querySelector('img').style.cssText='max-width:100%;max-height:90vh;object-fit:contain;border-radius:12px';document.addEventListener('keydown',e=>{if(e.key==='Escape'&&modal.style.display!=='none')modal.querySelector('button').click()});document.body.appendChild(modal)} if(modal.dataset.url)URL.revokeObjectURL(modal.dataset.url);modal.dataset.url=url;modal.querySelector('img').src=url;modal.style.display='flex'; },
    async previewComplaint(payload) { return request('/complaints/preview',{method:'POST',body:JSON.stringify(payload)}); },
    async createComplaint(payload) { return request('/complaints',{method:'POST',body:JSON.stringify(payload)}); },
    async complaints() { return request('/complaints'); },
    async complaint(id) { return request(`/complaints/${encodeURIComponent(id)}`); },
    async complaintByTicket(ticket) { return request(`/complaints/by-ticket/${encodeURIComponent(ticket)}`); },
    async history(id) { return request(`/complaints/${encodeURIComponent(id)}/history`); },
    async notifications() { return request('/notifications'); },
    async markNotificationRead(id) { return request(`/notifications/${encodeURIComponent(id)}/read`,{method:'PUT'}); },
    async feedback(id,rating,comment) { return request(`/complaints/${encodeURIComponent(id)}/feedback`,{method:'POST',body:JSON.stringify({rating,comment})}); },
    async reminder(id) { return request(`/complaints/${encodeURIComponent(id)}/reminder`,{method:'POST'}); },
    async getFeedback(id) { return request(`/complaints/${encodeURIComponent(id)}/feedback`); },
    async officerComplaints() { return request('/officer/complaints'); },
    async updateStatus(id,status,note,category_verified) { return request(`/officer/complaints/${encodeURIComponent(id)}/status`,{method:'PUT',body:JSON.stringify({status,note,category_verified})}); },
    async adminSummary() { return request('/admin/health-summary'); },
    async adminComplaints() { return request('/admin/complaints'); },
    async adminFeedback() { return request('/admin/feedback'); },
    async adminOfficers() { return request('/admin/officers'); },
    async adminRegistrationIds() { return request('/admin/registration-ids'); },
    async assignComplaint(id,officer_id) { return request(`/admin/complaints/${encodeURIComponent(id)}/assign`,{method:'PUT',body:JSON.stringify({officer_id})}); },
    async escalationCheck() { return request('/admin/run-escalation-check',{method:'POST'}); },
    async seedDemoUsers() { return request('/dev/seed-demo-users',{method:'POST'}); },
    clearSession() { ['sg_access_token','sg_user','sg_authenticated','sg_login_time'].forEach(k=>localStorage.removeItem(k)); }
  };
})();
