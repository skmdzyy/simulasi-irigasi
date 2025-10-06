import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import io
from datetime import datetime
import requests
import json
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="Simulasi Irigasi Sawah", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk tema light dengan responsive design
tema_light_css = """
<style>
    /* Latar belakang utama */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Header aplikasi */
    .css-1avcm0n {
        background-color: #F5F5F5;
    }
    
    .css-1avcm0n h1 {
        color: #000000;
    }
    
    /* Sidebar */
    .css-1lcbmhc, .css-1lcbmhc * {
        background-color: #F5F5F5 !important;
        color: #000000 !important;
    }
    
    .css-1lcbmhc .stNumberInput > div > div > input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    .css-1lcbmhc .stSlider > div > div > div > div {
        background-color: #4E8BF5 !important;
    }
    
    .css-1lcbmhc .stSlider > div > div > div > div:hover {
        background-color: #6B9BFF !important;
    }
    
    .css-1lcbmhc .stButton > button {
        background-color: #4E8BF5 !important;
        color: white !important;
        width: 100%;
    }
    
    .css-1lcbmhc .stButton > button:hover {
        background-color: #6B9BFF !important;
    }
    
    /* Sidebar label dan teks */
    .css-1lcbmhc label, .css-1lcbmhc p, .css-1lcbmhc span, .css-1lcbmhc div {
        color: #000000 !important;
    }
    
    /* Sidebar header */
    .css-1lcbmhc h1, .css-1lcbmhc h2, .css-1lcbmhc h3, .css-1lcbmhc h4, .css-1lcbmhc h5, .css-1lcbmhc h6 {
        color: #000000 !important;
    }
    
    /* Sidebar divider */
    .css-1lcbmhc hr {
        border-color: #E0E0E0 !important;
    }
    
    /* Main content area */
    .css-1d391kg {
        background-color: #FFFFFF;
    }
    
    /* Header */
    h1, h2, h3, h4, h5, h6 {
        color: #000000;
    }
    
    /* Teks biasa */
    p, div, span, label {
        color: #000000;
    }
    
    /* Input widget di main area */
    .stSelectbox, .stSlider, .stNumberInput {
        color: #000000;
    }
    
    /* Tombol di main area */
    .stButton>button {
        background-color: #4E8BF5;
        color: white;
    }
    
    .stButton>button:hover {
        background-color: #6B9BFF;
    }
    
    /* Metric */
    div[data-testid="stMetricValue"] {
        color: #4E8BF5;
    }
    
    /* Warning dan error */
    .stWarning {
        background-color: #FFF8E1;
        color: #FF8F00;
    }
    
    .stError {
        background-color: #FFEBEE;
        color: #D32F2F;
    }
    
    .stSuccess {
        background-color: #E8F5E9;
        color: #388E3C;
    }
    
    .stInfo {
        background-color: #E3F2FD;
        color: #1976D2;
    }
    
    /* Slider di main area */
    .stSlider > div > div > div > div {
        background-color: #4E8BF5;
    }
    
    /* Dataframe */
    .stDataFrame {
        background-color: #FFFFFF;
    }
    
    /* Tabs */
    .stTabs > div > div > div > div > button {
        color: #000000;
    }
    
    .stTabs > div > div > div > div > button:hover {
        background-color: #E0E0E0;
    }
    
    /* Selectbox di main area */
    .stSelectbox > div > div > select {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Number input di main area */
    .stNumberInput > div > div > input {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Text input di main area */
    .stTextInput > div > div > input {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Text area di main area */
    .stTextArea > div > div > textarea {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Checkbox di main area */
    .stCheckbox label {
        color: #000000;
    }
    
    /* Radio di main area */
    .stRadio label {
        color: #000000;
    }
    
    /* Date input di main area */
    .stDateInput > div > div > input {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Time input di main area */
    .stTimeInput > div > div > input {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* File uploader di main area */
    .stFileUploader > div > div > div {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Color picker di main area */
    .stColorPicker > div > div > input {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #F5F5F5;
        color: #000000;
    }
    
    /* Card */
    .element-container .stAlert {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: #4E8BF5;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #4E8BF5;
    }
    
    /* Matplotlib figure */
    .stPlotlyChart, .stDataFrame, .stFigure {
        background-color: #FFFFFF;
    }
    
    /* Z.AI Chat Container */
    .zai-chat-container {
        background-color: #F5F5F5;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        border: 1px solid #E0E0E0;
    }
    
    .zai-chat-messages {
        height: 300px;
        overflow-y: auto;
        padding: 10px;
        background-color: #FFFFFF;
        border-radius: 5px;
        margin-bottom: 15px;
        border: 1px solid #E0E0E0;
    }
    
    .zai-message {
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 5px;
    }
    
    .zai-user-message {
        background-color: #E3F2FD;
        text-align: right;
    }
    
    .zai-ai-message {
        background-color: #F5F5F5;
        text-align: left;
    }
    
    .zai-input-container {
        display: flex;
        gap: 10px;
    }
    
    .zai-input {
        flex-grow: 1;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        /* Mobile styles */
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }
        
        .css-1avcm0n {
            font-size: 1.5rem !important;
        }
        
        .css-1lcbmhc {
            font-size: 0.9rem !important;
        }
        
        .stMetric {
            font-size: 0.9rem !important;
        }
        
        .stMetricValue {
            font-size: 1.2rem !important;
        }
        
        h1 {
            font-size: 1.8rem !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
        }
        
        h3 {
            font-size: 1.2rem !important;
        }
        
        .stMarkdown {
            font-size: 0.9rem !important;
        }
        
        .stButton {
            font-size: 0.9rem !important;
        }
        
        .stSlider > div > div {
            font-size: 0.8rem !important;
        }
    }
    
    @media (min-width: 769px) and (max-width: 1024px) {
        /* Tablet styles */
        .main .block-container {
            padding-left: 1.5rem;
            padding-right: 1.5rem;
            padding-top: 1.5rem;
        }
        
        .css-1avcm0n {
            font-size: 1.8rem !important;
        }
        
        .css-1lcbmhc {
            font-size: 1rem !important;
        }
        
        .stMetric {
            font-size: 1rem !important;
        }
        
        .stMetricValue {
            font-size: 1.4rem !important;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        h2 {
            font-size: 1.7rem !important;
        }
        
        h3 {
            font-size: 1.4rem !important;
        }
        
        .stMarkdown {
            font-size: 1rem !important;
        }
        
        .stButton {
            font-size: 1rem !important;
        }
    }
    
    @media (min-width: 1025px) {
        /* Desktop styles */
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
            padding-top: 2rem;
        }
        
        .css-1avcm0n {
            font-size: 2rem !important;
        }
        
        .css-1lcbmhc {
            font-size: 1.1rem !important;
        }
        
        .stMetric {
            font-size: 1.1rem !important;
        }
        
        .stMetricValue {
            font-size: 1.6rem !important;
        }
        
        h1 {
            font-size: 2.2rem !important;
        }
        
        h2 {
            font-size: 1.9rem !important;
        }
        
        h3 {
            font-size: 1.6rem !important;
        }
        
        .stMarkdown {
            font-size: 1.1rem !important;
        }
        
        .stButton {
            font-size: 1.1rem !important;
        }
    }
    
    /* Custom styles for better readability */
    .plot-container {
        margin-bottom: 2rem;
    }
    
    .plot-container .stPlotlyChart {
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .metric-card h3 {
        margin-top: 0;
        margin-bottom: 0.5rem;
        color: #4E8BF5;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #4E8BF5;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
    }
</style>
"""

