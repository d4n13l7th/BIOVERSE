<?php

use App\Http\Controllers\EvaluationController;
use App\Http\Controllers\MultisensoryController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Rute komunikasi frontend ke backend.
| Digunakan oleh komponen Vue untuk mengambil aset dan mengirim evaluasi.
|
*/

// Prefix: /api

// ── Multisensory Assets ──────────────────────────────────────

// Mendapatkan aset audio untuk modul tertentu
Route::get('/assets/audio/{module}', [MultisensoryController::class, 'getAudioAssets'])
    ->name('api.assets.audio');

// Mendapatkan aset animasi Lottie untuk modul tertentu
Route::get('/assets/animation/{module}', [MultisensoryController::class, 'getAnimationAssets'])
    ->name('api.assets.animation');

// ── Evaluation & Progress ────────────────────────────────────

// Menyimpan hasil evaluasi/kuis siswa
Route::post('/evaluation', [EvaluationController::class, 'store'])
    ->name('api.evaluation.store');

// Mendapatkan riwayat progress siswa
Route::get('/evaluation/history/{studentId}', [EvaluationController::class, 'history'])
    ->name('api.evaluation.history');
