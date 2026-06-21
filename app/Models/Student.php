<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

/**
 * Model Student
 *
 * Merepresentasikan data siswa ABK beserta kategori disabilitasnya.
 * Kategori yang didukung: Autis, Tunanetra, Tunarungu, dll.
 *
 * @property int    $id
 * @property string $name
 * @property string $abk_category    Kategori ABK (autis|tunanetra|tunarungu)
 * @property int    $age
 * @property int    $current_level   Level kesulitan saat ini
 * @property string $preferences     Preferensi UI yang di-override manual (JSON)
 * @property \Illuminate\Support\Carbon $created_at
 * @property \Illuminate\Support\Carbon $updated_at
 */
class Student extends Model
{
    use HasFactory;

    /**
     * Konstanta kategori ABK yang didukung.
     */
    public const CATEGORY_AUTIS     = 'autis';
    public const CATEGORY_TUNANETRA = 'tunanetra';
    public const CATEGORY_TUNARUNGU = 'tunarungu';

    public const CATEGORIES = [
        self::CATEGORY_AUTIS,
        self::CATEGORY_TUNANETRA,
        self::CATEGORY_TUNARUNGU,
    ];

    /**
     * Atribut yang boleh diisi secara massal.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'name',
        'abk_category',
        'age',
        'current_level',
        'preferences',
    ];

    /**
     * Casting atribut.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'age'           => 'integer',
        'current_level' => 'integer',
        'preferences'   => 'array',
    ];

    /**
     * Relasi ke riwayat belajar (ProgressTracker).
     *
     * @return \Illuminate\Database\Eloquent\Relations\HasMany
     */
    public function progressTracker(): HasMany
    {
        return $this->hasMany(ProgressTracker::class);
    }

    /**
     * Scope: Filter berdasarkan kategori ABK.
     */
    public function scopeByCategory($query, string $category)
    {
        return $query->where('abk_category', $category);
    }
}
