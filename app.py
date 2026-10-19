import streamlit as st
import os
import pandas as pd
import base64
from datetime import datetime, date, timedelta
import altair as alt
from dotenv import load_dotenv
from supabase import create_client, Client
from PIL import Image
import io

# ==========================================
# KONFIGURASI TANGGAL KELULUSAN FLEKSIBEL
# ==========================================
GRADUATION_DATE_OVERRIDE = None 

# Memuat konfigurasi dari file .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Inisialisasi koneksi Supabase
@st.cache_resource
def init_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_supabase()

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="RuangKelas - SDN Bringin 02",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fungsi untuk membaca file gambar lokal ke Base64
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# Fungsi untuk memproses Logo SD (Menghapus Background Putih menjadi Transparan PNG Base64)
def get_clean_logo_base64():
    logo_paths = ["Logo SD.jpeg", "Logo SD.jpg", "Logo_SD.jpeg", "Logo_SD.jpg"]
    target_path = None
    for p in logo_paths:
        if os.path.exists(p):
            target_path = p
            break
            
    if target_path:
        try:
            img = Image.open(target_path).convert("RGBA")
            datas = img.getdata()
            
            new_data = []
            for item in datas:
                if item[0] > 220 and item[1] > 220 and item[2] > 220:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
                    
            img.putdata(new_data)
            
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode()
        except Exception:
            return ""
    return ""

img_base64 = get_base64_of_bin_file("Nasa.jpg")
logo_clean_b64 = get_clean_logo_base64()

bg_css = f"""
    .stApp {{
        background: linear-gradient(rgba(7, 9, 14, 0.82), rgba(7, 9, 14, 0.88)), 
                    url('data:image/jpg;base64,{img_base64}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #E2E8F0;
    }}
""" if img_base64 else ".stApp { background-color: #07090E; color: #E2E8F0; }"

