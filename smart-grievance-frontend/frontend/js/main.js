(function(){
'use strict';
const $=s=>document.querySelector(s), $$=s=>document.querySelectorAll(s);


// Profile + persistent language
(function(){
  const profile=JSON.parse(localStorage.getItem('sg_profile')||localStorage.getItem('sg_user')||'null');
  if(profile){
    const n=document.querySelector('#profileMiniName'); if(n)n.textContent=profile.name||'Citizen';
    const img=document.querySelector('#profileMiniPhoto'); if(img && profile.photo)img.src=profile.photo;
  }
  const logout=document.querySelector('#logoutBtn');
  logout?.addEventListener('click',e=>{e.preventDefault();window.SG_API?.clearSession();location.href='login.html'});
  const lang=localStorage.getItem('sg_lang')||'en'; const sel=document.querySelector('#dashboardLanguage'); if(sel)sel.value=lang;
  const dict={en:{home:'Home',report:'Report',dashboard:'Dashboard',emergency:'Emergency',map:'Map',track:'Track',profile:'Profile',logout:'Logout',reportIssue:'Report Issue'},hi:{home:'होम',report:'शिकायत दर्ज करें',dashboard:'\u0921\u0948\u0936\u092c\u094b\u0930\u094d\u0921',emergency:'आपातकाल',map:'मानचित्र',track:'ट्रैक करें',profile:'प्रोफ़ाइल',logout:'लॉगआउट',reportIssue:'शिकायत दर्ज करें'}};
  const pageText={
    en:{
      heroEyebrow:'AI-POWERED GRIEVANCE INTELLIGENCE',
      heroTitle:'Your Problem.<br><span>Understood by AI.</span><br>Resolved Faster.',
      heroDescription:'Transform citizen complaints into intelligent, actionable solutions with AI analysis, smart routing, real-time monitoring and predictive governance.',
      heroPrimary:'Report a Complaint',
      heroSecondary:'Dashboard',
      trustSecure:'Secure',
      trustAi:'AI Powered',
      trustLocation:'Location Aware',
      trustTransparent:'Transparent',
      cardsStatus:'SYSTEM STATUS',
      cardsTitle:'AI Complaint Intelligence',
      cardsLive:'LIVE AI ANALYSIS',
      cardsAnalysis:'AI ANALYSIS',
      cardsPreview:'“There has been no water supply in our village for two days.”',
      cardsWater:'Water',
      cardsCritical:'CRITICAL',
      cardsNegative:'Negative',
      cardsDepartment:'Water Department',
      cardsEtaValue:'24 Hours',
      cardsCategory:'CATEGORY',
      cardsPriority:'PRIORITY',
      cardsSentiment:'SENTIMENT',
      cardsImpact:'IMPACT SCORE',
      cardsRouting:'SMART ROUTING',
      cardsEta:'AI PREDICTED ETA',
      statsTotal:'Total Complaints',
      statsResolved:'Resolved',
      statsSla:'SLA Success',
      statsAvg:'Avg Resolution',
      statsTotalValue:'1,247',
      statsResolvedValue:'986',
      statsSlaValue:'91%',
      statsAvgValue:'18.4h',
      reportEyebrow:'CITIZEN SERVICES',
      reportTitle:'Report a Complaint <em>Smarter.</em>',
      reportSubtitle:'Submit text, evidence and location. Your AI model can analyze the complaint and return an actionable result.',
      newGrievance:'NEW GRIEVANCE',
      tellUs:'Tell us what happened',
      complaintDesc:'Complaint Description',
      locationLabel:'Location / Area',
      areaLocationHint:'Enter a village, ward, or area. A map pin is not required when this is provided.',
      mapPinTitle:'Map location',
      mapLocationHint:'Tap the map to select the problem location, or use your current location.',
      locationChoiceHint:'Provide an area or set either map pin. You do not need to provide both.',
      evidence:'Supporting Evidence',
      uploadImage:'Upload Complaint Image',
      useLocation:'Pin Current Location',
      chooseProblemLocation:'Pin Problem Location',
      analyzeAi:'Analyze Complaint with AI',
      aiIntelligence:'AI INTELLIGENCE',
      analysisResult:'Analysis Result',
      waitingComplaint:'Waiting for complaint',
      waitingMessage:'Submit a complaint and the result will appear here.',
      ticketId:'TICKET ID',
      category:'CATEGORY',
      priority:'PRIORITY',
      sentiment:'SENTIMENT',
      impact:'IMPACT',
      department:'DEPARTMENT',
      predictedEta:'PREDICTED ETA',
      emergency:'EMERGENCY',
      process:'INTELLIGENT WORKFLOW',
      workflowTitle:'From Complaint to <em>Resolution</em>',
      workflowText:'One connected workflow from citizen report to responsible action.',
      workflowStep1:'Complaint Submission',
      workflowStep1Text:'Submit a description, location, and supporting evidence.',
      workflowStep2:'AI Assessment',
      workflowStep2Text:'Classifies the issue and evaluates urgency and public impact.',
      workflowStep3:'Department Assignment',
      workflowStep3Text:'Routes the case to the department responsible for action.',
      workflowStep4:'Resolution Tracking',
      workflowStep4Text:'Follow progress, escalation, and final resolution.',
      features:'INTELLIGENCE LAYER',
      featuresTitle:'More Than a Complaint Portal',
      featuresText:'Advanced capabilities designed around real public-service workflows.',
      featureAiAnalysis:'AI Complaint Analysis',
      featureAiAnalysisText:'Understands and structures citizen complaints.',
      featureImpact:'Impact Scoring',
      featureImpactText:'Prioritizes incidents by potential public impact.',
      featureRouting:'Smart Routing',
      featureRoutingText:'Maps complaints to responsible departments.',
      featureSla:'Predictive SLA',
      featureSlaText:'Highlights cases at risk of delay.',
      featureEscalation:'Automatic Escalation',
      featureEscalationText:'Escalation workflow for unresolved critical cases.',
      featureHotspots:'Complaint Hotspots',
      featureHotspotsText:'Geographic clusters and emerging problems.',
      featureRelief:'Immediate Relief',
      featureReliefText:'AI recommends temporary relief for critical incidents.',
      featureCommunity:'Community Detection',
      featureCommunityText:'Groups similar complaints into incidents.',
      featureEvidence:'Evidence Intelligence',
      featureEvidenceText:'Images can support verification and AI analysis.',
      dashboardEyebrow:'AI GOVERNANCE COMMAND CENTER',
      dashboardTitle:'Intelligence at a <em>Glance</em>',
      dashboardText:'Real-time operational view for complaints, service performance and AI insights.',
      dashboardTrend:'Complaint Trends',
      dashboardTrendTitle:'Complaints vs Resolution',
      dashboardDepartment:'Department',
      dashboardDepartmentTitle:'Distribution',
      dashboardStatus:'Resolution Status',
      dashboardStatusTitle:'Current Overview',
      dashboardInsights:'AI INTELLIGENCE',
      dashboardInsightsTitle:'Smart Insights',
      insightWater:'Critical water issue detected',
      insightWaterText:'Water complaints increased in the selected region.',
      insightSla:'SLA risk detected',
      insightSlaText:'12 complaints may breach expected resolution time.',
      insightCommunity:'Community incident',
      insightCommunityText:'24 similar complaints detected in one area.',
      aiRecommendation:'AI Recommendation',
      aiRecommendationText:'Review the affected service zone and prioritize critical cases.',
      kpiTotal:'TOTAL COMPLAINTS',
      kpiResolved:'RESOLVED',
      kpiSla:'SLA SUCCESS',
      kpiAvg:'AVG RESOLUTION',
      emergencyEyebrow:'AI EMERGENCY RESPONSE ENGINE',
      emergencyTitle:'Don\'t Just Register Problems. <em>Respond to Them.</em>',
      emergencyText:'Critical incidents can trigger intelligent immediate-relief recommendations and escalation.',
      emergencyIncidentTitle:'Water Supply Failure',
      emergencyIncidentSubtitle:'Village ABC • Service unavailable for approximately 48 hours',
      emergencyImpact:'IMPACT SCORE',
      emergencyRelief:'IMMEDIATE RELIEF',
      emergencyReliefTitle:'Emergency Water Supply',
      emergencyReliefDesc:'AI recommendation',
      emergencyReliefTime:'Estimated Arrival',
      emergencyReliefPeople:'Affected Population',
      emergencyButton:'Initiate Relief Workflow',
      emergencyNote:'Prototype recommendation; actual dispatch requires authorized integration.',
      emergencyStatus:'RESPONSE STATUS',
      emergencyStatusTitle:'Incident Timeline',
      emergencyStep1:'Complaint detected',
      emergencyStep1Text:'AI analysis completed',
      emergencyStep2:'Department notified',
      emergencyStep2Text:'Water Department',
      emergencyStep3:'Immediate relief',
      emergencyStep3Text:'Recommendation ready',
      emergencyStep4:'Permanent repair',
      emergencyStep4Text:'Engineering action queued',
      mapEyebrow:'LOCATION INTELLIGENCE',
      mapTitle:'Complaint <em>Hotspot Map</em>',
      mapText:'Visualize where public-service problems are concentrated.',
      hotspotsTitle:'AI HOTSPOTS',
      hotspotsHeading:'Areas Needing Attention',
      hotspotCritical:'Critical',
      hotspotHigh:'High',
      hotspotMedium:'Medium',
      trackEyebrow:'COMPLAINT TRACKING',
      trackTitle:'Know Exactly <em>What\'s Happening</em>',
      trackLead:'Enter a ticket ID to see assignment, status, ETA and escalation updates.',
      complaintId:'Complaint ID',
      trackButton:'Track',
      demoTicket:'Enter your ticket number to track',
      ticket:'TICKET',
      inProgress:'IN PROGRESS',
      submitted:'Submitted',
      assigned:'Assigned',
      resolved:'Resolved',
      ctaTitle:'Every Complaint Deserves <em>to Be Heard.</em>',
      ctaText:'Report. Understand. Respond. Resolve.',
      ctaButton:'Start Your Complaint',
      footerText:'An AI-powered intelligent grievance management and public-service resolution ecosystem.',
      platform:'Platform',
      intelligence:'Intelligence',
      footerReport:'Report',
      footerDashboard:'Dashboard',
      footerTrack:'Track',
      footerFeatures:'AI Features',
      footerEmergency:'Emergency',
      footerHotspots:'Hotspots',
      footerBuilt:'Built with AI • For Better Governance',
      footerText:'An AI-powered intelligent grievance management and public-service resolution ecosystem.'
    },
    hi:{
      heroEyebrow:'एआई-आधारित शिकायत इंटेलिजेंस',
      heroTitle:'आपकी समस्या।<br><span>एआई ने समझ ली है।</span><br>तेज़ी से हल होगी।',
      heroDescription:'सिविल शिकायतों को एआई विश्लेषण, स्मार्ट रूटिंग, रियल-टाइम निगरानी और भविष्यसूचक शासन के साथ उपयोगी समाधान में बदलें।',
      heroPrimary:'शिकायत दर्ज करें',
      heroSecondary:'\u0921\u0948\u0936\u092c\u094b\u0930\u094d\u0921',
      trustSecure:'सुरक्षित',
      trustAi:'एआई समर्थित',
      trustLocation:'स्थान जागरूक',
      trustTransparent:'पारदर्शी',
      cardsStatus:'सिस्टम स्थिति',
      cardsTitle:'एआई शिकायत इंटेलिजेंस',
      cardsLive:'लाइव एआई विश्लेषण',
      cardsAnalysis:'एआई विश्लेषण',
      cardsPreview:'“हमारे गाँव में दो दिनों से पानी की आपूर्ति नहीं है।”',
      cardsWater:'पानी',
      cardsCritical:'महत्वपूर्ण',
      cardsNegative:'नकारात्मक',
      cardsDepartment:'जल विभाग',
      cardsEtaValue:'24 घंटे',
      cardsCategory:'श्रेणी',
      cardsPriority:'प्राथमिकता',
      cardsSentiment:'भावनात्मक स्थिति',
      cardsImpact:'प्रभाव स्कोर',
      cardsRouting:'स्मार्ट रूटिंग',
      cardsEta:'एआई अनुमानित ETA',
      statsTotal:'कुल शिकायतें',
      statsResolved:'हल हुई',
      statsSla:'SLA सफलता',
      statsAvg:'औसत समाधान',
      statsTotalValue:'1,247',
      statsResolvedValue:'986',
      statsSlaValue:'91%',
      statsAvgValue:'18.4h',
      reportEyebrow:'नागरिक सेवाएँ',
      reportTitle:'शिकायत दर्ज करें <em>और स्मार्ट तरीके से।</em>',
      reportSubtitle:'टेक्स्ट, सबूत और स्थान दर्ज करें। आपका एआई मॉडल शिकायत का विश्लेषण कर कार्ययोज्य परिणाम देगा।',
      newGrievance:'नई शिकायत',
      tellUs:'हुआ क्या',
      complaintDesc:'शिकायत विवरण',
      locationLabel:'स्थान / क्षेत्र',
      areaLocationHint:'गाँव, वार्ड या क्षेत्र दर्ज करें। यह देने पर मानचित्र पिन आवश्यक नहीं है।',
      mapPinTitle:'मानचित्र पर स्थान',
      mapLocationHint:'समस्या का स्थान चुनने के लिए मानचित्र पर टैप करें या वर्तमान स्थान का उपयोग करें।',
      locationChoiceHint:'क्षेत्र दर्ज करें या कोई एक मानचित्र पिन सेट करें। दोनों देना आवश्यक नहीं है।',
      evidence:'सहायक सबूत',
      uploadImage:'शिकायत छवि अपलोड करें',
      useLocation:'वर्तमान स्थान पिन करें',
      chooseProblemLocation:'मानचित्र पर स्थान चुनें',
      analyzeAi:'एआई से शिकायत का विश्लेषण करें',
      aiIntelligence:'एआई इंटेलिजेंस',
      analysisResult:'विश्लेषण परिणाम',
      waitingComplaint:'शिकायत का इंतज़ार है',
      waitingMessage:'शिकायत दर्ज करें और परिणाम यहाँ दिखाई देगा।',
      ticketId:'टिकट आईडी',
      category:'श्रेणी',
      priority:'प्राथमिकता',
      sentiment:'भावना',
      impact:'प्रभाव',
      department:'विभाग',
      predictedEta:'अनुमानित ETA',
      emergency:'आपातकाल',
      process:'स्मार्ट वर्कफ़्लो',
      workflowTitle:'शिकायत से <em>समाधान</em> तक',
      workflowText:'नागरिक रिपोर्ट से जिम्मेदार कार्रवाई तक एक जुड़ा वर्कफ़्लो।',
      workflowStep1:'शिकायत दर्ज करना',
      workflowStep1Text:'विवरण, स्थान और सहायक साक्ष्य जमा करें।',
      workflowStep2:'एआई मूल्यांकन',
      workflowStep2Text:'समस्या का वर्गीकरण कर तात्कालिकता और सार्वजनिक प्रभाव का आकलन करता है।',
      workflowStep3:'विभाग को भेजना',
      workflowStep3Text:'शिकायत को कार्रवाई के लिए जिम्मेदार विभाग तक पहुँचाता है।',
      workflowStep4:'समाधान की स्थिति',
      workflowStep4Text:'प्रगति, एस्केलेशन और अंतिम समाधान की स्थिति देखें।',
      features:'इंटेलिजेंस लेयर',
      featuresTitle:'शिकायत पोर्टल से आगे',
      featuresText:'वास्तविक लोक सेवा वर्कफ़्लोज़ के आधार पर तैयार उन्नत क्षमताएँ।',
      featureAiAnalysis:'एआई शिकायत विश्लेषण',
      featureAiAnalysisText:'नागरिक शिकायतों को समझता है और संरचित करता है।',
      featureImpact:'प्रभाव स्कोरिंग',
      featureImpactText:'सामाजिक प्रभाव के आधार पर घटनाओं को प्राथमिकता देता है।',
      featureRouting:'स्मार्ट रूटिंग',
      featureRoutingText:'शिकायतों को जिम्मेदार विभागों तक पहुँचाता है।',
      featureSla:'प्रेडिक्टिव SLA',
      featureSlaText:'देरी के जोखिम वाली घटनाओं को दिखाता है।',
      featureEscalation:'ऑटो एस्केलेशन',
      featureEscalationText:'असुलझी गई महत्वपूर्ण घटनाओं के लिए एस्केलेशन वर्कफ़्लो।',
      featureHotspots:'शिकायत हॉटस्पॉट',
      featureHotspotsText:'भौगोलिक क्लस्टर और उभरती हुई समस्याएँ।',
      featureRelief:'तत्काल राहत',
      featureReliefText:'एआई महत्वपूर्ण घटनाओं के लिए अस्थायी राहत सुझाता है।',
      featureCommunity:'कम्युनिटी डिटेक्शन',
      featureCommunityText:'समान शिकायतों को घटनाओं में समूहित करता है।',
      featureEvidence:'प्रमाण इंटेलिजेंस',
      featureEvidenceText:'तस्वीरें सत्यापन और एआई विश्लेषण में मदद कर सकती हैं।',
      dashboardEyebrow:'एआई गवर्नेंस कमांड सेंटर',
      dashboardTitle:'एक नज़र में <em>इंटेलिजेंस</em>',
      dashboardText:'शिकायतों, सेवा प्रदर्शन और एआई इनसाइट्स की रियल-टाइम परिचालन दृश्य।',
      dashboardTrend:'शिकायत ट्रेंड',
      dashboardTrendTitle:'शिकायतें बनाम समाधान',
      dashboardDepartment:'विभाग',
      dashboardDepartmentTitle:'वितरण',
      dashboardStatus:'समाधान स्थिति',
      dashboardStatusTitle:'वर्तमान अवलोकन',
      dashboardInsights:'एआई इंटेलिजेंस',
      dashboardInsightsTitle:'स्मार्ट इनसाइट्स',
      insightWater:'महत्वपूर्ण जल समस्या का पता चला',
      insightWaterText:'चयनित क्षेत्र में जल शिकायतें बढ़ी हैं।',
      insightSla:'SLA जोखिम का पता चला',
      insightSlaText:'12 शिकायतें अपेक्षित समाधान समय से अधिक हो सकती हैं।',
      insightCommunity:'कम्युनिटी घटना',
      insightCommunityText:'एक क्षेत्र में 24 जैसी शिकायतें पाई गईं।',
      aiRecommendation:'एआई सुझाव',
      aiRecommendationText:'प्रभावित सेवा क्षेत्र की समीक्षा करें और महत्वपूर्ण मामलों को प्राथमिकता दें।',
      kpiTotal:'कुल शिकायतें',
      kpiResolved:'हल हुई',
      kpiSla:'SLA सफलता',
      kpiAvg:'औसत समाधान',
      emergencyEyebrow:'एआई इमरजेंसी रिस्पॉन्स इंजन',
      emergencyTitle:'बस समस्या दर्ज न करें। <em>उसका जवाब दें।</em>',
      emergencyText:'महत्वपूर्ण घटनाएँ तुरंत राहत सुझाव और एस्केलेशन को ट्रिगर कर सकती हैं।',
      emergencyIncidentTitle:'पानी आपूर्ति विफलता',
      emergencyIncidentSubtitle:'गाँव ABC • लगभग 48 घंटे से सेवा उपलब्ध नहीं',
      emergencyImpact:'प्रभाव स्कोर',
      emergencyRelief:'तत्काल राहत',
      emergencyReliefTitle:'आपातकालीन जल आपूर्ति',
      emergencyReliefDesc:'एआई सुझाव',
      emergencyReliefTime:'अनुमानित आगमन',
      emergencyReliefPeople:'प्रभावित जनसंख्या',
      emergencyButton:'रिलिफ वर्कफ़्लो शुरू करें',
      emergencyNote:'प्रोटोटाइप सुझाव; वास्तविक डिस्पैच के लिए अधिकृत इंटीग्रेशन आवश्यक है।',
      emergencyStatus:'रिस्पॉन्स स्थिति',
      emergencyStatusTitle:'घटना टाइमलाइन',
      emergencyStep1:'शिकायत दर्ज',
      emergencyStep1Text:'एआई विश्लेषण पूरा',
      emergencyStep2:'विभाग को सूचना',
      emergencyStep2Text:'जल विभाग',
      emergencyStep3:'तत्काल राहत',
      emergencyStep3Text:'सुझाव तैयार',
      emergencyStep4:'स्थायी मरम्मत',
      emergencyStep4Text:'इंजीनियरिंग कार्य लंबित',
      mapEyebrow:'लोकেশন इंटेलिजेंस',
      mapTitle:'शिकायत <em>हॉटस्पॉट मैप</em>',
      mapText:'देखें कि लोक सेवा समस्याएँ कहाँ केंद्रित हैं।',
      hotspotsTitle:'एआई हॉटस्पॉट',
      hotspotsHeading:'ध्यान देने योग्य क्षेत्र',
      hotspotCritical:'महत्वपूर्ण',
      hotspotHigh:'उच्च',
      hotspotMedium:'मध्यम',
      trackEyebrow:'शिकायत ट्रैकिंग',
      trackTitle:'सही पता लगाएँ <em>क्या हो रहा है</em>',
      trackLead:'टिकट आईडी दर्ज करें ताकि असाइनमेंट, स्थिति, ETA और एस्केलेशन अपडेट देखें।',
      complaintId:'शिकायत आईडी',
      trackButton:'ट्रैक करें',
      demoTicket:'ट्रैक करने के लिए टिकट नंबर दर्ज करें',
      ticket:'टिकट',
      inProgress:'प्रगति में',
      submitted:'जमा किया गया',
      assigned:'असाइन किया गया',
      resolved:'हल हुआ',
      ctaTitle:'हर शिकायत का <em>सुनना जरूरी है।</em>',
      ctaText:'रिपोर्ट करें। समझें। जवाब दें। हल करें।',
      ctaButton:'अपनी शिकायत शुरू करें',
      footerText:'एआई-संचालित एक बुद्धिमान शिकायत प्रबंधन और लोक सेवा समाधान पारिस्थितिकी।',
      platform:'प्लेटफ़ॉर्म',
      intelligence:'इंटेलिजेंस',
      footerReport:'रिपोर्ट',
      footerDashboard:'डैशबोर्ड',
      footerTrack:'ट्रैक',
      footerFeatures:'एआई फीचर्स',
      footerEmergency:'आपातकाल',
      footerHotspots:'हॉटस्पॉट्स',
      footerBuilt:'एआई के साथ निर्मित • बेहतर शासन के लिए',
      footerText:'एआई-आधारित एक बुद्धिमान शिकायत प्रबंधन और लोक सेवा समाधान पारिस्थितिकी।'
    }
  };

  function applyPageText(lang){
    const t=(pageText[lang]||pageText.en);
    const map={
      heroEyebrow:'[id="heroEyebrow"]',
      heroTitle:'[id="heroTitle"]',
      heroDescription:'[id="heroDescription"]',
      heroPrimary:'[id="heroPrimaryBtn"]',
      heroSecondary:'[id="heroSecondaryBtn"]',
      trustSecure:'[id="trustSecure"]',
      trustAi:'[id="trustAi"]',
      trustLocation:'[id="trustLocation"]',
      trustTransparent:'[id="trustTransparent"]',
      reportEyebrow:'[id="reportEyebrow"]',
      reportTitle:'[id="reportTitle"]',
      reportSubtitle:'[id="reportSubtitle"]',
      newGrievance:'[id="newGrievance"]',
      tellUs:'[id="tellUs"]',
      complaintDesc:'[id="complaintDesc"]',
      locationLabel:'[id="locationLabel"]',
      evidence:'[id="evidence"]',
      uploadImage:'[id="uploadImage"]',
      useLocation:'[id="useLocationBtn"] span',
      analyzeAi:'[id="analyzeComplaintBtn"]',
      aiIntelligence:'[id="aiIntelligence"]',
      analysisResult:'[id="analysisResult"]',
      waitingComplaint:'[id="waitingComplaint"]',
      waitingMessage:'[id="waitingMessage"]',
      process:'[id="processEyebrow"]',
      features:'[id="featuresEyebrow"]',
      dashboardEyebrow:'[id="dashboardEyebrow"]',
      dashboardTitle:'[id="dashboardTitle"]',
      emergencyEyebrow:'[id="emergencyEyebrow"]',
      emergencyTitle:'[id="emergencyTitle"]',
      mapEyebrow:'[id="mapEyebrow"]',
      mapTitle:'[id="mapTitle"]',
      trackEyebrow:'[id="trackEyebrow"]',
      trackTitle:'[id="trackTitle"]',
      ctaTitle:'[id="ctaTitle"]',
      footerText:'footer p'
    };
    Object.entries(map).forEach(([key, selector]) => {
      const el=document.querySelector(selector);
      if(!el) return;
      if (selector === 'footer p') { el.textContent = t.footerText; return; }
      if (key === 'heroTitle' || key === 'reportTitle' || key === 'dashboardTitle' || key === 'emergencyTitle' || key === 'mapTitle' || key === 'trackTitle' || key === 'ctaTitle') {
        el.innerHTML = t[key];
      } else if (key === 'heroPrimary' || key === 'heroSecondary' || key === 'analyzeAi' || key === 'useLocation') {
        el.innerHTML = t[key];
      } else {
        el.textContent = t[key];
      }
    });
    const complaintText=document.getElementById('complaintText');
    if(complaintText){complaintText.placeholder = lang === 'hi' ? 'उदाहरण: हमारे गांव को पिछले दो दिनों से पानी नहीं मिला है...' : 'Example: Our village has not received water for the last two days...';}
    const complaintLocation=document.getElementById('complaintLocation');
    if(complaintLocation){complaintLocation.placeholder = lang === 'hi' ? 'गाँव / वार्ड / क्षेत्र' : 'Village / Ward / Area';}
    const trackingId=document.getElementById('trackingId');
    if(trackingId){trackingId.placeholder = lang === 'hi' ? 'उदाहरण: ' : 'e.g. ';}
    document.querySelectorAll('[data-i18n]').forEach(node=>{const key=node.dataset.i18n; if(!key) return; const value=(pageText[lang]||pageText.en)[key]; if(value) node.innerHTML=value;});
    const extra={
      en:{
        cardsAnalysis:'AI ANALYSIS',cardsWater:'Water',cardsNegative:'Negative',online:'ONLINE',aiReady:'AI READY',locationStatus:'Location not selected',jpg:'JPG / PNG • Optional',
        total:'Total Complaints',resolved:'Resolved',sla:'SLA Success',average:'Avg Resolution',
        ticketId:'TICKET ID',category:'CATEGORY',priority:'PRIORITY',sentiment:'SENTIMENT',impact:'IMPACT',department:'DEPARTMENT',eta:'PREDICTED ETA',emergency:'EMERGENCY',ready:'READY',
        submit:'Complaint Submission',submitText:'Submit a description, location, and supporting evidence.',understands:'AI Assessment',understandsText:'Classifies the issue and evaluates urgency and public impact.',routing:'Department Assignment',routingText:'Routes the case to the department responsible for action.',resolution:'Resolution Tracking',resolutionText:'Follow progress, escalation, and final resolution.',
        trend:'COMPLAINT TRENDS',trendTitle:'Complaints vs Resolution',departmentTitle:'DEPARTMENT',distribution:'Distribution',status:'RESOLUTION STATUS',overview:'Current Overview',intelligence:'AI INTELLIGENCE',insights:'Smart Insights',live:'LIVE',
        criticalWater:'Critical water issue detected',criticalWaterText:'Water complaints increased in the selected region.',slaRisk:'SLA risk detected',slaRiskText:'12 complaints may breach expected resolution time.',community:'Community incident',communityText:'24 similar complaints detected in one area.',recommendation:'AI Recommendation',recommendationText:'Review the affected service zone and prioritize critical cases.',
        emergencyEngine:'AI EMERGENCY RESPONSE ENGINE',emergencyTitle:'Don\'t Just Register Problems. <em>Respond to Them.</em>',emergencyText:'Critical incidents can trigger intelligent immediate-relief recommendations and escalation.',incident:'CRITICAL INCIDENT DETECTED',waterFailure:'Water Supply Failure',villageService:'Village ABC • Service unavailable for approximately 48 hours',impactScore:'IMPACT SCORE',relief:'IMMEDIATE RELIEF',emergencySupply:'Emergency Water Supply',aiRecommendation:'AI RECOMMENDATION',tanker:'Emergency tanker supply',arrival:'ESTIMATED ARRIVAL',population:'AFFECTED POPULATION',minutes:'45 minutes',people:'~800 people',reliefButton:'Initiate Relief Workflow',prototype:'Prototype recommendation; actual dispatch requires authorized integration.',response:'RESPONSE STATUS',timeline:'Incident Timeline',detected:'Complaint detected',analysisDone:'AI analysis completed',notified:'Department notified',waterDepartment:'Water Department',immediate:'Immediate relief',recommendationReady:'Recommendation ready',permanent:'Permanent repair',engineering:'Engineering action queued',
        hotspots:'AI HOTSPOTS',attention:'Areas Needing Attention',critical:'Critical',high:'High',medium:'Medium',normal:'Normal',complaints:'complaints',tracking:'COMPLAINT TRACKING',trackLead:'Enter a ticket ID to see assignment, status, ETA and escalation updates.',complaintId:'Complaint ID',track:'Track',demo:'Enter your ticket number to track',ticket:'TICKET',progress:'IN PROGRESS',submitted:'Submitted',assigned:'Assigned',inProgress:'In Progress',resolvedStatus:'Resolved',
        cta:'BUILDING BETTER PUBLIC SERVICE',start:'Start Your Complaint',platform:'Platform',footerReport:'Report',footerDashboard:'Dashboard',footerTrack:'Track',intelligenceTitle:'Intelligence',features:'AI Features',footerEmergency:'Emergency',footerHotspots:'Hotspots',built:'Built with AI • For Better Governance'
      },
      hi:{
        cardsAnalysis:'एआई विश्लेषण',cardsWater:'पानी',cardsNegative:'नकारात्मक',online:'ऑनलाइन',aiReady:'एआई तैयार',locationStatus:'स्थान चुना नहीं गया',jpg:'JPG / PNG • वैकल्पिक',
        total:'कुल शिकायतें',resolved:'हल हुई',sla:'SLA सफलता',average:'औसत समाधान',
        ticketId:'टिकट आईडी',category:'श्रेणी',priority:'प्राथमिकता',sentiment:'भावना',impact:'प्रभाव',department:'विभाग',eta:'अनुमानित ETA',emergency:'आपातकाल',ready:'तैयार',
        submit:'शिकायत दर्ज करना',submitText:'विवरण, स्थान और सहायक साक्ष्य जमा करें।',understands:'एआई मूल्यांकन',understandsText:'समस्या का वर्गीकरण कर तात्कालिकता और सार्वजनिक प्रभाव का आकलन करता है।',routing:'विभाग को भेजना',routingText:'शिकायत को कार्रवाई के लिए जिम्मेदार विभाग तक पहुँचाता है।',resolution:'समाधान की स्थिति',resolutionText:'प्रगति, एस्केलेशन और अंतिम समाधान की स्थिति देखें।',
        trend:'शिकायत ट्रेंड',trendTitle:'शिकायतें बनाम समाधान',departmentTitle:'विभाग',distribution:'वितरण',status:'समाधान स्थिति',overview:'वर्तमान अवलोकन',intelligence:'एआई इंटेलिजेंस',insights:'स्मार्ट इनसाइट्स',live:'लाइव',
        criticalWater:'महत्वपूर्ण जल समस्या का पता चला',criticalWaterText:'चयनित क्षेत्र में जल शिकायतें बढ़ी हैं।',slaRisk:'SLA जोखिम का पता चला',slaRiskText:'12 शिकायतें अपेक्षित समाधान समय से अधिक हो सकती हैं।',community:'कम्युनिटी घटना',communityText:'एक क्षेत्र में 24 समान शिकायतें पाई गईं।',recommendation:'एआई सुझाव',recommendationText:'प्रभावित सेवा क्षेत्र की समीक्षा करें और महत्वपूर्ण मामलों को प्राथमिकता दें।',
        emergencyEngine:'एआई आपातकालीन प्रतिक्रिया इंजन',emergencyTitle:'सिर्फ समस्याएँ दर्ज न करें। <em>उनका समाधान करें।</em>',emergencyText:'महत्वपूर्ण घटनाएँ तुरंत राहत सुझाव और एस्केलेशन को ट्रिगर कर सकती हैं।',incident:'महत्वपूर्ण घटना का पता चला',waterFailure:'जल आपूर्ति विफलता',villageService:'गाँव ABC • लगभग 48 घंटे से सेवा उपलब्ध नहीं',impactScore:'प्रभाव स्कोर',relief:'तत्काल राहत',emergencySupply:'आपातकालीन जल आपूर्ति',aiRecommendation:'एआई सुझाव',tanker:'आपातकालीन टैंकर आपूर्ति',arrival:'अनुमानित आगमन',population:'प्रभावित जनसंख्या',minutes:'45 मिनट',people:'लगभग 800 लोग',reliefButton:'राहत वर्कफ़्लो शुरू करें',prototype:'प्रोटोटाइप सुझाव; वास्तविक डिस्पैच के लिए अधिकृत इंटीग्रेशन आवश्यक है।',response:'रिस्पॉन्स स्थिति',timeline:'घटना टाइमलाइन',detected:'शिकायत दर्ज',analysisDone:'एआई विश्लेषण पूरा',notified:'विभाग को सूचना',waterDepartment:'जल विभाग',immediate:'तत्काल राहत',recommendationReady:'सुझाव तैयार',permanent:'स्थायी मरम्मत',engineering:'इंजीनियरिंग कार्य लंबित',
        hotspots:'एआई हॉटस्पॉट',attention:'ध्यान देने योग्य क्षेत्र',critical:'महत्वपूर्ण',high:'उच्च',medium:'मध्यम',normal:'सामान्य',complaints:'शिकायतें',tracking:'शिकायत ट्रैकिंग',trackLead:'टिकट आईडी दर्ज करें ताकि असाइनमेंट, स्थिति, ETA और एस्केलेशन अपडेट देखें।',complaintId:'शिकायत आईडी',track:'ट्रैक करें',demo:'ट्रैक करने के लिए टिकट नंबर दर्ज करें',ticket:'टिकट',progress:'प्रगति में',submitted:'जमा किया गया',assigned:'असाइन किया गया',inProgress:'प्रगति में',resolvedStatus:'हल हुआ',
        cta:'बेहतर सार्वजनिक सेवा का निर्माण',start:'अपनी शिकायत शुरू करें',platform:'प्लेटफ़ॉर्म',footerReport:'रिपोर्ट',footerDashboard:'डैशबोर्ड',footerTrack:'ट्रैक',intelligenceTitle:'इंटेलिजेंस',features:'एआई फीचर्स',footerEmergency:'आपातकाल',footerHotspots:'हॉटस्पॉट्स',built:'एआई के साथ निर्मित • बेहतर शासन के लिए'
      }
    }[lang]||null;
    if(extra){
      const set=(selector,key,html=false)=>document.querySelectorAll(selector).forEach(el=>{const value=extra[key]??t[key];if(value===undefined)return;if(html){el.innerHTML=value;return}const textNode=[...el.childNodes].find(node=>node.nodeType===Node.TEXT_NODE&&node.textContent.trim());if(textNode)textNode.textContent=` ${value} `;else el.textContent=value});
      set('.ai-card .card-top small','cardsStatus'); set('.ai-card .card-top h5','cardsTitle'); set('.ai-card .complaint-preview small','cardsLive'); set('.ai-card .complaint-preview p','cardsPreview'); set('.ai-card .analysis-label > span:first-of-type','cardsAnalysis'); set('.ai-card .analysis-grid div:nth-child(1) small','category'); set('.ai-card .analysis-grid div:nth-child(1) strong','cardsWater'); set('.ai-card .analysis-grid div:nth-child(2) small','priority'); set('.ai-card .analysis-grid div:nth-child(2) strong','critical'); set('.ai-card .analysis-grid div:nth-child(3) small','sentiment'); set('.ai-card .analysis-grid div:nth-child(3) strong','cardsNegative'); set('.ai-card .analysis-grid div:nth-child(4) small','impact'); set('.ai-card .route-box small','routing'); set('.ai-card .route-box strong','waterDepartment'); set('.ai-card .eta-row small','eta');
      set('.stats-grid div:nth-child(1) span','total'); set('.stats-grid div:nth-child(2) span','resolved'); set('.stats-grid div:nth-child(3) span','sla'); set('.stats-grid div:nth-child(4) span','average');
      set('.kpi:nth-child(1) small','total'); set('.kpi:nth-child(2) small','resolved'); set('.kpi:nth-child(3) small','sla'); set('.kpi:nth-child(4) small','average');
      set('.dark-section .row > .col-md-3:nth-child(1) .process h4','submit'); set('.dark-section .row > .col-md-3:nth-child(1) .process p','submitText'); set('.dark-section .row > .col-md-3:nth-child(2) .process h4','understands'); set('.dark-section .row > .col-md-3:nth-child(2) .process p','understandsText'); set('.dark-section .row > .col-md-3:nth-child(3) .process h4','routing'); set('.dark-section .row > .col-md-3:nth-child(3) .process p','routingText'); set('.dark-section .row > .col-md-3:nth-child(4) .process h4','resolution'); set('.dark-section .row > .col-md-3:nth-child(4) .process p','resolutionText');
      const featureKeys=[['featureAiAnalysis','featureAiAnalysisText'],['featureImpact','featureImpactText'],['featureRouting','featureRoutingText'],['featureSla','featureSlaText'],['featureEscalation','featureEscalationText'],['featureHotspots','featureHotspotsText'],['featureRelief','featureReliefText'],['featureCommunity','featureCommunityText'],['featureEvidence','featureEvidenceText']];document.querySelectorAll('.feature').forEach((card,i)=>{const keys=featureKeys[i];if(!keys)return;const title=card.querySelector('h4'),description=card.querySelector('p');if(title&&t[keys[0]])title.innerHTML=t[keys[0]];if(description&&t[keys[1]])description.textContent=t[keys[1]]});
      const kpiCards=document.querySelectorAll('.dashboard-section .kpi'),kpiData=lang==='hi'?[['कुल शिकायतें','1,247','↑ 12.4%','files','blue'],['हल हुई','986','↑ 18.2%','check-circle','green'],['लंबित','143','12.1%','clock','orange'],['एस्केलेटेड','12','1.0%','exclamation-triangle','red']]:[['Total Complaints','1,247','↑ 12.4%','files','blue'],['Solved','986','↑ 18.2%','check-circle','green'],['Pending','143','12.1%','clock','orange'],['Escalated','12','1.0%','exclamation-triangle','red']];kpiCards.forEach((card,index)=>{const item=kpiData[index];if(!item)return;const label=card.querySelector('small'),value=card.querySelector('b'),change=card.querySelector('span'),icon=card.querySelector('i');if(label)label.textContent=item[0];if(value)value.textContent=item[1];if(change)change.textContent=item[2];if(icon){icon.className=`bi bi-${item[3]} ${item[4]}`}});
      set('.dash-panel:nth-child(1) .dash-head small','trend'); set('.dash-panel:nth-child(1) h4','trendTitle'); set('.dash-panel:nth-child(2) .dash-head small','departmentTitle'); set('.dash-panel:nth-child(2) h4','distribution'); set('.dash-panel:nth-child(3) .dash-head small','status'); set('.dash-panel:nth-child(3) h4','overview'); set('.insights .dash-head small','intelligence'); set('.insights .dash-head h4','insights'); set('.insight:nth-of-type(1) b','criticalWater'); set('.insight:nth-of-type(1) p','criticalWaterText'); set('.insight:nth-of-type(2) b','slaRisk'); set('.insight:nth-of-type(2) p','slaRiskText'); set('.insight:nth-of-type(3) b','community'); set('.insight:nth-of-type(3) p','communityText'); set('.recommend b','recommendation'); set('.recommend p','recommendationText');
      set('.emergency-section .section-head span','emergencyEngine'); set('.emergency-section .section-head h2','emergencyTitle',true); set('.emergency-section .section-head p','emergencyText'); set('.emergency-top small','incident'); set('.emergency-top h3','waterFailure'); set('.emergency-top p','villageService'); set('.impact small','impactScore'); set('.relief-title small','relief'); set('.relief-title h4','emergencySupply'); set('.relief-grid div:nth-child(1) small','aiRecommendation'); set('.relief-grid div:nth-child(1) b','tanker'); set('.relief-grid div:nth-child(2) small','arrival'); set('.relief-grid div:nth-child(2) b','minutes'); set('.relief-grid div:nth-child(3) small','population'); set('.relief-grid div:nth-child(3) b','people'); set('#reliefBtn','reliefButton'); set('.note','prototype'); set('.response > small','response'); set('.response h4','timeline');
      const responseSteps=[['detected','analysisDone'],['notified','waterDepartment'],['immediate','recommendationReady'],['permanent','engineering']];document.querySelectorAll('.response-step').forEach((step,index)=>{const keys=responseSteps[index];if(!keys)return;const title=step.querySelector('b'),description=step.querySelector('small'),titleValue=extra[keys[0]]??t[keys[0]],descriptionValue=extra[keys[1]]??t[keys[1]];if(title&&titleValue)title.textContent=titleValue;if(description&&descriptionValue)description.textContent=descriptionValue});
      set('.hotspot-panel .dash-head small','hotspots'); set('.hotspot-panel .dash-head h4','attention'); set('.hotspot:nth-of-type(2) span,.legend span:nth-child(1)','critical'); set('.hotspot:nth-of-type(3) span,.legend span:nth-child(2)','high'); set('.hotspot:nth-of-type(4) span,.legend span:nth-child(3)','medium'); set('.tracking-box label','complaintId'); set('#trackButton','track'); set('.tracking-box > small','trackLead'); set('.ticket-summary small','ticket'); set('.ticket-summary > span','progress'); set('.progress-labels span:nth-child(1)','submitted'); set('.progress-labels span:nth-child(2)','assigned'); set('.progress-labels span:nth-child(3)','inProgress'); set('.progress-labels span:nth-child(4)','resolvedStatus'); set('.cta-section > .container > span','cta'); set('.cta-section .btn-main','start'); set('footer h6:nth-of-type(1)','platform'); set('footer h6:nth-of-type(2)','intelligenceTitle'); set('footer .col-lg-3:nth-child(2) a:nth-child(1)','footerReport'); set('footer .col-lg-3:nth-child(2) a:nth-child(2)','footerDashboard'); set('footer .col-lg-3:nth-child(2) a:nth-child(3)','footerTrack'); set('footer .col-lg-3:nth-child(3) a:nth-child(1)','features'); set('footer .col-lg-3:nth-child(3) a:nth-child(2)','footerEmergency'); set('footer .col-lg-3:nth-child(3) a:nth-child(3)','footerHotspots'); set('.footer-bottom span:nth-child(2)','built');
    }
  }

  function apply(lang){localStorage.setItem('sg_lang',lang);const d=dict[lang]||dict.en;const links=document.querySelectorAll('.nav-link');links.forEach(a=>{const h=a.getAttribute('href');const map={'#home':'home','#report':'report','#dashboard':'dashboard','#emergency':'emergency','#map':'map','#track':'track','profile.html':'profile','#':'logout'};const k=map[h];if(k)a.textContent=d[k]});const c=document.querySelector('.nav-cta');if(c)c.innerHTML=d.reportIssue+' <i class="bi bi-arrow-up-right"></i>';document.documentElement.lang=lang;applyPageText(lang)}
  apply(lang); sel?.addEventListener('change',e=>apply(e.target.value));
})();

// Navbar
window.addEventListener('scroll',()=>$('.smart-navbar')?.classList.toggle('scrolled',scrollY>30));
(function setupNavIndicator(){
  const list=$('.smart-navbar .navbar-nav'),links=[...$$('.smart-navbar .navbar-nav .nav-link')];
  if(!list||!links.length)return;
  const indicator=document.createElement('span');indicator.className='nav-active-indicator';indicator.setAttribute('aria-hidden','true');list.prepend(indicator);
  let activeLink=null;
  function setActive(link,force=false){
    if(!link||!links.includes(link))return;
    links.forEach(item=>{const active=item===link;item.classList.toggle('active',active);if(active)item.setAttribute('aria-current','page');else item.removeAttribute('aria-current')});
    if(link===activeLink&&!force)return;
    activeLink=link;
    const listRect=list.getBoundingClientRect(),linkRect=link.getBoundingClientRect();
    indicator.style.width=`${linkRect.width}px`;indicator.style.height=`${linkRect.height}px`;
    indicator.style.transform=`translate(${linkRect.left-listRect.left}px,${linkRect.top-listRect.top}px)`;
    indicator.classList.add('is-visible');
  }
  const sectionLinks=links.map(link=>{const href=link.getAttribute('href'),section=href?.startsWith('#')&&href.length>1?document.getElementById(href.slice(1)):null;return {link,section}}).filter(item=>item.section);
  function syncWithScroll(){
    const line=window.innerHeight*.38;
    let visible=sectionLinks[0];
    for(const item of sectionLinks)if(item.section.getBoundingClientRect().top<=line)visible=item;
    if(visible)setActive(visible.link);
  }
  links.forEach(link=>link.addEventListener('click',()=>{
    setActive(link,true);
    const collapse=$('.navbar-collapse');
    if(collapse?.classList.contains('show'))bootstrap.Collapse.getOrCreateInstance(collapse).hide();
  }));
  let scrollFrame=0;
  window.addEventListener('scroll',()=>{if(scrollFrame)return;scrollFrame=requestAnimationFrame(()=>{scrollFrame=0;syncWithScroll()})},{passive:true});
  window.addEventListener('resize',()=>setActive(activeLink,true));
  window.addEventListener('hashchange',()=>{const link=links.find(item=>item.getAttribute('href')===location.hash);if(link)setActive(link,true)});
  $('.navbar-collapse')?.addEventListener('shown.bs.collapse',()=>setActive(activeLink,true));
  setActive(links.find(link=>link.getAttribute('href')===location.hash)||links[0],true);
  setTimeout(syncWithScroll,80);
})();

// Counters
const counters=$$('[data-count]');const observer=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;const el=e.target,target=+el.dataset.count;let start=0;const step=Math.max(1,Math.ceil(target/50));const t=setInterval(()=>{start+=step;if(start>=target){start=target;clearInterval(t)}el.textContent=start.toLocaleString()},20);observer.unobserve(el)}),{threshold:.5});counters.forEach(x=>observer.observe(x));

