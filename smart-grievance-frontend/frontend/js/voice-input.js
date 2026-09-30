(() => {
  const button=document.querySelector('#voiceReportBtn');
  const textarea=document.querySelector('#complaintText');
  const status=document.querySelector('#voiceReportStatus');
  if(!button||!textarea||!status)return;
  const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;
  const ui=()=>localStorage.getItem('sg_lang')==='hi'
    ? {start:'\u092c\u094b\u0932\u0915\u0930 \u0936\u093f\u0915\u093e\u092f\u0924 \u0926\u0930\u094d\u091c \u0915\u0930\u0947\u0902',stop:'\u092c\u094b\u0932\u0928\u093e \u0930\u094b\u0915\u0947\u0902',hint:'\u092e\u093e\u0907\u0915 \u0926\u092c\u093e\u0915\u0930 \u092c\u094b\u0932\u0947\u0902, \u0906\u092a\u0915\u0940 \u0936\u093f\u0915\u093e\u092f\u0924 \u092f\u0939\u093e\u0901 \u0932\u093f\u0916\u0940 \u091c\u093e\u090f\u0917\u0940\u0964',listening:'\u0938\u0941\u0928 \u0930\u0939\u0947 \u0939\u0948\u0902\u2026 \u092c\u094b\u0932\u0928\u093e \u0936\u0941\u0930\u0942 \u0915\u0930\u0947\u0902\u0964',stopped:'\u092e\u093e\u0907\u0915 \u092c\u0902\u0926 \u0915\u093f\u092f\u093e \u0917\u092f\u093e\u0964',autoStopped:'4 \u0938\u0947\u0915\u0902\u0921 \u0924\u0915 \u0906\u0935\u093e\u091c\u093c \u0928 \u0906\u0928\u0947 \u092a\u0930 \u092e\u093e\u0907\u0915 \u092c\u0902\u0926 \u0939\u094b \u0917\u092f\u093e\u0964',unsupported:'\u0907\u0938 \u092c\u094d\u0930\u093e\u0909\u091c\u093c\u0930 \u092e\u0947\u0902 \u0935\u0949\u0907\u0938 \u091f\u093e\u0907\u092a\u093f\u0902\u0917 \u0909\u092a\u0932\u092c\u094d\u0927 \u0928\u0939\u0940\u0902 \u0939\u0948\u0964 Chrome \u092f\u093e Edge \u0915\u093e \u0909\u092a\u092f\u094b\u0917 \u0915\u0930\u0947\u0902\u0964',denied:'\u092e\u093e\u0907\u0915 \u0915\u0940 \u0905\u0928\u0941\u092e\u0924\u093f \u0928\u0939\u0940\u0902 \u092e\u093f\u0932\u0940\u0964 \u092c\u094d\u0930\u093e\u0909\u091c\u093c\u0930 \u0938\u0947\u091f\u093f\u0902\u0917 \u092e\u0947\u0902 \u092e\u093e\u0907\u0915 \u0915\u0940 \u0905\u0928\u0941\u092e\u0924\u093f \u0926\u0947\u0902\u0964',empty:'\u0906\u0935\u093e\u091c\u093c \u0938\u092e\u091d \u0928\u0939\u0940\u0902 \u0906\u0908\u0964 \u092b\u093f\u0930 \u0938\u0947 \u092c\u094b\u0932\u0947\u0902\u0964',microphone:'\u092e\u093e\u0907\u0915 \u0915\u093e\u092e \u0928\u0939\u0940\u0902 \u0915\u0930 \u0930\u0939\u093e\u0964'}
    : {start:'Start voice typing',stop:'Stop voice typing',hint:'Use the microphone to dictate your complaint.',listening:'Listening... start speaking.',stopped:'Microphone stopped.',autoStopped:'Microphone stopped after 4 seconds of silence.',unsupported:'Voice typing is not available in this browser. Try Chrome or Edge.',denied:'Microphone access was denied. Allow microphone access in browser settings.',empty:'No speech was detected. Please try again.',microphone:'Microphone is unavailable.'};
  const setLabel=text=>{button.setAttribute('aria-label',text);button.title=text;};
  const paint=active=>{button.classList.toggle('is-recording',active);const icon=button.querySelector('i');icon?.classList.toggle('bi-mic-fill',!active);icon?.classList.toggle('bi-stop-circle-fill',active);button.setAttribute('aria-pressed',String(active));setLabel(active?ui().stop:ui().start);};
  setLabel(ui().start);status.textContent=ui().hint;
  if(!SpeechRecognition){button.disabled=true;setLabel(ui().unsupported);status.textContent=ui().unsupported;return;}

  let recognition=null,listening=false,originalText='',finalText='',failureMessage='',stopReason=null,silenceTimer=null;
  const clearSilenceTimer=()=>{if(silenceTimer)clearTimeout(silenceTimer);silenceTimer=null;};
  const stopRecording=reason=>{if(!listening)return;listening=false;stopReason=reason;clearSilenceTimer();paint(false);try{recognition?.abort();}catch{}};
  const restartSilenceTimer=()=>{clearSilenceTimer();silenceTimer=setTimeout(()=>stopRecording('silence'),4000);};

  button.addEventListener('click',()=>{
    if(listening){stopRecording('tap');return;}
    recognition=new SpeechRecognition();
    listening=true;stopReason=null;failureMessage='';finalText='';originalText=textarea.value.trim();
    const selectedLanguage=document.documentElement.lang||localStorage.getItem('sg_lang')||'en';
    recognition.lang=selectedLanguage.toLowerCase().startsWith('hi')?'hi-IN':'en-IN';
    recognition.continuous=true;recognition.interimResults=true;
    recognition.onstart=()=>{if(!listening)return;status.textContent=ui().listening;restartSilenceTimer();};
    recognition.onresult=event=>{
      if(!listening)return;
      restartSilenceTimer();let interim='';
      for(let i=event.resultIndex;i<event.results.length;i++){
        const phrase=event.results[i][0].transcript.trim();
        if(event.results[i].isFinal&&phrase)finalText+=`${finalText?' ':''}${phrase}`;
        else interim+=`${interim?' ':''}${phrase}`;
      }
      textarea.value=[originalText,finalText,interim].filter(Boolean).join(originalText?' ':'');
      textarea.dispatchEvent(new Event('input',{bubbles:true}));
    };
    recognition.onerror=event=>{
      clearSilenceTimer();listening=false;paint(false);
      if(event.error==='not-allowed'||event.error==='service-not-allowed')failureMessage=ui().denied;
      else if(event.error==='audio-capture')failureMessage=ui().microphone;
      else if(event.error!=='no-speech'&&event.error!=='aborted')failureMessage=event.error;
    };
    recognition.onend=()=>{
      clearSilenceTimer();listening=false;paint(false);
      if(failureMessage)status.textContent=failureMessage;
      else if(stopReason==='silence')status.textContent=ui().autoStopped;
      else if(stopReason==='tap')status.textContent=ui().stopped;
      else if(!finalText&&textarea.value===originalText)status.textContent=ui().empty;
      else status.textContent=ui().hint;
      textarea.focus();
    };
    paint(true);status.textContent=ui().listening;restartSilenceTimer();
    try{recognition.start();}
    catch{listening=false;clearSilenceTimer();paint(false);status.textContent=ui().microphone;}
  });
})();