# Kustomisasi CSS Modern dengan Tema Luar Angkasa & Aksen Warna #00fff0
st.markdown(f"""
    <style>
    {bg_css}
    
    .top-left-credit {{
        font-size: 0.82rem;
        color: #00fff0;
        background: rgba(1, 89, 90, 0.35);
        border: 1px solid rgba(0, 255, 240, 0.4);
        padding: 4px 14px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 15px;
        font-weight: 600;
        letter-spacing: 0.5px;
        backdrop-filter: blur(6px);
        box-shadow: 0 0 10px rgba(0, 255, 240, 0.15);
    }}
    .main-header {{
        font-size: 2.2rem;
        color: #00fff0;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0px;
        text-shadow: 0 0 15px rgba(0, 255, 240, 0.35);
    }}
    .sub-header {{
        font-size: 1.05rem;
        color: #ff0066;
        margin-bottom: 25px;
        font-weight: 500;
    }}
    .footer-credit {{
        font-size: 0.82rem;
        color: #e445ff;
        text-align: center;
        margin-top: 15px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}
    .quote-card-guru {{
        background: linear-gradient(135deg, rgba(1, 89, 90, 0.85) 0%, rgba(11, 15, 23, 0.95) 100%);
        color: #FFFFFF;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 30px -5px rgba(1, 89, 90, 0.3);
        margin-bottom: 25px;
        border: 1px solid rgba(0, 255, 240, 0.4);
        border-left: 6px solid #00fff0;
        backdrop-filter: blur(8px);
    }}
    .quote-card-siswa {{
        background: linear-gradient(135deg, rgba(9, 44, 62, 0.85) 0%, rgba(1, 89, 90, 0.85) 100%);
        color: #F8FAFC;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 30px -5px rgba(0, 255, 240, 0.2);
        margin-bottom: 25px;
        border: 1px solid rgba(0, 255, 240, 0.4);
        border-left: 6px solid #00fff0;
        backdrop-filter: blur(8px);
    }}
    .arabic-text {{
        font-size: 1.5rem;
        font-family: 'Amiri', 'Traditional Arabic', 'Naskh', serif;
        line-height: 2.3rem;
        color: #00fff0;
        direction: rtl;
        text-align: right;
        margin-bottom: 12px;
        text-shadow: 0 0 10px rgba(0, 255, 240, 0.35);
    }}
    .translation-text {{
        font-size: 0.95rem;
        color: #b6ff3b;
        font-style: italic;
        line-height: 1.5rem;
    }}
    .card {{
        background-color: rgba(17, 24, 39, 0.80);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(1, 89, 90, 0.6);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
        margin-bottom: 15px;
        backdrop-filter: blur(8px);
    }}
    .announcement-card {{
        background-color: rgba(17, 24, 39, 0.80);
        padding: 20px;
        border-radius: 14px;
        border-left: 5px solid #00fff0;
        border-top: 1px solid rgba(30, 41, 59, 0.8);
        border-right: 1px solid rgba(30, 41, 59, 0.8);
        border-bottom: 1px solid rgba(30, 41, 59, 0.8);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        margin-bottom: 15px;
        backdrop-filter: blur(8px);
    }}
    .warning-card {{
        background: linear-gradient(135deg, rgba(120, 53, 15, 0.85) 0%, rgba(30, 41, 59, 0.95) 100%);
        border: 1px solid #FDE047;
        border-left: 6px solid #FDE047;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 0 20px rgba(253, 224, 71, 0.2);
        backdrop-filter: blur(8px);
    }}
    .countdown-card {{
        background: linear-gradient(135deg, rgba(1, 89, 90, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid #00fff0;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(0, 255, 240, 0.25);
        backdrop-filter: blur(8px);
    }}
    .countdown-text {{
        font-size: 2rem;
        font-weight: 800;
        color: #00fff0;
        letter-spacing: 1px;
        text-shadow: 0 0 15px rgba(0, 255, 240, 0.5);
        margin: 5px 0;
    }}
    .graduation-congrats-card {{
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(6, 78, 59, 0.85) 100%);
        border: 2px solid #34D399;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 0 25px rgba(52, 211, 153, 0.35);
        backdrop-filter: blur(8px);
    }}
    .graduation-congrats-text {{
        font-size: 1.25rem;
        font-weight: 700;
        color: #ECFDF5;
        line-height: 1.8rem;
    }}
    [data-testid="stMetricValue"] {{
        color: #00fff0 !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 255, 240, 0.3);
    }}
    [data-testid="stMetricLabel"] {{
        color: #b6ff3b !important;
        font-weight: 600;
    }}
    
    /* PEWARNAAN MENU NAVIGASI SIDEBAR, USERNAME/NISN, PASSWORD, DAN LABEL INPUT MENJADI #00fff0 */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p,
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span,
    label, 
    [data-testid="stWidgetLabel"] p, 
    [data-testid="stWidgetLabel"] span,
    .stSelectbox label p, 
    .stTextInput label p, 
    .stTextArea label p, 
    .stNumberInput label p, 
    .stDateInput label p, 
    .stFileUploader label p {{
        color: #00fff0 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.3px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Status Koneksi Database di Sidebar
with st.sidebar:
    st.write("### 🌐 Status Sistem")
    if supabase:
        st.success("Supabase Terhubung 🟢")
    else:
        st.warning("Supabase Terputus 🟡")
    st.markdown("---")

# Status Sesi Login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None  
    st.session_state.user_name = ""
    st.session_state.username = ""

def render_top_left_credit():
    st.markdown('<div class="top-left-credit">⚡ Built by M. Ainul Hurri Jailani</div>', unsafe_allow_html=True)

def cleanup_expired_announcements():
    try:
        cutoff_date = (datetime.now() - timedelta(days=14)).isoformat()
        supabase.table("announcements").delete().lt("created_at", cutoff_date).execute()
    except Exception:
        pass

if supabase:
    cleanup_expired_announcements()

def render_graduation_countdown():
    today = date.today()
    if GRADUATION_DATE_OVERRIDE:
        grad_date = datetime.strptime(GRADUATION_DATE_OVERRIDE, "%Y-%m-%d").date()
    else:
        if today >= date(today.year, 7, 14):
            grad_year = today.year + 1
        else:
            grad_year = today.year
        grad_date = date(grad_year, 6, 14)
        
    days_left = (grad_date - today).days
    
    if days_left > 0:
        st.markdown(f"""
        <div class="countdown-card">
            <div style="font-size: 0.9rem; color: #b6ff3b; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">🎓 Hitung Mundur Kelulusan</div>
            <div class="countdown-text">🎓 {days_left} days until graduating</div>
            <div style="font-size: 0.88rem; color: #b6ff3b; font-weight: 500;">Target Kelulusan: <b>{grad_date.strftime('%d %B %Y')}</b></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="graduation-congrats-card">
            <div style="font-size: 2.2rem; margin-bottom: 8px;">🎉🎓✨</div>
            <div class="graduation-congrats-text">
                "Selamat telah menyelesaikan jenjang pendidikan dasar!<br>Semoga sukses di perjalanan selanjutnya! Doa saya selalu menyertai anda!"
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_quote_guru():
    st.markdown("""
    <div class="quote-card-guru">
        <div style="margin-bottom: 10px;">
            <span style="background: rgba(0, 255, 240, 0.2); color: #00fff0; border: 1px solid #00fff0; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">✨ Motivasi Pendidik</span>
        </div>
        <div style="font-size: 1.15rem; font-weight: 500; line-height: 1.7rem; font-style: italic; margin-bottom: 10px; color: #F8FAFC;">
            "Guru yang biasa-biasa saja menceritakan. Guru yang baik menjelaskan. Guru yang unggul menunjukkan. Guru hebat menginspirasi."
        </div>
        <div style="font-size: 0.9rem; color: #38BDF8; text-align: right; font-weight: 600;">
            — William A. Ward
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_quote_siswa():
    st.markdown("""
    <div class="quote-card-siswa">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="background: #01595A; color: #00fff0; border: 1px solid #00fff0; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">📜 Mutiara Hikmah — Diwan Imam Asy-Syafi'i</span>
        </div>
        <div class="arabic-text">
            تَعَلَّمْ فَلَيْسَ الْمَرْءُ يُولَدُ عَالِمًا ... وَلَيْسَ أَخُو عِلْمٍ كَمَنْ هُوَ جَاهِلُ<br>
            وَإِنَّ كَبِيرَ الْقَوْمِ لَا عِلْمَ عِنْدَهُ ... صَغِيرٌ إِذَا الْتَفَّتْ عَلَيْهِ الْجَحَافِلُ<br>
            وَإِنَّ صَغِيرَ الْقَوْمِ إِنْ كَانَ عَالِمًا ... كَبِيرٌ إِذَا رُدَّتْ إِلَيْهِ الْمَحَافِلُ
        </div>
        <hr style="border-color: rgba(1, 89, 90, 0.8); margin: 12px 0;">
        <div class="translation-text">
            "Belajarlah! Karena tidak ada seorang pun yang terlahir langsung menjadi orang berilmu, dan tidaklah sama orang yang berilmu dengan orang yang bodoh. 
            Sesungguhnya tokoh suatu kaum yang tidak berilmu akan menjadi kecil saat dihadapkan pada persoalan besar. 
            Sebaliknya, anak kecil dari suatu kaum jika ia berilmu, ia akan menjadi orang besar saat diserahi permusyawaratan."
        </div>
    </div>
    """, unsafe_allow_html=True)

def auth_page():
    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if logo_clean_b64:
            st.markdown(f'''
            <div style="text-align: center; margin-bottom: 10px;">
                <img src="data:image/png;base64,{logo_clean_b64}" width="110" style="filter: drop-shadow(0 0 10px rgba(0,255,240,0.3));">
            </div>
            ''', unsafe_allow_html=True)
            
        st.markdown('<p class="main-header" style="text-align: center;">📚 RuangKelas</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header" style="text-align: center;">Platform Akademik Kelas 6 SDN Bringin 02</p>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            with st.form("login_form"):
                st.write("### Masuk ke Akun Anda")
                login_username = st.text_input("Username / NISN")
                login_password = st.text_input("Kata Sandi", type="password")
                submit_login = st.form_submit_button("Masuk Sekarang", use_container_width=True)
                
                if submit_login:
                    if login_username and login_password:
                        if supabase:
                            try:
                                response = supabase.table("users").select("*").eq("username", str(login_username)).eq("password", str(login_password)).execute()
                                user_data = response.data
                                
                                if user_data:
                                    user = user_data[0]
                                    st.session_state.logged_in = True
                                    st.session_state.user_role = user["role"]
                                    st.session_state.user_name = user["full_name"]
                                    st.session_state.username = user["username"]
                                    st.success(f"Selamat datang, {user['full_name']}!")
                                    st.rerun()
                                else:
                                    st.error("Username atau kata sandi salah.")
                            except Exception as e:
                                st.error(f"Error database: {e}")
                        else:
                            st.error("Koneksi database tidak tersedia.")
                    else:
                        st.warning("Mohon lengkapi kolom login.")
                        
            st.markdown('<div class="footer-credit">Built by M. Ainul Hurri Jailani</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

def dashboard_guru():
    render_top_left_credit()
    st.markdown(f'<p class="main-header">Panel Guru / Admin</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Selamat datang, <b style="color:#00fff0;">{st.session_state.user_name}</b>.</p>', unsafe_allow_html=True)
    
    st.sidebar.title("🧭 Navigasi Guru")
    menu = st.sidebar.radio("Pilih Menu", ["Beranda", "Pengumuman & Tugas", "Absensi Kelas", "Pelanggaran Siswa", "Manajemen Akun Siswa", "Nilai"])
    
    if menu == "Beranda":
        render_quote_guru()
        
        col1, col2, col3 = st.columns(3)
        try:
            res_s = supabase.table("users").select("id", count="exact").eq("role", "siswa").execute()
            total_siswa = res_s.count if res_s.count is not None else 0
            col1.metric("Total Siswa Aktif", total_siswa)
        except:
            col1.metric("Total Siswa Aktif", "-")
            
        try:
            res_p = supabase.table("announcements").select("id", count="exact").execute()
            total_pengumuman = res_p.count if res_p.count is not None else 0
            col2.metric("Pengumuman Aktif", total_pengumuman)
        except:
            col2.metric("Pengumuman Aktif", "-")
            
        col3.metric("Sistem Absensi", "Aktif 🟢")
        
        st.markdown("---")
        st.subheader("📌 Pengumuman Terbaru untuk Siswa")
        try:
            anc = supabase.table("announcements").select("id, author_name, category, title, content, file_name, created_at").order("created_at", desc=True).limit(5).execute().data
            if anc:
                for a in anc:
                    file_info = f"<br><small style='color:#00fff0;'>📎 Lampiran: <b>{a['file_name']}</b></small>" if a.get('file_name') else ""
                    st.markdown(f"""
                    <div class="announcement-card">
                        <span style="background-color:#01595A; color:#00fff0; padding:2px 10px; border-radius:6px; font-size:12px; font-weight:bold; border:1px solid #00fff0;">{a['category']}</span>
                        <h4 style="margin:10px 0 4px 0; color:#F8FAFC;">{a['title']}</h4>
                        <p style="color:#00fff0; font-size:14px; margin-bottom:8px;">{a['content']}</p>
                        <small style="color:#00fff0;">Oleh: {a['author_name']} | Tanggal: {a['created_at'][:10]}</small>{file_info}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Belum ada pengumuman.")
        except Exception as e:
            st.error(f"Gagal memuat pengumuman: {e}")

    elif menu == "Pengumuman & Tugas":
        st.subheader("📢 Buat Pengumuman, Tugas, Kuis, atau Materi")
        st.caption("ℹ️ Pengumuman akan otomatis terhapus dari sistem setelah 14 hari (2 minggu).")
        
        with st.form("form_buat_pengumuman"):
            kategori = st.selectbox("Kategori", ["Tugas/PR", "Pengumuman", "Materi", "Kuis"])
            judul = st.text_input("Judul Pengumuman / Tugas", placeholder="Misal: PR Matematika Bab 3 - Persamaan Kuadrat")
            isi = st.text_area("Isi Pengumuman / Instruksi Tugas", placeholder="Tuliskan detail instruksi, batas waktu pengumpulan, atau informasi penting di sini...")
            
            uploaded_attach = st.file_uploader("📎 Melampirkan File (Opsional: PDF, Word, Gambar, dll)", type=["pdf", "docx", "xlsx", "pptx", "png", "jpg", "jpeg", "zip"])
            
            btn_post = st.form_submit_button("🚀 Terbitkan ke Beranda Siswa", use_container_width=True)
            if btn_post:
                if judul and isi:
                    try:
                        file_name = None
                        file_b64 = None
                        
                        if uploaded_attach is not None:
                            file_name = uploaded_attach.name
                            file_b64 = base64.b64encode(uploaded_attach.read()).decode("utf-8")
                            
                        payload = {
                            "author_name": st.session_state.user_name,
                            "category": kategori,
                            "title": judul,
                            "content": isi,
                            "file_name": file_name,
                            "file_data": file_b64
                        }
                        supabase.table("announcements").insert(payload).execute()
                        st.success("Berhasil menerbitkan pengumuman ke seluruh siswa!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal menerbitkan: {e}")
                else:
                    st.warning("Judul dan Isi pengumuman tidak boleh kosong.")
                    
        st.markdown("---")
        st.subheader("📋 Kelola Pengumuman Yang Sudah Diterbitkan")
        try:
            anc_list = supabase.table("announcements").select("*").order("created_at", desc=True).execute().data
            if anc_list:
                for item in anc_list:
                    with st.expander(f"[{item['category']}] {item['title']} — ({item['created_at'][:10]})"):
                        st.write(item['content'])
                        if item.get("file_name") and item.get("file_data"):
                            st.download_button(
                                label=f"📥 Download Lampiran: {item['file_name']}",
                                data=base64.b64decode(item["file_data"]),
                                file_name=item['file_name'],
                                key=f"dl_guru_manage_{item['id']}"
                            )
                        st.caption(f"Diterbitkan oleh: {item['author_name']}")
                        if st.button("🗑️ Hapus Pengumuman Ini", key=f"del_anc_{item['id']}"):
                            supabase.table("announcements").delete().eq("id", item['id']).execute()
                            st.success("Pengumuman berhasil dihapus.")
                            st.rerun()
            else:
                st.info("Belum ada pengumuman yang diterbitkan.")
        except Exception as e:
            st.error(f"Gagal memuat pengumuman: {e}")

    elif menu == "Pelanggaran Siswa":
        st.subheader("⚠️ Catatan Pelanggaran & Hukuman Siswa (Rekap Bulanan)")
        st.info("Catatan pelanggaran terekap setiap akhir bulan. Guru dapat mendownload rekapitulasi dalam format Excel, lalu menghapusnya jika diperlukan.")
        
        try:
            students = supabase.table("users").select("username, full_name").eq("role", "siswa").order("full_name").execute().data
        except:
            students = []
            
        if not students:
            st.warning("Belum ada akun siswa terdaftar.")
        else:
            student_options = {f"{s['full_name']} (`@{s['username']}`)": s["username"] for s in students}
            
            with st.form("form_catat_pelanggaran"):
                selected_student_label = st.selectbox("Pilih Siswa", options=list(student_options.keys()))
                pelanggaran_text = st.text_input("Bentuk Pelanggaran", placeholder="Misal: Terlambat masuk kelas / Tidak mengerjakan PR")
                hukuman_text = st.text_input("Hukuman / Konsekuensi", placeholder="Misal: Menghafal surat pendek / Membersihkan perpustakaan")
                
                btn_simpan_pelanggaran = st.form_submit_button("🚨 Simpan Catatan Pelanggaran", use_container_width=True)
                
                if btn_simpan_pelanggaran:
                    if pelanggaran_text and hukuman_text:
                        target_username = student_options[selected_student_label]
                        try:
                            payload = {
                                "student_username": target_username,
                                "violation": pelanggaran_text.strip(),
                                "punishment": hukuman_text.strip(),
                                "teacher_name": st.session_state.user_name
                            }
                            supabase.table("violations").insert(payload).execute()
                            st.success("Catatan pelanggaran berhasil disimpan!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Gagal menyimpan catatan pelanggaran: {e}")
                    else:
                        st.warning("Bentuk pelanggaran dan hukuman tidak boleh kosong.")
            
            st.markdown("---")
            st.subheader("📊 Rekapitulasi & Download Pelanggaran Akhir Bulan")
            
            col_rm1, col_rm2 = st.columns(2)
            with col_rm1:
                months_dict = {
                    1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
                    7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
                }
                rekap_month = st.selectbox("Pilih Bulan Rekap", options=list(months_dict.keys()), format_func=lambda x: months_dict[x], index=datetime.now().month - 1, key="v_rekap_m")
            with col_rm2:
                rekap_year = st.selectbox("Pilih Tahun Rekap", [2025, 2026, 2027], index=1, key="v_rekap_y")
                
            try:
                v_all = supabase.table("violations").select("*").order("created_at", desc=True).execute().data
                filtered_violations = []
                for v in v_all:
                    if v.get("created_at"):
                        dt_v = datetime.strptime(v["created_at"][:10], "%Y-%m-%d")
                        if dt_v.month == rekap_month and dt_v.year == rekap_year:
                            filtered_violations.append(v)
                            
                if filtered_violations:
                    rekap_v_list = []
                    for v in filtered_violations:
                        s_name = next((s['full_name'] for s in students if s['username'] == v['student_username']), v['student_username'])
                        rekap_v_list.append({
                            "Tanggal": v["created_at"][:10],
                            "Nama Siswa": s_name,
                            "Username/NISN": v["student_username"],
                            "Bentuk Pelanggaran": v["violation"],
                            "Hukuman": v["punishment"],
                            "Pencatat": v["teacher_name"]
                        })
                    df_v_rekap = pd.DataFrame(rekap_v_list)
                    st.dataframe(df_v_rekap, use_container_width=True, hide_index=True)
                    
                    # Konversi ke Excel untuk didownload
                    output_excel = io.BytesIO()
                    with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
                        df_v_rekap.to_excel(writer, sheet_name='Rekap Pelanggaran', index=False)
                    excel_data = output_excel.getvalue()
                    
                    st.download_button(
                        label=f"📥 Download Rekap Pelanggaran ({months_dict[rekap_month]} {rekap_year}) [.xlsx]",
                        data=excel_data,
                        file_name=f"Rekap_Pelanggaran_{months_dict[rekap_month]}_{rekap_year}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🗑️ Hapus Seluruh Rekapan Bulan Ini Setelah Didownload", use_container_width=True):
                        for v in filtered_violations:
                            supabase.table("violations").delete().eq("id", v["id"]).execute()
                        st.success(f"Rekap pelanggaran bulan {months_dict[rekap_month]} {rekap_year} berhasil dihapus dari sistem.")
                        st.rerun()
                else:
                    st.info(f"Tidak ada catatan pelanggaran pada bulan {months_dict[rekap_month]} {rekap_year}.")
            except Exception as e:
                st.error(f"Gagal memuat rekap pelanggaran: {e}")

            st.markdown("---")
            st.subheader("📋 Riwayat Seluruh Pelanggaran Siswa")
            try:
                v_list = supabase.table("violations").select("*").order("created_at", desc=True).execute().data
                if v_list:
                    for v in v_list:
                        s_name = next((s['full_name'] for s in students if s['username'] == v['student_username']), v['student_username'])
                        with st.expander(f"⚠️ {s_name} — Pelanggaran: {v['violation']} ({v['created_at'][:10]})"):
                            st.write(f"**Bentuk Pelanggaran:** {v['violation']}")
                            st.write(f"**Hukuman / Konsekuensi:** {v['punishment']}")
                            st.caption(f"Dicatat oleh Guru: {v['teacher_name']} | Tanggal: {v['created_at'][:10]}")
                            if st.button("🗑️ Hapus Catatan Ini", key=f"del_v_{v['id']}"):
                                supabase.table("violations").delete().eq("id", v['id']).execute()
                                st.success("Catatan pelanggaran dihapus.")
                                st.rerun()
                else:
                    st.info("Belum ada catatan pelanggaran siswa.")
            except Exception as e:
                st.error(f"Gagal memuat riwayat pelanggaran: {e}")

    elif menu == "Manajemen Akun Siswa":
        st.subheader("👥 Manajemen Akun Pengguna")
        tab_excel, tab_single = st.tabs(["📁 Import Massal (Excel/CSV)", "➕ Tambah Satuan"])
        
        with tab_excel:
            st.info("Format kolom file: **nama**, **username**, **sandi**, **peran** (siswa/guru).")
            uploaded_file = st.file_uploader("Upload File Excel / CSV", type=["xlsx", "xls", "csv"])
            
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                    df.columns = [str(c).strip().lower() for c in df.columns]
                    st.dataframe(df, use_container_width=True)
                    
                    if {'nama', 'username', 'sandi', 'peran'}.issubset(set(df.columns)):
                        if st.button("🚀 Proses & Simpan ke Database", use_container_width=True):
                            success_count = 0
                            for _, row in df.iterrows():
                                try:
                                    supabase.table("users").insert({
                                        "full_name": str(row["nama"]).strip(),
                                        "username": str(row["username"]).strip(),
                                        "password": str(row["sandi"]).strip(),
                                        "role": str(row["peran"]).strip().lower()
                                    }).execute()
                                    success_count += 1
                                except:
                                    pass
                            st.success(f"Berhasil mengimpor {success_count} akun!")
                            st.rerun()
                    else:
                        st.error("Kolom file Excel wajib memiliki: **nama**, **username**, **sandi**, **peran**.")
                except Exception as e:
                    st.error(f"Gagal membaca file: {e}")

        with tab_single:
            with st.form("add_user_form"):
                new_name = st.text_input("Nama Lengkap Siswa/Guru")
                new_username = st.text_input("Username / NISN")
                new_password = st.text_input("Kata Sandi", type="password", value="123456")
                new_role = st.selectbox("Peran (Role)", ["siswa", "guru"])
                if st.form_submit_button("Simpan Akun Baru", use_container_width=True):
                    if new_name and new_username and new_password:
                        try:
                            supabase.table("users").insert({
                                "username": str(new_username).strip(),
                                "password": str(new_password).strip(),
                                "role": new_role,
                                "full_name": str(new_name).strip()
                            }).execute()
                            st.success(f"Akun untuk {new_name} berhasil ditambahkan!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Gagal: {e}")
                    else:
                        st.warning("Mohon lengkapi data.")

        st.markdown("---")
        st.subheader("Daftar Akun Terdaftar")
        try:
            users_list = supabase.table("users").select("id, full_name, username, role, password").execute().data
            if users_list:
                for u in users_list:
                    with st.expander(f"👤 {u['full_name']} — `@{u['username']}` ({u['role'].upper()})"):
                        c1, c2 = st.columns(2)
                        with c1:
                            st.write("Reset Sandi Akun")
                            st.caption("Mengembalikan sandi ke default: `Bringin02`")
                            if st.button("🔄 Reset Sandi ke 'Bringin02'", key=f"reset_btn_{u['id']}"):
                                supabase.table("users").update({"password": "Bringin02"}).eq("id", u['id']).execute()
                                st.success(f"Sandi akun {u['full_name']} berhasil direset ke 'Bringin02'!")
                                st.rerun()
                        with c2:
                            st.write("Zona Bahaya")
                            if st.button(f"🗑️ Hapus Akun Ini", key=f"del_{u['id']}"):
                                supabase.table("users").delete().eq("id", u['id']).execute()
                                st.success("Akun dihapus.")
                                st.rerun()
            else:
                st.info("Belum ada akun terdaftar.")
        except Exception as e:
            st.error(f"Error memuat akun: {e}")
            
    elif menu == "Absensi Kelas":
        st.subheader("📋 Modul Absensi Interaktif Kelas")
        
        try:
            students = supabase.table("users").select("username, full_name").eq("role", "siswa").order("full_name").execute().data
        except:
            students = []
            
        if not students:
            st.warning("Belum ada akun siswa. Tambahkan siswa terlebih dahulu di menu Manajemen Akun.")
        else:
            tab_input, tab_rekap = st.tabs(["✍️ Input Absensi Harian", "📈 Rekapitulasi Absen Bulanan Siswa"])
            
            with tab_input:
                selected_date = st.date_input("📅 Tanggal Absensi", value=date.today())
                date_str = selected_date.strftime("%Y-%m-%d")
                
                existing_att = {}
                try:
                    res_att = supabase.table("attendance").select("*").eq("date", date_str).execute().data
                    for item in res_att:
                        existing_att[item["student_username"]] = item
                except:
                    pass
                    
                st.markdown(f"**Pencatatan Kehadiran Siswa — {date_str}**")
                
                with st.form("form_absensi_modern"):
                    form_inputs = {}
                    
                    col_h1, col_h2, col_h3, col_h4 = st.columns([3, 2, 2, 3])
                    col_h1.markdown("**Nama Siswa**")
                    col_h2.markdown("**Status**")
                    col_h3.markdown("**Terlambat (m)**")
                    col_h4.markdown("**Keterangan / Alasan**")
                    
                    for s in students:
                        curr = existing_att.get(s["username"], {})
                        curr_status = curr.get("status", "Hadir")
                        curr_late = curr.get("late_minutes", 0)
                        curr_reason = curr.get("reason", "")
                        
                        status_options = ["Hadir", "Sakit", "Izin", "Alpha"]
                        default_idx = status_options.index(curr_status) if curr_status in status_options else 0
                        
                        c1, c2, c3, c4 = st.columns([3, 2, 2, 3])
                        c1.markdown(f"**{s['full_name']}**<br><span style='font-size:12px; color:#00fff0;'>`{s['username']}`</span>", unsafe_allow_html=True)
                        st_val = c2.selectbox("Status", status_options, index=default_idx, key=f"st_{s['username']}", label_visibility="collapsed")
                        lt_val = c3.number_input("Menit", min_value=0, value=int(curr_late), key=f"lt_{s['username']}", label_visibility="collapsed")
                        rs_val = c4.text_input("Keterangan", value=str(curr_reason), key=f"rs_{s['username']}", label_visibility="collapsed", placeholder="Opsional...")
                        
                        form_inputs[s["username"]] = {
                            "status": st_val,
                            "late": lt_val,
                            "reason": rs_val
                        }
                        st.markdown("<hr style='margin: 5px 0px; border-color: rgba(1, 89, 90, 0.4);'>", unsafe_allow_html=True)
                    
                    submitted = st.form_submit_button("💾 Simpan Seluruh Absensi", use_container_width=True)
                    if submitted:
                        try:
                            for s in students:
                                uname = s["username"]
                                payload = {
                                    "student_username": uname,
                                    "date": date_str,
                                    "status": form_inputs[uname]["status"],
                                    "late_minutes": form_inputs[uname]["late"],
                                    "reason": form_inputs[uname]["reason"]
                                }
                                chk = supabase.table("attendance").select("id").eq("student_username", uname).eq("date", date_str).execute().data
                                if chk:
                                    supabase.table("attendance").update(payload).eq("id", chk[0]["id"]).execute()
                                else:
                                    supabase.table("attendance").insert(payload).execute()
                            st.success("✅ Data absensi berhasil disimpan secara real-time!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Gagal menyimpan: {e}")
            
            with tab_rekap:
                st.subheader("📊 Tabel Rekapitulasi Bulanan Kehadiran Siswa")
                st.info("Tabel di bawah ini merangkum total kehadiran, keterlambatan, sakit, izin, dan alpha setiap siswa selama bulan yang dipilih.")
                
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    months_dict = {
                        1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
                        7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
                    }
                    selected_month_num = st.selectbox("Pilih Bulan", options=list(months_dict.keys()), format_func=lambda x: months_dict[x], index=datetime.now().month - 1)
                with col_m2:
                    selected_year = st.selectbox("Pilih Tahun", [2025, 2026, 2027], index=1)
                    
                try:
                    all_att = supabase.table("attendance").select("*").execute().data
                    
                    filtered_records = []
                    for item in all_att:
                        d_obj = datetime.strptime(item["date"], "%Y-%m-%d")
                        if d_obj.month == selected_month_num and d_obj.year == selected_year:
                            filtered_records.append(item)
                            
                    rekap_data = []
                    for s in students:
                        uname = s["username"]
                        name = s["full_name"]
                        
                        s_records = [r for r in filtered_records if r["student_username"] == uname]
                        
                        hadir = sum(1 for r in s_records if r["status"] == "Hadir")
                        sakit = sum(1 for r in s_records if r["status"] == "Sakit")
                        izin = sum(1 for r in s_records if r["status"] == "Izin")
                        alpha = sum(1 for r in s_records if r["status"] == "Alpha")
                        terlambat = sum(1 for r in s_records if r["late_minutes"] > 0)
                        
                        rekap_data.append({
                            "Nama Siswa": name,
                            "Username / NISN": uname,
                            "Hadir": hadir,
                            "Terlambat": terlambat,
                            "Sakit": sakit,
                            "Izin": izin,
                            "Alpha": alpha
                        })
                        
                    df_rekap = pd.DataFrame(rekap_data)
                    st.dataframe(df_rekap, use_container_width=True, hide_index=True)
                except Exception as e:
                    st.error(f"Gagal memuat rekapitulasi: {e}")
        
    elif menu == "Nilai":
        st.subheader("🎓 Pengelolaan Nilai Akademik Siswa")
        
        subjects_list = [
            "Matematika", "Bahasa Indonesia", "Pendidikan Pancasila", 
            "IPAS", "Bahasa Inggris", "Seni Budaya", "Bahasa Jawa", "KKA"
        ]
        
        tab_input_manual, tab_input_excel, tab_rekap_nilai = st.tabs(["✍️ Input Manual", "📁 Import Excel / CSV", "📈 Rekapitulasi Per Mapel"])
        
        with tab_input_manual:
            st.info("Pilih mata pelajaran, Bab, KKM, nama materi, lalu masukkan nilai untuk masing-masing siswa.")
            
            try:
                students = supabase.table("users").select("username, full_name").eq("role", "siswa").order("full_name").execute().data
            except:
                students = []
                
            if not students:
                st.warning("Belum ada akun siswa. Tambahkan siswa terlebih dahulu di menu Manajemen Akun.")
            else:
                with st.form("form_input_nilai"):
                    col_i1, col_i2 = st.columns(2)
                    with col_i1:
                        sel_subject = st.selectbox("Mata Pelajaran", subjects_list, key="man_subj")
                        sel_chapter = st.selectbox("Bab", [1, 2, 3, 4, 5, 6, 7, 8], key="man_chap")
                    with col_i2:
                        sel_kkm = st.number_input("KKM (Kriteria Ketuntasan Minimal)", min_value=0, max_value=100, value=75, key="man_kkm")
                        sel_material = st.text_input("Nama Materi / Topik Evaluasi", placeholder="Misal: Ulangan Harian Bab 1", key="man_mat")
                        
                    st.markdown("---")
                    st.markdown("**Daftar Nilai Siswa**")
                    
                    score_inputs = {}
                    for s in students:
                        c_n, c_s = st.columns([3, 2])
                        c_n.markdown(f"**{s['full_name']}**<br><span style='font-size:12px; color:#00fff0;'>`{s['username']}`</span>", unsafe_allow_html=True)
                        sc_val = c_s.number_input("Nilai", min_value=0.0, max_value=100.0, value=75.0, step=0.5, key=f"score_{s['username']}", label_visibility="collapsed")
                        score_inputs[s["username"]] = sc_val
                        st.markdown("<hr style='margin: 5px 0px; border-color: rgba(1, 89, 90, 0.4);'>", unsafe_allow_html=True)
                        
                    submitted_scores = st.form_submit_button("💾 Simpan Seluruh Nilai Siswa", use_container_width=True)
                    if submitted_scores:
                        if sel_material.strip():
                            try:
                                for s in students:
                                    uname = s["username"]
                                    val_score = score_inputs[uname]
                                    
                                    payload = {
                                        "student_username": uname,
                                        "subject": sel_subject,
                                        "chapter": sel_chapter,
                                        "material_name": sel_material.strip(),
                                        "kkm": sel_kkm,
                                        "score": val_score
                                    }
                                    
                                    chk = supabase.table("grades").select("id").eq("student_username", uname).eq("subject", sel_subject).eq("chapter", sel_chapter).eq("material_name", sel_material.strip()).execute().data
                                    if chk:
                                        supabase.table("grades").update(payload).eq("id", chk[0]["id"]).execute()
                                    else:
                                        supabase.table("grades").insert(payload).execute()
                                        
                                st.success("✅ Nilai seluruh siswa berhasil disimpan ke database!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Gagal menyimpan nilai: {e}")
                        else:
                            st.warning("Mohon isi Nama Materi / Topik Evaluasi terlebih dahulu.")
                            
        with tab_input_excel:
            st.info("Upload file Excel (.xlsx / .xls) atau CSV. File cukup berisi 2 kolom: **nama** (Nama lengkap siswa) dan **nilai**.")
            
            with st.form("form_excel_nilai"):
                ex_subject = st.selectbox("Mata Pelajaran", subjects_list, key="ex_subj")
                ex_chapter = st.selectbox("Bab", [1, 2, 3, 4, 5, 6, 7, 8], key="ex_chap")
                ex_kkm = st.number_input("KKM", min_value=0, max_value=100, value=75, key="ex_kkm")
                ex_material = st.text_input("Nama Materi / Topik Evaluasi", placeholder="Misal: Tugas Proyek Bab 2", key="ex_mat")
                
                uploaded_grade_file = st.file_uploader("Pilih File Excel / CSV", type=["xlsx", "xls", "csv"])
                
                submit_ex = st.form_submit_button("🚀 Proses & Upload Nilai dari File", use_container_width=True)
                
                if submit_ex:
                    if uploaded_grade_file is not None and ex_material.strip():
                        try:
                            df_ex = pd.read_csv(uploaded_grade_file) if uploaded_grade_file.name.endswith('.csv') else pd.read_excel(uploaded_grade_file)
                            df_ex.columns = [str(c).strip().lower() for c in df_ex.columns]
                            
                            if {'nama', 'nilai'}.issubset(set(df_ex.columns)):
                                db_students = supabase.table("users").select("username, full_name").eq("role", "siswa").execute().data
                                name_to_username = {s["full_name"].strip().lower(): s["username"] for s in db_students}
                                
                                success_cnt = 0
                                not_found_list = []
                                
                                for _, row in df_ex.iterrows():
                                    try:
                                        student_name_raw = str(row["nama"]).strip()
                                        student_name_key = student_name_raw.lower()
                                        val_score = float(row["nilai"])
                                        
                                        if student_name_key in name_to_username:
                                            uname = name_to_username[student_name_key]
                                            
                                            payload = {
                                                "student_username": uname,
                                                "subject": ex_subject,
                                                "chapter": ex_chapter,
                                                "material_name": ex_material.strip(),
                                                "kkm": ex_kkm,
                                                "score": val_score
                                            }
                                            
                                            chk = supabase.table("grades").select("id").eq("student_username", uname).eq("subject", ex_subject).eq("chapter", ex_chapter).eq("material_name", ex_material.strip()).execute().data
                                            if chk:
                                                supabase.table("grades").update(payload).eq("id", chk[0]["id"]).execute()
                                            else:
                                                supabase.table("grades").insert(payload).execute()
                                            success_cnt += 1
                                        else:
                                            not_found_list.append(student_name_raw)
                                    except:
                                        pass
                                        
                                if success_cnt > 0:
                                    st.success(f"Berhasil mengimpor nilai untuk {success_cnt} siswa dari file Excel!")
                                if not_found_list:
                                    st.warning(f"Siswa berikut tidak ditemukan di sistem: {', '.join(not_found_list)}")
                                st.rerun()
                            else:
                                st.error("Kolom file Excel wajib memiliki: **nama** dan **nilai**.")
                        except Exception as e:
                            st.error(f"Gagal membaca file Excel: {e}")
                    else:
                        st.warning("Mohon isi Nama Materi dan pilih file Excel terlebih dahulu.")

        with tab_rekap_nilai:
            st.subheader("📈 Rekapitulasi Nilai Kelas Per Mata Pelajaran")
            st.info("Pilih mata pelajaran untuk melihat rangkuman nilai seluruh siswa dari Bab 1 hingga Bab 8.")
            
            rekap_subject = st.selectbox("Pilih Mata Pelajaran untuk Rekap", subjects_list, key="rekap_subj_select")
            
            try:
                all_grades = supabase.table("grades").select("*").eq("subject", rekap_subject).execute().data
                students = supabase.table("users").select("username, full_name").eq("role", "siswa").order("full_name").execute().data
                
                if all_grades and students:
                    matrix_data = []
                    for s in students:
                        uname = s["username"]
                        row_dict = {"Nama Siswa": s["full_name"], "NISN / Username": uname}
                        
                        for ch in range(1, 9):
                            ch_scores = [g["score"] for g in all_grades if g["student_username"] == uname and g["chapter"] == ch]
                            if ch_scores:
                                row_dict[f"Bab {ch}"] = round(sum(ch_scores) / len(ch_scores), 1)
                            else:
                                row_dict[f"Bab {ch}"] = "-"
                                
                        matrix_data.append(row_dict)
                        
                    df_matrix = pd.DataFrame(matrix_data)
                    st.dataframe(df_matrix, use_container_width=True, hide_index=True)
                else:
                    st.info(f"Belum ada data nilai tercatat untuk mata pelajaran **{rekap_subject}**.")
            except Exception as e:
                st.error(f"Gagal memuat rekap nilai: {e}")

def dashboard_siswa():
    render_top_left_credit()
    st.markdown(f'<p class="main-header">Panel Siswa</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Selamat datang, <b style="color:#00fff0;">{st.session_state.user_name}</b>.</p>', unsafe_allow_html=True)
    
    st.sidebar.title("🧭 Navigasi Siswa")
    menu = st.sidebar.radio("Pilih Menu", ["Beranda", "Absensi Pribadi", "Nilai Saya", "Ganti Kata Sandi"])
    
    if menu == "Beranda":
        render_quote_siswa()
        render_graduation_countdown()
        
        # Pengecekan Pelanggaran Siswa (Otomatis hilang setelah 3 hari)
        try:
            my_uname = st.session_state.username
            all_my_violations = supabase.table("violations").select("*").eq("student_username", my_uname).order("created_at", desc=True).execute().data
            
            valid_violations = []
            today_dt = datetime.now()
            for v in all_my_violations:
                if v.get("created_at"):
                    v_date = datetime.strptime(v["created_at"][:10], "%Y-%m-%d")
                    diff_days = (today_dt - v_date).days
                    if diff_days <= 3:
                        valid_violations.append(v)
                        
            if valid_violations:
                st.markdown("### ⚠️ Catatan & Peringatan Pelanggaran")
                for v in valid_violations:
                    st.markdown(f"""
                    <div class="warning-card">
                        <span style="background-color: #FDE047; color: #07090E; padding: 2px 10px; border-radius: 6px; font-size: 11px; font-weight: bold;">⚠️ PERINGATAN / WARNING (Otomatis hilang setelah 3 hari)</span>
                        <h4 style="margin: 8px 0 4px 0; color: #F8FAFC;">Pelanggaran: {v['violation']}</h4>
                        <p style="color: #E2E8F0; font-size: 14px; margin-bottom: 6px;"><b>Hukuman / Konsekuensi:</b> {v['punishment']}</p>
                        <small style="color: #cbd5e1;">Dicatat oleh Guru: {v['teacher_name']} | Tanggal: {v['created_at'][:10]}</small>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            pass

        st.subheader("📢 Pengumuman, Tugas & Informasi Kelas")
        try:
            anc = supabase.table("announcements").select("*").order("created_at", desc=True).execute().data
            if anc:
                for a in anc:
                    badge_color = "#01595A"
                    text_color = "#00fff0"
                    if a['category'] == "Tugas/PR":
                        badge_color = "#7F1D1D"
                        text_color = "#FCA5A5"
                    elif a['category'] == "Kuis":
                        badge_color = "#78350F"
                        text_color = "#FDE047"
                    elif a['category'] == "Materi":
                        badge_color = "#064E3B"
                        text_color = "#6EE7B7"

                    st.markdown(f"""
                    <div class="announcement-card">
                        <span style="background-color:{badge_color}; color:{text_color}; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:bold; border:1px solid {text_color};">{a['category']}</span>
                        <h3 style="margin:10px 0 6px 0; color:#F8FAFC;">{a['title']}</h3>
                        <p style="color:#b6ff3b; font-size:15px; line-height:1.5rem; margin-bottom:12px;">{a['content']}</p>
                        <small style="color:#b6ff3b;">Oleh: <b>{a['author_name']}</b> | Diterbitkan: {a['created_at'][:10]}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if a.get("file_name") and a.get("file_data"):
                        st.download_button(
                            label=f"📥 Download Lampiran: {a['file_name']}",
                            data=base64.b64decode(a["file_data"]),
                            file_name=a['file_name'],
                            key=f"dl_siswa_home_{a['id']}"
                        )
                    st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.info("Belum ada pengumuman atau tugas baru dari guru saat ini. Silakan periksa kembali nanti!")
        except Exception as e:
            st.error(f"Gagal memuat pengumuman: {e}")
        
    elif menu == "Absensi Pribadi":
        st.subheader("📈 Rekam Jejak Kehadiran Anda")
        
        try:
            my_username = st.session_state.username
            res = supabase.table("attendance").select("*").eq("student_username", my_username).execute().data
            
            if res:
                df_my = pd.DataFrame(res)
                total_hadir = len(df_my[df_my["status"] == "Hadir"])
                total_sakit = len(df_my[df_my["status"] == "Sakit"])
                total_izin = len(df_my[df_my["status"] == "Izin"])
                total_alpha = len(df_my[df_my["status"] == "Alpha"])
                total_terlambat = len(df_my[df_my["late_minutes"] > 0])
                total_hari = len(df_my)
                
                attendance_rate = round((total_hadir / total_hari) * 100, 1) if total_hari > 0 else 0
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Persentase Hadir", f"{attendance_rate}%", "Optimal")
                c2.metric("Total Hadir", f"{total_hadir} Hari")
                c3.metric("Sakit / Izin / Alpha", f"{total_sakit} / {total_izin} / {total_alpha}")
                c4.metric("Terlambat", f"{total_terlambat} Kali")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                col_chart, col_info = st.columns([1.2, 1])
                with col_chart:
                    st.write("#### 📊 Proporsi Status Kehadiran")
                    status_counts = df_my["status"].value_counts().reset_index()
                    status_counts.columns = ["Status", "Jumlah"]
                    
                    pie_chart = alt.Chart(status_counts).mark_arc(innerRadius=65, outerRadius=110).encode(
                        theta=alt.Theta(field="Jumlah", type="quantitative"),
                        color=alt.Color(field="Status", type="nominal", scale=alt.Scale(scheme="dark2")),
                        tooltip=["Status", "Jumlah"]
                    ).properties(height=280)
                    st.altair_chart(pie_chart, use_container_width=True)
                    
                with col_info:
                    st.write("#### 💡 Catatan & Evaluasi")
                    if total_terlambat > 0:
                        st.warning(f"Anda tercatat `{total_terlambat}` kali datang terlambat ke kelas. Tingkatkan ketepatan waktu Anda!")
                    else:
                        st.success("🌟 Luar biasa! Anda memiliki rekor ketepatan waktu yang sangat baik tanpa catatan keterlambatan.")
                    
                    if total_alpha > 0:
                        st.error(f"Perhatian: Anda memiliki catatan absen tanpa keterangan (Alpha) sebanyak `{total_alpha}` kali.")
                    else:
                        st.info("Bagus! Tidak ada catatan Alpha dalam rekap kehadiran Anda.")

                st.markdown("---")
                st.subheader("📅 Tabel Rekap Harian Bulan Berjalan (Real-Time)")
                st.info("Tabel ini diperbarui secara otomatis setiap hari berdasarkan input presensi dari guru.")
                
                current_month = datetime.now().month
                current_year = datetime.now().year
                
                df_my["date_dt"] = pd.to_datetime(df_my["date"])
                df_current_month = df_my[(df_my["date_dt"].dt.month == current_month) & (df_my["date_dt"].dt.year == current_year)].copy()
                
                if not df_current_month.empty:
                    df_current_month = df_current_month.sort_values(by="date", ascending=False)
                    display_df = df_current_month[["date", "status", "late_minutes", "reason"]].copy()
                    display_df.columns = ["Tanggal", "Status Kehadiran", "Terlambat (Menit)", "Keterangan / Alasan"]
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                else:
                    st.info("Belum ada catatan absensi yang diinputkan oleh guru untuk bulan ini.")
                
            else:
                st.info("Belum ada data catatan absensi untuk akun Anda.")
        except Exception as e:
            st.error(f"Gagal memuat rekap absensi: {e}")
        
    elif menu == "Nilai Saya":
        st.subheader("🎓 Transkrip & Perkembangan Nilai Akademik Anda")
        
        try:
            my_username = st.session_state.username
            grades_res = supabase.table("grades").select("*").eq("student_username", my_username).order("created_at", desc=True).execute().data
            
            if grades_res:
                df_grades = pd.DataFrame(grades_res)
                df_grades["created_at_dt"] = pd.to_datetime(df_grades["created_at"])
                
                st.markdown("### ⚡ Nilai Terbaru (2 Minggu Terakhir)")
                df_grades["is_recent"] = df_grades["created_at_dt"] >= (pd.Timestamp.now(tz=df_grades["created_at_dt"].dt.tz) - pd.Timedelta(days=14))
                df_recent = df_grades[df_grades["is_recent"]].copy()
                
                if not df_recent.empty:
                    recent_display = []
                    for _, r in df_recent.iterrows():
                        predikat = "🟢 Lulus" if r["score"] >= r["kkm"] else "🔴 Remedi"
                        recent_display.append({
                            "Tanggal": r["created_at"][:10],
                            "Mata Pelajaran": r["subject"],
                            "Bab": f"Bab {r['chapter']}",
                            "Materi": r["material_name"],
                            "KKM": r["kkm"],
                            "Nilai Anda": r["score"],
                            "Predikat": predikat
                        })
                    st.dataframe(pd.DataFrame(recent_display), use_container_width=True, hide_index=True)
                else:
                    st.info("Belum ada catatan nilai baru dalam 2 minggu terakhir.")
                    
                st.markdown("---")
                st.markdown("### 📊 Analisis & Diagram Progres Nilai Per Mata Pelajaran")
                
                subjects_list = df_grades["subject"].unique().tolist()
                selected_mapel = st.selectbox("Pilih Mata Pelajaran untuk Dilihat Detail & Grafiknya", subjects_list)
                
                df_mapel = df_grades[df_grades["subject"] == selected_mapel].sort_values(by="created_at")
                
                if not df_mapel.empty:
                    col_tabel, col_grafik = st.columns([1, 1.2])
                    
                    with col_tabel:
                        st.markdown(f"**Tabel Rinci Nilai: {selected_mapel}**")
                        table_view = df_mapel[["chapter", "material_name", "kkm", "score"]].copy()
                        table_view["Predikat"] = table_view.apply(lambda x: "Lulus" if x["score"] >= x["kkm"] else "Remedi", axis=1)
                        table_view.columns = ["Bab", "Materi", "KKM", "Nilai", "Predikat"]
                        st.dataframe(table_view, use_container_width=True, hide_index=True)
                        
                    with col_grafik:
                        st.markdown(f"**Diagram Titik & Tren: {selected_mapel}**")
                        chart = alt.Chart(df_mapel).mark_circle(size=80, color="#00fff0").encode(
                            x=alt.X('material_name:N', sort=None, title='Materi Evaluasi'),
                            y=alt.Y('score:Q', title='Nilai Siswa', scale=alt.Scale(domain=[0, 100])),
                            tooltip=['subject', 'chapter', 'material_name', 'score', 'kkm']
                        ) + alt.Chart(df_mapel).mark_line(color="#38BDF8", strokeWidth=2).encode(
                            x=alt.X('material_name:N', sort=None),
                            y=alt.Y('score:Q')
                        )
                        
                        kkm_line = alt.Chart(pd.DataFrame({'kkm': [df_mapel['kkm'].iloc[0]]})).mark_rule(color="#EF4444", strokeDash=[5, 5]).encode(
                            y='kkm:Q'
                        )
                        
                        final_chart = (chart + kkm_line).properties(height=280).interactive()
                        st.altair_chart(final_chart, use_container_width=True)
                        st.caption("🔴 Garis putus-putus merah menunjukkan batas KKM.")
                else:
                    st.info(f"Belum ada data nilai untuk mapel {selected_mapel}.")
            else:
                st.info("Belum ada catatan nilai akademik yang diinputkan untuk akun Anda.")
        except Exception as e:
            st.error(f"Gagal memuat rekap nilai: {e}")

    elif menu == "Ganti Kata Sandi":
        st.subheader("🔐 Ganti Kata Sandi Akun Anda")
        st.info("Demi keamanan akun, Anda disarankan untuk mengganti kata sandi awal yang diberikan oleh guru dengan kata sandi baru yang mudah diingat.")
        
        with st.form("form_ganti_sandi_siswa"):
            old_password_input = st.text_input("Kata Sandi Lama / Saat Ini", type="password")
            new_password_input = st.text_input("Kata Sandi Baru", type="password")
            confirm_password_input = st.text_input("Konfirmasi Kata Sandi Baru", type="password")
            
            btn_change_pwd = st.form_submit_button("🔄 Perbarui Kata Sandi", use_container_width=True)
            
            if btn_change_pwd:
                if not old_password_input or not new_password_input or not confirm_password_input:
                    st.warning("Mohon isi semua kolom sandi.")
                elif new_password_input != confirm_password_input:
                    st.error("Konfirmasi kata sandi baru tidak cocok.")
                else:
                    try:
                        my_uname = st.session_state.username
                        res = supabase.table("users").select("password").eq("username", my_uname).execute().data
                        
                        if res and res[0]["password"] == old_password_input:
                            supabase.table("users").update({"password": new_password_input}).eq("username", my_uname).execute()
                            st.success("🎉 Kata sandi berhasil diperbarui! Gunakan sandi baru ini untuk login selanjutnya.")
                        else:
                            st.error("Kata sandi lama yang Anda masukkan salah.")
                    except Exception as e:
                        st.error(f"Gagal memperbarui kata sandi: {e}")

# Pengalihan Sesi Utama
if not st.session_state.logged_in:
    auth_page()
else:
    with st.sidebar:
        st.markdown(f"👤 **{st.session_state.user_name}**")
        st.markdown(f"Role: `{st.session_state.user_role.upper()}`")
        if st.button("🚪 Keluar (Logout)", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.user_name = ""
            st.session_state.username = ""
            st.rerun()
            
    if st.session_state.user_role == "guru":
        dashboard_guru()
    else:
        dashboard_siswa()
