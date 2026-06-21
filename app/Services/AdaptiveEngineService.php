<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

/**
 * AdaptiveEngineService
 *
 * Service layer untuk berkomunikasi dengan microservice Python (FastAPI).
 * Mengirim data evaluasi siswa dan menerima rekomendasi adaptif
 * (naik/turun level, ubah kecepatan, ganti modul, dll).
 */
class AdaptiveEngineService
{
    /**
     * Base URL endpoint Python FastAPI.
     *
     * @var string
     */
    private string $baseUrl;

    /**
     * Timeout untuk HTTP request ke engine (dalam detik).
     *
     * @var int
     */
    private int $timeout;

    public function __construct()
    {
        $this->baseUrl = config('services.adaptive_engine.url', 'http://localhost:8000');
        $this->timeout = config('services.adaptive_engine.timeout', 10);
    }

    /**
     * Mengirim data evaluasi ke engine Python untuk mendapatkan rekomendasi.
     *
     * @param  array  $evaluationData  Data evaluasi siswa
     * @return array  Rekomendasi dari engine (level baru, kecepatan, modul berikutnya)
     */
    public function evaluate(array $evaluationData): array
    {
        try {
            $response = Http::timeout($this->timeout)
                ->post("{$this->baseUrl}/api/evaluate", $evaluationData);

            if ($response->successful()) {
                return $response->json();
            }

            Log::warning('Adaptive Engine returned non-success status', [
                'status' => $response->status(),
                'body'   => $response->body(),
            ]);

            return $this->fallbackRecommendation($evaluationData);

        } catch (\Exception $e) {
            Log::error('Failed to communicate with Adaptive Engine', [
                'error'   => $e->getMessage(),
                'payload' => $evaluationData,
            ]);

            return $this->fallbackRecommendation($evaluationData);
        }
    }

    /**
     * Mendapatkan status kesehatan engine Python.
     *
     * @return array
     */
    public function healthCheck(): array
    {
        try {
            $response = Http::timeout(5)->get("{$this->baseUrl}/health");

            return [
                'status'  => $response->successful() ? 'healthy' : 'unhealthy',
                'details' => $response->json(),
            ];
        } catch (\Exception $e) {
            return [
                'status' => 'unreachable',
                'error'  => $e->getMessage(),
            ];
        }
    }

    /**
     * Rekomendasi fallback jika engine Python tidak tersedia.
     * Menjaga pengalaman belajar tetap berjalan meskipun
     * microservice sedang down.
     *
     * @param  array  $data
     * @return array
     */
    private function fallbackRecommendation(array $data): array
    {
        return [
            'action'         => 'maintain',
            'new_level'      => null,
            'message'        => 'Sistem adaptif sedang tidak tersedia. Melanjutkan di level saat ini.',
            'audio_speed'    => 1.0,
            'animation_speed'=> 1.0,
            'fallback'       => true,
        ];
    }
}