# Terapkan CSS
st.markdown(tema_light_css, unsafe_allow_html=True)

# Atur tema matplotlib untuk tema terang
plt.style.use('default')

# Initialize session states
if 'zai_api_key' not in st.session_state:
    st.session_state.zai_api_key = ""
if 'use_zai' not in st.session_state:
    st.session_state.use_zai = True
if 'zai_messages' not in st.session_state:
    st.session_state.zai_messages = []
if 'zai_input' not in st.session_state:
    st.session_state.zai_input = ""
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = None
if 'connection_status' not in st.session_state:
    st.session_state.connection_status = None
if 'show_zai' not in st.session_state:
    st.session_state.show_zai = False
if 'chat_input_key' not in st.session_state:
    st.session_state.chat_input_key = 0

# Fungsi untuk Z.AI - Koneksi langsung ke API
def tanya_z_ai(pertanyaan, api_key=None, max_retries=2, timeout=60):
    """
    Fungsi untuk mengirim pertanyaan langsung ke Z.AI API
    """
    if not api_key:
        return "⚠️ Silakan masukkan API key Z.AI untuk menggunakan fitur ini."
    
    # Endpoint Z.AI yang benar
    url = "https://api.z.ai/api/paas/v4/chat/completions"  # endpoint Z.AI
    
    # Headers untuk request
    headers = {
        "Authorization": f"Bearer {api_key.strip()}",  # .strip() untuk menghapus spasi
        "Content-Type": "application/json"
    }
    
    # Payload untuk request
    payload = {
        "model": "glm-4.5-flash",  # Model Z.AI yang sesuai
        "messages": [
            {
                "role": "system",
                "content": "Anda adalah asisten AI ahli irigasi pertanian. Jawab pertanyaan tentang irigasi, erosi, sedimentasi, debit air, dan simulasi aliran air dengan jelas dan informatif. Berikan jawaban yang praktik dan dapat diimplementasikan oleh petani."
            },
            {
                "role": "user",
                "content": pertanyaan
            }
        ],
        "max_tokens": 800,
        "temperature": 0.7
    }
    
    # Retry mechanism
    for attempt in range(max_retries + 1):
        try:
            # Tampilkan percobaan jika lebih dari 1
            if max_retries > 0 and attempt > 0:
                print(f"Retry attempt {attempt} for question: {pertanyaan[:50]}...")
            
            # Kirim request ke API
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)
            
            # Cek response
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            elif response.status_code == 429:
                # Error khusus untuk saldo tidak mencukupi
                try:
                    error_data = response.json()
                    if "Insufficient balance" in error_data.get("error", {}).get("message", ""):
                        return "❌ Saldo Z.AI tidak mencukupi. Silakan tambahkan saldo di dashboard Z.AI Anda."
                    else:
                        return f"❌ Terlalu banyak permintaan. Silakan coba lagi nanti."
                except:
                    return f"❌ Terlalu banyak permintaan. Silakan coba lagi nanti."
            else:
                return f"❌ Error dari server Z.AI: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            if attempt < max_retries:
                # Tunggu sebentar sebelum retry
                import time
                time.sleep(1)
                continue
            return f"⏱️ Request timeout setelah {timeout} detik. Silakan coba lagi atau gunakan koneksi yang lebih stabil."
        except requests.exceptions.ConnectionError:
            if attempt < max_retries:
                # Tunggu sebentar sebelum retry
                import time
                time.sleep(1)
                continue
            return "🌐 Tidak dapat terhubung ke server Z.AI. Periksa koneksi internet Anda."
        except requests.exceptions.RequestException as e:
            if attempt < max_retries:
                # Tunggu sebentar sebelum retry
                import time
                time.sleep(1)
                continue
            return f"❌ Error koneksi: {str(e)}"
        except json.JSONDecodeError as e:
            return f"❌ Error parsing response: {str(e)}"
        except Exception as e:
            return f"❌ Error tidak diketahui: {str(e)}"
    
    return "❌ Gagal mendapatkan respons setelah beberapa percobaan."

# Fungsi untuk mengecek koneksi internet
def cek_koneksi():
    """Fungsi untuk mengecek koneksi internet"""
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return True
    except:
        return False

# Fungsi inisialisasi grid
def inisialisasi_grid(panjangSaluran, lebarSaluran, jumlahGridX, jumlahGridY):  
    x = np.linspace(0, panjangSaluran, jumlahGridX)
    y = np.linspace(0, lebarSaluran, jumlahGridY)
    X, Y = np.meshgrid(x, y)
    return X, Y, x, y

# Fungsi inisialisasi variabel
def inisialisasi_variabel(jumlahGridX, jumlahGridY, debitMasuk, lebarSaluran, kedalamanAwal):
    kecepatanX = np.zeros((jumlahGridY, jumlahGridX))
    kecepatanY = np.zeros((jumlahGridY, jumlahGridX))
    ketinggian = np.ones((jumlahGridY, jumlahGridX)) * kedalamanAwal
    
    # Kondisi batas hulu
    kecepatanX[:, 0] = debitMasuk / (lebarSaluran * kedalamanAwal)
    
    return kecepatanX, kecepatanY, ketinggian

# Fungsi penerapan kondisi batas
def terapkan_kondisi_batas(kecepatanX, kecepatanY, ketinggian):
    # Kondisi batas hilir
    kecepatanX[:, -1] = kecepatanX[:, -2]
    kecepatanY[:, -1] = kecepatanY[:, -2]
    ketinggian[:, -1] = ketinggian[:, -2]
    
    # Kondisi batas dinding
    kecepatanX[0, :] = 0
    kecepatanX[-1, :] = 0
    kecepatanY[0, :] = 0
    kecepatanY[-1, :] = 0
    
    return kecepatanX, kecepatanY, ketinggian

