<?php

namespace App\Http\Controllers;

use App\Models\Student;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

/**
 * MultisensoryController
 *
 * Menyediakan aset audio/visual yang tepat berdasarkan kategori ABK
 * dan konteks pembelajaran. Controller ini mengelola distribusi
 * konten multisensori (suara, animasi, haptic cues).
 */
class MultisensoryController extends Controller
{
    /**
     * Mendapatkan daftar aset audio yang sesuai untuk modul tertentu.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  string  $module
     * @return \Illuminate\Http\JsonResponse
     */
    public function getAudioAssets(Request $request, string $module): JsonResponse
    {
        $student  = $request->user();
        $category = $student->abk_category ?? 'autis';

        $assets = $this->resolveAudioAssets($module, $category);

        return response()->json([
            'module'   => $module,
            'category' => $category,
            'audio'    => $assets,
        ]);
    }

    /**
     * Mendapatkan daftar aset animasi Lottie untuk modul tertentu.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  string  $module
     * @return \Illuminate\Http\JsonResponse
     */
    public function getAnimationAssets(Request $request, string $module): JsonResponse
    {
        $student  = $request->user();
        $category = $student->abk_category ?? 'autis';

        $assets = $this->resolveAnimationAssets($module, $category);

        return response()->json([
            'module'    => $module,
            'category'  => $category,
            'animation' => $assets,
        ]);
    }

    /**
     * Menentukan aset audio berdasarkan modul dan kategori ABK.
     *
     * @param  string  $module
     * @param  string  $category
     * @return array
     */
    private function resolveAudioAssets(string $module, string $category): array
    {
        // TODO: Implementasi logika pemilihan aset audio dari database/storage.
        // Contoh: anak tunarungu tidak memerlukan voice-over, tapi butuh vibration cues.
        return [
            'voiceover'   => $category !== 'tunarungu' ? "/audio/{$module}/voiceover.mp3" : null,
            'sfx'         => "/audio/{$module}/sfx.mp3",
            'speed'       => $category === 'autis' ? 0.75 : 1.0,
            'auto_play'   => $category === 'tunanetra',
        ];
    }

    /**
     * Menentukan aset animasi berdasarkan modul dan kategori ABK.
     *
     * @param  string  $module
     * @param  string  $category
     * @return array
     */
    private function resolveAnimationAssets(string $module, string $category): array
    {
        // TODO: Implementasi logika pemilihan animasi dari database/storage.
        return [
            'lottie_path' => "/animations/{$module}/main.json",
            'speed'       => $category === 'autis' ? 0.5 : 1.0,
            'loop'        => true,
            'autoplay'    => true,
        ];
    }
}
