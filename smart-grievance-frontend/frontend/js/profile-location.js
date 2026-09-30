(()=>{
  const $=selector=>document.querySelector(selector);
  const input=$('#locationInput');
  const status=$('#locationDetected');
  const summary=$('#detectedLocation');
  const state=$('#state');
  const district=$('#district');
  const village=$('#village');
  const addressInput=$('#address');
  let addressWasManuallyEdited=Boolean(addressInput?.value.trim());
  if(saved?.gender&&$('#gender')){
    const gender=String(saved.gender).toLowerCase();
    $('#gender').value=gender==='woman'?'female':gender==='man'?'male':gender;
  }
  let lookupTimer;
  let lookupId=0;
  let controller;
  let profileMap;
  let profileMapMarker;
  let profileSelectedCoordinates=null;

  function setMapPoint(latitude,longitude){
    profileSelectedCoordinates={latitude:Number(latitude),longitude:Number(longitude)};
    window.profileSelectedCoordinates=profileSelectedCoordinates;
    localStorage.setItem('sg_gps',JSON.stringify(profileSelectedCoordinates));
    if(!profileMap)return;
    if(profileMapMarker)profileMap.removeLayer(profileMapMarker);
    profileMapMarker=L.marker([latitude,longitude]).addTo(profileMap);
    profileMap.setView([latitude,longitude],Math.max(profileMap.getZoom(),14));
  }

  function setSelectValue(select,value){
    if(!select||!value)return;
    let option=[...select.options].find(item=>item.value.toLowerCase()===value.toLowerCase());
    if(!option){option=new Option(value,value);select.add(option)}
    select.value=option.value;
  }

  function showDetectedLocation(location,query,coordinates){
    const detectedDistrict=location.district||location.state_district||location.county||location.city_district||location.municipality;
    const detectedState=location.state;
    const detectedPlace=location.city||location.town||location.village||location.municipality||location.suburb||query;
    if(!detectedDistrict||!detectedState)throw new Error('District and state were not found');

    setSelectValue(state,detectedState);
    if(typeof fillDistrict==='function')fillDistrict();
    setSelectValue(district,detectedDistrict);
    if(village)village.value=detectedPlace;
    if($('#cityName'))$('#cityName').value=detectedPlace;
    detectedCity=detectedPlace;

    if(addressInput&&!addressWasManuallyEdited){
      const locality=location.neighbourhood||location.suburb||location.village||location.hamlet||location.quarter||location.road||location.residential||location.locality;
      const city=location.city||location.town||location.municipality||detectedDistrict;
      const parts=[locality,city].filter(Boolean).filter((part,index,all)=>all.findIndex(other=>other.toLowerCase()===part.toLowerCase())===index);
      if(parts.length)addressInput.value=parts.join(', ');
    }

    const latitude=Number(coordinates?.latitude??location.lat),longitude=Number(coordinates?.longitude??location.lon);
    if(Number.isFinite(latitude)&&Number.isFinite(longitude))setMapPoint(latitude,longitude);

    $('#detectedCityLabel').textContent=detectedPlace;
    $('#detectedDistrictLabel').textContent=detectedDistrict;
    $('#detectedStateLabel').textContent=detectedState;
    window.profileSelectedAddress=location.display_name||`${detectedPlace}, ${detectedDistrict}, ${detectedState}`;
    $('#detectedAddressLabel').textContent=window.profileSelectedAddress;
    summary.href=profileSelectedCoordinates
      ?`https://www.google.com/maps/search/?api=1&query=${profileSelectedCoordinates.latitude},${profileSelectedCoordinates.longitude}`
      :`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${detectedPlace}, ${detectedDistrict}, ${detectedState}`)}`;
    summary.hidden=false;
    status.textContent=document.documentElement.lang==='hi'?'जिला और राज्य अपने आप मिल गए।':'District and state detected automatically.';
    status.className='small text-success mt-2';
  }

  function normalizePostcodeResult(result,query){
    const office=result?.[0]?.PostOffice?.[0];
    if(!office)throw new Error('PIN code not found');
    return {city:office.Name,district:office.District,state:office.State,postcode:query};
  }

  async function lookupLocation(query,id){
    controller?.abort();
    controller=new AbortController();
    const signal=controller.signal;
    try{
      let location;
      if(/^\d{6}$/.test(query)){
        const response=await fetch(`https://api.postalpincode.in/pincode/${query}`,{signal});
        if(!response.ok)throw new Error('PIN lookup failed');
        location=normalizePostcodeResult(await response.json(),query);
        const mapParams=new URLSearchParams({format:'jsonv2',addressdetails:'1',countrycodes:'in',limit:'1',q:`${location.city}, ${location.district}, ${location.state}, India`});
        const mapResponse=await fetch(`https://nominatim.openstreetmap.org/search?${mapParams}`,{signal});
        if(mapResponse.ok){
          const mapResult=(await mapResponse.json())?.[0];
          if(mapResult){location.lat=mapResult.lat;location.lon=mapResult.lon;location.display_name=mapResult.display_name;Object.assign(location,mapResult.address||{})}
        }
      }else{
        const params=new URLSearchParams({format:'jsonv2',addressdetails:'1',countrycodes:'in',limit:'1',q:`${query}, India`});
        const response=await fetch(`https://nominatim.openstreetmap.org/search?${params}`,{signal});
        if(!response.ok)throw new Error('City lookup failed');
        const results=await response.json();
        location=results?.[0]?.address;
        if(location){location.lat=results[0].lat;location.lon=results[0].lon;location.display_name=results[0].display_name}
        if(!location)throw new Error('City not found');
      }
      if(id!==lookupId)return;
      showDetectedLocation(location,query);
    }catch(error){
      if(error.name==='AbortError'||id!==lookupId)return;
      summary.hidden=true;
      status.textContent=document.documentElement.lang==='hi'?'स्थान नहीं मिला। शहर का नाम या 6 अंकों का PIN कोड जाँचें।':'Location not found. Check the city name or 6-digit PIN code.';
      status.className='small text-danger mt-2';
    }
  }

  function clearLocationLookup(){
    lookupId++;
    controller?.abort();
    state.value='';
    if(typeof fillDistrict==='function')fillDistrict();
    district.value='';
    if(village)village.value='';
    detectedCity='';
    profileSelectedCoordinates=null;
    window.profileSelectedCoordinates=null;
    localStorage.removeItem('sg_gps');
    if(profileMapMarker){profileMap.removeLayer(profileMapMarker);profileMapMarker=null}
    summary.hidden=true;
  }

  if(window.L&&$('#profileLocationMap')){
    let savedCoordinates=null;
    try{savedCoordinates=JSON.parse(localStorage.getItem('sg_gps')||'null')}catch{}
    const start=saved?.locationCoordinates||savedCoordinates;
    profileMap=L.map('profileLocationMap',{scrollWheelZoom:false}).setView(start?[start.latitude,start.longitude]:[23.2599,77.4126],start?14:5.5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'© OpenStreetMap contributors'}).addTo(profileMap);
    profileMap.on('click',async event=>{
      const {lat,lng}=event.latlng;
      setMapPoint(lat,lng);
      status.textContent=document.documentElement.lang==='hi'?'चुने गए स्थान का पता खोज रहे हैं…':'Finding the selected address…';
      status.className='small text-secondary mt-2';
      try{
        const params=new URLSearchParams({format:'jsonv2',addressdetails:'1',lat:String(lat),lon:String(lng)});
        params.set('zoom','18');
        const response=await fetch(`https://nominatim.openstreetmap.org/reverse?${params}`);
        if(!response.ok)throw new Error('Address lookup failed');
        const result=await response.json(),address=result.address||{};
        const city=address.city||address.town||address.village||address.municipality||address.suburb||address.postcode;
        if(!city)throw new Error('No address found');
        input.value=city;
        showDetectedLocation({...address,lat,lon:lng,display_name:result.display_name},city,{latitude:lat,longitude:lng});
        $('#gpsStatus').textContent='Map location selected.';
      }catch{
        summary.hidden=true;
        status.textContent='Could not resolve this map point. Try another location.';
        status.className='small text-danger mt-2';
      }
    });
    if(start){
      profileSelectedCoordinates={latitude:Number(start.latitude),longitude:Number(start.longitude)};
      window.profileSelectedCoordinates=profileSelectedCoordinates;
      profileMapMarker=L.marker([start.latitude,start.longitude]).addTo(profileMap);
      profileMap.setView([start.latitude,start.longitude],14);
    }
    setTimeout(()=>profileMap.invalidateSize(),300);
  }

  input?.addEventListener('input',event=>{
    event.stopImmediatePropagation();
    addressWasManuallyEdited=false;
    const query=event.target.value.trim();
    clearTimeout(lookupTimer);
    clearLocationLookup();
    status.textContent='';
    if(query.length<2)return;

    const id=++lookupId;
    status.textContent=document.documentElement.lang==='hi'?'जिला और राज्य खोज रहे हैं…':'Detecting district and state…';
    status.className='small text-secondary mt-2';
    lookupTimer=setTimeout(()=>lookupLocation(query,id),/^\d{6}$/.test(query)?100:1000);
  },true);

  addressInput?.addEventListener('input',()=>{addressWasManuallyEdited=true});

  const gpsButton=$('#gpsBtn');
  if(gpsButton)gpsButton.onclick=()=>{
    if(!navigator.geolocation){$('#gpsStatus').textContent='Location services are not available in this browser.';return}
    $('#gpsStatus').textContent=document.documentElement.lang==='hi'?'वर्तमान स्थान खोज रहे हैं…':'Detecting your current location…';
    navigator.geolocation.getCurrentPosition(async position=>{
      const latitude=position.coords.latitude,longitude=position.coords.longitude;
      setMapPoint(latitude,longitude);
      profileMap?.setView([latitude,longitude],14);
      try{
        const params=new URLSearchParams({format:'jsonv2',addressdetails:'1',lat:String(latitude),lon:String(longitude)});
        params.set('zoom','18');
        const response=await fetch(`https://nominatim.openstreetmap.org/reverse?${params}`);
        if(!response.ok)throw new Error('GPS address lookup failed');
        const result=await response.json(),address=result.address||{};
        const city=address.city||address.town||address.village||address.municipality||address.suburb||address.postcode;
        if(!city)throw new Error('City was not found for GPS location');
        input.value=city;
        lookupId++;
        address.lat=latitude;address.lon=longitude;address.display_name=result.display_name;
        showDetectedLocation(address,city,{latitude,longitude});
        $('#gpsStatus').textContent=document.documentElement.lang==='hi'?'वर्तमान स्थान प्रोफ़ाइल में जोड़ दिया गया।':'Current location added to your profile.';
        input.dispatchEvent(new Event('change',{bubbles:true}));
      }catch(error){
        $('#gpsStatus').textContent=document.documentElement.lang==='hi'?'GPS मिला, लेकिन जिला/राज्य नहीं मिल सका। कृपया शहर या PIN कोड दर्ज करें।':'GPS captured, but the district and state could not be resolved. Enter a city or PIN code.';
      }
    },()=>{$('#gpsStatus').textContent='Location permission was not granted. Enter a city or PIN code instead.'},{enableHighAccuracy:true,timeout:12000});
  };

  $('#setupLaterBtn')?.addEventListener('click',()=>{
    sessionStorage.removeItem('sg_return_to_complaint');
    sessionStorage.removeItem('sg_pending_complaint_category');
  });

  $('#profileForm')?.addEventListener('submit',event=>{
    if(!input.value.trim()||summary.hidden){
      event.preventDefault();
      event.stopImmediatePropagation();
      $('#formError').textContent=document.documentElement.lang==='hi'?'आगे बढ़ने के लिए मान्य शहर या PIN कोड दर्ज करें और जिला/राज्य का पता चलने दें।':'Enter a valid city or PIN code and wait for its district and state to be detected.';
      $('#formError').classList.add('show');
    }
  },true);

  if(input?.value.trim()&&state.value&&district.value){
    showDetectedLocation({city:saved?.city||saved?.village||input.value,district:saved.district,state:saved.state,display_name:saved?.locationAddress},input.value,saved?.locationCoordinates);
  }

  function applyServerProfile(user){
    if(!user||user.role!=='citizen'||!user.city)return;
    const coordinates=user.latitude!=null&&user.longitude!=null?{latitude:Number(user.latitude),longitude:Number(user.longitude)}:null;
    input.value=user.pincode||user.city;
    detectedCity=user.city;
    if($('#cityName'))$('#cityName').value=user.city;
    setSelectValue(state,user.state);
    if(typeof fillDistrict==='function')fillDistrict();
    setSelectValue(district,user.district);
    if(village)village.value=user.village||user.city;
    if(addressInput&&user.address)addressInput.value=user.address;
    const location={city:user.city,district:user.district,state:user.state,display_name:user.address||`${user.city}, ${user.district||''}, ${user.state||''}`};
    if(coordinates){setMapPoint(coordinates.latitude,coordinates.longitude);profileMap?.setView([coordinates.latitude,coordinates.longitude],14)}
    else{profileSelectedCoordinates=null;window.profileSelectedCoordinates=null;localStorage.removeItem('sg_gps');if(profileMapMarker){profileMap?.removeLayer(profileMapMarker);profileMapMarker=null}}
    if(user.district&&user.state)showDetectedLocation(location,user.city,coordinates||undefined);
  }
  window.addEventListener('sg-citizen-profile-loaded',event=>applyServerProfile(event.detail));
  if(window.sgLoadedCitizenProfile)applyServerProfile(window.sgLoadedCitizenProfile);

  $('#profileForm')?.addEventListener('submit',()=>{
    try{
      const profile=JSON.parse(localStorage.getItem('sg_profile')||'null');
      if(!profile)return;
      profile.gender=$('#gender')?.value||'';
      if(window.profileSelectedAddress)profile.locationAddress=window.profileSelectedAddress;
      profile.locationCoordinates=profileSelectedCoordinates||profile.locationCoordinates||null;
      localStorage.setItem('sg_profile',JSON.stringify(profile));
    }catch{}
  });
})();