# Fungsi simulasi satu langkah waktu dengan pengecekan NaN
def langkah(kecepatanX, kecepatanY, ketinggian, deltaWaktu, deltaX, deltaY, gravitasi, kemiringan, koefisienManning):
    # Cek NaN di input
    if np.any(np.isnan(kecepatanX)) or np.any(np.isnan(kecepatanY)) or np.any(np.isnan(ketinggian)):
        st.error("NaN terdeteksi di input fungsi langkah!")
        return kecepatanX, kecepatanY, ketinggian
    
    # Hitung gradien ketinggian
    gradienKetinggianX = np.zeros_like(ketinggian)
    gradienKetinggianY = np.zeros_like(ketinggian)
    gradienKetinggianX[:, 1:-1] = (ketinggian[:, 2:] - ketinggian[:, :-2]) / (2 * deltaX)
    gradienKetinggianY[1:-1, :] = (ketinggian[2:, :] - ketinggian[:-2, :]) / (2 * deltaY)
    
    # Hitung kecepatan total
    kecepatanTotal = np.sqrt(kecepatanX**2 + kecepatanY**2)
    
    # Suku gesekan (Manning) dengan pengecekan pembagian nol
    gesekanX = np.zeros_like(kecepatanX)
    gesekanY = np.zeros_like(kecepatanY)
    
    # Hindari pembagian dengan nol dan nilai negatif
    masker = (ketinggian > 0.01) & (kecepatanTotal > 1e-10)
    gesekanX[masker] = (gravitasi * koefisienManning**2 * kecepatanTotal[masker] * kecepatanX[masker]) / (ketinggian[masker]**(4/3))
    gesekanY[masker] = (gravitasi * koefisienManning**2 * kecepatanTotal[masker] * kecepatanY[masker]) / (ketinggian[masker]**(4/3))
    
    # Update kecepatan
    kecepatanXBaru = kecepatanX + deltaWaktu * (-gravitasi * gradienKetinggianX - gesekanX + gravitasi * np.sin(np.radians(kemiringan)))
    kecepatanYBaru = kecepatanY + deltaWaktu * (-gravitasi * gradienKetinggianY - gesekanY)
    
    # Update ketinggian
    ketinggianBaru = ketinggian.copy()
    
    # Hitung flux untuk arah x dengan pengecekan
    aliranX = np.zeros_like(ketinggian)
    aliranX[:, 1:-1] = (ketinggian[:, 2:] * kecepatanX[:, 2:] - ketinggian[:, :-2] * kecepatanX[:, :-2]) / (2 * deltaX)
    
    # Hitung flux untuk arah y dengan pengecekan
    aliranY = np.zeros_like(ketinggian)
    aliranY[1:-1, :] = (ketinggian[2:, :] * kecepatanY[2:, :] - ketinggian[:-2, :] * kecepatanY[:-2, :]) / (2 * deltaY)
    
    # Update ketinggian
    ketinggianBaru = ketinggian - deltaWaktu * (aliranX + aliranY)
    
    # Pastikan ketinggian tidak negatif
    ketinggianBaru = np.maximum(ketinggianBaru, 0.01)
    
    # Cek NaN di output
    if np.any(np.isnan(kecepatanXBaru)) or np.any(np.isnan(kecepatanYBaru)) or np.any(np.isnan(ketinggianBaru)):
        st.error("NaN terdeteksi di output fungsi langkah!")
        return kecepatanX, kecepatanY, ketinggian  # Kembalikan nilai lama jika ada NaN
    
    return kecepatanXBaru, kecepatanYBaru, ketinggianBaru

# Fungsi validasi CFL (Courant-Friedrichs-Lewy)
def validasi_cfl(kecepatanX, kecepatanY, deltaX, deltaY, deltaWaktu):
    kecepatanMaksimum = np.max(np.sqrt(kecepatanX**2 + kecepatanY**2))
    if kecepatanMaksimum > 0:
        cfl = kecepatanMaksimum * deltaWaktu / min(deltaX, deltaY)
        return cfl < 0.5
    return True

# Fungsi simulasi lengkap dengan logging
@st.cache_data(show_spinner="Menjalankan simulasi...")
def jalankan_simulasi(panjangSaluran=10.0, lebarSaluran=2.0, jumlahGridX=50, jumlahGridY=20, jumlahIterasi=500, kemiringan=5.0, 
                     koefisienManning=0.03, debitMasuk=0.5, kedalamanAwal=0.5):
    # Inisialisasi grid
    X, Y, x, y = inisialisasi_grid(panjangSaluran, lebarSaluran, jumlahGridX, jumlahGridY)
    deltaX = panjangSaluran / (jumlahGridX - 1)
    deltaY = lebarSaluran / (jumlahGridY - 1)
    
    # Inisialisasi variabel
    kecepatanX, kecepatanY, ketinggian = inisialisasi_variabel(jumlahGridX, jumlahGridY, debitMasuk, lebarSaluran, kedalamanAwal)
    
    # Parameter konstan
    gravitasi = 9.81
    
    # Hitung langkah waktu maksimum (CFL)
    kecepatanAwal = debitMasuk / (lebarSaluran * kedalamanAwal)
    deltaWaktuMaksimum = 0.5 * min(deltaX, deltaY) / kecepatanAwal if kecepatanAwal > 0 else 0.01
    deltaWaktu = min(0.01, deltaWaktuMaksimum)
    
    # Simpan state untuk animasi
    kondisi = []
    peringatanTidakStabil = False
    nanTerdeteksi = False
    
    # Loop simulasi
    for t in range(jumlahIterasi):
        # Simpan state setiap 10 langkah
        if t % 10 == 0:
            kondisi.append((kecepatanX.copy(), kecepatanY.copy(), ketinggian.copy()))
        
        # Update variabel
        kecepatanXLama, kecepatanYLama, ketinggianLama = kecepatanX.copy(), kecepatanY.copy(), ketinggian.copy()
        kecepatanX, kecepatanY, ketinggian = langkah(kecepatanX, kecepatanY, ketinggian, deltaWaktu, deltaX, deltaY, gravitasi, kemiringan, koefisienManning)
        kecepatanX, kecepatanY, ketinggian = terapkan_kondisi_batas(kecepatanX, kecepatanY, ketinggian)
        
        # Cek NaN
        if np.any(np.isnan(kecepatanX)) or np.any(np.isnan(kecepatanY)) or np.any(np.isnan(ketinggian)):
            nanTerdeteksi = True
            st.warning(f"NaN terdeteksi pada iterasi {t}. Mengembalikan ke nilai sebelumnya.")
            kecepatanX, kecepatanY, ketinggian = kecepatanXLama, kecepatanYLama, ketinggianLama
            break
        
        # Validasi stabilitas
        if not validasi_cfl(kecepatanX, kecepatanY, deltaX, deltaY, deltaWaktu):
            peringatanTidakStabil = True
            deltaWaktu *= 0.5
    
    return X, Y, kecepatanX, kecepatanY, ketinggian, kondisi, peringatanTidakStabil, nanTerdeteksi

