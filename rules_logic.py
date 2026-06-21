"""
Bioverse - Adaptive Rules Logic
================================
Logika penentu naik/turun tingkat kesulitan berdasarkan
performa siswa (skor, waktu respon, tren historis).
"""

from typing import Optional


class AdaptiveRulesEngine:
    """
    Engine berbasis aturan (rule-based) untuk menentukan
    penyesuaian tingkat kesulitan pembelajaran.

    Threshold default:
    - Skor >= 80 dengan waktu respon cepat → Naikkan level
    - Skor <= 40 atau waktu respon sangat lambat → Turunkan level
    - Di antara keduanya → Pertahankan level saat ini
    """

    # ─── Konfigurasi Threshold ────────────────────────────────

    SCORE_THRESHOLD_HIGH: float = 80.0
    SCORE_THRESHOLD_LOW: float = 40.0

    RESPONSE_TIME_FAST: float = 30.0   # detik
    RESPONSE_TIME_SLOW: float = 120.0  # detik

    CONSECUTIVE_SUCCESS_NEEDED: int = 3
    CONSECUTIVE_FAILURE_NEEDED: int = 2

    def process(
        self,
        student_id: int,
        module: str,
        score: float,
        response_time: float,
        history: list[dict],
    ) -> dict:
        """
        Memproses data evaluasi dan menghasilkan rekomendasi.

        Args:
            student_id:    ID siswa
            module:        Nama modul yang baru diselesaikan
            score:         Skor evaluasi terbaru (0-100)
            response_time: Waktu respon dalam detik
            history:       Riwayat evaluasi sebelumnya

        Returns:
            dict dengan keys: action, new_level, audio_speed,
            animation_speed, message, fallback
        """
        trend = self._analyze_trend(history)
        action = self._determine_action(score, response_time, trend)

        return {
            "action": action,
            "new_level": self._calculate_new_level(action, history),
            "audio_speed": self._recommend_audio_speed(action, score),
            "animation_speed": self._recommend_animation_speed(action, score),
            "message": self._generate_message(action, score, module),
            "fallback": False,
        }

    def _analyze_trend(self, history: list[dict]) -> str:
        """
        Menganalisis tren performa dari riwayat evaluasi.

        Returns:
            'improving' | 'declining' | 'stable'
        """
        if len(history) < 2:
            return "stable"

        recent_scores = [h.get("score", 0) for h in history[:5]]
        avg_recent = sum(recent_scores) / len(recent_scores)

        if len(history) >= 5:
            older_scores = [h.get("score", 0) for h in history[5:10]]
            if older_scores:
                avg_older = sum(older_scores) / len(older_scores)
                if avg_recent > avg_older + 10:
                    return "improving"
                elif avg_recent < avg_older - 10:
                    return "declining"

        return "stable"

    def _determine_action(
        self, score: float, response_time: float, trend: str
    ) -> str:
        """Menentukan aksi: increase, decrease, atau maintain."""
        if score >= self.SCORE_THRESHOLD_HIGH and response_time <= self.RESPONSE_TIME_FAST:
            return "increase"

        if score <= self.SCORE_THRESHOLD_LOW or response_time >= self.RESPONSE_TIME_SLOW:
            return "decrease"

        if trend == "improving" and score >= 70:
            return "increase"

        if trend == "declining" and score <= 50:
            return "decrease"

        return "maintain"

    def _calculate_new_level(
        self, action: str, history: list[dict]
    ) -> Optional[int]:
        """Menghitung level baru berdasarkan aksi."""
        # TODO: Implementasi logika level berdasarkan data siswa dari DB.
        level_map = {"increase": 1, "decrease": -1, "maintain": 0}
        return level_map.get(action, 0)

    def _recommend_audio_speed(self, action: str, score: float) -> float:
        """Rekomendasi kecepatan audio."""
        if action == "decrease":
            return 0.75  # Perlambat suara instruksi
        elif action == "increase" and score >= 90:
            return 1.25  # Percepat sedikit untuk tantangan
        return 1.0

    def _recommend_animation_speed(self, action: str, score: float) -> float:
        """Rekomendasi kecepatan animasi."""
        if action == "decrease":
            return 0.5  # Perlambat animasi agar lebih mudah dipahami
        elif action == "increase":
            return 1.0
        return 0.75

    def _generate_message(
        self, action: str, score: float, module: str
    ) -> str:
        """Menghasilkan pesan deskriptif untuk log/UI."""
        messages = {
            "increase": f"Bagus! Skor {score:.0f} di modul '{module}'. "
                        f"Naik ke level berikutnya.",
            "decrease": f"Skor {score:.0f} di modul '{module}'. "
                        f"Menurunkan tingkat kesulitan untuk penguatan materi.",
            "maintain": f"Skor {score:.0f} di modul '{module}'. "
                        f"Melanjutkan di level saat ini.",
        }
        return messages.get(action, "Evaluasi selesai.")
