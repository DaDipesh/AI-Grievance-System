(() => {
  const openButton=document.querySelector('#showRegistrationIds');
  const dialog=document.querySelector('#registrationIdsDialog');
  const closeButton=document.querySelector('#closeRegistrationIds');
  const body=dialog?.querySelector('tbody');
  const message=document.querySelector('#registrationIdsMessage');
  if(!openButton||!dialog||!body||!message)return;

  const addRow=(label,id)=>{
    const row=document.createElement('tr');
    const category=document.createElement('td');category.textContent=label;
    const codeCell=document.createElement('td');
    const code=document.createElement('code');code.textContent=id||'Not configured';codeCell.append(code);
    const actionCell=document.createElement('td');
    const copy=document.createElement('button');copy.type='button';copy.className='btn btn-sm btn-outline-info';copy.disabled=!id;
    copy.innerHTML='<i class="bi bi-copy me-1" aria-hidden="true"></i>Copy';
    copy.addEventListener('click',async()=>{
      try{
        if(navigator.clipboard?.writeText)await navigator.clipboard.writeText(id);
        else{
          const field=document.createElement('textarea');field.value=id;field.style.position='fixed';field.style.opacity='0';document.body.append(field);field.select();
          const copied=document.execCommand('copy');field.remove();if(!copied)throw new Error('Clipboard access is unavailable.');
        }
        copy.innerHTML='<i class="bi bi-check2 me-1" aria-hidden="true"></i>Copied';
        setTimeout(()=>{copy.innerHTML='<i class="bi bi-copy me-1" aria-hidden="true"></i>Copy'},1400);
      }catch{message.textContent='Could not copy automatically. Select and copy the ID instead.';}
    });
    actionCell.append(copy);row.append(category,codeCell,actionCell);body.append(row);
  };

  openButton.addEventListener('click',async()=>{
    dialog.showModal();body.replaceChildren();message.textContent='Loading registration IDs…';
    try{
      const ids=await SG_API.adminRegistrationIds();
      addRow(ids.admin?.label||'Administrator',ids.admin?.registration_id);
      (ids.officers||[]).forEach(officer=>addRow(officer.category||officer.department,officer.registration_id));
      message.textContent='Use these IDs when registering admin and officer accounts.';
    }catch(error){message.textContent=error.message;}
  });
  closeButton.addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
})();
