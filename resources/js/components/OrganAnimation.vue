<template>
  <div
    class="organ-animation"
    ref="animationContainer"
    role="img"
    :aria-label="ariaLabel"
  >
    <!-- Fallback jika animasi gagal dimuat -->
    <div v-if="hasError" class="animation-fallback">
      <p>⚠️ Animasi tidak dapat dimuat.</p>
    </div>
  </div>
</template>

<script>
import lottie from 'lottie-web';

export default {
  name: 'OrganAnimation',

  props: {
    /**
     * Path ke file JSON Lottie (relatif terhadap /public/animations/).
     */
    animationPath: {
      type: String,
      required: true,
    },

    /**
     * Kecepatan animasi.
     * - Anak autis: 0.5 (lebih lambat agar tidak overwhelm)
     * - Default: 1.0
     * - Bisa dipercepat untuk tantangan: 1.5
     */
    speed: {
      type: Number,
      default: 1.0,
    },

    /**
     * Apakah animasi di-loop.
     */
    loop: {
      type: Boolean,
      default: true,
    },

    /**
     * Otomatis mulai animasi saat komponen dimuat.
     */
    autoplay: {
      type: Boolean,
      default: true,
    },

    /**
     * Label aksesibilitas untuk screen reader.
     */
    ariaLabel: {
      type: String,
      default: 'Animasi organ tubuh',
    },
  },

  data() {
    return {
      animationInstance: null,
      hasError: false,
    };
  },

  watch: {
    animationPath() {
      this.loadAnimation();
    },
    speed(newSpeed) {
      if (this.animationInstance) {
        this.animationInstance.setSpeed(newSpeed);
      }
    },
  },

  mounted() {
    this.loadAnimation();
  },

  beforeUnmount() {
    this.destroyAnimation();
  },

  methods: {
    /**
     * Memuat dan merender animasi Lottie.
     */
    loadAnimation() {
      this.destroyAnimation();
      this.hasError = false;

      try {
        this.animationInstance = lottie.loadAnimation({
          container: this.$refs.animationContainer,
          renderer: 'svg',
          loop: this.loop,
          autoplay: this.autoplay,
          path: this.animationPath,
        });

        this.animationInstance.setSpeed(this.speed);

        this.animationInstance.addEventListener('DOMLoaded', () => {
          this.$emit('loaded');
        });

        this.animationInstance.addEventListener('complete', () => {
          this.$emit('complete');
        });

        this.animationInstance.addEventListener('data_failed', () => {
          this.hasError = true;
          this.$emit('error', 'Failed to load animation data');
        });
      } catch (error) {
        this.hasError = true;
        console.error('[OrganAnimation] Error:', error);
        this.$emit('error', error.message);
      }
    },

    /**
     * Memutar animasi.
     */
    play() {
      this.animationInstance?.play();
    },

    /**
     * Menjeda animasi.
     */
    pause() {
      this.animationInstance?.pause();
    },

    /**
     * Menghentikan animasi dan kembali ke frame awal.
     */
    stop() {
      this.animationInstance?.stop();
    },

    /**
     * Menuju frame tertentu (berguna untuk highlight bagian organ).
     */
    goToFrame(frame, isFrame = true) {
      this.animationInstance?.goToAndStop(frame, isFrame);
    },

    /**
     * Membersihkan instance animasi.
     */
    destroyAnimation() {
      if (this.animationInstance) {
        this.animationInstance.destroy();
        this.animationInstance = null;
      }
    },
  },
};
</script>

<style scoped>
.organ-animation {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  aspect-ratio: 1 / 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.animation-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background-color: #f5f5f5;
  border-radius: 1rem;
  color: #666;
  font-size: 1rem;
}
</style>
