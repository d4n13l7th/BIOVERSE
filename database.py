"""
Bioverse - Database (Dummy Data Store)
=======================================
Data dummy in-memory untuk tahap pengembangan awal.
Nanti akan diganti dengan Supabase client.

Struktur:
- 6 siswa (2 per kategori ABK)
- 5 modul pembelajaran (Sistem Pencernaan)
- 15 pertanyaan kuis (3 per modul)
- Progress tracker (empty, diisi saat runtime)
"""

from models import (
    Student, AbkCategory, LearningModule, ContentStep,
    QuizQuestion, QuizOption, ProgressRecord,
)
from supabase_client import supabase


# ═══════════════════════════════════════════════════════════════
# STUDENTS
# ═══════════════════════════════════════════════════════════════

STUDENTS: list[Student] = [
    # ── Autis ──
    Student(
        id=1, name="Andi", abk_category=AbkCategory.AUTIS,
        age=10, current_level=1, avatar_emoji="🧒",
        preferences={"animation_speed": 0.5, "audio_speed": 0.75},
    ),
    Student(
        id=2, name="Budi", abk_category=AbkCategory.AUTIS,
        age=11, current_level=2, avatar_emoji="👦",
        preferences={"animation_speed": 0.5, "audio_speed": 0.75},
    ),
    # ── Tunanetra ──
    Student(
        id=3, name="Citra", abk_category=AbkCategory.TUNANETRA,
        age=9, current_level=1, avatar_emoji="👧",
        preferences={"audio_speed": 1.0, "high_contrast": True},
    ),
    Student(
        id=4, name="Dewi", abk_category=AbkCategory.TUNANETRA,
        age=12, current_level=3, avatar_emoji="👩",
        preferences={"audio_speed": 0.9, "high_contrast": True},
    ),
    # ── Tunarungu ──
    Student(
        id=5, name="Eka", abk_category=AbkCategory.TUNARUNGU,
        age=10, current_level=1, avatar_emoji="🧑",
        preferences={"subtitles": True, "visual_cues": True},
    ),
    Student(
        id=6, name="Fajar", abk_category=AbkCategory.TUNARUNGU,
        age=11, current_level=2, avatar_emoji="👨",
        preferences={"subtitles": True, "visual_cues": True},
    ),
]


# ═══════════════════════════════════════════════════════════════
# LEARNING MODULES (Sistem Pencernaan)
# ═══════════════════════════════════════════════════════════════