# Fungsi visualisasi hasil yang diperbarui
def tampilkan_hasil(X, Y, kecepatanX, kecepatanY, ketinggian):
    # Hitung kecepatan total
    kecepatanTotal = np.sqrt(kecepatanX**2 + kecepatanY**2)
    
    # Buat figure dengan 2 kolom
    figur = plt.figure(figsize=(16, 8), facecolor='#FFFFFF', edgecolor='none')
    
    # Contour plot kecepatan dengan peningkatan keterbacaan
    sumbu1 = figur.add_subplot(121)
    
    # Gunakan levels yang lebih detail untuk kecepatan
    v_kecepatan = np.linspace(np.min(kecepatanTotal), np.max(kecepatanTotal), 30)
    kontur = sumbu1.contourf(X, Y, kecepatanTotal, levels=v_kecepatan, cmap='viridis', extend='both')
    
    # Tambahkan colorbar dengan label yang lebih jelas
    cbar = plt.colorbar(kontur, ax=sumbu1, label='Kecepatan Air (m/s)', shrink=0.8)
    cbar.ax.tick_params(labelsize=10)
    
    # Tambahkan streamplot dengan densitas yang lebih baik
    sumbu1.streamplot(X, Y, kecepatanX, kecepatanY, color='white', density=1.2, linewidth=0.8, arrowsize=1.2)
    
    # Tambahkan anotasi untuk area kritis
    if np.max(kecepatanTotal) > 1.2:  # Threshold erosi
        idx_max = np.unravel_index(np.argmax(kecepatanTotal), kecepatanTotal.shape)
        sumbu1.annotate('Risiko Erosi', 
                        xy=(X[idx_max], Y[idx_max]), 
                        xytext=(X[idx_max] + 1, Y[idx_max] + 0.5),
                        arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, headwidth=8),
                        fontsize=10, color='red', weight='bold')
    
    # Set label dan judul dengan ukuran font yang lebih besar
    sumbu1.set_xlabel('Panjang Saluran (m)', color='black', fontsize=12)
    sumbu1.set_ylabel('Lebar Saluran (m)', color='black', fontsize=12)
    sumbu1.set_title('Distribusi Kecepatan Air', color='black', fontsize=14, weight='bold')
    sumbu1.tick_params(colors='black', labelsize=10)
    
    # Atur batas sumbu
    sumbu1.set_xlim(np.min(X), np.max(X))
    sumbu1.set_ylim(np.min(Y), np.max(Y))
    
    # 3D plot ketinggian air dengan peningkatan keterbacaan
    sumbu2 = figur.add_subplot(122, projection='3d')
    
    # Gunakan levels yang lebih detail untuk ketinggian
    v_ketinggian = np.linspace(np.min(ketinggian), np.max(ketinggian), 30)
    
    # Tambahkan contour plot di bagian bawah 3D
    sumbu2.contourf(X, Y, ketinggian, zdir='z', offset=np.min(ketinggian), cmap='Blues', alpha=0.5)
    
    # Plot surface dengan alpha untuk melihat kontour di bawah
    permukaan = sumbu2.plot_surface(X, Y, ketinggian, cmap='Blues', edgecolor='none', alpha=0.9, 
                                   linewidth=0, antialiased=True, shade=True)
    
    # Tambahkan colorbar untuk ketinggian
    cbar2 = plt.colorbar(permukaan, ax=sumbu2, pad=0.1, shrink=0.6)
    cbar2.set_label('Ketinggian Air (m)', fontsize=10)
    cbar2.ax.tick_params(labelsize=10)
    
    # Set label dan judul dengan ukuran font yang lebih besar
    sumbu2.set_xlabel('Panjang Saluran (m)', color='black', fontsize=12)
    sumbu2.set_ylabel('Lebar Saluran (m)', color='black', fontsize=12)
    sumbu2.set_zlabel('Ketinggian Air (m)', color='black', fontsize=12)
    sumbu2.set_title('Profil Ketinggian Air', color='black', fontsize=14, weight='bold')
    
    # Atur sudut pandang 3D yang lebih baik
    sumbu2.view_init(elev=30, azim=45)
    
    # Atur batas sumbu
    sumbu2.set_xlim(np.min(X), np.max(X))
    sumbu2.set_ylim(np.min(Y), np.max(Y))
    sumbu2.set_zlim(np.min(ketinggian), np.max(ketinggian))
    
    # Hapus background figure
    figur.patch.set_alpha(0.0)
    
    plt.tight_layout()
    return figur

