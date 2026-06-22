/**
 * Bioverse — Quiz Engine
 * ========================
 * Mesin kuis interaktif yang mengirim hasil evaluasi
 * ke adaptive engine via REST API.
 *
 * Flow:
 * 1. User klik "Mulai Kuis"
 * 2. Pertanyaan ditampilkan satu per satu
 * 3. Timer response_time berjalan per pertanyaan
 * 4. Setelah jawaban dipilih → feedback visual
 * 5. Setelah semua pertanyaan → kirim ke /api/evaluate
 * 6. Terima rekomendasi → update UI
 */

var QuizEngine = (function() {
  // ── State ──
  var questions = [];
  var currentIndex = 0;
  var score = 0;
  var totalCorrect = 0;
  var startTime = 0;
  var totalResponseTime = 0;
  var studentId = 0;
  var sessionId = ''; // NEW: session ID for Hook integration
  var moduleName = '';
  var isActive = false;
  var answered = false;

  /**
   * Inisialisasi quiz engine.
   * @param {Object} config
   * @param {Array} config.questions - Array pertanyaan dari template
   * @param {number} config.studentId - ID siswa
   * @param {string} config.sessionId - Session ID
   * @param {string} config.moduleName - Nama modul
   */
  function init(config) {
    questions = config.questions || [];
    studentId = config.studentId || 0;
    moduleName = config.moduleName || '';
    currentIndex = 0;
    score = 0;
    totalCorrect = 0;
    totalResponseTime = 0;
    isActive = true;
    answered = false;

    if (questions.length > 0) {
      showQuestion(0);
    }
  }

  /**
   * Tampilkan pertanyaan ke-n.
   */
  function showQuestion(index) {
    var q = questions[index];
    if (!q) return;

    currentIndex = index;
    answered = false;
    startTime = Date.now();

    // Update counter
    var counter = document.getElementById('quiz-counter');
    if (counter) {
      counter.textContent = 'Pertanyaan ' + (index + 1) + ' dari ' + questions.length;
    }

    // Update question text
    var questionEl = document.getElementById('quiz-question');
    if (questionEl) {
      questionEl.textContent = q.question;
    }

    // Render options
    var optionsContainer = document.getElementById('quiz-options');
    if (optionsContainer) {
      optionsContainer.innerHTML = '';
      q.options.forEach(function(option, optIndex) {
        var btn = document.createElement('button');
        btn.className = getOptionClass();
        btn.setAttribute('data-index', optIndex);
        btn.setAttribute('data-correct', option.correct ? 'true' : 'false');

        if (option.icon) {
          var icon = document.createElement('span');
          icon.className = getOptionIconClass();
          icon.textContent = option.icon;
          btn.appendChild(icon);
        }

        var text = document.createTextNode(option.text);
        btn.appendChild(text);

        btn.addEventListener('click', function() {
          if (!answered) {
            selectAnswer(optIndex, option);
          }
        });

        optionsContainer.appendChild(btn);
      });
    }

    // Hide feedback
    var feedback = document.getElementById('quiz-feedback');
    if (feedback) {
      feedback.style.display = 'none';
    }

    // Hide next button
    var nextBtn = document.getElementById('quiz-next-btn');
    if (nextBtn) {
      nextBtn.style.display = 'none';
    }
  }

  /**
   * Handle jawaban yang dipilih.
   */
  function selectAnswer(optIndex, option) {
    if (answered) return;
    answered = true;

    var responseTime = (Date.now() - startTime) / 1000; // detik
    totalResponseTime += responseTime;

    var isCorrect = option.correct === true;

    if (isCorrect) {
      totalCorrect++;
    }

    // Update score (percentage based)
    score = Math.round((totalCorrect / questions.length) * 100);

    // Visual feedback on options
    var buttons = document.querySelectorAll('#quiz-options button');
    buttons.forEach(function(btn, idx) {
      btn.disabled = true;
      var correct = btn.getAttribute('data-correct') === 'true';
      if (correct) {
        btn.classList.add(getOptionCorrectClass());
      } else if (idx === optIndex && !isCorrect) {
        btn.classList.add(getOptionWrongClass());
      }
    });

    // Show feedback
    var feedback = document.getElementById('quiz-feedback');
    if (feedback) {
      feedback.style.display = 'block';
      feedback.className = getFeedbackClass(isCorrect);

      var feedbackText = document.getElementById('quiz-feedback-text');
      if (feedbackText) {
        feedbackText.textContent = isCorrect
          ? '✅ Benar! Hebat sekali!'
          : '❌ Belum tepat. Tidak apa-apa!';
      }

      var explanationEl = document.getElementById('quiz-explanation');
      if (explanationEl) {
        var q = questions[currentIndex];
        explanationEl.textContent = q.explanation || '';
      }
    }

    // Haptic feedback
    if (typeof triggerHaptic === 'function') {
      triggerHaptic(isCorrect ? 'success' : 'error');
    }

    // Show next button or finish
    var nextBtn = document.getElementById('quiz-next-btn');
    if (nextBtn) {
      if (currentIndex < questions.length - 1) {
        nextBtn.textContent = 'Pertanyaan Berikutnya →';
        nextBtn.style.display = 'block';
        nextBtn.onclick = function() {
          showQuestion(currentIndex + 1);
        };
      } else {
        nextBtn.textContent = '🎉 Lihat Hasil';
        nextBtn.style.display = 'block';
        nextBtn.onclick = function() {
          finishQuiz();
        };
      }
    }
  }

  /**
   * Selesai kuis — kirim evaluasi ke API.
   */
  function finishQuiz() {
    isActive = false;
    var avgResponseTime = totalResponseTime / questions.length;

    // Show loading state
    var quizSection = document.getElementById('quiz-section');
    if (quizSection) {
      quizSection.innerHTML =
        '<div style="text-align: center; padding: 2rem;">' +
        '<p style="font-size: 2rem; margin-bottom: 1rem;">⏳</p>' +
        '<p>Menganalisis jawaban...</p>' +
        '</div>';
    }

    // Send to adaptive engine
    var payload = {
      student_id: studentId,
      module: moduleName,
      score: score,
      response_time: Math.round(avgResponseTime * 10) / 10,
      history: []
    };

    fetch('/api/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    .then(function(res) { return res.json(); })
    .then(function(data) {
      showResult(data);
    })
    .catch(function(err) {
      console.error('[Quiz] Evaluation error:', err);
      showResult({
        action: 'maintain',
        message: 'Evaluasi selesai! Skor: ' + score,
        audio_speed: 1.0,
        animation_speed: 1.0,
        fallback: true
      });
    });
  }

  /**
   * Tampilkan hasil evaluasi.
   */
  function showResult(recommendation) {
    var quizSection = document.getElementById('quiz-section');
    if (!quizSection) return;

    var actionEmoji = {
      'increase': '🚀',
      'decrease': '🌱',
      'maintain': '⭐'
    };

    var actionLabel = {
      'increase': 'Naik Level!',
      'decrease': 'Penguatan Materi',
      'maintain': 'Lanjut di Level Ini'
    };

    var emoji = actionEmoji[recommendation.action] || '⭐';
    var label = actionLabel[recommendation.action] || 'Evaluasi Selesai';

    quizSection.innerHTML =
      '<div style="text-align: center; padding: 2rem;">' +
        '<p style="font-size: 4rem; margin-bottom: 1rem;">' + emoji + '</p>' +
        '<h2 style="font-size: 1.5rem; margin-bottom: 0.5rem;">' + label + '</h2>' +
        '<p style="font-size: 1.125rem; color: #666; margin-bottom: 1.5rem;">' +
          recommendation.message +
        '</p>' +
        '<div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem;">' +
          '<div style="background: rgba(0,0,0,0.05); padding: 0.75rem 1.25rem; border-radius: 0.75rem;">' +
            '<div style="font-size: 0.75rem; color: #999;">Skor</div>' +
            '<div style="font-size: 1.5rem; font-weight: 700;">' + score + '%</div>' +
          '</div>' +
          '<div style="background: rgba(0,0,0,0.05); padding: 0.75rem 1.25rem; border-radius: 0.75rem;">' +
            '<div style="font-size: 0.75rem; color: #999;">Benar</div>' +
            '<div style="font-size: 1.5rem; font-weight: 700;">' + totalCorrect + '/' + questions.length + '</div>' +
          '</div>' +
        '</div>' +
        '<button onclick="goHome()" style="padding: 0.75rem 2rem; border-radius: 0.75rem; font-weight: 600; cursor: pointer; border: none; background: #e8dff5; color: #5b4a8a; font-size: 1rem; margin-right: 0.5rem;">' +
          '← Kembali ke Profil' +
        '</button>' +
      '</div>';

    // DISPATCH CUSTOM EVENT FOR HOOK.JS (loose coupling)
    // After showResult is called, emit quiz-complete event
    // hook.js will listen and handle reward claiming
    try {
      document.dispatchEvent(new CustomEvent('quiz-complete', {
        detail: {
          student_id: studentId,
          session_id: sessionId,
          module: moduleName,
          score: score
        }
      }));
    } catch (e) {
      console.warn('[Quiz] Failed to dispatch quiz-complete event', e);
    }
  }

  // ── CSS class helpers (auto-detect layout) ──

  function getOptionClass() {
    if (document.querySelector('.autis-layout')) return 'au-option-btn';
    if (document.querySelector('.tunanetra-layout')) return 'tn-option-btn';
    if (document.querySelector('.tunarungu-layout')) return 'tr-option-btn';
    return 'au-option-btn';
  }

  function getOptionIconClass() {
    if (document.querySelector('.autis-layout')) return 'au-option-icon';
    if (document.querySelector('.tunanetra-layout')) return 'tn-option-icon';
    if (document.querySelector('.tunarungu-layout')) return 'tr-option-icon';
    return 'au-option-icon';
  }

  function getOptionCorrectClass() {
    if (document.querySelector('.autis-layout')) return 'au-option-btn--correct';
    if (document.querySelector('.tunanetra-layout')) return 'tn-option-btn--correct';
    if (document.querySelector('.tunarungu-layout')) return 'tr-option-btn--correct';
    return 'au-option-btn--correct';
  }

  function getOptionWrongClass() {
    if (document.querySelector('.autis-layout')) return 'au-option-btn--wrong';
    if (document.querySelector('.tunanetra-layout')) return 'tn-option-btn--wrong';
    if (document.querySelector('.tunarungu-layout')) return 'tr-option-btn--wrong';
    return 'au-option-btn--wrong';
  }

  function getFeedbackClass(isCorrect) {
    var base = '';
    if (document.querySelector('.autis-layout')) {
      base = 'au-feedback';
      return base + ' ' + (isCorrect ? 'au-feedback--correct' : 'au-feedback--wrong');
    }
    if (document.querySelector('.tunanetra-layout')) {
      base = 'tn-feedback';
      return base + ' ' + (isCorrect ? 'tn-feedback--correct' : 'tn-feedback--wrong');
    }
    if (document.querySelector('.tunarungu-layout')) {
      base = 'tr-feedback';
      return base + ' ' + (isCorrect ? 'tr-feedback--correct' : 'tr-feedback--wrong');
    }
    return 'au-feedback ' + (isCorrect ? 'au-feedback--correct' : 'au-feedback--wrong');
  }

  // ── Public API ──
  return {
    init: init,
    showQuestion: showQuestion,
  };
})();