MODULES: list[LearningModule] = [
    LearningModule(
        id=1, title="Mulut & Gigi", organ="mulut", icon="🦷",
        description="Proses pencernaan dimulai di mulut. Gigi mengunyah makanan menjadi potongan kecil, dan air liur mulai memecah zat tepung.",
        content_steps=[
            ContentStep(
                step=1, title="Pengenalan Mulut",
                description="Mulut adalah pintu masuk makanan ke dalam tubuh. Di dalam mulut terdapat gigi, lidah, dan kelenjar air liur.",
                subtitle="Mulut adalah tempat pertama makanan diproses.",
                audio_file="/static/audio/mulut_intro.mp3",
                visual_cues=[{"icon": "🦷", "label": "Gigi"}, {"icon": "👅", "label": "Lidah"}, {"icon": "💧", "label": "Air Liur"}],
            ),
            ContentStep(
                step=2, title="Fungsi Gigi",
                description="Gigi seri memotong makanan, gigi taring merobek, dan gigi geraham mengunyah makanan menjadi halus.",
                subtitle="Setiap jenis gigi punya tugas berbeda.",
                visual_cues=[{"icon": "🔪", "label": "Gigi Seri"}, {"icon": "🦁", "label": "Gigi Taring"}, {"icon": "⚙️", "label": "Gigi Geraham"}],
            ),
            ContentStep(
                step=3, title="Peran Air Liur",
                description="Air liur mengandung enzim amilase yang mulai memecah zat tepung menjadi gula sederhana.",
                subtitle="Air liur membantu memecah makanan secara kimiawi.",
                visual_cues=[{"icon": "🧪", "label": "Enzim Amilase"}, {"icon": "🍞", "label": "Zat Tepung"}, {"icon": "🍬", "label": "Gula"}],
            ),
        ],
    ),
    LearningModule(
        id=2, title="Kerongkongan", organ="kerongkongan", icon="⬇️",
        description="Kerongkongan mengantarkan makanan dari mulut ke lambung melalui gerakan peristaltik.",
        content_steps=[
            ContentStep(
                step=1, title="Apa itu Kerongkongan?",
                description="Kerongkongan (esofagus) adalah saluran panjang sekitar 25 cm yang menghubungkan mulut dengan lambung.",
                subtitle="Kerongkongan menghubungkan mulut dan lambung.",
                visual_cues=[{"icon": "📏", "label": "25 cm"}, {"icon": "🔗", "label": "Penghubung"}],
            ),
            ContentStep(
                step=2, title="Gerakan Peristaltik",
                description="Otot kerongkongan berkontraksi secara bergelombang (peristaltik) untuk mendorong makanan ke bawah, bahkan jika kamu berdiri terbalik!",
                subtitle="Otot mendorong makanan dengan gerakan bergelombang.",
                visual_cues=[{"icon": "🌊", "label": "Peristaltik"}, {"icon": "💪", "label": "Otot"}],
            ),
            ContentStep(
                step=3, title="Epiglotis",
                description="Epiglotis adalah katup yang menutup saluran napas saat kamu menelan, agar makanan tidak masuk ke paru-paru.",
                subtitle="Epiglotis melindungi saluran napas saat menelan.",
                visual_cues=[{"icon": "🚪", "label": "Epiglotis"}, {"icon": "🫁", "label": "Paru-paru"}, {"icon": "🛡️", "label": "Pelindung"}],
            ),
        ],
    ),
    LearningModule(
        id=3, title="Lambung", organ="lambung", icon="🫀",
        description="Lambung mencerna makanan secara mekanis dan kimiawi menggunakan asam lambung dan enzim pepsin.",
        content_steps=[
            ContentStep(
                step=1, title="Bentuk Lambung",
                description="Lambung berbentuk seperti kantong huruf J yang terletak di perut bagian kiri atas. Lambung bisa menampung sekitar 1-1,5 liter makanan.",
                subtitle="Lambung berbentuk seperti huruf J.",
                visual_cues=[{"icon": "🅹", "label": "Bentuk J"}, {"icon": "🫙", "label": "1-1,5 Liter"}],
            ),
            ContentStep(
                step=2, title="Asam Lambung",
                description="Lambung menghasilkan asam klorida (HCl) yang sangat kuat untuk membunuh bakteri dan memecah protein bersama enzim pepsin.",
                subtitle="Asam lambung memecah protein dan membunuh bakteri.",
                visual_cues=[{"icon": "⚗️", "label": "HCl"}, {"icon": "🦠", "label": "Bakteri"}, {"icon": "🥩", "label": "Protein"}],
            ),
            ContentStep(
                step=3, title="Pengadukan Makanan",
                description="Otot lambung mengaduk makanan selama 2-6 jam hingga menjadi bubur halus yang disebut kimus (chyme).",
                subtitle="Makanan diaduk menjadi bubur halus bernama kimus.",
                visual_cues=[{"icon": "🥣", "label": "Kimus"}, {"icon": "⏱️", "label": "2-6 Jam"}, {"icon": "🔄", "label": "Pengadukan"}],
            ),
        ],
    ),
    LearningModule(
        id=4, title="Usus Halus", organ="usus_halus", icon="🔬",
        description="Usus halus adalah tempat utama penyerapan nutrisi. Panjangnya sekitar 6 meter!",
        content_steps=[
            ContentStep(
                step=1, title="Tiga Bagian Usus Halus",
                description="Usus halus terdiri dari duodenum (usus 12 jari), jejunum, dan ileum. Total panjangnya sekitar 6 meter.",
                subtitle="Usus halus punya 3 bagian dan panjangnya 6 meter.",
                visual_cues=[{"icon": "1️⃣", "label": "Duodenum"}, {"icon": "2️⃣", "label": "Jejunum"}, {"icon": "3️⃣", "label": "Ileum"}],
            ),
            ContentStep(
                step=2, title="Vili Usus",
                description="Dinding usus halus dipenuhi jutaan tonjolan kecil bernama vili yang memperluas permukaan penyerapan nutrisi.",
                subtitle="Vili memperluas permukaan untuk menyerap nutrisi.",
                visual_cues=[{"icon": "🌿", "label": "Vili"}, {"icon": "📈", "label": "Luas Permukaan"}, {"icon": "🍎", "label": "Nutrisi"}],
            ),
            ContentStep(
                step=3, title="Penyerapan Nutrisi",
                description="Nutrisi dari makanan diserap melalui vili masuk ke pembuluh darah dan diedarkan ke seluruh tubuh.",
                subtitle="Nutrisi diserap ke darah dan diedarkan ke seluruh tubuh.",
                visual_cues=[{"icon": "🩸", "label": "Pembuluh Darah"}, {"icon": "🚚", "label": "Distribusi"}, {"icon": "💪", "label": "Energi"}],
            ),
        ],
    ),
    LearningModule(
        id=5, title="Usus Besar & Anus", organ="usus_besar", icon="♻️",
        description="Usus besar menyerap air dari sisa makanan dan membentuk feses yang dikeluarkan melalui anus.",
        content_steps=[
            ContentStep(
                step=1, title="Fungsi Usus Besar",
                description="Usus besar (kolon) menyerap air dan mineral dari sisa makanan yang tidak tercerna. Panjangnya sekitar 1,5 meter.",
                subtitle="Usus besar menyerap air dari sisa makanan.",
                visual_cues=[{"icon": "💧", "label": "Penyerapan Air"}, {"icon": "📏", "label": "1,5 Meter"}],
            ),
            ContentStep(
                step=2, title="Pembentukan Feses",
                description="Sisa makanan yang sudah kehilangan air menjadi padat dan membentuk feses. Bakteri baik di usus besar membantu proses ini.",
                subtitle="Sisa makanan menjadi padat dan membentuk feses.",
                visual_cues=[{"icon": "🦠", "label": "Bakteri Baik"}, {"icon": "🧱", "label": "Pemadatan"}],
            ),
            ContentStep(
                step=3, title="Pengeluaran (Anus)",
                description="Feses disimpan di rektum dan dikeluarkan melalui anus. Ini adalah tahap akhir dari proses pencernaan.",
                subtitle="Feses dikeluarkan melalui anus sebagai tahap akhir.",
                visual_cues=[{"icon": "🚪", "label": "Anus"}, {"icon": "✅", "label": "Selesai"}],
            ),
        ],
    ),
]


