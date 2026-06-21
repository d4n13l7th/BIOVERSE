<template>
  <div class="tunanetra-layout" role="main" aria-label="Halaman Pembelajaran Tunanetra">
    <!--
      Layout khusus Tunanetra:
      - High contrast (latar gelap, teks terang besar)
      - Screen-reader friendly (aria labels lengkap)
      - Audio sebagai media utama
      - Navigasi keyboard-first
      - Haptic feedback pada interaksi
    -->

    <!-- Header dengan navigasi keyboard-friendly -->
    <header class="tn-header" role="banner">
      <h1 class="tn-title" tabindex="0">{{ moduleTitle }}</h1>
      <p class="tn-subtitle" aria-live="polite">
        Level {{ currentLevel }} — {{ student.name }}
      </p>
    </header>

    <!-- Konten utama -->
    <section class="tn-content" aria-label="Area pembelajaran">
      <!-- Audio instruksi (autoplay untuk tunanetra) -->
      <AudioFeedback
        v-if="audioSrc"
        :src="audioSrc"
        :speed="audioSpeed"
        :autoplay="true"
        :show-controls="false"
        label="Instruksi audio"
        @ended="onAudioEnded"
      />

      <!-- Animasi organ (dengan deskripsi audio) -->
      <OrganAnimation
        v-if="animationPath"
        :animation-path="animationPath"
        :speed="animationSpeed"
        aria-label="Animasi ilustrasi organ"
      />

      <!-- Area interaksi/kuis -->
      <div class="tn-quiz" v-if="quizActive" role="form" aria-label="Kuis interaktif">
        <p class="tn-question" tabindex="0">{{ currentQuestion }}</p>
        <div class="tn-options">
          <button
            v-for="(option, index) in options"
            :key="index"
            class="tn-option-btn"
            :aria-label="`Pilihan ${index + 1}: ${option.text}`"
            @click="selectAnswer(option)"
            @keydown.enter="selectAnswer(option)"
          >
            {{ option.text }}
          </button>
        </div>
      </div>
    </section>

    <!-- Navigasi bawah -->
    <nav class="tn-nav" role="navigation" aria-label="Navigasi modul">
      <button
        class="tn-nav-btn"
        @click="previousModule"
        aria-label="Kembali ke modul sebelumnya"
      >
        ← Sebelumnya
      </button>
      <button
        class="tn-nav-btn tn-nav-btn--primary"
        @click="nextModule"
        aria-label="Lanjut ke modul berikutnya"
      >
        Selanjutnya →
      </button>
    </nav>
  </div>
</template>

<script>
import AudioFeedback from '../components/AudioFeedback.vue';
import OrganAnimation from '../components/OrganAnimation.vue';
import { triggerHaptic } from '../utils/hapticFeedback.js';

export default {
  name: 'TunanetraLayout',

  components: {
    AudioFeedback,
    OrganAnimation,
  },

  props: {
    student: { type: Object, required: true },
    category: { type: String, default: 'tunanetra' },
    config: { type: Object, default: () => ({}) },
  },

  data() {
    return {
      moduleTitle: 'Sistem Pencernaan',
      currentLevel: 1,
      audioSrc: '/audio/pencernaan/voiceover.mp3',
      audioSpeed: 1.0,
      animationPath: '/animations/pencernaan/main.json',
      animationSpeed: 1.0,
      quizActive: false,
      currentQuestion: '',
      options: [],
    };
  },

  methods: {
    onAudioEnded() {
      triggerHaptic('light');
      // TODO: Lanjut ke konten berikutnya atau aktifkan kuis.
    },

    selectAnswer(option) {
      triggerHaptic('medium');
      this.$emit('answer-selected', option);
      // TODO: Kirim jawaban ke EvaluationController.
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
/* ── High Contrast Theme untuk Tunanetra ── */

.tunanetra-layout {
  background-color: #0a0a0a;
  color: #fafafa;
  min-height: 100vh;
  font-family: 'Arial', sans-serif;
  font-size: 1.5rem;
  line-height: 2;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.tn-header {
  text-align: center;
  border-bottom: 3px solid #ffd700;
  padding-bottom: 1rem;
}

.tn-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #ffd700;
}

.tn-subtitle {
  font-size: 1.25rem;
  color: #cccccc;
}

.tn-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.tn-quiz {
  width: 100%;
  max-width: 600px;
}

.tn-question {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-align: center;
}

.tn-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tn-option-btn {
  background-color: #1a1a2e;
  color: #fafafa;
  border: 3px solid #ffd700;
  border-radius: 1rem;
  padding: 1.25rem 2rem;
  font-size: 1.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tn-option-btn:hover,
.tn-option-btn:focus {
  background-color: #ffd700;
  color: #0a0a0a;
  transform: scale(1.03);
  outline: none;
}

.tn-nav {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: auto;
}

.tn-nav-btn {
  background-color: #1a1a2e;
  color: #fafafa;
  border: 2px solid #ffd700;
  border-radius: 0.75rem;
  padding: 1rem 2rem;
  font-size: 1.25rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tn-nav-btn:hover,
.tn-nav-btn:focus {
  background-color: #ffd700;
  color: #0a0a0a;
}

.tn-nav-btn--primary {
  background-color: #ffd700;
  color: #0a0a0a;
}
</style>
