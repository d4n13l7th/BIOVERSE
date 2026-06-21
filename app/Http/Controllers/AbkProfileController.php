<?php

namespace App\Http\Controllers;

use App\Models\Student;
use Illuminate\Http\Request;
use Inertia\Inertia;

/**
 * AbkProfileController
 *
 * Mengatur rute UI berdasarkan kategori ABK (Anak Berkebutuhan Khusus).
 * Controller ini bertanggung jawab untuk menentukan layout dan konfigurasi
 * tampilan yang sesuai berdasarkan profil disabilitas siswa.
 */
class AbkProfileController extends Controller
{
    /**
     * Mapping kategori ABK ke layout Vue yang sesuai.
     */
    private const CATEGORY_LAYOUT_MAP = [
        'tunanetra'  => 'TunanetraLayout',
        'autis'      => 'AutisLayout',
        'tunarungu'  => 'TunarunguLayout',
    ];

    /**
     * Menampilkan halaman utama berdasarkan profil ABK siswa.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Models\Student  $student
     * @return \Inertia\Response
     */
    public function show(Request $request, Student $student)
    {
        $category = $student->abk_category;
        $layout   = self::CATEGORY_LAYOUT_MAP[$category] ?? 'AutisLayout';

        return Inertia::render($layout, [
            'student'  => $student->load('progressTracker'),
            'category' => $category,
            'config'   => $this->getUiConfig($category),
        ]);
    }

    /**
     * Mendapatkan konfigurasi UI spesifik untuk setiap kategori ABK.
     *
     * @param  string  $category
     * @return array
     */
    private function getUiConfig(string $category): array
    {
        $configs = [
            'tunanetra' => [
                'high_contrast'     => true,
                'screen_reader'     => true,
                'font_scale'        => 1.5,
                'audio_primary'     => true,
                'haptic_feedback'   => true,
            ],
            'autis' => [
                'minimal_ui'        => true,
                'pastel_colors'     => true,
                'disable_popups'    => true,
                'animation_speed'   => 0.5,
                'transition_smooth' => true,
            ],
            'tunarungu' => [
                'visual_dominant'   => true,
                'subtitle_enabled'  => true,
                'sign_language'     => true,
                'vibration_cues'    => true,
                'animation_speed'   => 1.0,
            ],
        ];

        return $configs[$category] ?? $configs['autis'];
    }
}
