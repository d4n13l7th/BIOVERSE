<template>
  <div class="autis-layout" role="main" aria-label="Halaman Pembelajaran Autis">
    <!--
      Layout khusus Autis:
      - Desain minimalis, bersih, tanpa distraksi
      - Warna pastel yang menenangkan
      - TANPA pop-up, modal, atau transisi mendadak
      - Animasi lambat dan smooth
      - Struktur prediktif (selalu konsisten)
    -->

    <!-- Header sederhana dan konsisten -->
    <header class="au-header">
      <h1 class="au-title">{{ moduleTitle }}</h1>
      <div class="au-progress-bar">
        <div
          class="au-progress-fill"
          :style="{ width: progressPercent + '%' }"
          role="progressbar"
          :aria-valuenow="progressPercent"
          aria-valuemin="0"
          aria-valuemax="100"
        ></div>
      </div>
    </header>

    <!-- Konten utama — satu fokus pada satu waktu -->
    <section class="au-content">
      <!-- Animasi organ (kecepatan lambat untuk autis) -->
      <div class="au-animation-area">
        <OrganAnimation
          v-if="animationPath"
          :animation-path="animationPath"
          :speed="0.5"
          aria-label="Animasi organ tubuh"
        />
      </div>

      <!-- Audio (dengan kontrol visual yang jelas) -->
      <div class="au-audio-area">
        <AudioFeedback
          v-if="audioSrc"
          :src="audioSrc"
          :speed="0.75"
          :autoplay="false"
          :show-controls="true"
          label="Dengarkan penjelasan"
        />
      </div>

      <!-- Teks penjelasan (singkat, satu paragraf) -->
      <div class="au-text-area">
        <p class="au-description">{{ description }}</p>
      </div>
    </section>

    <!-- Area kuis (tampil inline, TANPA pop-up) -->
    <section v-if="quizActive" class="au-quiz" aria-label="Latihan soal">
      <p class="au-question">{{ currentQuestion }}</p>

      <div class="au-options">
        <button
          v-for="(option, index) in options"
          :key="index"
          class="au-option-btn"
          :class="{ 'au-option-btn--selected': selectedIndex === index }"
          @click="selectAnswer(option, index)"
        >
          {{ option.text }}
        </button>
      </div>

      <!-- Feedback inline (tanpa pop-up) -->
      <div v-if="feedbackMessage" class="au-feedback" role="status">
        <p>{{ feedbackMessage }}</p>
      </div>
    </section>

    <!-- Navigasi bawah — selalu terlihat, prediktif -->
    <nav class="au-nav">
      <button class="au-nav-btn" @click="previousModule">
        ← Sebelumnya
      </button>
      <span class="au-nav-indicator">{{ currentStep }} / {{ totalSteps }}</span>
      <button class="au-nav-btn au-nav-btn--next" @click="nextModule">
        Selanjutnya →
      </button>
    </nav>
  </div>
</template>

<script>
import AudioFeedback from '../components/AudioFeedback.vue';
import OrganAnimation from '../components/OrganAnimation.vue';

export default {
  name: 'AutisLayout',

  components: {
    AudioFeedback,
    OrganAnimation,
  },

  props: {
    student: { type: Object, required: true },
    category: { type: String, default: 'autis' },
    config: { type: Object, default: () => ({}) },
  },

  data() {
    return {
      moduleTitle: 'Sistem Pencernaan',
      description: '',
      audioSrc: '/audio/pencernaan/voiceover.mp3',
      animationPath: '/animations/pencernaan/main.json',
      quizActive: false,
      currentQuestion: '',
      options: [],
      selectedIndex: null,
      feedbackMessage: '',
      currentStep: 1,
      totalSteps: 5,
      progressPercent: 20,
    };
  },

  methods: {
    selectAnswer(option, index) {
      this.selectedIndex = index;
      // Feedback inline, tanpa pop-up
      this.feedbackMessage = option.correct
        ? '✅ Benar! Hebat sekali.'
        : '🔄 Coba lagi ya. Tidak apa-apa.';
      this.$emit('answer-selected', option);
    },

    previousModule() {
      // TODO: Navigasi mulus tanpa transisi mendadak.
    },

    nextModule() {
      // TODO: Navigasi mulus tanpa transisi mendadak.
    },
  },
};
</script>

<style scoped>
/* ── Tema Pastel & Minimalis untuk Autis ── */

.autis-layout {
  background-color: #fdf6f0;
  color: #3d3d3d;
  min-height: 100vh;
  font-family: 'Nunito', 'Segoe UI', sans-serif;
  font-size: 1.125rem;
  line-height: 1.8;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
}

.au-header {
  text-align: center;
}

.au-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #5b4a8a;
  margin-bottom: 1rem;
}

.au-progress-bar {
  width: 100%;
  height: 0.5rem;
  background-color: #e8dff5;
  border-radius: 1rem;
  overflow: hidden;
}

.au-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #b8a9d9, #7c6aad);
  border-radius: 1rem;
  transition: width 0.8s ease;
}

.au-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.au-animation-area {
  width: 100%;
  max-width: 400px;
  background-color: #ffffff;
  border-radius: 1.5rem;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.au-audio-area {
  display: flex;
  justify-content: center;
}

.au-text-area {
  text-align: center;
  max-width: 600px;
}

.au-description {
  color: #555;
  font-size: 1.125rem;
}

.au-quiz {
  background-color: #ffffff;
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.au-question {
  font-size: 1.25rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: 1.5rem;
  color: #5b4a8a;
}

.au-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.au-option-btn {
  background-color: #f0eaf8;
  color: #3d3d3d;
  border: 2px solid transparent;
  border-radius: 1rem;
  padding: 1rem 1.5rem;
  font-size: 1.125rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.au-option-btn:hover {
  border-color: #b8a9d9;
  background-color: #e8dff5;
}

.au-option-btn--selected {
  border-color: #7c6aad;
  background-color: #e8dff5;
  font-weight: 600;
}

.au-feedback {
  text-align: center;
  margin-top: 1rem;
  font-size: 1.125rem;
  padding: 1rem;
  border-radius: 0.75rem;
  background-color: #f0eaf8;
}

.au-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  padding-top: 1rem;
}

.au-nav-btn {
  background-color: #e8dff5;
  color: #5b4a8a;
  border: none;
  border-radius: 0.75rem;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.au-nav-btn:hover {
  background-color: #d4c8e8;
}

.au-nav-btn--next {
  background-color: #b8a9d9;
  color: #ffffff;
}

.au-nav-indicator {
  font-size: 0.875rem;
  color: #999;
}
</style>
