/* Visual-Haptic module for Tunarungu learning page.
 * 
 * Features:
 * - Feature detection for vibration API
 * - Haptic trigger with visual fallback
 * - Interaction handler for .interactive-element clicks
 * - Video-infographic sync via sync_timestamps
 * - Intersection Observer for animate-in
 * - Content preloader for next content
 */

(() => {
  // ────────────────────────────────────────
  // 1. FEATURE DETECTION
  // ────────────────────────────────────────

  const hasVibration = 'vibrate' in navigator;
  sessionStorage.setItem('has_vibration', hasVibration);

  // ────────────────────────────────────────
  // 2. HAPTIC EXECUTOR
  // ────────────────────────────────────────

  window.triggerHaptic = function(pattern) {
    if (hasVibration) {
      navigator.vibrate(pattern);
    } else {
      triggerVisualFallback(pattern);
    }
  };

  function triggerVisualFallback(pattern) {
    const overlay = document.getElementById('haptic-overlay');
    if (!overlay) return;

    // Calculate total duration
    const duration = pattern.reduce((a, b) => a + b, 0);

    // Determine color based on context (simplified: assume correct for green)
    const color = pattern[0] === 200 ? '#4CAF50' : pattern[0] === 100 ? '#FF5722' : '#2196F3';

    overlay.style.backgroundColor = color;
    overlay.style.opacity = '0.3';

    // Animate back to transparent
    setTimeout(() => {
      overlay.style.transition = `opacity ${duration}ms ease-out`;
      overlay.style.opacity = '0';
    }, 50);

    setTimeout(() => {
      overlay.style.transition = 'none';
      overlay.style.backgroundColor = 'transparent';
    }, duration + 50);
  }

  // ────────────────────────────────────────
  // 3. INTERACTION HANDLER
  // ────────────────────────────────────────

  const studentId = document.body.dataset.studentId || null;
  const sessionId = document.body.dataset.sessionId || null;

  if (!studentId || !sessionId) {
    console.warn('[Visual-Haptic] Missing studentId or sessionId');
    return;
  }

  // Attach click handlers to interactive elements
  document.querySelectorAll('.interactive-element').forEach(el => {
    el.addEventListener('click', async (e) => {
      const elementId = el.id || el.dataset.elementId || 'unknown';
      const actionType = el.dataset.actionType || 'click';

      // Disable all interactive elements during loading
      document.querySelectorAll('.interactive-element').forEach(ie => {
        ie.disabled = true;
        ie.style.opacity = '0.6';
      });

      try {
        const response = await fetch('/api/visual/interaction', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            student_id: studentId,
            session_id: sessionId,
            element_id: elementId,
            action_type: actionType,
            is_correct: el.dataset.isCorrect === 'true'
          })
        });

        if (!response.ok) {
          throw new Error('interaction failed');
        }

        const data = await response.json();

        // Trigger haptic/visual feedback IMMEDIATE
        triggerHaptic(data.haptic_pattern);

        if (data.is_correct) {
          el.classList.add('interactive-element--correct');
          // Preload next content if available
          if (data.next_content) {
            preloadNext(data.next_content);
            setTimeout(() => {
              // Navigate to next content
              window.location.href = data.next_url || '#';
            }, 800);
          }
        } else {
          el.classList.add('interactive-element--wrong', 'shake');
          setTimeout(() => {
            el.classList.remove('interactive-element--wrong', 'shake');
          }, 600);
        }
      } catch (e) {
        console.error('[Visual-Haptic] interaction error', e);
      } finally {
        // Re-enable interactive elements
        document.querySelectorAll('.interactive-element').forEach(ie => {
          ie.disabled = false;
          ie.style.opacity = '1';
        });
      }
    });
  });

  // ────────────────────────────────────────
  // 4. VIDEO-INFOGRAPHIC SYNC
  // ────────────────────────────────────────

  const video = document.querySelector('video');
  const syncTimestamps = video ? JSON.parse(video.dataset.syncTimestamps || '[]') : [];

  if (video && syncTimestamps.length > 0) {
    video.addEventListener('timeupdate', () => {
      const currentTime = Math.floor(video.currentTime);

      syncTimestamps.forEach(ts => {
        const { time, elementSelector } = ts;
        const el = document.querySelector(elementSelector);
        if (!el) return;

        if (Math.floor(time) === currentTime) {
          el.classList.add('infographic-highlight');
        } else {
          el.classList.remove('infographic-highlight');
        }
      });
    });
  }

  // ────────────────────────────────────────
  // 5. INTERSECTION OBSERVER (animate-in)
  // ────────────────────────────────────────

  const observerOptions = {
    threshold: 0.3,
    rootMargin: '0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
        observer.unobserve(entry.target); // once: true equivalent
      }
    });
  }, observerOptions);

  document.querySelectorAll('.infographic-section').forEach(el => {
    observer.observe(el);
  });

  // ────────────────────────────────────────
  // 6. CONTENT PRELOADER
  // ────────────────────────────────────────

  function preloadNext(nextContent) {
    if (!nextContent) return;

    // Preload video
    if (nextContent.video_url) {
      const videoEl = document.createElement('video');
      videoEl.src = nextContent.video_url;
      videoEl.style.display = 'none';
      document.body.appendChild(videoEl);
    }

    // Preload images
    if (nextContent.images && Array.isArray(nextContent.images)) {
      nextContent.images.forEach(img => {
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = img;
        document.head.appendChild(link);
      });
    }
  }

})();
