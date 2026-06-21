<template>
  <div class="tunarungu-layout" role="main" aria-label="Halaman Pembelajaran Tunarungu">
    <!--
      Layout khusus Tunarungu:
      - Dominasi visual (gambar, animasi, warna)
      - Takarir (subtitle) selalu aktif
      - Tanpa ketergantungan pada audio
      - Isyarat visual untuk feedback (flash, border color)
      - Vibration cues untuk interaksi penting
    -->

    <!-- Header visual -->
    <header class="tr-header">
      <h1 class="tr-title">{{ moduleTitle }}</h1>
      <div class="tr-level-badge">Level {{ currentLevel }}</div>
    </header>

    <!-- Konten utama — visual-first -->
    <section class="tr-content">
      <!-- Area animasi (full-width, menjadi fokus utama) -->
      <div class="tr-animation-area">
        <OrganAnimation
          v-if="animationPath"
          :animation-path="animationPath"
          :speed="animationSpeed"
          aria-label="Animasi visual organ"
        />
      </div>

      <!-- Takarir / Subtitle (selalu terlihat) -->
      <div class="tr-subtitle-area" role="region" aria-label="Teks penjelasan">
        <div class="tr-subtitle-box">
          <p class="tr-subtitle-text">{{ currentSubtitle }}</p>
        </div>
      </div>

      <!-- Area visual instruksi (gambar/ikon pengganti audio) -->
      <div class="tr-visual-cues">
        <div
          v-for="(cue, index) in visualCues"
          :key="index"
          class="tr-cue-card"
        >
          <span class="tr-cue-icon">{{ cue.icon }}</span>
          <span class="tr-cue-label">{{ cue.label }}</span>
        </div>
      </div>
    </section>

    <!-- Area kuis — visual-heavy -->
    <section v-if="quizActive" class="tr-quiz" aria-label="Kuis visual">
      <p class="tr-question">{{ currentQuestion }}</p>

      <div class="tr-options">
        <button
          v-for="(option, index) in options"
          :key="index"
          class="tr-option-btn"
          :class="{
            'tr-option-btn--correct': showResult && option.correct,
            'tr-option-btn--wrong': showResult && selectedIndex === index && !option.correct,
          }"
          @click="selectAnswer(option, index)"
        >
          <span class="tr-option-icon" v-if="option.icon">{{ option.icon }}</span>
          {{ option.text }}
        </button>
      </div>

      <!-- Feedback visual (flash warna, bukan teks panjang) -->
      <div
        v-if="showResult"
        class="tr-feedback"
        :class="isCorrect ? 'tr-feedback--correct' : 'tr-feedback--wrong'"
        role="alert"
      >
        <span class="tr-feedback-icon">{{ isCorrect ? '✅' : '❌' }}</span>
        <span>{{ isCorrect ? 'Benar!' : 'Coba lagi' }}</span>
      </div>
    </section>

    <!-- Navigasi bawah -->
    <nav class="tr-nav">
      <button class="tr-nav-btn" @click="previousModule">
        ← Sebelumnya
      </button>
      <div class="tr-step-dots">
        <span
          v-for="step in totalSteps"
          :key="step"
          class="tr-dot"
          :class="{ 'tr-dot--active': step <= currentStep }"
        ></span>
      </div>
      <button class="tr-nav-btn tr-nav-btn--primary" @click="nextModule">
        Selanjutnya →
      </button>
    </nav>
  </div>
</template>

<script>
import OrganAnimation from '../components/OrganAnimation.vue';
import { triggerHaptic } from '../utils/hapticFeedback.js';

export default {
  name: 'TunarunguLayout',

  components: {
    OrganAnimation,
  },

  props: {
    student: { type: Object, required: true },
    category: { type: String, default: 'tunarungu' },
    config: { type: Object, default: () => ({}) },
  },

  data() {
    return {
      moduleTitle: 'Sistem Pencernaan',
      currentLevel: 1,
      animationPath: '/animations/pencernaan/main.json',
      animationSpeed: 1.0,
      currentSubtitle: 'Makanan masuk melalui mulut dan dikunyah oleh gigi.',
      visualCues: [
        { icon: '🦷', label: 'Mulut & Gigi' },
        { icon: '🫁', label: 'Kerongkongan' },
        { icon: '🫀', label: 'Lambung' },
      ],
      quizActive: false,
      currentQuestion: '',
      options: [],
      selectedIndex: null,
      showResult: false,
      isCorrect: false,
      currentStep: 1,
      totalSteps: 5,
    };
  },

  methods: {
    selectAnswer(option, index) {
      this.selectedIndex = index;
      this.isCorrect = option.correct;
      this.showResult = true;

      // Vibration feedback untuk interaksi
      triggerHaptic(option.correct ? 'success' : 'error');

      this.$emit('answer-selected', option);
    },

    previousModule() {
      triggerHaptic('light');
      // TODO: Navigasi ke modul sebelumnya.
    },

    nextModule() {
      triggerHaptic('light');
      // TODO: Navigasi ke modul berikutnya.
    },
  },
};
</script>

