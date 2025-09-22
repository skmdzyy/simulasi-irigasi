import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import io
from datetime import datetime
import requests
import json
# import zai
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="Simulasi Irigasi Sawah", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk tema light
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

# Fungsi untuk Z.AI - Koneksi langsung ke API
def tanya_z_ai(pertanyaan, api_key=None, max_retries=2, timeout=15):
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
                "content": "Anda adalah asisten AI ahli irigasi pertanian. Jawab pertanyaan tentang irigasi, erosi, sedimentasi, debit air, dan simulasi aliran air dengan jelas dan informatif. Berikan jawaban yang praktis dan dapat diimplementasikan oleh petani."
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

# Fungsi visualisasi hasil
def tampilkan_hasil(X, Y, kecepatanX, kecepatanY, ketinggian):
    # Hitung kecepatan total
    kecepatanTotal = np.sqrt(kecepatanX**2 + kecepatanY**2)
    
    # Buat figure dengan 2 kolom
    figur = plt.figure(figsize=(16, 8), facecolor='#FFFFFF', edgecolor='none')
    
    # Contour plot kecepatan
    sumbu1 = figur.add_subplot(121)
    kontur = sumbu1.contourf(X, Y, kecepatanTotal, levels=20, cmap='viridis')
    plt.colorbar(kontur, ax=sumbu1, label='Kecepatan (m/s)')
    sumbu1.set_xlabel('Panjang Saluran (m)', color='black')
    sumbu1.set_ylabel('Lebar Saluran (m)', color='black')
    sumbu1.set_title('Distribusi Kecepatan Air', color='black')
    sumbu1.tick_params(colors='black')
    sumbu1.spines['bottom'].set_color('#FFFFFF')
    sumbu1.spines['top'].set_color('#FFFFFF')
    sumbu1.spines['right'].set_color('#FFFFFF')
    sumbu1.spines['left'].set_color('#FFFFFF')
    
    # Tambahkan streamplot
    sumbu1.streamplot(X, Y, kecepatanX, kecepatanY, color='black', density=1.5, linewidth=0.5)
    
    # 3D plot ketinggian air
    sumbu2 = figur.add_subplot(122, projection='3d')
    permukaan = sumbu2.plot_surface(X, Y, ketinggian, cmap='Blues', edgecolor='none')
    sumbu2.set_xlabel('Panjang Saluran (m)', color='black')
    sumbu2.set_ylabel('Lebar Saluran (m)', color='black')
    sumbu2.set_zlabel('Ketinggian (m)', color='black')
    sumbu2.set_title('Profil Ketinggian Air', color='black')
    sumbu2.tick_params(colors='black')
    sumbu2.xaxis.pane.fill = False
    sumbu2.yaxis.pane.fill = False
    sumbu2.zaxis.pane.fill = False
    sumbu2.grid(True, alpha=0.3)
    
    # Hapus background figure
    figur.patch.set_alpha(0.0)
    
    plt.tight_layout()
    return figur

# Fungsi visualisasi animasi
def tampilkan_animasi(X, Y, kondisi, frame):
    kecepatanXAnim, kecepatanYAnim, ketinggianAnim = kondisi[frame]
    
    figurAnim = plt.figure(figsize=(12, 5), facecolor='#FFFFFF', edgecolor='none')
    
    sumbu1 = figurAnim.add_subplot(121)
    kontur = sumbu1.contourf(X, Y, np.sqrt(kecepatanXAnim**2 + kecepatanYAnim**2), levels=20, cmap='viridis')
    plt.colorbar(kontur, ax=sumbu1, label='Kecepatan (m/s)')
    sumbu1.set_title(f'Kecepatan pada Iterasi {frame*10}', color='black')
    sumbu1.set_xlabel('Panjang Saluran (m)', color='black')
    sumbu1.set_ylabel('Lebar Saluran (m)', color='black')
    sumbu1.tick_params(colors='black')
    sumbu1.spines['bottom'].set_color('#FFFFFF')
    sumbu1.spines['top'].set_color('#FFFFFF')
    sumbu1.spines['right'].set_color('#FFFFFF')
    sumbu1.spines['left'].set_color('#FFFFFF')
    
    sumbu2 = figurAnim.add_subplot(122)
    sumbu2.contourf(X, Y, ketinggianAnim, levels=20, cmap='Blues')
    sumbu2.set_title(f'Ketinggian Air pada Iterasi {frame*10}', color='black')
    sumbu2.set_xlabel('Panjang Saluran (m)', color='black')
    sumbu2.set_ylabel('Lebar Saluran (m)', color='black')
    sumbu2.tick_params(colors='black')
    sumbu2.spines['bottom'].set_color('#FFFFFF')
    sumbu2.spines['top'].set_color('#FFFFFF')
    sumbu2.spines['right'].set_color('#FFFFFF')
    sumbu2.spines['left'].set_color('#FFFFFF')
    
    # Hapus background figure
    figurAnim.patch.set_alpha(0.0)
    
    return figurAnim

