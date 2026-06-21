<?php

namespace App\Http\Controllers;

use App\Models\ProgressTracker;
use App\Models\Student;
use App\Services\AdaptiveEngineService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

/**
 * EvaluationController
 *
 * Merekam hasil interaksi/kuis siswa dan mengirimkan data
 * ke Adaptive Engine (Python) untuk mendapatkan rekomendasi
 * penyesuaian tingkat kesulitan.
 */
class EvaluationController extends Controller
{
    public function __construct(
        private readonly AdaptiveEngineService $adaptiveEngine
    ) {}

    /**
     * Menyimpan hasil evaluasi/kuis siswa.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'student_id'    => 'required|exists:students,id',
            'module'        => 'required|string|max:100',
            'score'         => 'required|numeric|min:0|max:100',
            'response_time' => 'required|numeric|min:0',
            'interactions'  => 'nullable|array',
        ]);

        // Simpan progress ke database
        $progress = ProgressTracker::create([
            'student_id'    => $validated['student_id'],
            'module'        => $validated['module'],
            'score'         => $validated['score'],
            'response_time' => $validated['response_time'],
            'interactions'  => $validated['interactions'] ?? [],
            'evaluated_at'  => now(),
        ]);

        // Kirim data ke Adaptive Engine (Python) untuk analisis
        $recommendation = $this->adaptiveEngine->evaluate([
            'student_id'    => $validated['student_id'],
            'module'        => $validated['module'],
            'score'         => $validated['score'],
            'response_time' => $validated['response_time'],
            'history'       => $this->getRecentHistory($validated['student_id']),
        ]);

        return response()->json([
            'progress'       => $progress,
            'recommendation' => $recommendation,
        ], 201);
    }

    /**
     * Mendapatkan riwayat progress terbaru siswa.
     *
     * @param  int  $studentId
     * @return array
     */
    public function history(int $studentId): JsonResponse
    {
        $student = Student::with(['progressTracker' => function ($query) {
            $query->orderBy('evaluated_at', 'desc')->limit(20);
        }])->findOrFail($studentId);

        return response()->json([
            'student'  => $student->only(['id', 'name', 'abk_category']),
            'progress' => $student->progressTracker,
        ]);
    }

    /**
     * Mengambil riwayat terbaru untuk dikirim ke engine adaptif.
     *
     * @param  int  $studentId
     * @return array
     */
    private function getRecentHistory(int $studentId): array
    {
        return ProgressTracker::where('student_id', $studentId)
            ->orderBy('evaluated_at', 'desc')
            ->limit(10)
            ->get(['module', 'score', 'response_time', 'evaluated_at'])
            ->toArray();
    }
}