# ═══════════════════════════════════════════════════════════════
# QUIZ QUESTIONS
# ═══════════════════════════════════════════════════════════════

QUIZ_QUESTIONS: list[QuizQuestion] = [
    # ── Modul 1: Mulut & Gigi ──
    QuizQuestion(
        id=1, module_id=1,
        question="Enzim apa yang terdapat dalam air liur?",
        explanation="Air liur mengandung enzim amilase yang memecah zat tepung.",
        options=[
            QuizOption(text="Amilase", icon="🧪", correct=True),
            QuizOption(text="Pepsin", icon="💊"),
            QuizOption(text="Lipase", icon="🧫"),
            QuizOption(text="Tripsin", icon="🔬"),
        ],
    ),
    QuizQuestion(
        id=2, module_id=1,
        question="Gigi jenis apa yang berfungsi mengunyah makanan menjadi halus?",
        explanation="Gigi geraham memiliki permukaan yang lebar untuk mengunyah.",
        options=[
            QuizOption(text="Gigi Seri", icon="🔪"),
            QuizOption(text="Gigi Taring", icon="🦁"),
            QuizOption(text="Gigi Geraham", icon="⚙️", correct=True),
            QuizOption(text="Gigi Susu", icon="🍼"),
        ],
    ),
    QuizQuestion(
        id=3, module_id=1,
        question="Apa fungsi utama mulut dalam pencernaan?",
        explanation="Mulut memulai pencernaan mekanis (mengunyah) dan kimiawi (air liur).",
        options=[
            QuizOption(text="Menyerap nutrisi", icon="🍎"),
            QuizOption(text="Memulai pencernaan mekanis dan kimiawi", icon="🦷", correct=True),
            QuizOption(text="Menyimpan makanan", icon="🫙"),
            QuizOption(text="Mengeluarkan sisa makanan", icon="🚪"),
        ],
    ),
    # ── Modul 2: Kerongkongan ──
    QuizQuestion(
        id=4, module_id=2,
        question="Gerakan otot kerongkongan yang mendorong makanan disebut?",
        explanation="Peristaltik adalah kontraksi otot bergelombang yang mendorong makanan.",
        options=[
            QuizOption(text="Peristaltik", icon="🌊", correct=True),
            QuizOption(text="Osmosis", icon="💧"),
            QuizOption(text="Difusi", icon="🌫️"),
            QuizOption(text="Kontraksi", icon="💪"),
        ],
    ),
    QuizQuestion(
        id=5, module_id=2,
        question="Apa fungsi epiglotis?",
        explanation="Epiglotis menutup saluran napas agar makanan tidak masuk paru-paru.",
        options=[
            QuizOption(text="Memecah makanan", icon="🔨"),
            QuizOption(text="Menyerap air", icon="💧"),
            QuizOption(text="Menutup saluran napas saat menelan", icon="🛡️", correct=True),
            QuizOption(text="Menghasilkan enzim", icon="🧪"),
        ],
    ),
    QuizQuestion(
        id=6, module_id=2,
        question="Berapa panjang kerongkongan manusia?",
        explanation="Kerongkongan manusia dewasa panjangnya sekitar 25 cm.",
        options=[
            QuizOption(text="10 cm", icon="📏"),
            QuizOption(text="25 cm", icon="📏", correct=True),
            QuizOption(text="50 cm", icon="📏"),
            QuizOption(text="100 cm", icon="📏"),
        ],
    ),
    # ── Modul 3: Lambung ──
    QuizQuestion(
        id=7, module_id=3,
        question="Asam apa yang dihasilkan lambung?",
        explanation="Lambung menghasilkan asam klorida (HCl) untuk mencerna makanan.",
        options=[
            QuizOption(text="Asam Sulfat", icon="⚗️"),
            QuizOption(text="Asam Klorida (HCl)", icon="⚗️", correct=True),
            QuizOption(text="Asam Sitrat", icon="🍋"),
            QuizOption(text="Asam Asetat", icon="🫗"),
        ],
    ),
    QuizQuestion(
        id=8, module_id=3,
        question="Bubur halus hasil pencernaan di lambung disebut?",
        explanation="Kimus (chyme) adalah bubur makanan yang terbentuk di lambung.",
        options=[
            QuizOption(text="Bolus", icon="🍞"),
            QuizOption(text="Kimus", icon="🥣", correct=True),
            QuizOption(text="Feses", icon="🧱"),
            QuizOption(text="Plasma", icon="🩸"),
        ],
    ),
    QuizQuestion(
        id=9, module_id=3,
        question="Berapa lama makanan dicerna di lambung?",
        explanation="Lambung mengaduk makanan selama 2-6 jam.",
        options=[
            QuizOption(text="30 menit", icon="⏱️"),
            QuizOption(text="1 jam", icon="⏱️"),
            QuizOption(text="2-6 jam", icon="⏱️", correct=True),
            QuizOption(text="12 jam", icon="⏱️"),
        ],
    ),
    # ── Modul 4: Usus Halus ──
    QuizQuestion(
        id=10, module_id=4,
        question="Tonjolan kecil di dinding usus halus yang menyerap nutrisi disebut?",
        explanation="Vili adalah tonjolan kecil yang memperluas permukaan penyerapan.",
        options=[
            QuizOption(text="Alveoli", icon="🫁"),
            QuizOption(text="Vili", icon="🌿", correct=True),
            QuizOption(text="Neuron", icon="🧠"),
            QuizOption(text="Kapiler", icon="🩸"),
        ],
    ),
    QuizQuestion(
        id=11, module_id=4,
        question="Berapa panjang usus halus manusia?",
        explanation="Usus halus panjangnya sekitar 6 meter.",
        options=[
            QuizOption(text="1 meter", icon="📏"),
            QuizOption(text="3 meter", icon="📏"),
            QuizOption(text="6 meter", icon="📏", correct=True),
            QuizOption(text="10 meter", icon="📏"),
        ],
    ),
    QuizQuestion(
        id=12, module_id=4,
        question="Bagian pertama usus halus yang terhubung ke lambung disebut?",
        explanation="Duodenum (usus 12 jari) adalah bagian pertama usus halus.",
        options=[
            QuizOption(text="Ileum", icon="3️⃣"),
            QuizOption(text="Jejunum", icon="2️⃣"),
            QuizOption(text="Duodenum", icon="1️⃣", correct=True),
            QuizOption(text="Kolon", icon="🔄"),
        ],
    ),
    # ── Modul 5: Usus Besar & Anus ──
    QuizQuestion(
        id=13, module_id=5,
        question="Apa fungsi utama usus besar?",
        explanation="Usus besar menyerap air dan mineral dari sisa makanan.",
        options=[
            QuizOption(text="Mencerna protein", icon="🥩"),
            QuizOption(text="Menyerap nutrisi", icon="🍎"),
            QuizOption(text="Menyerap air dan mineral", icon="💧", correct=True),
            QuizOption(text="Menghasilkan enzim", icon="🧪"),
        ],
    ),
    QuizQuestion(
        id=14, module_id=5,
        question="Apa yang membantu proses pembentukan feses di usus besar?",
        explanation="Bakteri baik (flora usus) membantu proses pembentukan feses.",
        options=[
            QuizOption(text="Virus", icon="🦠"),
            QuizOption(text="Bakteri baik", icon="🦠", correct=True),
            QuizOption(text="Enzim lambung", icon="⚗️"),
            QuizOption(text="Air liur", icon="💧"),
        ],
    ),
    QuizQuestion(
        id=15, module_id=5,
        question="Tahap terakhir pencernaan terjadi di organ apa?",
        explanation="Anus adalah tempat feses dikeluarkan, tahap akhir pencernaan.",
        options=[
            QuizOption(text="Lambung", icon="🫀"),
            QuizOption(text="Usus halus", icon="🔬"),
            QuizOption(text="Ginjal", icon="🫘"),
            QuizOption(text="Anus", icon="🚪", correct=True),
        ],
    ),
]