# Fungsi analisis erosi dan sedimentasi
def tampilkan_analisis_erosi(X, Y, kecepatanTotal):
    # Hitung potensi erosi (kecepatan > threshold)
    batasErosi = 1.2  # m/s
    risikoErosi = kecepatanTotal > batasErosi
    
    # Hitung potensi sedimentasi (kecepatan < threshold)
    batasSedimentasi = 0.2  # m/s
    risikoSedimentasi = kecepatanTotal < batasSedimentasi
    
    # Visualisasi
    figurErosi = plt.figure(figsize=(15, 5), facecolor='#FFFFFF', edgecolor='none')
    
    sumbu1 = figurErosi.add_subplot(131)
    sumbu1.contourf(X, Y, risikoErosi.astype(int), levels=[0, 0.5, 1], colors=['#FFFFFF', '#FF6B6B'])
    sumbu1.set_title("Area Risiko Erosi", color='black')
    sumbu1.set_xlabel('Panjang Saluran (m)', color='black')
    sumbu1.set_ylabel('Lebar Saluran (m)', color='black')
    sumbu1.tick_params(colors='black')
    sumbu1.spines['bottom'].set_color('#FFFFFF')
    sumbu1.spines['top'].set_color('#FFFFFF')
    sumbu1.spines['right'].set_color('#FFFFFF')
    sumbu1.spines['left'].set_color('#FFFFFF')
    
    sumbu2 = figurErosi.add_subplot(132)
    sumbu2.contourf(X, Y, risikoSedimentasi.astype(int), levels=[0, 0.5, 1], colors=['#FFFFFF', '#8B4513'])
    sumbu2.set_title("Area Risiko Sedimentasi", color='black')
    sumbu2.set_xlabel('Panjang Saluran (m)', color='black')
    sumbu2.set_ylabel('Lebar Saluran (m)', color='black')
    sumbu2.tick_params(colors='black')
    sumbu2.spines['bottom'].set_color('#FFFFFF')
    sumbu2.spines['top'].set_color('#FFFFFF')
    sumbu2.spines['right'].set_color('#FFFFFF')
    sumbu2.spines['left'].set_color('#FFFFFF')
    
    sumbu3 = figurErosi.add_subplot(133)
    gabungan = np.zeros_like(kecepatanTotal)
    gabungan[risikoErosi] = 1
    gabungan[risikoSedimentasi] = -1
    sumbu3.contourf(X, Y, gabungan, levels=[-1, 0, 1], colors=['#8B4513', '#FFFFFF', '#FF6B6B'])
    sumbu3.set_title("Kombinasi Risiko", color='black')
    sumbu3.set_xlabel('Panjang Saluran (m)', color='black')
    sumbu3.set_ylabel('Lebar Saluran (m)', color='black')
    sumbu3.tick_params(colors='black')
    sumbu3.spines['bottom'].set_color('#FFFFFF')
    sumbu3.spines['top'].set_color('#FFFFFF')
    sumbu3.spines['right'].set_color('#FFFFFF')
    sumbu3.spines['left'].set_color('#FFFFFF')
    
    # Hapus background figure
    figurErosi.patch.set_alpha(0.0)
    
    plt.tight_layout()
    return figurErosi, risikoErosi, risikoSedimentasi

# Fungsi grafik perbandingan debit
def tampilkan_perbandingan_debit(debitMasuk, debitKeluaran):
    figurDebit = plt.figure(figsize=(10, 4), facecolor='#FFFFFF', edgecolor='none')
    
    plt.bar(["Debit Masuk", "Debit Keluaran"], [debitMasuk, debitKeluaran], color=['#4E8BF5', '#4CAF50'])
    plt.ylabel("Debit (m³/s)", color='black')
    plt.title("Perbandingan Debit Masuk dan Keluaran", color='black')
    plt.tick_params(colors='black')
    
    # Hapus background dan frame
    ax = plt.gca()
    ax.spines['bottom'].set_color('#FFFFFF')
    ax.spines['top'].set_color('#FFFFFF')
    ax.spines['right'].set_color('#FFFFFF')
    ax.spines['left'].set_color('#FFFFFF')
    
    # Hapus background figure
    figurDebit.patch.set_alpha(0.0)
    
    # Hitung efisiensi
    efisiensi = (debitKeluaran / debitMasuk) * 100
    
    return figurDebit, efisiensi

# UI Streamlit
st.title("🌾 Simulasi Aliran Air di Saluran Irigasi Sawah")

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
    
    # Tombol simulasi
    st.markdown("---")
    tombolJalankan = st.button("🚀 Jalankan Simulasi", use_container_width=True)

