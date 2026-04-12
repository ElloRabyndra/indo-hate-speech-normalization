import os
import re
import sys
import pickle
import types
import nltk

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

# ──────────────────────────────────────────────
# NLTK Data Path Configuration for Vercel
# ──────────────────────────────────────────────
# We point to a local directory so Vercel doesn't download it on every start
base_dir = os.path.dirname(__file__)
nltk_data_path = os.path.join(base_dir, "nltk_data")
if nltk_data_path not in nltk.data.path:
    nltk.data.path.append(nltk_data_path)

# Download only if not found (mostly for local development, 
# Vercel will use the pre-packaged folder)
try:
    from nltk.tokenize import sent_tokenize, word_tokenize
except ImportError:
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)
    from nltk.tokenize import sent_tokenize, word_tokenize

# ──────────────────────────────────────────────
# Sastrawi — try real package, fall back gracefully
# ──────────────────────────────────────────────
try:
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
    from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
    _sastrawi_available = True
except ImportError:
    _sastrawi_available = False


# ══════════════════════════════════════════════
# IndonesianNLPPreprocessor — MUST match notebook
# exactly so pickle.load() can deserialise it.
# ══════════════════════════════════════════════
class IndonesianNLPPreprocessor:
    def __init__(self):
        if _sastrawi_available:
            factory = StemmerFactory()
            self.stemmer = factory.create_stemmer()
            stop_factory = StopWordRemoverFactory()
            self.stopwords = set(stop_factory.get_stop_words())
        else:
            self.stemmer = None
            self.stopwords = set()
            
        negasi = {'tidak', 'bukan', 'jangan', 'belum', 'tanpa', 'tiada', 'tak'}
        self.stopwords = self.stopwords - negasi

        self.slang_dict = {
            'gue': 'saya', 'gw': 'saya', 'w': 'saya', 'aku': 'saya', 'ak': 'saya',
            'lu': 'kamu', 'loe': 'kamu', 'lo': 'kamu', 'elo': 'kamu', 'u': 'kamu',
            'elu': 'kamu', 'dia': 'dia', 'dy': 'dia', 'doi': 'dia', 'gua': 'saya',
            'sy': 'saya', 'km': 'kamu', 'kau': 'kamu', 'mu': 'kamu', 'mrk': 'mereka',
            'kalian': 'kalian', 'ni': 'ini', 'tu': 'itu', 'si': 'si', 'bang': 'abang',
            'mas': 'mas', 'pak': 'bapak', 'pas': 'saat', 'dlm': 'dalam', 'spt': 'seperti',
            'kyk': 'seperti', 'kayak': 'seperti', 'kek': 'seperti', 'sbg': 'sebagai',
            'pdhl': 'padahal', 'drpd': 'daripada', 'ama': 'sama', 'klo': 'kalau',
            'pake': 'pakai', 'sampe': 'sampai', 'gini': 'begini', 'gitu': 'begitu',
            'malah': 'malah', 'pasti': 'pasti', 'banyak': 'banyak', 'dulu': 'dahulu',
            'nanti': 'nanti', 'coba': 'coba', 'temen': 'teman', 'gak': 'tidak',
            'ga': 'tidak', 'nggak': 'tidak', 'ngga': 'tidak', 'enggak': 'tidak',
            'kagak': 'tidak', 'gk': 'tidak', 'tdk': 'tidak', 'tak': 'tidak',
            'g': 'tidak', 'banget': 'sangat', 'bgt': 'sangat', 'bngt': 'sangat',
            'bener': 'benar', 'bner': 'benar', 'emg': 'memang', 'emang': 'memang',
            'mmg': 'memang', 'bilang': 'berkata', 'ngomong': 'berbicara',
            'ngobrol': 'berbicara', 'ngasih': 'memberi', 'kasih': 'beri', 'liat': 'lihat',
            'diliat': 'dilihat', 'liatnya': 'lihatnya', 'tau': 'tahu', 'taw': 'tahu',
            'tw': 'tahu', 'mau': 'mau', 'mo': 'mau', 'udah': 'sudah', 'udh': 'sudah',
            'dah': 'sudah', 'sdh': 'sudah', 'belom': 'belum', 'blm': 'belum',
            'blum': 'belum', 'bisa': 'bisa', 'bs': 'bisa', 'kaga': 'tidak',
            'aja': 'saja', 'doang': 'saja', 'dong': 'dong', 'sih': 'sih', 'deh': 'deh',
            'nih': 'ini', 'tuh': 'itu', 'tp': 'tapi', 'tpi': 'tapi', 'kl': 'kalau',
            'klu': 'kalau', 'kalo': 'kalau', 'klau': 'kalau', 'krn': 'karena',
            'karna': 'karena', 'krena': 'karena', 'utk': 'untuk', 'buat': 'untuk',
            'bwat': 'untuk', 'dgn': 'dengan', 'dg': 'dengan', 'sm': 'sama',
            'sama': 'sama', 'jg': 'juga', 'juga': 'juga', 'lg': 'lagi', 'lagi': 'lagi',
            'jd': 'jadi', 'jadi': 'jadi', 'sdg': 'sedang', 'yg': 'yang',
            'bikin': 'membuat', 'dapet': 'dapat', 'dpt': 'dapat', 'br': 'baru',
            'td': 'tadi', 'trus': 'terus', 'gt': 'begitu', 'gtu': 'begitu',
            'cm': 'cuma', 'cuman': 'cuma', 'mngkn': 'mungkin', 'mgkn': 'mungkin',
            'jgn': 'jangan', 'bkn': 'bukan', 'bagus': 'bagus', 'keren': 'keren',
            'jelek': 'jelek', 'jahat': 'jahat', 'bego': 'bodoh', 'bodo': 'bodoh',
            'tolol': 'bodoh', 'dungu': 'bodoh', 'idiot': 'bodoh', 'gila': 'gila',
            'edan': 'gila', 'gilak': 'gila', 'sarap': 'gila', 'kesel': 'kesal',
            'sebal': 'kesal', 'sebel': 'kesal', 'marah': 'marah', 'mara': 'marah',
            'lah': 'lah', 'kan': 'kan', 'mah': 'mah', 'pun': 'pun', 'eh': 'eh',
            'ah': 'ah', 'kok': 'kok', 'wkwk': 'tertawa', 'wkwkwk': 'tertawa',
            'wkkwk': 'tertawa', 'haha': 'tertawa', 'hehe': 'tertawa', 'hihi': 'tertawa',
            'xixi': 'tertawa', 'kwkwk': 'tertawa', 'anjir': 'anjing', 'anying': 'anjing',
            'bgst': 'bangsat', 'kntl': 'kontol', 'mek': 'memek', 'gblk': 'goblok',
            'jncok': 'jancok', 'jancuk': 'jancok', 'asuww': 'asu', 'makasih': 'terima kasih',
            'mksh': 'terima kasih', 'tks': 'terima kasih', 'sok': 'sombong',
            'sotoy': 'sok tahu', 'lebay': 'berlebihan', 'alay': 'berlebihan',
            'mending': 'lebih baik', 'mendingan': 'lebih baik', 'gimana': 'bagaimana',
            'gmn': 'bagaimana', 'kenapa': 'mengapa', 'knp': 'mengapa', 'siapa': 'siapa',
            'sapa': 'siapa', 'napa': 'mengapa', 'kapan': 'kapan', 'kpn': 'kapan',
            'dimana': 'di mana', 'dmn': 'di mana', 'sedih': 'sedih', 'seneng': 'senang',
            'senengg': 'senang', 'happy': 'senang', 'baper': 'bawa perasaan',
            'baperan': 'bawa perasaan', 'bete': 'buruk suasana hati', 'males': 'malas',
            'mager': 'malas gerak', 'capek': 'lelah', 'cape': 'lelah',
            'caper': 'cari perhatian', 'kzl': 'kesal', 'emosi': 'marah',
            'ngamuk': 'marah', 'sewot': 'marah', 'ngambek': 'merajuk',
            'mewek': 'menangis', 'nangis': 'menangis', 'nangsi': 'menangis',
            'asik': 'menyenangkan', 'asyik': 'menyenangkan', 'mantap': 'bagus',
            'mantep': 'bagus', 'mantul': 'mantap betul', 'josss': 'bagus',
            'jos': 'bagus', 'goks': 'luar biasa', 'gokil': 'luar biasa',
            'parah': 'sangat', 'gilaa': 'gila', 'gileeee': 'gila', 'anjayy': 'buruk',
            'wanjir': 'buruk', 'wkwkwkwk': 'tertawa', 'lmao': 'tertawa', 'lol': 'tertawa',
            '😂': 'tertawa', 'kepo': 'ingin tahu', 'kepoan': 'ingin tahu',
            'bodo amat': 'tidak peduli', 'ga peduli': 'tidak peduli',
            'gabut': 'tidak ada kerjaan', 'gabuttt': 'tidak ada kerjaan',
            'gercep': 'gerak cepat', 'modus': 'berpura-pura', 'nyebelin': 'menjengkelkan',
            'nyebel': 'menjengkelkan', 'ribet': 'rumit', 'rempong': 'rumit',
            'receh': 'tidak penting', 'julid': 'iri dengki', 'julidan': 'iri dengki',
            'halu': 'berhalusinasi', 'healing': 'menenangkan diri', 'bestie': 'teman',
            'jamet': 'urakan', 'cringe': 'memalukan', 'jijik': 'jijik',
            'nyinyir': 'mengkritik pedas', 'nyindir': 'menyindir',
            'ghosting': 'mengabaikan', 'nge-gas': 'marah', 'ngegas': 'marah',
            'smg': 'semoga',
        }

        self.abbrev_dict = {
            'rt': 'retweet', 'dm': 'pesan langsung', 'ff': 'follow',
            'ootd': 'outfit of the day', 'yg': 'yang', 'dg': 'dengan',
            'dgn': 'dengan', 'krn': 'karena', 'krna': 'karena', 'utk': 'untuk',
            'tdk': 'tidak', 'sdh': 'sudah', 'blm': 'belum', 'jg': 'juga',
            'tp': 'tapi', 'tpi': 'tapi', 'ttg': 'tentang', 'ttng': 'tentang',
            'dr': 'dari', 'dri': 'dari', 'pd': 'pada', 'spy': 'supaya',
            'spya': 'supaya', 'biar': 'supaya', 'sm': 'sama', 'jd': 'jadi',
            'lg': 'lagi', 'lbh': 'lebih', 'lbih': 'lebih', 'skrg': 'sekarang',
            'skrang': 'sekarang', 'skg': 'sekarang', 'kmrn': 'kemarin',
            'kmrin': 'kemarin', 'bsk': 'besok', 'bsok': 'besok', 'hrs': 'harus',
            'msh': 'masih', 'msih': 'masih', 'sllu': 'selalu', 'sll': 'selalu',
            'org': 'orang', 'orng': 'orang', 'pke': 'pakai', 'pkai': 'pakai',
            'dpke': 'dipakai', 'mslh': 'masalah', 'mskpn': 'meskipun',
            'kpd': 'kepada', 'thd': 'terhadap', 'tsb': 'tersebut',
            'dll': 'dan lain lain', 'dsb': 'dan sebagainya',
            'dkk': 'dan kawan kawan', 'tlg': 'tolong', 'tlng': 'tolong',
            'plz': 'tolong', 'pls': 'tolong', 'mksh': 'terima kasih',
            'tks': 'terima kasih', 'tnks': 'terima kasih', 'bnr': 'benar',
            'bner': 'benar', 'salah': 'salah', 'slh': 'salah', 'smg': 'semoga',
            'amp': 'dan', 'hoax': 'berita bohong', 'ad': 'ada', 'stlh': 'setelah',
            'mngkn': 'mungkin', 'mgkn': 'mungkin', 'pdhl': 'padahal', 'td': 'tadi',
            'jgn': 'jangan', 'sd': 'sampai', 'tgl': 'tanggal', 'dlm': 'dalam',
            'sb': 'seseorang', 'sblm': 'sebelum', 'stgh': 'setengah',
            'dpt': 'dapat', 'dgr': 'dengar', 'dngr': 'dengar', 'ntn': 'nonton',
            'tggl': 'tinggal', 'mnt': 'menit', 'dtg': 'datang', 'prnh': 'pernah',
            'sdkt': 'sedikit', 'bnyk': 'banyak', 'byk': 'banyak', 'sgt': 'sangat',
            'smp': 'sampai', 'sprt': 'seperti', 'gtw': 'tidak tahu',
            'idk': 'tidak tahu', 'imo': 'menurut saya', 'imho': 'menurut saya',
            'fyi': 'untuk informasi', 'btw': 'ngomong-ngomong',
            'afaik': 'sejauh yang saya tahu', 'tbh': 'jujur saja',
            'ngl': 'tidak bohong', 'irl': 'di dunia nyata',
            'smh': 'menggelengkan kepala', 'istg': 'demi tuhan', 'omg': 'ya tuhan',
            'wtf': 'apa-apaan', 'wth': 'apa-apaan', 'asap': 'sesegera mungkin',
            'thx': 'terima kasih', 'ty': 'terima kasih', 'np': 'tidak masalah',
            'nvm': 'tidak jadi', 'jk': 'bercanda', 'lmk': 'beritahu saya',
            'hmu': 'hubungi saya', 'ootw': 'outfit of the week',
            'sotd': 'song of the day',
        }

    # 1. Sentence Segmentation
    def sentence_segmentation(self, text: str) -> List[str]:
        if not text or not str(text).strip():
            return []
        return sent_tokenize(str(text))

    # 2. Tokenisasi + Cleaning + Lowercase
    def tokenize(self, text: str) -> List[str]:
        if not text or not str(text).strip():
            return []
        text = str(text).lower()
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'@\w+', 'user', text)
        text = re.sub(r'#\w+', '', text)
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        tokens = word_tokenize(text)
        return [t for t in tokens if len(t) > 1]

    # 3. Normalisasi Kata Tidak Baku
    def normalize_slang(self, tokens: List[str]) -> List[str]:
        return [self.slang_dict.get(t, t) for t in tokens]

    # 4. Abbreviation Expansion
    def expand_abbrev(self, tokens: List[str]) -> List[str]:
        result = []
        for t in tokens:
            if t in self.abbrev_dict:
                result.extend(self.abbrev_dict[t].split())
            else:
                result.append(t)
        return result

    # 5. Stopword Removal
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        return [t for t in tokens if t not in self.stopwords]

    # 6. Stemming
    def stem(self, tokens: List[str]) -> List[str]:
        if self.stemmer:
            return [self.stemmer.stem(t) for t in tokens]
        return tokens

    # Main preprocess method with lexical normalization
    def preprocess(self, text: str) -> str:
        sentences = self.sentence_segmentation(text)
        text = ' '.join(sentences) if sentences else str(text)
        tokens = self.tokenize(text)
        tokens = self.normalize_slang(tokens)
        tokens = self.expand_abbrev(tokens)
        tokens = self.remove_stopwords(tokens)
        tokens = self.stem(tokens)
        return ' '.join(tokens)

    # Preprocess without lexical normalization
    def preprocess_no_lexnorm(self, text: str) -> str:
        sentences = self.sentence_segmentation(text)
        all_tokens = []
        for sentence in sentences:
            tokens = self.tokenize(sentence)
            tokens = self.remove_stopwords(tokens)
            tokens = self.stem(tokens)
            all_tokens.extend(tokens)
        return ' '.join(all_tokens)