// Image preview
$('#complaintImage')?.addEventListener('change',e=>{const f=e.target.files[0],box=$('#imagePreview');if(!f)return;const url=URL.createObjectURL(f);box.innerHTML=`<img src="${url}" alt="Complaint evidence preview"><small class="d-block text-secondary mt-1">${f.name}</small>`});

// Keep current and problem pins independent and persistent.
const grievancePins=(()=>{try{return JSON.parse(localStorage.getItem('sg_complaint_locations')||'{}')||{}}catch{return {}}})();
const grievancePinMarkers={current:null,problem:null};
let complaintPickerMap=null;
window.grievanceLocations=grievancePins;
window.grievanceLocation=grievancePins.current||null;
function setGrievancePin(kind,latitude,longitude,address){
  const previous=grievancePins[kind];
  const point={latitude:Number(latitude),longitude:Number(longitude),address:address||(previous?.latitude===Number(latitude)&&previous?.longitude===Number(longitude)?previous.address:'')||''};
  if(!Number.isFinite(point.latitude)||!Number.isFinite(point.longitude)||Math.abs(point.latitude)>90||Math.abs(point.longitude)>180)return false;
  grievancePins[kind]=point;
  localStorage.setItem('sg_complaint_locations',JSON.stringify(grievancePins));
  if(kind==='current')window.grievanceLocation=point;
  for(const map of [window.grievanceMap,complaintPickerMap])if(map){
    if(grievancePinMarkers[kind]?.[map._leaflet_id])map.removeLayer(grievancePinMarkers[kind][map._leaflet_id]);
    const color=kind==='current'?'#2563eb':'#ef4444';
    const label=kind==='current'?'Current location':'Problem location';
    grievancePinMarkers[kind]=grievancePinMarkers[kind]||{};
    grievancePinMarkers[kind][map._leaflet_id]=L.circleMarker([point.latitude,point.longitude],{radius:10,color:'#fff',weight:3,fillColor:color,fillOpacity:1}).addTo(map).bindPopup(label);
    if(map===complaintPickerMap)map.setView([point.latitude,point.longitude],Math.max(map.getZoom(),13));
  }
  const out=$('#locationStatus');
  const selected=point;
  if(out)out.textContent=selected.address||`${selected.latitude.toFixed(5)}, ${selected.longitude.toFixed(5)}`;
  const addressLink=$('#complaintSelectedAddress');
  if(addressLink&&selected.address){
    addressLink.href=`https://www.google.com/maps/search/?api=1&query=${selected.latitude},${selected.longitude}`;
    addressLink.querySelector('span').textContent=selected.address;
    addressLink.hidden=false;
  }else if(addressLink)addressLink.hidden=true;
  return true;
}
async function resolveGrievanceAddress(kind,latitude,longitude){
  const out=$('#locationStatus');
  if(out)out.textContent='Finding selected address…';
  try{
    const params=new URLSearchParams({format:'jsonv2',addressdetails:'1',lat:String(latitude),lon:String(longitude)});
    const response=await fetch(`https://nominatim.openstreetmap.org/reverse?${params}`);
    if(!response.ok)throw new Error('Address lookup failed');
    const result=await response.json(),address=result.display_name||'';
    setGrievancePin(kind,latitude,longitude,address);
    if(!address&&out)out.textContent='Location selected. Address could not be resolved.';
  }catch{
    setGrievancePin(kind,latitude,longitude);
    if(out)out.textContent='Location selected. Address lookup is unavailable.';
  }
}

