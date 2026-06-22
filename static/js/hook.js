/* Hook system for Autis learning page.
 * CONSTRAINT: hook_enabled DEFAULT = FALSE
 * All functions check hook_enabled from sessionStorage before running.
 * 
 * Features:
 * - Idle monitoring (mousemove, keydown, touchstart, scroll)
 * - Escalation stages (1, 2, 3) with smooth animations
 * - Premack reward gate (check task status before pet interaction)
 * - Quiz completion listener (loose coupling via Custom Event)
 */

(() => {
  // ────────────────────────────────────────
  // 1. INIT — Check hook_enabled, setup sessionStorage
  // ────────────────────────────────────────

  const studentId = document.body.dataset.studentId || null;
  const sessionId = document.body.dataset.sessionId || null;
  const petContainer = document.getElementById('pet-container');
  const petMessage = document.getElementById('pet-message');
  
  if (!studentId || !sessionId) {
    console.warn('[Hook] Missing studentId or sessionId');
    return;
  }

  let hookEnabled = false;
  let currentEscalationLevel = 0;
  let idleTimer = null;
  let lastInteractionTime = Date.now();

  // Fetch hook_enabled from session state
  async function initHookState() {
    try {
      const res = await fetch(`/api/session/${sessionId}`);
      const session = await res.json();
      hookEnabled = session.hook_enabled || false;
      sessionStorage.setItem('hook_enabled', hookEnabled);
      
      if (!hookEnabled) {
        console.log('[Hook] Hook disabled — idle detection inactive');
        return;
      }
      
      setupIdleMonitor();
    } catch (e) {
      console.warn('[Hook] Failed to fetch session state', e);
    }
  }

  initHookState();

  // ────────────────────────────────────────
  // 2. IDLE MONITOR (only if hook_enabled = true)
  // ────────────────────────────────────────

  const threshold = 180; // default 180 seconds

  function setupIdleMonitor() {
    const resetIdleTimer = () => {
      lastInteractionTime = Date.now();
      if (idleTimer) clearTimeout(idleTimer);
      currentEscalationLevel = 0;
      if (petContainer) {
        petContainer.classList.remove('pet-stage-1', 'pet-stage-2', 'pet-stage-3');
        petContainer.classList.add('pet-hidden');
      }
      idleTimer = setTimeout(checkIdleEscalation, threshold * 1000);
    };

    // Event listeners for activity
    document.addEventListener('mousemove', resetIdleTimer);
    document.addEventListener('keydown', resetIdleTimer);
    document.addEventListener('touchstart', resetIdleTimer);
    document.addEventListener('scroll', resetIdleTimer);

    // Page Visibility API
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        // Page hidden — trigger idle check
        checkIdleEscalation();
      } else {
        // Page visible again — reset
        resetIdleTimer();
      }
    });

    resetIdleTimer();
  }

  function checkIdleEscalation() {
    if (!hookEnabled) return;
    
    const idleSecs = Math.floor((Date.now() - lastInteractionTime) / 1000);

    if (idleSecs < threshold) return;

    // Determine stage and POST to server async
    const stage1 = threshold;
    const stage2 = threshold + 120;
    const stage3 = threshold + 240;

    let level = 1;
    if (idleSecs >= stage3) level = 3;
    else if (idleSecs >= stage2) level = 2;
    else if (idleSecs >= stage1) level = 1;

    currentEscalationLevel = level;

    // POST to /api/hook/idle-event (non-blocking)
    fetch('/api/hook/idle-event', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        student_id: studentId,
        session_id: sessionId,
        idle_duration: idleSecs,
        current_screen: window.location.pathname
      })
    }).catch(e => console.warn('[Hook] idle-event POST failed', e));

    // Update UI escalation
    updatePetEscalation(level);
  }

  // ────────────────────────────────────────
  // 3. ESCALATION STAGES — Pet visualization
  // ────────────────────────────────────────

  function updatePetEscalation(level) {
    if (!petContainer) return;

    petContainer.classList.remove('pet-hidden', 'pet-stage-1', 'pet-stage-2', 'pet-stage-3');

    if (level === 0) {
      petContainer.classList.add('pet-hidden');
    } else if (level === 1) {
      petContainer.classList.add('pet-stage-1');
      if (petMessage) petMessage.textContent = 'Halo! Ayo kita lanjutkan belajar...';
    } else if (level === 2) {
      petContainer.classList.add('pet-stage-2');
      if (petMessage) petMessage.textContent = 'Psst... jangan lupa tugas kita!';
      // Optional: play soft audio
    } else if (level === 3) {
      petContainer.classList.add('pet-stage-3');
      if (petMessage) petMessage.textContent = 'Saatnya kita selesaikan materi! 🎯';
    }
  }

  // ────────────────────────────────────────
  // 4. PREMACK REWARD GATE — Pet click handler
  // ────────────────────────────────────────

  if (petContainer) {
    petContainer.addEventListener('click', async (e) => {
      try {
        // Fetch reward status from server
        const res = await fetch(`/api/hook/reward-status/${studentId}`);
        const status = await res.json();

        if (status.current_task_status === 'in_progress') {
          // Task still in progress — show redirect message
          if (petMessage) {
            petMessage.textContent = '⏳ Selesaikan materi terlebih dahulu!';
          }
          return;
        }

        if (status.current_task_status === 'reward_unlocked') {
          // Check if reward is still valid (compare server timestamp)
          const expiresAt = new Date(status.reward_expires_at);
          const now = new Date();
          
          if (now < expiresAt) {
            // Valid reward — open interactive mode
            if (petMessage) {
              petMessage.textContent = '🎉 Yay! Saatnya bermain!';
            }
            // TODO: owner will implement pet interactive mode here
            console.log('[Hook] Pet interactive mode would start here');
            return;
          } else {
            // Expired — show message and revert
            if (petMessage) {
              petMessage.textContent = '⏰ Reward sudah habis. Kembali ke materi!';
            }
            return;
          }
        }
      } catch (e) {
        console.warn('[Hook] reward-status fetch failed', e);
      }
    });
  }

  // ────────────────────────────────────────
  // 5. QUIZ COMPLETION LISTENER (Loose Coupling)
  // ────────────────────────────────────────

  document.addEventListener('quiz-complete', async (e) => {
    const detail = e.detail || {};
    const module = detail.module || 'unknown';
    const score = detail.score || 0;

    console.log('[Hook] quiz-complete event received:', detail);

    try {
      // Update task status to completed_pending_reward
      const updateRes = await fetch(`/api/session/${sessionId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          current_task_status: 'completed_pending_reward',
          last_topic_attempted: module
        })
      });

      if (!updateRes.ok) {
        console.warn('[Hook] session update failed');
        return;
      }

      // Claim reward immediately
      const claimRes = await fetch('/api/hook/reward-claim', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          student_id: studentId,
          session_id: sessionId
        })
      });

      if (claimRes.ok) {
        const rewardStatus = await claimRes.json();
        console.log('[Hook] reward claimed:', rewardStatus);
        // Pet is now in reward_unlocked state — will respond to clicks
      } else {
        console.warn('[Hook] reward-claim failed');
      }
    } catch (e) {
      console.error('[Hook] quiz-complete handler error', e);
    }
  });

})();