<style scoped>
/* ── Tema Visual-Dominant untuk Tunarungu ── */

.tunarungu-layout {
  background: linear-gradient(180deg, #eef4fb 0%, #f8faff 100%);
  color: #2d3748;
  min-height: 100vh;
  font-family: 'Nunito', 'Segoe UI', sans-serif;
  font-size: 1.125rem;
  line-height: 1.6;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 900px;
  margin: 0 auto;
}

.tr-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tr-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #2b6cb0;
}

.tr-level-badge {
  background-color: #bee3f8;
  color: #2b6cb0;
  padding: 0.375rem 1rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 700;
}

.tr-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.tr-animation-area {
  width: 100%;
  background-color: #ffffff;
  border-radius: 1.5rem;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.tr-subtitle-area {
  width: 100%;
}

.tr-subtitle-box {
  background-color: #2d3748;
  color: #ffffff;
  padding: 1rem 1.5rem;
  border-radius: 1rem;
  text-align: center;
}

.tr-subtitle-text {
  font-size: 1.25rem;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.tr-visual-cues {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.tr-cue-card {
  background-color: #ffffff;
  border: 2px solid #bee3f8;
  border-radius: 1rem;
  padding: 1rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  min-width: 100px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
  transition: transform 0.2s ease;
}

.tr-cue-card:hover {
  transform: translateY(-2px);
}

.tr-cue-icon {
  font-size: 2rem;
}

.tr-cue-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #4a5568;
}

.tr-quiz {
  background-color: #ffffff;
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.tr-question {
  font-size: 1.25rem;
  font-weight: 700;
  text-align: center;
  color: #2b6cb0;
  margin-bottom: 1.5rem;
}

.tr-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}

.tr-option-btn {
  background-color: #ebf8ff;
  color: #2d3748;
  border: 2px solid #bee3f8;
  border-radius: 1rem;
  padding: 1rem;
  font-size: 1.125rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: center;
  transition: all 0.2s ease;
}

.tr-option-btn:hover {
  border-color: #63b3ed;
  background-color: #bee3f8;
}

.tr-option-btn--correct {
  border-color: #48bb78;
  background-color: #c6f6d5;
}

.tr-option-btn--wrong {
  border-color: #fc8181;
  background-color: #fed7d7;
}

.tr-option-icon {
  font-size: 1.5rem;
}

.tr-feedback {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 1rem;
  font-size: 1.25rem;
  font-weight: 700;
  animation: feedbackFlash 0.3s ease;
}

.tr-feedback--correct {
  background-color: #c6f6d5;
  color: #22543d;
}

.tr-feedback--wrong {
  background-color: #fed7d7;
  color: #742a2a;
}

.tr-feedback-icon {
  font-size: 1.5rem;
}

@keyframes feedbackFlash {
  0% { opacity: 0; transform: scale(0.95); }
  100% { opacity: 1; transform: scale(1); }
}

.tr-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.tr-nav-btn {
  background-color: #ebf8ff;
  color: #2b6cb0;
  border: 2px solid #bee3f8;
  border-radius: 0.75rem;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tr-nav-btn:hover {
  background-color: #bee3f8;
}

.tr-nav-btn--primary {
  background-color: #3182ce;
  color: #ffffff;
  border-color: #3182ce;
}

.tr-step-dots {
  display: flex;
  gap: 0.375rem;
}

.tr-dot {
  width: 0.625rem;
  height: 0.625rem;
  border-radius: 50%;
  background-color: #cbd5e0;
  transition: background-color 0.3s ease;
}

.tr-dot--active {
  background-color: #3182ce;
}
</style>
