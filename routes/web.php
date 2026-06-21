<?php

use App\Http\Controllers\AbkProfileController;
use App\Http\Controllers\MultisensoryController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Rute halaman utama platform Bioverse.
| Menggunakan Inertia.js untuk rendering SPA-like.
|
*/

// Halaman landing / beranda
Route::get('/', function () {
    return inertia('Welcome');
})->name('home');

// Halaman profil siswa berdasarkan kategori ABK
Route::get('/student/{student}', [AbkProfileController::class, 'show'])
    ->name('student.profile');

// Halaman pembelajaran dengan layout adaptif
Route::get('/learn/{student}/{module}', [AbkProfileController::class, 'show'])
    ->name('learn.module');