# Fungsi visualisasi analisis erosi dan sedimentasi yang diperbarui
def tampilkan_analisis_erosi(X, Y, kecepatanTotal):
    # Hitung potensi erosi (kecepatan > threshold)
    batasErosi = 1.2  # m/s
    risikoErosi = kecepatanTotal > batasErosi
    
    # Hitung potensi sedimentasi (kecepatan < threshold)
    batasSedimentasi = 0.2  # m/s
    risikoSedimentasi = kecepatanTotal < batasSedimentasi
    
    # Visualisasi dengan peningkatan keterbacaan
    figurErosi = plt.figure(figsize=(15, 5), facecolor='#FFFFFF', edgecolor='none')
    
    # Plot 1: Risiko Erosi
    sumbu1 = figurErosi.add_subplot(131)
    kontur1 = sumbu1.contourf(X, Y, kecepatanTotal, levels=30, cmap='viridis', alpha=0.7)
    
    # Tambahkan contour untuk area erosi
    sumbu1.contour(X, Y, risikoErosi.astype(int), levels=[0.5], colors=['red'], linewidths=2)
    
    # Tambahkan anotasi
    if np.any(risikoErosi):
        idx_erosi = np.unravel_index(np.argmax(kecepatanTotal * risikoErosi), kecepatanTotal.shape)
        sumbu1.annotate('Area Risiko Erosi\n(>1.2 m/s)', 
                        xy=(X[idx_erosi], Y[idx_erosi]), 
                        xytext=(X[idx_erosi] + 1, Y[idx_erosi] + 0.5),
                        arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, headwidth=8),
                        fontsize=10, color='red', weight='bold')
    
    # Tambahkan colorbar
    cbar1 = plt.colorbar(kontur1, ax=sumbu1, label='Kecepatan (m/s)', shrink=0.8)
    cbar1.ax.tick_params(labelsize=10)
    
    sumbu1.set_title("Risiko Erosi", color='black', fontsize=14, weight='bold')
    sumbu1.set_xlabel('Panjang Saluran (m)', color='black', fontsize=12)
    sumbu1.set_ylabel('Lebar Saluran (m)', color='black', fontsize=12)
    sumbu1.tick_params(colors='black', labelsize=10)
    
    # Plot 2: Risiko Sedimentasi
    sumbu2 = figurErosi.add_subplot(132)
    kontur2 = sumbu2.contourf(X, Y, kecepatanTotal, levels=30, cmap='viridis', alpha=0.7)
    
    # Tambahkan contour untuk area sedimentasi
    sumbu2.contour(X, Y, risikoSedimentasi.astype(int), levels=[0.5], colors=['brown'], linewidths=2)
    
    # Tambahkan anotasi
    if np.any(risikoSedimentasi):
        idx_sedimen = np.unravel_index(np.argmin(kecepatanTotal * risikoSedimentasi), kecepatanTotal.shape)
        sumbu2.annotate('Area Risiko\nSedimentasi\n(<0.2 m/s)', 
                        xy=(X[idx_sedimen], Y[idx_sedimen]), 
                        xytext=(X[idx_sedimen] + 1, Y[idx_sedimen] + 0.5),
                        arrowprops=dict(facecolor='brown', shrink=0.05, width=1.5, headwidth=8),
                        fontsize=10, color='brown', weight='bold')
    
    # Tambahkan colorbar
    cbar2 = plt.colorbar(kontur2, ax=sumbu2, label='Kecepatan (m/s)', shrink=0.8)
    cbar2.ax.tick_params(labelsize=10)
    
    sumbu2.set_title("Risiko Sedimentasi", color='black', fontsize=14, weight='bold')
    sumbu2.set_xlabel('Panjang Saluran (m)', color='black', fontsize=12)
    sumbu2.set_ylabel('Lebar Saluran (m)', color='black', fontsize=12)
    sumbu2.tick_params(colors='black', labelsize=10)
    
    # Plot 3: Kombinasi Risiko
    sumbu3 = figurErosi.add_subplot(133)
    
    # Gun palet warna yang lebih jelas
    colors = ['#8B4513', '#FFFFFF', '#FF6B6B']  # Brown, White, Red
    gabungan = np.zeros_like(kecepatanTotal)
    gabungan[risikoErosi] = 1
    gabungan[risikoSedimentasi] = -1
    
    # Tambahkan contour untuk kecepatan
    kontur3 = sumbu3.contourf(X, Y, kecepatanTotal, levels=30, cmap='viridis', alpha=0.7)
    
    # Tambahkan contour untuk area kritis
    sumbu3.contour(X, Y, risikoErosi.astype(int), levels=[0.5], colors=['red'], linewidths=2)
    sumbu3.contour(X, Y, risikoSedimentasi.astype(int), levels=[0.5], colors=['brown'], linewidths=2)
    
    # Tambahkan legenda
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', label='Risiko Erosi (>1.2 m/s)'),
        Patch(facecolor='white', label='Area Normal'),
        Patch(facecolor='brown', label='Risiko Sedimentasi (<0.2 m/s)')
    ]
    sumbu3.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    # Tambahkan colorbar
    cbar3 = plt.colorbar(kontur3, ax=sumbu3, label='Kecepatan (m/s)', shrink=0.8)
    cbar3.ax.tick_params(labelsize=10)
    
    sumbu3.set_title("Kombinasi Risiko", color='black', fontsize=14, weight='bold')
    sumbu3.set_xlabel('Panjang Saluran (m)', color='black', fontsize=12)
    sumbu3.set_ylabel('Lebar Saluran (m)', color='black', fontsize=12)
    sumbu3.tick_params(colors='black', labelsize=10)
    
    # Hapus background figure
    figurErosi.patch.set_alpha(0.0)
    
    plt.tight_layout()
    return figurErosi, risikoErosi, risikoSedimentasi

# Fungsi grafik perbandingan debit yang diperbarui
def tampilkan_perbandingan_debit(debitMasuk, debitKeluaran):
    figurDebit = plt.figure(figsize=(10, 6), facecolor='#FFFFFF', edgecolor='none')
    
    # Hitung efisiensi
    efisiensi = (debitKeluaran / debitMasuk) * 100
    
    # Buat bar chart dengan anotasi
    bars = plt.bar(["Debit Masuk", "Debit Keluaran"], [debitMasuk, debitKeluaran], 
                   color=['#4E8BF5', '#4CAF50'], alpha=0.7, width=0.6)
    
    # Tambahkan nilai di atas setiap bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f} m³/s',
                 ha='center', va='bottom', fontsize=10, weight='bold')
    
    # Tambahkan garis referensi untuk efisiensi
    plt.axhline(y=debitMasuk, color='gray', linestyle='--', alpha=0.5)
    plt.text(debitMasuk + 0.05, debitMasuk, '100% Efisiensi', 
             color='gray', fontsize=9, va='bottom')
    
    # Set label dan judul
    plt.ylabel("Debit (m³/s)", color='black', fontsize=12)
    plt.title("Perbandingan Debit Masuk dan Keluaran", color='black', fontsize=14, weight='bold')
    plt.tick_params(colors='black', labelsize=10)
    
    # Hapus background dan frame
    ax = plt.gca()
    ax.spines['bottom'].set_color('#FFFFFF')
    ax.spines['top']. set_color('#FFFFFF')
    ax.spines['right'].set_color('#FFFFFF')
    ax.spines['left'].set_color('#FFFFFF')
    
    # Tambahkan kotak informasi efisiensi
    info_text = f"Efisiensi: {efisiensi:.1f}%"
    if efisiensi < 80:
        info_color = 'red'
        info_text += " (Rendah)"
    elif efisiensi < 90:
        info_color = 'orange'
        info_text += " (Sedang)"
    else:
        info_color = 'green'
        info_text += " (Baik)"
    
    plt.text(0.5, 0.95, info_text, transform=ax.transAxes, 
             fontsize=12, color=info_color, weight='bold',
             ha='center', va='top',
             bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))
    
    # Hapus background figure
    figurDebit.patch.set_alpha(0.0)
    
    return figurDebit, efisiensi

