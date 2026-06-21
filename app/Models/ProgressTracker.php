<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/**
 * Model ProgressTracker
 *
 * Tabel riwayat belajar siswa. Menyimpan skor, waktu respon,
 * dan detail interaksi per modul untuk dianalisis oleh Adaptive Engine.
 *
 * @property int    $id
 * @property int    $student_id
 * @property string $module          Nama modul/materi yang dikerjakan
 * @property float  $score           Skor evaluasi (0-100)
 * @property float  $response_time   Waktu respon dalam detik
 * @property array  $interactions    Detail interaksi (klik, scroll, dsb.)
 * @property \Illuminate\Support\Carbon $evaluated_at
 * @property \Illuminate\Support\Carbon $created_at
 * @property \Illuminate\Support\Carbon $updated_at
 */
class ProgressTracker extends Model
{
    use HasFactory;

    /**
     * Nama tabel database.
     *
     * @var string
     */
    protected $table = 'progress_trackers';

    /**
     * Atribut yang boleh diisi secara massal.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'student_id',
        'module',
        'score',
        'response_time',
        'interactions',
        'evaluated_at',
    ];

    /**
     * Casting atribut.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'score'         => 'float',
        'response_time' => 'float',
        'interactions'  => 'array',
        'evaluated_at'  => 'datetime',
    ];

    /**
     * Relasi ke siswa.
     *
     * @return \Illuminate\Database\Eloquent\Relations\BelongsTo
     */
    public function student(): BelongsTo
    {
        return $this->belongsTo(Student::class);
    }

    /**
     * Scope: Ambil progress terbaru.
     */
    public function scopeRecent($query, int $limit = 10)
    {
        return $query->orderBy('evaluated_at', 'desc')->limit($limit);
    }

    /**
     * Scope: Filter berdasarkan modul.
     */
    public function scopeForModule($query, string $module)
    {
        return $query->where('module', $module);
    }
}
