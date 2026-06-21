/**
 * Bioverse — App.js
 * ==================
 * Global navigation, profile selection, dan module navigation.
 */

// ─── Profile Selection ─────────────────────────────────────────

/**
 * Navigate ke halaman pembelajaran kategori.
 * @param {string} category - Kategori ABK
 */
function selectProfile(category) {
  window.location.href = '/learn/' + category;
}

/**
 * Navigate ke modul pembelajaran tertentu.
 * @param {string} category - Kategori ABK
 * @param {number} moduleId - ID modul
 * @param {number} step - Step index (default: 0)
 */
function navigateToModule(category, moduleId, step) {
  step = step || 0;
  window.location.href = '/learn/' + category + '/' + moduleId + '?step=' + step;
}

/**
 * Navigate ke step berikutnya dalam modul.
 */
function nextStep(category, moduleId, currentStep, totalSteps) {
  if (currentStep < totalSteps - 1) {
    navigateToModule(category, moduleId, currentStep + 1);
  }
}

/**
 * Navigate ke step sebelumnya dalam modul.
 */
function prevStep(category, moduleId, currentStep) {
  if (currentStep > 0) {
    navigateToModule(category, moduleId, currentStep - 1);
  }
}

/**
 * Kembali ke halaman profil selector.
 */
function goHome() {
  window.location.href = '/';
}


// ─── Audio Controls ─────────────────────────────────────────────

var currentAudio = null;
var isAudioPlaying = false;

/**
 * Toggle audio playback.
 * @param {string} src - Path ke file audio
 * @param {number} speed - Kecepatan playback (default: 1.0)
 */
function toggleAudio(src, speed) {
  speed = speed || 1.0;
  var btn = document.getElementById('audio-play-btn');

  if (currentAudio && isAudioPlaying) {
    currentAudio.pause();
    isAudioPlaying = false;
    if (btn) {
      btn.textContent = '▶️';
      btn.classList.remove('au-audio-btn--active', 'tn-audio-btn--active');
    }
    return;
  }

  if (!currentAudio || currentAudio.src !== src) {
    if (currentAudio) currentAudio.pause();
    currentAudio = new Audio(src);
    currentAudio.playbackRate = speed;
    currentAudio.addEventListener('ended', function() {
      isAudioPlaying = false;
      if (btn) {
        btn.textContent = '▶️';
        btn.classList.remove('au-audio-btn--active', 'tn-audio-btn--active');
      }
    });
  }

  currentAudio.play().then(function() {
    isAudioPlaying = true;
    if (btn) {
      btn.textContent = '⏸️';
      btn.classList.add('au-audio-btn--active', 'tn-audio-btn--active');
    }
  }).catch(function(err) {
    console.warn('[Audio] Playback failed:', err.message);
  });
}

/**
 * Replay audio dari awal.
 */
function replayAudio() {
  if (currentAudio) {
    currentAudio.currentTime = 0;
    currentAudio.play().catch(function() {});
    isAudioPlaying = true;
    var btn = document.getElementById('audio-play-btn');
    if (btn) {
      btn.textContent = '⏸️';
      btn.classList.add('au-audio-btn--active', 'tn-audio-btn--active');
    }
  }
}


// ─── Page Load ──────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function() {
  // Add page enter animation
  var main = document.querySelector('[role="main"]');
  if (main) {
    main.classList.add('page-enter');
  }

  // Set up keyboard navigation for profile cards
  var cards = document.querySelectorAll('.profile-card');
  cards.forEach(function(card) {
    card.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        card.click();
      }
    });
  });
});