# UI Streamlit dengan layout yang diperbarui
st.title("🌾 Simulasi Aliran Air di Saluran Irigasi Sawah")

# Layout responsif menggunakan columns
main_col = st.container()

with main_col:
    # Sidebar untuk parameter input
    with st.sidebar:
        st.header("⚙️ Parameter Simulasi")
        
        # Parameter geometri
        st.subheader("📏 Geometri Saluran")
        panjangSaluran = st.slider("Panjang Saluran (m)", 5.0, 20.0, 10.0)
        lebarSaluran = st.slider("Lebar Saluran (m)", 1.0, 5.0, 2.0)
        jumlahGridX = st.slider("Jumlah Grid X", 30, 100, 50)
        jumlahGridY = st.slider("Jumlah Grid Y", 15, 40, 20)
        
        # Parameter fisika
        st.subheader("🔬 Parameter Fisika")
        kemiringan = st.slider("Kemiringan Saluran (derajat)", 1.0, 15.0, 5.0)
        koefisienManning = st.slider("Koefisien Manning", 0.01, 0.1, 0.03, step=0.01)
        debitMasuk = st.slider("Debit Air (m³/s)", 0.1, 2.0, 0.5, step=0.1)
        kedalamanAwal = st.slider("Kedalaman Air Awal (m)", 0.2, 1.0, 0.5, step=0.1)
        
        # Parameter simulasi
        st.subheader("⏱️ Parameter Simulasi")
        jumlahIterasi = st.slider("Jumlah Iterasi", 100, 2000, 500, step=100)
        
        # Parameter tambahan
        st.subheader("🌱 Parameter Tambahan")
        luasSawah = st.number_input("Luas Sawah (Ha)", min_value=0.1, value=1.0, step=0.1)
        
        # Z.AI Configuration - DITAMBAHKAN KEMBALI
        st.markdown("---")
        st.header("🤖 Z.AI Configuration")
        st.session_state.zai_api_key = st.text_input("Z.AI API Key", value=st.session_state.zai_api_key, type="password", help="Masukkan API key Z.AI Anda")
        st.session_state.use_zai = st.checkbox("Aktifkan Z.AI Assistant", value=st.session_state.use_zai)
        
        if st.session_state.use_zai:
            st.info("""
            ℹ️ **Informasi Penting:**
            - Fitur Z.AI memerlukan koneksi internet yang stabil
            - Pastikan API key Z.AI Anda valid
            - Response time bergantung pada kekuatan sinyal
            - Semua pertanyaan diproses langsung oleh AI
            """)
        
        # Tombol simulasi
        st.markdown("---")
        tombolJalankan = st.button("🚀 Jalankan Simulasi", use_container_width=True)
    
    # Handle simulation button
    if tombolJalankan:
        with st.spinner("Menjalankan simulasi..."):
            # Jalankan simulasi
            X, Y, kecepatanX, kecepatanY, ketinggian, kondisi, peringatanTidakStabil, nanTerdeteksi = jalankan_simulasi(
                panjangSaluran=panjangSaluran, lebarSaluran=lebarSaluran, jumlahGridX=jumlahGridX, jumlahGridY=jumlahGridY, 
                jumlahIterasi=jumlahIterasi, kemiringan=kemiringan, koefisienManning=koefisienManning, 
                debitMasuk=debitMasuk, kedalamanAwal=kedalamanAwal
            )
            
            # Simpan hasil ke session state
            st.session_state.simulation_results = {
                'X': X, 'Y': Y, 'kecepatanX': kecepatanX, 'kecepatanY': kecepatanY, 'ketinggian': ketinggian,
                'kondisi': kondisi, 'peringatanTidakStabil': peringatanTidakStabil, 'nanTerdeteksi': nanTerdeteksi,
                'panjangSaluran': panjangSaluran, 'lebarSaluran': lebarSaluran, 'luasSawah': luasSawah,
                'debitMasuk': debitMasuk
            }
            
            # Set show_zai ke True setelah simulasi selesai
            st.session_state.show_zai = True
    
    # Display results if available
    if st.session_state.simulation_results is not None:
        results = st.session_state.simulation_results
        X, Y, kecepatanX, kecepatanY, ketinggian, kondisi = results['X'], results['Y'], results['kecepatanX'], results['kecepatanY'], results['ketinggian'], results['kondisi']
        peringatanTidakStabil, nanTerdeteksi = results['peringatanTidakStabil'], results['nanTerdeteksi']
        panjangSaluran, lebarSaluran, luasSawah, debitMasuk = results['panjangSaluran'], results['lebarSaluran'], results['luasSawah'], results['debitMasuk']
        
        # Tampilkan warning jika simulasi tidak stabil
        if peringatanTidakStabil:
            st.warning("⚠️ Simulasi tidak stabil pada beberapa iterasi. Langkah waktu telah dikurangi otomatis.")
        
        if nanTerdeteksi:
            st.error("❌ NaN terdeteksi selama simulasi. Parameter mungkin tidak stabil.")
        
        # Debug: Tampilkan nilai min/max dari variabel
        st.subheader("🔍 Informasi Debug")
        with st.expander("Lihat Detail Debug"):
            kolom1, kolom2, kolom3 = st.columns(3)
            kolom1.write(f"Kecepatan X: min={np.nanmin(kecepatanX):.4f}, max={np.nanmax(kecepatanX):.4f}")
            kolom2.write(f"Kecepatan Y: min={np.nanmin(kecepatanY):.4f}, max={np.nanmax(kecepatanY):.4f}")
            kolom3.write(f"Ketinggian: min={np.nanmin(ketinggian):.4f}, max={np.nanmax(ketinggian):.4f}")
        
        # Hitung metrik dengan pengecekan NaN
        kecepatanTotal = np.sqrt(kecepatanX**2 + kecepatanY**2)
        
        # Ganti NaN dengan 0 untuk perhitungan metrik
        kecepatanTotalBersih = np.nan_to_num(kecepatanTotal, nan=0.0)
        ketinggianBersih = np.nan_to_num(ketinggian, nan=0.0)
        kecepatanXBersih = np.nan_to_num(kecepatanX, nan=0.0)
        
        kecepatanRataRata = np.mean(kecepatanTotalBersih)
        kecepatanMaksimum = np.max(kecepatanTotalBersih)
        ketinggianRataRata = np.mean(ketinggianBersih)
        
        # Hitung debit keluaran dengan pengecekan
        kecepatanHilir = kecepatanXBersih[:, -1]  # Kecepatan di hilir
        ketinggianHilir = ketinggianBersih[:, -1]    # Ketinggian air di hilir
        lebarHilir = lebarSaluran / len(kecepatanHilir)  # Lebar elemen grid di hilir
        luasHilir = ketinggianHilir * lebarHilir  # Luas penampang di hilir
        debitKeluaran = np.sum(kecepatanHilir * luasHilir)
        
        # Tampilkan metrik dengan card layout
        st.subheader("📊 Hasil Simulasi")
        metrik_col1, metrik_col2, metrik_col3, metrik_col4 = st.columns(4)
        
        with metrik_col1:
            st.metric("Kecepatan Rata-rata", "{:.2f} m/s".format(kecepatanRataRata))
        with metrik_col2:
            st.metric("Kecepatan Maksimum", "{:.2f} m/s".format(kecepatanMaksimum))
        with metrik_col3:
            st.metric("Ketinggian Rata-rata", "{:.2f} m".format(ketinggianRataRata))
        with metrik_col4:
            st.metric("Debit Keluaran", "{:.2f} m³/s".format(debitKeluaran))
        
        # Tampilkan visualisasi dengan tabs untuk organisasi yang lebih baik
        st.subheader("📈 Visualisasi Hasil")
        tab1, tab2, tab3 = st.tabs(["Distribusi Kecepatan & Ketinggian", "Analisis Erosi & Sedimentasi", "Analisis Debit"])
        
        with tab1:
            figur = tampilkan_hasil(X, Y, kecepatanX, kecepatanY, ketinggian)
            st.pyplot(figur)
        
        with tab2:
            figurErosi, risikoErosi, risikoSedimentasi = tampilkan_analisis_erosi(X, Y, kecepatanTotal)
            st.pyplot(figurErosi)
            
            # Rekomendasi erosi dan sedimentasi
            rekomendasi_col1, rekomendasi_col2 = st.columns(2)
            
            with rekomendasi_col1:
                if np.any(risikoErosi):
                    st.warning("⚠️ Terdapat area berisiko erosi! Pertimbangkan: \n- Perkuat dinding saluran \n- Kurangi kemiringan \n- Tambahkan tanaman penahan")
                else:
                    st.success("✅ Tidak ada area berisiko erosi")
            
            with rekomendasi_col2:
                if np.any(risikoSedimentasi):
                    st.warning("⚠️ Terdapat area berisiko sedimentasi! Pertimbangkan: \n- Tambahkan kemiringan \n- Perbesar debit air \n- Rutin melakukan pengerukan")
                else:
                    st.success("✅ Tidak ada area berisiko sedimentasi")
        
        with tab3:
            figurDebit, efisiensi = tampilkan_perbandingan_debit(debitMasuk, debitKeluaran)
            st.pyplot(figurDebit)
            
            # Analisis kebutuhan air
            kebutuhanAir = luasSawah * 10000 * 0.01  # Asumsi 1 cm/Ha/hari
            debitHarian = kebutuhanAir / 86400  # Konversi ke m³/detik
            
            analisis_col1, analisis_col2 = st.columns(2)
            
            with analisis_col1:
                st.metric("Efisiensi Saluran", f"{efisiensi:.1f}%")
            
            with analisis_col2:
                if debitKeluaran < debitHarian:
                    st.error("❌ Debit air tidak mencukupi kebutuhan sawah!")
                    st.write(f"Debit yang dibutuhkan: {debitHarian:.4f} m³/s")
                    st.write(f"Debit tersedia: {debitKeluaran:.4f} m³/s")
                else:
                    st.success("✅ Debit air mencukupi kebutuhan sawah")
                    st.write(f"Debit yang dibutuhkan: {debitHarian:.4f} m³/s")
                    st.write(f"Debit tersedia: {debitKeluaran:.4f} m³/s")
        
        # Rekomendasi lengkap
        st.subheader("💡 Rekomendasi untuk Petani")
        rekomendasi = []
        
        # Analisis kecepatan
        if kecepatanRataRata < 0.3:
            rekomendasi.append("Aliran terlalu lambat → Tambahkan kemiringan atau perbesar debit")
        elif kecepatanRataRata > 1.5:
            rekomendasi.append("Aliran terlalu cepat → Kurangi kemiringan atau tambahkan hambatan")
        
        # Analisis ketinggian
        if ketinggianRataRata < 0.3:
            rekomendasi.append("Kedalaman air kurang → Tambahkan debit atau perkecil lebar saluran")
        
        # Analisis efisiensi
        if efisiensi < 80:
            rekomendasi.append("Efisiensi rendah → Periksa kebocoran atau sedimentasi")
        
        # Tampilkan rekomendasi
        if rekomendasi:
            for i, rec in enumerate(rekomendasi, 1):
                st.info(f"{i}. {rec}")
        else:
            st.success("✅ Semua parameter optimal! Tidak ada rekomendasi.")
        
        # Export hasil dengan tabs
        st.subheader("💾 Export Hasil")
        export_tab1, export_tab2 = st.tabs(["Export Data", "Export Gambar"])
        
        with export_tab1:
            # Export data
            if st.button("📊 Export Data CSV", use_container_width=True):
                data = {
                    'X': X.flatten(),
                    'Y': Y.flatten(),
                    'Kecepatan': kecepatanTotal.flatten(),
                    'Ketinggian': ketinggian.flatten(),
                    'Kecepatan_X': kecepatanX.flatten(),
                    'Kecepatan_Y': kecepatanY.flatten()
                }
                dataframe = pd.DataFrame(data)
                csv = dataframe.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download Data",
                    data=csv,
                    file_name=f'hasil_simulasi_irigasi_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                    mime='text/csv'
                )
        
        with export_tab2:
            # Export gambar
            if st.button("🖼️ Export Gambar", use_container_width=True):
                buffer = io.BytesIO()
                figur.savefig(buffer, format='png', facecolor='#FFFFFF', edgecolor='none')
                st.download_button(
                    label="⬇️ Download Gambar",
                    data=buffer.getvalue(),
                    file_name=f'hasil_simulasi_irigasi_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png',
                    mime='image/png'
                )
    
    # Z.AI Assistant Section - Hanya muncul setelah simulasi
    if st.session_state.show_zai and st.session_state.use_zai:
        st.subheader("🤖 Z.AI Assistant - Sobat Pintar")
        
        # Cek koneksi internet
        if st.button("🔍 Cek Koneksi Internet"):
            with st.spinner("Mengecek koneksi..."):
                if cek_koneksi():
                    st.session_state.connection_status = "Terhubung"
                    st.success("✅ Koneksi internet tersedia!")
                else:
                    st.session_state.connection_status = "Tidak ada koneksi"
                    st.error("❌ Tidak ada koneksi internet")
        
        # Tampilkan status koneksi
        if st.session_state.connection_status:
            if st.session_state.connection_status == "Terhubung":
                st.success("Status: 🌐 Koneksi internet OK")
            else:
                st.error("Status: ❌ Tidak ada koneksi internet")
        
        # Display chat messages
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.zai_messages:
                if message["role"] == "user":
                    st.markdown(f'<div class="zai-message zai-user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="zai-message zai-ai-message"><strong>Z.AI:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            
            # Input untuk pesan baru - PERBAIKAN BUG
            st.markdown('<div class="zai-input-container">', unsafe_allow_html=True)
            
            # Gunakan form dengan key yang unik untuk mencegah refresh
            with st.form(key=f"zai_form_{st.session_state.chat_input_key}", clear_on_submit=True):
                user_input = st.text_input(
                    "Tanyakan kepada Z.AI (tekan Enter untuk mengirim):", 
                    value="",
                    placeholder="Contoh: Bagaimana cara mengatasi erosi pada saluran irigasi?",
                    key="zai_chat_input"
                )
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    submitted = st.form_submit_button("Kirim", use_container_width=True)
                with col2:
                    clear_button = st.form_submit_button("Hapus Chat", use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle form submission - PERBAIKAN BUG
        if submitted and user_input:  # Jika ada input dan tombol kirim ditekan
            # Cek koneksi internet terlebih dahulu
            if not cek_koneksi():
                st.error("❌ Tidak ada koneksi internet. Silakan periksa koneksi Anda dan coba lagi.")
            elif not st.session_state.zai_api_key:
                st.error("❌ Silakan masukkan API key Z.AI terlebih dahulu di sidebar.")
            else:
                # Tambahkan pesan user ke riwayat
                st.session_state.zai_messages.append({"role": "user", "content": user_input})
                
                # Dapatkan respons dari Z.AI menggunakan API key dari session state
                with st.spinner("Z.AI sedang berpikir..."):
                    response = tanya_z_ai(user_input, st.session_state.zai_api_key)
                
                # Tambahkan respons AI ke riwayat
                st.session_state.zai_messages.append({"role": "assistant", "content": response})
                
                # Increment key untuk force refresh form
                st.session_state.chat_input_key += 1
                st.rerun()  # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()
        
        # Handle clear button - PERBAIKAN BUG
        if clear_button:
            st.session_state.zai_messages = []
            st.session_state.chat_input_key += 1
            st.rerun()  # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()
        
        # Pertanyaan cepat dengan grid layout
        st.subheader("💡 Pertanyaan Cepat:")
        
        # Grid layout untuk pertanyaan cepat
        question_col1, question_col2 = st.columns(2)
        
        with question_col1:
            if st.button("Bagaimana mencegah erosi?"):
                if not cek_koneksi():
                    st.error("❌ Tidak ada koneksi internet")
                elif not st.session_state.zai_api_key:
                    st.error("❌ Silakan masukkan API key Z.AI terlebih dahulu di sidebar.")
                else:
                    pertanyaan = "Bagaimana mencegah erosi pada saluran irigasi?"
                    st.session_state.zai_messages.append({"role": "user", "content": pertanyaan})
                    with st.spinner("Z.AI sedang berpikir..."):
                        response = tanya_z_ai(pertanyaan, st.session_state.zai_api_key)
                    st.session_state.zai_messages.append({"role": "assistant", "content": response})
                    st.rerun()  # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()
            
            if st.button("Optimalkan debit air"):
                if not cek_koneksi():
                    st.error("❌ Tidak ada koneksi internet")
                elif not st.session_state.zai_api_key:
                    st.error("❌ Silakan masukkan API key Z.AI terlebih dahulu di sidebar.")
                else:
                    pertanyaan = "Bagaimana cara mengoptimalkan debit air untuk irigasi sawah?"
                    st.session_state.zai_messages.append({"role": "user", "content": pertanyaan})
                    with st.spinner("Z.AI sedang berpikir..."):
                        response = tanya_z_ai(pertanyaan, st.session_state.zai_api_key)
                    st.session_state.zai_messages.append({"role": "assistant", "content": response})
                    st.rerun()  # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()
        
        with question_col2:
            if st.button("Atasi sedimentasi"):
                if not cek_koneksi():
                    st.error("❌ Tidak ada koneksi internet")
                elif not st.session_state.zai_api_key:
                    st.error("❌ Silakan masukkan API key Z.AI terlebih dahulu di sidebar.")
                else:
                    pertanyaan = "Bagaimana cara mengatasi sedimentasi pada saluran irigasi?"
                    st.session_state.zai_messages.append({"role": "user", "content": pertanyaan})
                    with st.spinner("Z.AI sedang berpikir..."):
                        response = tanya_z_ai(pertanyaan, st.session_state.zai_api_key)
                    st.session_state.zai_messages.append({"role": "assistant", "content": response})
                    st.rerun()  # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()
            
            if st.button("Tingkatkan efisiensi"):
                if not cek_koneksi():
                    st.error("❌ Tidak ada koneksi internet")
                elif not st.session_state.zai_api_key:
                    st.error("❌ Silakan masukkan API key Z.AI terlebih dahulu di sidebar.")
                else:
                    pertanyaan = "Bagaimana cara meningkatkan efisiensi saluran irigasi?"
                    st.session_state.zai_messages.append({"role": "user", "content": pertanyaan})
                    with st.spinner("Z.AI sedang berpikir..."):
                        response = tanya_z_ai(pertanyaan, st.session_state.zai_api_key)
                    st.session_state.zai_messages.append({"role": "assistant", "content": response})
                    st.rerun()  # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()
        
        # Tambahkan informasi tambahan
        st.info("""
        ℹ️ **Informasi Penting:**
        - 🌐 Fitur ini memerlukan koneksi internet yang stabil
        - 🔑 Pastikan API key Z.AI Anda valid
        - ⏱️ Response time bergantung pada kekuatan sinyal
        - 🤖 Semua jawaban dihasilkan langsung oleh AI
        - 💡 Ajukan pertanyaan spesifik untuk jawaban yang lebih akurat
        - ⌨️ Tekan Enter untuk mengirim pesan
        """)