if(window.L&&$('#complaintLocationPickerMap')){
  const start=grievancePins.problem||grievancePins.current;
  complaintPickerMap=L.map('complaintLocationPickerMap',{scrollWheelZoom:false}).setView(start?[start.latitude,start.longitude]:[23.2599,77.4126],start?14:5.5);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'© OpenStreetMap contributors'}).addTo(complaintPickerMap);
  complaintPickerMap.on('click',event=>{
    setGrievancePin('problem',event.latlng.lat,event.latlng.lng);
    resolveGrievanceAddress('problem',event.latlng.lat,event.latlng.lng);
  });
  for(const kind of ['current','problem'])if(grievancePins[kind])setGrievancePin(kind,grievancePins[kind].latitude,grievancePins[kind].longitude,grievancePins[kind].address);
  setTimeout(()=>complaintPickerMap.invalidateSize(),250);
}
$('#useLocationBtn')?.addEventListener('click',()=>{
  const out=$('#locationStatus');
  if(!navigator.geolocation){if(out)out.textContent='Location access is unavailable in this browser.';return}
  if(out)out.textContent='Getting current location…';
  navigator.geolocation.getCurrentPosition(position=>{
    const {latitude,longitude}=position.coords;
    setGrievancePin('current',latitude,longitude);
    if(complaintPickerMap)complaintPickerMap.setView([latitude,longitude],15);
    resolveGrievanceAddress('current',latitude,longitude);
  },()=>{if(out)out.textContent='Location permission was denied.'},{enableHighAccuracy:true,timeout:10000});
});
$('#pinProblemBtn')?.addEventListener('click',()=>{
  $('#complaintLocationPickerMap')?.scrollIntoView({behavior:'smooth',block:'center'});
  if($('#locationStatus'))$('#locationStatus').textContent='Tap the map to select the problem location.';
});
if(grievancePins.current)setGrievancePin('current',grievancePins.current.latitude,grievancePins.current.longitude);
if(grievancePins.problem)setGrievancePin('problem',grievancePins.problem.latitude,grievancePins.problem.longitude);

