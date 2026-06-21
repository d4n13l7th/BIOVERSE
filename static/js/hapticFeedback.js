/**
 * Haptic Feedback Utility
 * =======================
 * Trigger getaran pada perangkat mobile/tablet menggunakan
 * Vibration API. Menyediakan pola getaran berbeda untuk
 * berbagai konteks interaksi.
 *
 * Kompatibilitas: Android Chrome, Samsung Internet, Opera Mobile.
 * iOS Safari TIDAK mendukung Vibration API.
 *
 * Dimigrasi dari resources/js/utils/hapticFeedback.js
 * Diubah dari ES module export → global function.
 */

/**
 * Cek apakah perangkat mendukung Vibration API.
 * @returns {boolean}
 */
function isHapticSupported() {
  return 'vibrate' in navigator;
}

/**
 * Pola getaran yang tersedia.
 * Angka dalam array: [vibrate_ms, pause_ms, vibrate_ms, ...]
 */
var HAPTIC_PATTERNS = {
  // Getaran ringan — navigasi, sentuhan biasa
  light: [30],

  // Getaran sedang — konfirmasi pilihan
  medium: [50],

  // Getaran kuat — perhatian penting
  heavy: [100],

  // Pola sukses — dua getaran pendek (tik-tik)
  success: [40, 60, 40],

  // Pola error — satu getaran panjang
  error: [150],

  // Pola peringatan — tiga getaran pendek (tik-tik-tik)
  warning: [30, 50, 30, 50, 30],

  // Pola notifikasi — getaran bertahap
  notification: [50, 100, 80],
};

/**
 * Trigger getaran haptic pada perangkat.
 *
 * @param {string} pattern - Nama pola: 'light' | 'medium' | 'heavy' |
 *                           'success' | 'error' | 'warning' | 'notification'
 * @returns {boolean} true jika berhasil, false jika tidak didukung
 *
 * @example
 * // Pada saat user menekan tombol jawaban benar
 * triggerHaptic('success');
 *
 * // Pada saat navigasi
 * triggerHaptic('light');
 */
function triggerHaptic(pattern) {
  pattern = pattern || 'light';

  if (!isHapticSupported()) {
    return false;
  }

  var vibrationPattern = HAPTIC_PATTERNS[pattern];

  if (!vibrationPattern) {
    console.warn('[HapticFeedback] Unknown pattern: "' + pattern + '". Using "light".');
    navigator.vibrate(HAPTIC_PATTERNS.light);
    return true;
  }

  navigator.vibrate(vibrationPattern);
  return true;
}

/**
 * Menghentikan getaran yang sedang berjalan.
 * @returns {boolean}
 */
function stopHaptic() {
  if (!isHapticSupported()) return false;
  navigator.vibrate(0);
  return true;
}

/**
 * Trigger getaran kustom dengan pola manual.
 *
 * @param {number[]} pattern - Array angka [vibrate, pause, vibrate, ...]
 * @returns {boolean}
 */
function triggerCustomHaptic(pattern) {
  if (!isHapticSupported()) return false;
  if (!Array.isArray(pattern) || pattern.length === 0) {
    console.warn('[HapticFeedback] Invalid custom pattern.');
    return false;
  }
  navigator.vibrate(pattern);
  return true;
}
