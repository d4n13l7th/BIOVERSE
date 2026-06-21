<template>
  <div class="audio-feedback" role="status" :aria-live="ariaLive">
    <!-- Status indikator audio (hanya muncul jika screen reader aktif) -->
    <span class="sr-only" v-if="isPlaying">
      Sedang memutar: {{ currentLabel }}
    </span>

    <!-- Kontrol audio visual (opsional, ditampilkan sesuai kategori ABK) -->
    <div v-if="showControls" class="audio-controls">
      <button
        @click="togglePlayback"
        :aria-label="isPlaying ? 'Pause audio' : 'Putar audio'"
        class="audio-btn"
      >
        {{ isPlaying ? '⏸️' : '▶️' }}
      </button>

      <button
        @click="replay"
        aria-label="Putar ulang audio"
        class="audio-btn"
      >
        🔁
      </button>
    </div>
  </div>
</template>

<script>
import { Howl } from 'howler';

export default {
  name: 'AudioFeedback',

  props: {
    /**
     * Path ke file audio (voiceover/SFX).
     */
    src: {
      type: String,
      required: true,
    },

    /**
     * Kecepatan pemutaran (0.5 - 2.0).
     * Untuk anak autis, direkomendasikan 0.75.
     */
    speed: {
      type: Number,
      default: 1.0,
      validator: (v) => v >= 0.25 && v <= 4.0,
    },

    /**
     * Volume audio (0.0 - 1.0).
     */
    volume: {
      type: Number,
      default: 0.8,
    },

    /**
     * Otomatis putar saat komponen dimuat.
     * Aktifkan untuk kategori tunanetra.
     */
    autoplay: {
      type: Boolean,
      default: false,
    },

    /**
     * Apakah audio diloop.
     */
    loop: {
      type: Boolean,
      default: false,
    },

    /**
     * Label deskriptif untuk aksesibilitas (screen reader).
     */
    label: {
      type: String,
      default: 'Audio instruksi',
    },

    /**
     * Tampilkan kontrol audio visual.
     * Untuk tunanetra, kontrol ini biasanya disembunyikan.
     */
    showControls: {
      type: Boolean,
      default: true,
    },
  },

  data() {
    return {
      howl: null,
      isPlaying: false,
      currentLabel: this.label,
    };
  },

  computed: {
    ariaLive() {
      return this.autoplay ? 'assertive' : 'polite';
    },
  },

  watch: {
    src(newSrc) {
      this.loadAudio(newSrc);
    },
    speed(newSpeed) {
      if (this.howl) {
        this.howl.rate(newSpeed);
      }
    },
  },

  mounted() {
    this.loadAudio(this.src);
  },

  beforeUnmount() {
    this.cleanup();
  },

  methods: {
    /**
     * Memuat file audio menggunakan Howler.js.
     */
    loadAudio(src) {
      this.cleanup();

      this.howl = new Howl({
        src: [src],
        volume: this.volume,
        rate: this.speed,
        loop: this.loop,
        html5: true,
        onplay: () => {
          this.isPlaying = true;
          this.$emit('play');
        },
        onend: () => {
          this.isPlaying = false;
          this.$emit('ended');
        },
        onstop: () => {
          this.isPlaying = false;
          this.$emit('stop');
        },
        onloaderror: (_id, error) => {
          console.error('[AudioFeedback] Load error:', error);
          this.$emit('error', error);
        },
      });

      if (this.autoplay) {
        this.howl.play();
      }
    },

    /**
     * Toggle play/pause.
     */
    togglePlayback() {
      if (!this.howl) return;

      if (this.isPlaying) {
        this.howl.pause();
        this.isPlaying = false;
      } else {
        this.howl.play();
      }
    },

    /**
     * Putar ulang dari awal.
     */
    replay() {
      if (!this.howl) return;
      this.howl.stop();
      this.howl.play();
    },

    /**
     * Membersihkan instance Howl.
     */
    cleanup() {
      if (this.howl) {
        this.howl.unload();
        this.howl = null;
      }
    },
  },
};
</script>

<style scoped>
.audio-feedback {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.audio-controls {
  display: flex;
  gap: 0.25rem;
}

.audio-btn {
  background: none;
  border: 2px solid currentColor;
  border-radius: 50%;
  width: 3rem;
  height: 3rem;
  font-size: 1.25rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s ease, background-color 0.15s ease;
}

.audio-btn:hover {
  transform: scale(1.1);
  background-color: rgba(0, 0, 0, 0.05);
}

.audio-btn:focus-visible {
  outline: 3px solid #4a90d9;
  outline-offset: 2px;
}

/* Screen reader only */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>