# ═══════════════════════════════════════════════════════════════
# PROGRESS RECORDS (runtime storage)
# ═══════════════════════════════════════════════════════════════

PROGRESS_RECORDS: list[ProgressRecord] = []


# ═══════════════════════════════════════════════════════════════
# DATA ACCESS FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def get_students() -> list[Student]:
    """Mendapatkan semua siswa."""
    return STUDENTS


def get_student(student_id: int) -> Student | None:
    """Mendapatkan siswa berdasarkan ID."""
    for s in STUDENTS:
        if s.id == student_id:
            return s
    return None


def get_student_by_category(category: str) -> Student | None:
    """Mendapatkan profil siswa (atau profil kategori) dari Supabase."""
    if supabase:
        try:
            res = supabase.table('abk_profiles').select('*').eq('category', category.lower()).execute()
            if res.data:
                data = res.data[0]
                return Student(
                    id=data['id'], name=data['name'], abk_category=AbkCategory(data['category']),
                    age=data.get('age', 10), current_level=data.get('default_level', 1),
                    avatar_emoji=data.get('avatar_emoji', '🧑'),
                    preferences=data.get('preferences', {})
                )
        except Exception as e:
            print(f"Supabase Error (get_student_by_category): {e}")

    # Fallback to dummy
    for s in STUDENTS:
        if s.abk_category.value == category.lower():
            return s
    return None