# Z.AI Configuration
st.sidebar.markdown("---")
st.sidebar.header("🤖 Z.AI Configuration")
st.session_state.zai_api_key = st.sidebar.text_input("Z.AI API Key", value=st.session_state.zai_api_key, type="password", help="Masukkan API key Z.AI Anda")
st.session_state.use_zai = st.sidebar.checkbox("Aktifkan Z.AI Assistant", value=st.session_state.use_zai)

# Informasi tentang koneksi internet
if st.session_state.use_zai:
    st.sidebar.info("""
    ℹ️ **Informasi Penting:**
    - Fitur Z.AI memerlukan koneksi internet yang stabil
    - Pastikan API key Z.AI Anda valid
    - Response time bergantung pada kekuatan sinyal
    - Semua pertanyaan diproses langsung oleh AI
    """)

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
    
    # Tampilkan metrik
    st.subheader("📊 Hasil Simulasi")
    kolom1, kolom2, kolom3, kolom4 = st.columns(4)
    kolom1.metric("Kecepatan Rata-rata", "{:.2f} m/s".format(kecepatanRataRata))
    kolom2.metric("Kecepatan Maksimum", "{:.2f} m/s".format(kecepatanMaksimum))
    kolom3.metric("Ketinggian Rata-rata", "{:.2f} m".format(ketinggianRataRata))
    kolom4.metric("Debit Keluaran", "{:.2f} m³/s".format(debitKeluaran))
    
    # Tampilkan visualisasi
    figur = tampilkan_hasil(X, Y, kecepatanX, kecepatanY, ketinggian)
    st.pyplot(figur)
    
    # Analisis erosi dan sedimentasi
    st.subheader("⛏️ Analisis Erosi dan Sedimentasi")
    figurErosi, risikoErosi, risikoSedimentasi = tampilkan_analisis_erosi(X, Y, kecepatanTotal)
    st.pyplot(figurErosi)
    
    # Rekomendasi erosi dan sedimentasi
    if np.any(risikoErosi):
        st.warning("⚠️ Terdapat area berisiko erosi! Pertimbangkan: \n- Perkuat dinding saluran \n- Kurangi kemiringan \n- Tambahkan tanaman penahan")
        
    if np.any(risikoSedimentasi):
        st.warning("⚠️ Terdapat area berisiko sedimentasi! Pertimbangkan: \n- Tambahkan kemiringan \n- Perbesar debit air \n- Rutin melakukan pengerukan")
    
    # Grafik perbandingan debit
    st.subheader("💧 Analisis Debit")
    figurDebit, efisiensi = tampilkan_perbandingan_debit(debitMasuk, debitKeluaran)
    st.pyplot(figurDebit)
    
    kolom1, kolom2 = st.columns(2)
    kolom1.metric("Efisiensi Saluran", f"{efisiensi:.1f}%")
    
    # Kebutuhan air
    kebutuhanAir = luasSawah * 10000 * 0.01  # Asumsi 1 cm/Ha/hari
    kolom2.metric("Kebutuhan Air/Hari", f"{kebutuhanAir:.2f} m³")
    
    if debitKeluaran < kebutuhanAir / 86400:  # Konversi ke m³/detik
        kolom2.error("❌ Debit air tidak mencukupi kebutuhan sawah!")
    else:
        kolom2.success("✅ Debit air mencukupi kebutuhan sawah")
    
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
    
    # Export hasil
    st.subheader("💾 Export Hasil")
    kolom1, kolom2 = st.columns(2)
    
    with kolom1:
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
    
    with kolom2:
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
    
    # Z.AI Assistant Section

        if st.session_state.use_zai:
            st.subheader("🤖 Z.AI Assistant - Sobat Pintar")
    
    def handle_chat_submit():
    # Fungsi ini akan dipanggil saat form disubmit
        if st.session_state.zai_chat_input:
            user_input = st.session_state.zai_chat_input
        
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
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Input untuk pesan baru
        st.markdown('<div class="zai-input-container">', unsafe_allow_html=True)
        
        # Gunakan form untuk mencegah refresh
        with st.form("zai_form", clear_on_submit=True):
            user_input = st.text_input(
                "Tanyakan kepada Z.AI (tekan Enter untuk mengirim):", 
                value=st.session_state.zai_input,
                placeholder="Contoh: Bagaimana cara mengatasi erosi pada saluran irigasi?",
                key="zai_chat_input"
            )
            
            submitted = st.form_submit_button("Kirim", on_click=handle_chat_submit)
           
            # Hanya tombol clear saja
            clear_button = st.form_submit_button("Hapus Chat", on_click=handle_chat_submit)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle form submission
    if user_input:  # Jika ada input, otomatis kirim
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
            
            # Bersihkan input
            st.session_state.zai_input = ""
    
    # Handle clear button
    if clear_button:
        st.session_state.zai_messages = []
    
    # Pertanyaan cepat
    st.subheader("💡 Pertanyaan Cepat:")
    col1, col2 = st.columns(2)
    
    with col1:
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
    
    with col2:
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