// Demo AI result; replace function body with backend fetch later.
document.addEventListener('click',event=>{
  if(!event.target.closest('#analyzeComplaintBtn'))return;
  const hasArea=$('#complaintLocation')?.value.trim();
  const hasPin=Boolean(grievancePins.current||grievancePins.problem);
  if(hasArea||hasPin)return;
  event.preventDefault();
  event.stopImmediatePropagation();
  showToast(localStorage.getItem('sg_lang')==='hi'?'क्षेत्र दर्ज करें या कोई एक स्थान पिन करें।':'Enter an area or set either location pin.');
},true);

// Toast
function showToast(msg){const t=$('#toast');if(!t)return;t.querySelector('span').textContent=msg;t.classList.add('show');clearTimeout(window.toastTimer);window.toastTimer=setTimeout(()=>t.classList.remove('show'),2600)}window.showToast=showToast;

// Rotate service categories while keeping the system-status header fixed.
const rotatingCategories=[
  {emoji:'💧',en:'Water Supply',hi:'जल आपूर्ति',messageEn:'There has been no water supply in our village for two days.',messageHi:'हमारे गाँव में दो दिनों से पानी की आपूर्ति नहीं है।',departmentEn:'Water Department',departmentHi:'जल विभाग',resultCategory:'Water',total:399},
  {emoji:'⚡',en:'Electricity',hi:'बिजली',messageEn:'Power has been unavailable in our area since yesterday.',messageHi:'हमारे क्षेत्र में कल से बिजली उपलब्ध नहीं है।',departmentEn:'Electricity Department',departmentHi:'बिजली विभाग',resultCategory:'Electricity',total:299},
  {emoji:'💡',en:'Street Light',hi:'स्ट्रीट लाइट',messageEn:'Street lights are not working near the main market.',messageHi:'मुख्य बाजार के पास स्ट्रीट लाइट काम नहीं कर रही हैं।',departmentEn:'Municipal Lighting',departmentHi:'नगर प्रकाश विभाग',resultCategory:'Street Light',total:68},
  {emoji:'🛣️',en:'Road',hi:'सड़क',messageEn:'The road near our ward has deep potholes and needs repair.',messageHi:'हमारे वार्ड की सड़क पर बड़े गड्ढे हैं और मरम्मत जरूरी है।',departmentEn:'Roads Department',departmentHi:'सड़क विभाग',resultCategory:'Roads',total:224},
  {emoji:'🏥',en:'Healthcare',hi:'स्वास्थ्य सेवा',messageEn:'The local health centre needs medicines and staff support.',messageHi:'स्थानीय स्वास्थ्य केंद्र को दवाओं और कर्मचारियों की जरूरत है।',departmentEn:'Health Department',departmentHi:'स्वास्थ्य विभाग',resultCategory:'Healthcare',total:40},
  {emoji:'🧹',en:'Sanitation',hi:'स्वच्छता',messageEn:'Waste collection has not happened in our locality this week.',messageHi:'इस सप्ताह हमारे क्षेत्र में कचरा संग्रह नहीं हुआ है।',departmentEn:'Sanitation Department',departmentHi:'स्वच्छता विभाग',resultCategory:'Sanitation',total:175},
  {emoji:'🚰',en:'Drainage',hi:'जल निकासी',messageEn:'Blocked drains are causing waterlogging after rainfall.',messageHi:'नालियाँ बंद होने से बारिश के बाद जलभराव हो रहा है।',departmentEn:'Drainage Department',departmentHi:'जल निकासी विभाग',resultCategory:'Drainage',total:22},
  {emoji:'🌱',en:'Environment',hi:'पर्यावरण',messageEn:'Smoke and waste near the park are affecting the local environment.',messageHi:'पार्क के पास धुआँ और कचरा स्थानीय पर्यावरण को प्रभावित कर रहे हैं।',departmentEn:'Environment Department',departmentHi:'पर्यावरण विभाग',resultCategory:'Environment',total:20}
];
const aiCard=$('.ai-card'),aiCategory=aiCard?.querySelector('.analysis-grid div:nth-child(1) strong'),aiPreview=aiCard?.querySelector('.complaint-preview p'),aiDepartment=aiCard?.querySelector('.route-box strong'),aiCategoryIcon=aiCard?.querySelector('.complaint-icon'),aiCategoryEmoji=aiCard?.querySelector('.category-label-emoji');let rotatingIndex=0;
function rotateCategory(){if(!aiCard||!aiCategory||!aiPreview||!aiDepartment)return;const item=rotatingCategories[rotatingIndex%rotatingCategories.length],hi=localStorage.getItem('sg_lang')==='hi',textNode=[...aiCategory.childNodes].find(node=>node.nodeType===Node.TEXT_NODE&&node.textContent.trim());if(textNode)textNode.textContent=` ${hi?item.hi:item.en}`;else aiCategory.textContent=hi?item.hi:item.en;if(aiCategoryEmoji)aiCategoryEmoji.textContent=item.emoji;if(aiCategoryIcon)aiCategoryIcon.innerHTML=`<span class="category-emoji" aria-hidden="true">${item.emoji}</span>`;aiPreview.textContent=hi?`“${item.messageHi}”`:`“${item.messageEn}”`;aiDepartment.textContent=hi?item.departmentHi:item.departmentEn;aiCard.classList.remove('category-swipe-left');void aiCard.offsetWidth;aiCard.classList.add('category-swipe-left');rotatingIndex=(rotatingIndex+1)%rotatingCategories.length}
const categoryDialog=$('#categoryActionDialog'),categoryTrigger=aiCard;let selectedActionCategory=rotatingCategories[0];
function openCategoryActions(){
  const label=aiCategory?.textContent||'';
  selectedActionCategory=rotatingCategories.find(item=>label.includes(item.en)||label.includes(item.hi))||selectedActionCategory;
  const hi=localStorage.getItem('sg_lang')==='hi';
  $('#categoryActionTitle').textContent=hi?selectedActionCategory.hi:selectedActionCategory.en;
  $('#categoryActionDepartment').textContent=hi?selectedActionCategory.departmentHi:selectedActionCategory.departmentEn;
  $('#categoryDepartmentTotal').textContent='—';
  $('#categoryDialogEyebrow').textContent=hi?'विभागीय सेवाएँ':'DEPARTMENT SERVICES';
  $('#categoryTotalLabel').textContent=hi?'विभाग की कुल शिकायतें':'DEPARTMENT COMPLAINTS';
  $('#categoryTotalNote').textContent=hi?'लाइव आँकड़े एडमिन डैशबोर्ड में उपलब्ध हैं':'Live metrics are available in the admin dashboard';
  $('#raiseCategoryLabel').textContent=hi?'शिकायत दर्ज करें':'Raise a complaint';
  $('#raiseCategoryNote').textContent=hi?'इस श्रेणी के लिए रिपोर्ट शुरू करें':'Start a report for this category';
  $('#trackCategoryLabel').textContent=hi?'शिकायत ट्रैक करें':'Track a complaint';
  $('#trackCategoryNote').textContent=hi?'शिकायत की स्थिति और प्रगति देखें':'Check complaint status and progress';
  $('#viewDepartmentTotalLabel').textContent=hi?'शिकायत डैशबोर्ड देखें':'View Complaint Dashboard';
  $('#viewDepartmentTotalNote').textContent=hi?'शिकायतों और विभागीय आँकड़ों का डैशबोर्ड खोलें':'Open complaint analytics and department totals';
  categoryTrigger?.setAttribute('aria-label',`${hi?selectedActionCategory.hi:selectedActionCategory.en} ${hi?'विभागीय विकल्प खोलें':'department actions'}`);
  categoryDialog?.showModal();
}
categoryTrigger?.addEventListener('click',openCategoryActions);
categoryTrigger?.addEventListener('keydown',event=>{if(event.target===categoryTrigger&&(event.key==='Enter'||event.key===' ')){event.preventDefault();openCategoryActions()}});
$('#closeCategoryDialog')?.addEventListener('click',()=>categoryDialog?.close());
categoryDialog?.addEventListener('click',event=>{if(event.target===categoryDialog)categoryDialog.close()});
$('#raiseCategoryComplaint')?.addEventListener('click',()=>{
  $('#selectedComplaintCategory').value=selectedActionCategory.resultCategory;
  $('#selectedCategoryBanner').hidden=false;
  $('#selectedCategoryBanner span').textContent=`${localStorage.getItem('sg_lang')==='hi'?'चयनित श्रेणी':'Selected category'}: ${localStorage.getItem('sg_lang')==='hi'?selectedActionCategory.hi:selectedActionCategory.en}`;
  categoryDialog.close();
  location.hash='report';
  setTimeout(()=>$('#complaintText')?.focus(),150);
});
$('#clearSelectedCategory')?.addEventListener('click',()=>{$('#selectedComplaintCategory').value='';$('#selectedCategoryBanner').hidden=true});
$('#trackCategoryComplaint')?.addEventListener('click',()=>{
  categoryDialog.close();
  if(!$('#trackingId').value)$('#trackingId').value='';
  location.hash='track';
  setTimeout(()=>$('#trackButton')?.click(),150);
});
$('#viewDepartmentTotal')?.addEventListener('click',()=>{
  const hi=localStorage.getItem('sg_lang')==='hi';
  const department=hi?selectedActionCategory.departmentHi:selectedActionCategory.departmentEn;
  categoryDialog.close();
  location.hash='dashboard';
  showToast(department+' - live metrics are available in the admin dashboard');
});
setInterval(rotateCategory,5000);
// Administrative analytics are loaded from real API values in admin.html.\n\n// Map
if(window.L&&$('#complaintMap')){const indiaBounds=[[6.4,68.1],[35.7,97.4]],map=L.map('complaintMap',{minZoom:4,maxZoom:18,maxBounds:indiaBounds,maxBoundsViscosity:.85}).setView([23.2599,77.4126],5.5);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap contributors'}).addTo(map);if(!document.getElementById('mapMotionStyle')){const style=document.createElement('style');style.id='mapMotionStyle';style.textContent='.custom-pin span{display:grid;place-items:center;width:38px;height:38px;border:3px solid rgba(255,255,255,.8);border-radius:50%;color:#fff;font-weight:800;box-shadow:0 0 0 0 rgba(14,165,233,.55);animation:mapPulse 2.4s ease-out infinite}.custom-pin:nth-child(2) span{animation-delay:.8s}.custom-pin:nth-child(3) span{animation-delay:1.6s}@keyframes mapPulse{0%{box-shadow:0 0 0 0 rgba(14,165,233,.6)}70%{box-shadow:0 0 0 14px rgba(14,165,233,0)}100%{box-shadow:0 0 0 0 rgba(14,165,233,0)}}';document.head.appendChild(style)}window.grievanceMap=map;setTimeout(()=>map.invalidateSize(),400)}

if(window.grievanceMap){
  const map=window.grievanceMap;
  for(const kind of ['current','problem'])if(grievancePins[kind])setGrievancePin(kind,grievancePins[kind].latitude,grievancePins[kind].longitude);
  map.on('click',event=>setGrievancePin('problem',event.latlng.lat,event.latlng.lng));
}


})();