def get_modules(category: str = "", level: int = 1) -> list[LearningModule]:
    """Mendapatkan modul pembelajaran berdasarkan kategori dan level dari Supabase."""
    if supabase and category:
        try:
            res = supabase.table('modules').select('*, content_steps(*)').eq('category', category.lower()).eq('level', level).execute()
            if res.data:
                modules = []
                for m_data in res.data:
                    steps = [ContentStep(**step) for step in m_data.get('content_steps', [])]
                    modules.append(LearningModule(
                        id=m_data['id'], title=m_data['title'], organ=m_data['organ'], icon=m_data['icon'],
                        description=m_data['description'], content_steps=steps
                    ))
                return modules
        except Exception as e:
            print(f"Supabase Error (get_modules): {e}")
            
    return MODULES


def get_module(module_id: int) -> LearningModule | None:
    """Mendapatkan modul berdasarkan ID."""
    for m in MODULES:
        if m.id == module_id:
            return m
    return None


def get_quiz_questions(module_id: int) -> list[QuizQuestion]:
    """Mendapatkan pertanyaan kuis untuk modul tertentu."""
    return [q for q in QUIZ_QUESTIONS if q.module_id == module_id]


def get_progress(student_id: int) -> list[ProgressRecord]:
    """Mendapatkan riwayat progress siswa."""
    return [p for p in PROGRESS_RECORDS if p.student_id == student_id]


def add_progress(record: ProgressRecord) -> ProgressRecord:
    """Menambahkan record progress baru ke Supabase."""
    if supabase:
        try:
            data = record.model_dump()
            data.pop('id', None) # Remove optional id to let DB auto-increment or uuid
            supabase.table('progress_records').insert(data).execute()
        except Exception as e:
            print(f"Supabase Error (add_progress): {e}")

    PROGRESS_RECORDS.append(record)
    return record
