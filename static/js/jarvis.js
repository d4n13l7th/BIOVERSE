/* Jarvis client-side module for Tunanetra learning page.
 - Feature detection for SpeechRecognition
 - Web Audio Analyser for audio-reactive wave
 - STT via SpeechRecognition (per utterance)
 - Fetch to /api/jarvis/query with transcript
 - TTS via SpeechSynthesis
 - Simple UI state management
*/

(() => {
  const statusEl = document.getElementById('jarvis-status');
  const botEl = document.getElementById('jarvis-bot');
  const textEl = document.getElementById('jarvis-text');
  const canvas = document.getElementById('wave-canvas');
  const ctx = canvas ? canvas.getContext('2d') : null;

  function setStatus(s) {
    if (!statusEl) return;
    statusEl.innerText = s;
  }

  // FEATURE DETECTION
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition || null;
  if (!SpeechRecognition) {
    setStatus('STT tidak tersedia');
    // show fallback message
    return;
  }

  // AUDIO VISUALIZER
  let audioCtx, analyser, dataArray, source;
  function setupAudioVisualizer(stream) {
    try {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      analyser = audioCtx.createAnalyser();
      analyser.fftSize = 2048;
      dataArray = new Uint8Array(analyser.frequencyBinCount);
      source = audioCtx.createMediaStreamSource(stream);
      source.connect(analyser);
      draw();
    } catch (e) {
      console.warn('Visualizer init failed', e);
    }
  }

  function draw() {
    if (!ctx || !analyser) return;
    requestAnimationFrame(draw);
    analyser.getByteTimeDomainData(dataArray);
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.lineWidth = 2;
    ctx.strokeStyle = botEl.classList.contains('is-speaking') ? '#5B9BD5' : '#D4A853';
    ctx.beginPath();
    const sliceWidth = canvas.width * 1.0 / dataArray.length;
    let x = 0;
    for(let i = 0; i < dataArray.length; i++) {
      const v = dataArray[i] / 128.0;
      const y = v * canvas.height/2;
      if(i === 0) ctx.moveTo(x,y);
      else ctx.lineTo(x,y);
      x += sliceWidth;
    }
    ctx.lineTo(canvas.width, canvas.height/2);
    ctx.stroke();
  }

  // Resize canvas
  function resizeCanvas() {
    if (!canvas) return;
    canvas.width = canvas.clientWidth * devicePixelRatio;
    canvas.height = canvas.clientHeight * devicePixelRatio;
  }
  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();

  // SPEECH RECOGNITION
  const recog = new SpeechRecognition();
  recog.lang = 'id-ID';
  recog.interimResults = false;
  recog.continuous = false; // per-utterance

  recog.onstart = () => {
    botEl.classList.remove('is-speaking');
    botEl.classList.add('is-listening');
    setStatus('LISTENING');
  };
  recog.onresult = (ev) => {
    const transcript = Array.from(ev.results).map(r => r[0].transcript).join(' ');
    setStatus('PROCESSING');
    botEl.classList.remove('is-listening');
    fetchQuery(transcript);
  };
  recog.onerror = (e) => {
    console.warn('Recognition error', e);
    setStatus('ERROR');
    // restart after short delay
    setTimeout(()=>recog.start(), 1000);
  };
  recog.onend = () => {
    // keep listening cycle after TTS finishes; nothing here
  };

  async function fetchQuery(transcript) {
    const studentId = document.body.dataset.studentId || null;
    const sessionId = document.body.dataset.sessionId || null;
    try {
      const res = await fetch('/api/jarvis/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: studentId, session_id: sessionId, transcript })
      });
      const data = await res.json();
      const text = data.response_text || 'Maaf, saya tidak mengerti.';
      speak(text);
    } catch (e) {
      console.error(e);
      setStatus('ERROR');
      setTimeout(()=>recog.start(), 1000);
    }
  }

  // TTS
  function speak(text) {
    if (!('speechSynthesis' in window)) {
      // fallback: show text
      textEl.innerText = text;
      setStatus('SPEAKING');
      setTimeout(()=>{ setStatus('LISTENING'); recog.start(); }, 3000);
      return;
    }
    botEl.classList.remove('is-listening');
    botEl.classList.add('is-speaking');
    setStatus('SPEAKING');
    textEl.innerText = text;
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'id-ID';
    u.onend = () => {
      botEl.classList.remove('is-speaking');
      botEl.classList.add('is-listening');
      setStatus('LISTENING');
      recog.start();
    };
    speechSynthesis.cancel();
    speechSynthesis.speak(u);
  }

  // Start microphone and visualizer
  async function initMic() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setupAudioVisualizer(stream);
    } catch (e) {
      console.warn('Microphone permission denied', e);
    }
  }

  // Start sequence
  initMic().then(()=>{
    // Begin recognition loop
    try { recog.start(); } catch (e) { /* ignore start errors */ }
  });

})();