# ══════════════════════════════════════════════
# Pickle compatibility fix
# The preprocessor.pkl was saved from a Jupyter notebook where the class
# lived in __main__. When uvicorn loads this as 'api.index', pickle can't
# find the class in __main__. We fix this by:
#   1. Creating a fake __main__ module stub
#   2. Pointing IndonesianNLPPreprocessor on that stub to our class here
# ══════════════════════════════════════════════
_fake_main = types.ModuleType("__main__")
_fake_main.IndonesianNLPPreprocessor = IndonesianNLPPreprocessor  # type: ignore[attr-defined]
sys.modules.setdefault("__main__", _fake_main)
# Also patch the real __main__ if it exists and doesn't have the class yet
if not hasattr(sys.modules["__main__"], "IndonesianNLPPreprocessor"):
    sys.modules["__main__"].IndonesianNLPPreprocessor = IndonesianNLPPreprocessor  # type: ignore[attr-defined]


class _NLPUnpickler(pickle.Unpickler):
    """Custom unpickler that redirects __main__.IndonesianNLPPreprocessor
    to the class defined in this module."""
    def find_class(self, module: str, name: str):
        if name == "IndonesianNLPPreprocessor":
            return IndonesianNLPPreprocessor
        return super().find_class(module, name)


# ══════════════════════════════════════════════
# FastAPI App
# ══════════════════════════════════════════════
app = FastAPI(title="Indonesian Hate Speech API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model directory — resolved relative to this file
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

# Lazy-loaded model cache (module-level, survives across requests in same worker)
_cache: dict = {}


def load_models():
    if _cache:
        return _cache
    try:
        with open(os.path.join(MODELS_DIR, "preprocessor.pkl"), "rb") as f:
            _cache["preprocessor"] = _NLPUnpickler(f).load()
        with open(os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl"), "rb") as f:
            _cache["tfidf"] = pickle.load(f)
        with open(os.path.join(MODELS_DIR, "model_naive_bayes.pkl"), "rb") as f:
            _cache["model"] = pickle.load(f)
    except FileNotFoundError as e:
        raise RuntimeError(f"Model file not found: {e}")
    return _cache


# ── Request / Response schemas ─────────────────
class AnalyzeRequest(BaseModel):
    text: str


class AnalyzeResponse(BaseModel):
    label: str
    probability: float
    processed_text: str


# ── Endpoints ──────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=422, detail="Text cannot be empty.")
    try:
        models = load_models()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    preprocessor: IndonesianNLPPreprocessor = models["preprocessor"]
    tfidf = models["tfidf"]
    model = models["model"]

    processed = preprocessor.preprocess(req.text)
    features = tfidf.transform([processed])
    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0]

    # Class 1 = Hate Speech, Class 0 = Non Hate Speech
    label = "Hate Speech" if int(prediction) == 1 else "Non Hate Speech"
    confidence = float(proba[int(prediction)])

    return AnalyzeResponse(
        label=label,
        probability=confidence,
        processed_text=processed,
    )
