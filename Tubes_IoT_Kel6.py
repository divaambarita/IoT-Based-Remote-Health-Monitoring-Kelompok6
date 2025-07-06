import network
import time
import urequests
import json
from machine import Pin, ADC
import socket
import _thread
import ntptime

# --- Konfigurasi WiFi ---
WIFI_SSID = "Not4Public"
WIFI_PASSWORD = "password"

# --- Konfigurasi Firebase ---
FIREBASE_URL = "https://iotheartratemonitoring-default-rtdb.asia-southeast1.firebasedatabase.app/"

# --- Konfigurasi Sensor ---
PULSE_PIN = 34
PULSE_THRESHOLD = 2000
# =========================================================================

HTML_CODE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Monitoring Detak Jantung</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        body { font-family: 'Poppins', sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px 0; }
        .dashboard-container { background-color: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); text-align: center; width: 90%; max-width: 600px; }
        h1 { color: #1a73e8; margin-bottom: 10px; font-size: 1.8rem; }
        p { font-size: 1rem; color: #5f6368; margin-bottom: 20px; }
        .data-display { display: flex; justify-content: center; align-items: baseline; margin-bottom: 20px;}
        .bpm-display { font-size: 5rem; font-weight: 700; color: #202124; line-height: 1; }
        .bpm-unit { font-size: 1.2rem; font-weight: 400; color: #5f6368; margin-left: 8px; }
        .status-box { font-size: 1.2rem; font-weight: 600; padding: 10px; border-radius: 8px; margin-bottom: 30px;}
        .status-normal { color: #1e8e3e; background-color: #e6f4ea; }
        .status-warning { color: #d93025; background-color: #fce8e6; }
        .timestamp { margin-top: 30px; font-size: 0.9rem; color: #80868b; }
        .chart-container { margin-top: 30px; }
        .button-group { display: flex; justify-content: center; gap: 10px; margin-bottom: 20px;}
        .btn { border: none; padding: 12px 24px; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: background-color 0.3s, opacity 0.3s; }
        #toggle-monitor-btn { background-color: #1a73e8; color: white; }
        #toggle-monitor-btn:disabled { background-color: #9e9e9e; cursor: not-allowed; }
        #view-history-btn { background-color: #6c757d; color: white; }
        .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.5); }
        .modal-content { background-color: #fefefe; margin: 10% auto; padding: 20px; border: 1px solid #888; border-radius: 10px; width: 80%; max-width: 700px; }
        .modal-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #ddd; padding-bottom: 10px; margin-bottom: 20px; }
        .modal-header h2 { margin: 0; color: #1a73e8; }
        .close-btn { color: #aaa; font-size: 28px; font-weight: bold; cursor: pointer; }
        .modal-body { max-height: 60vh; overflow-y: auto; }
        #history-table { width: 100%; border-collapse: collapse; }
        #history-table th, #history-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        #history-table th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <h1>❤ IoT Heart Rate Monitor</h1>
        <p>Tekan tombol "Mulai" untuk pengukuran detak jantung selama 15 detik.</p>
        <div class="button-group">
            <button id="toggle-monitor-btn" class="btn">Mulai Mengukur</button>
            <button id="view-history-btn" class="btn">Lihat Riwayat</button>
        </div>
        <div class="data-display">
            <span id="bpm-value" class="bpm-display">--</span>
            <span class="bpm-unit">BPM</span>
        </div>
        <div id="status-text" class="status-box">Menunggu data...</div>
        <div class="chart-container">
            <canvas id="heartRateChart"></canvas>
        </div>
        <div id="timestamp" class="timestamp">Update terakhir: -</div>
    </div>
    <div id="history-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Riwayat Pengukuran</h2>
                <span id="close-modal-btn" class="close-btn">&times;</span>
            </div>
            <div class="modal-body">
                <table id="history-table">
                    <thead><tr><th>Tanggal & Waktu</th><th>BPM</th><th>Status</th></tr></thead>
                    <tbody id="history-table-body"></tbody>
                </table>
            </div>
        </div>
    </div>
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
        import { getDatabase, ref, set, onValue, query, limitToLast, get, onChildAdded, orderByChild, startAt } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-database.js";
        const firebaseConfig = {
            apiKey: "AIzaSyDH6fr2007UES7qKuV77SJkH0hrpXYGrGs",
            authDomain: "iotheartratemonitoring.firebaseapp.com",
            databaseURL: "https://iotheartratemonitoring-default-rtdb.asia-southeast1.firebasedatabase.app",
            projectId: "iotheartratemonitoring",
            storageBucket: "iotheartratemonitoring.appspot.com",
            messagingSenderId: "1015840225907",
            appId: "1:1015840225907:web:d7050b1bd502713f950806"
        };
        const app = initializeApp(firebaseConfig);
        const database = getDatabase(app);
        const controlRef = ref(database, 'control/isMonitoring');
        const historyRef = ref(database, 'history');
        const toggleBtn = document.getElementById('toggle-monitor-btn');
        const viewHistoryBtn = document.getElementById('view-history-btn');
        const historyModal = document.getElementById('history-modal');
        const closeModalBtn = document.getElementById('close-modal-btn');
        const bpmValueElement = document.getElementById('bpm-value');
        const statusTextElement = document.getElementById('status-text');
        const timestampElement = document.getElementById('timestamp');
        const ctx = document.getElementById('heartRateChart').getContext('2d');
        let lastTimestamp = 0;
        const heartRateChart = new Chart(ctx, {
            type: 'line', data: { labels: [], datasets: [{ label: 'Detak Jantung (BPM)', data: [], borderColor: 'rgba(239, 83, 80, 1)', backgroundColor: 'rgba(239, 83, 80, 0.2)', borderWidth: 2, fill: true, tension: 0.4 }] },
            options: { scales: { y: { beginAtZero: false, suggestedMin: 50, suggestedMax: 130, title: { display: true, text: 'BPM' } }, x: { title: { display: true, text: 'Waktu' } } }, plugins: { legend: { display: false } } }
        });
        function updateUI(data) {
            const bpm = data.bpm;
            const date = new Date(data.timestamp * 1000);
            const timeString = date.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            bpmValueElement.innerText = bpm;
            statusTextElement.innerText = `Status: ${data.status.charAt(0).toUpperCase() + data.status.slice(1)}`;
            statusTextElement.className = `status-box status-${data.status}`;
            timestampElement.innerText = `Update terakhir: ${date.toLocaleString('id-ID')}`;
            const MAX_DATA_POINTS_CHART = 20;
            heartRateChart.data.labels.push(timeString);
            heartRateChart.data.datasets[0].data.push(bpm);
            if (heartRateChart.data.labels.length > MAX_DATA_POINTS_CHART) {
                heartRateChart.data.labels.shift();
                heartRateChart.data.datasets[0].data.shift();
            }
            heartRateChart.update();
        }
        toggleBtn.addEventListener('click', () => { set(controlRef, true); });
        viewHistoryBtn.addEventListener('click', async () => {
            const historyTableBody = document.getElementById('history-table-body');
            historyTableBody.innerHTML = '<tr><td colspan="3">Memuat riwayat...</td></tr>';
            historyModal.style.display = 'block';
            const historyQuery = query(historyRef, orderByChild('timestamp'), limitToLast(100));
            try {
                const snapshot = await get(historyQuery);
                if (snapshot.exists()) {
                    historyTableBody.innerHTML = '';
                    let historyData = [];
                    snapshot.forEach(child => { historyData.push(child.val()); });
                    historyData.reverse().forEach(data => {
                        const date = new Date(data.timestamp * 1000);
                        const row = `<tr>
                            <td>${date.toLocaleString('id-ID')}</td>
                            <td>${data.bpm}</td>
                            <td style="color: ${data.status === 'normal' ? '#1e8e3e' : '#d93025'};">${data.status.charAt(0).toUpperCase() + data.status.slice(1)}</td>
                        </tr>`;
                        historyTableBody.innerHTML += row;
                    });
                } else {
                    historyTableBody.innerHTML = '<tr><td colspan="3">Tidak ada riwayat ditemukan.</td></tr>';
                }
            } catch (error) {
                console.error("Error fetching history:", error);
                historyTableBody.innerHTML = '<tr><td colspan="3" style="color:red;">Gagal memuat riwayat. Periksa Firebase Rules Anda.</td></tr>';
            }
        });
        closeModalBtn.addEventListener('click', () => { historyModal.style.display = 'none'; });
        window.addEventListener('click', (event) => { if (event.target == historyModal) historyModal.style.display = 'none'; });
        onValue(controlRef, (snapshot) => {
            const isMeasuring = snapshot.val();
            toggleBtn.innerText = isMeasuring ? 'Mengukur...' : 'Mulai Mengukur';
            toggleBtn.disabled = isMeasuring;
        });
        get(query(historyRef, limitToLast(20))).then(snapshot => {
            if(snapshot.exists()) {
                snapshot.forEach(child => {
                    const data = child.val();
                    lastTimestamp = data.timestamp;
                    updateUI(data);
                });
            }
            const newItemsQuery = query(historyRef, orderByChild('timestamp'), startAt(lastTimestamp + 1));
            onChildAdded(newItemsQuery, (newSnapshot) => { updateUI(newSnapshot.val()); });
        });
    </script>
</body>
</html>
"""

# --- BAGIAN KODE PYTHON UNTUK DEVICE (ESP32) ---

adc = ADC(Pin(PULSE_PIN))
adc.atten(ADC.ATTN_11DB)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Menghubungkan ke WiFi...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        max_wait = 15
        while not wlan.isconnected() and max_wait > 0:
            print('.', end='')
            time.sleep(1)
            max_wait -= 1
        if wlan.isconnected():
            print('\nKoneksi Berhasil! IP Address:', wlan.ifconfig()[0])
            return wlan
    else:
        print('Sudah terhubung. IP Address:', wlan.ifconfig()[0])
        return wlan
    return None

def sync_time():
    """Melakukan sinkronisasi RTC device dan memverifikasi hasilnya."""
    print("Mencoba sinkronisasi waktu (NTP)...")
    try:
        ntptime.settime()
        year = time.localtime()[0]
        if year < 2025:
            raise ValueError(f"Tahun tidak valid setelah sinkronisasi: {year}")
        
        utc_offset = 7 * 3600  # Offset UTC+7 untuk WIB
        actual_time = time.localtime(time.time() + utc_offset)
        print(f"Sinkronisasi waktu berhasil. Waktu saat ini (WIB): {actual_time[2]}-{actual_time[1]}-{actual_time[0]} {actual_time[3]:02d}:{actual_time[4]:02d}:{actual_time[5]:02d}")
    except Exception as e:
        print(f"Gagal total sinkronisasi waktu: {e}")

def set_monitoring_status(status):
    """Mengubah status monitoring di Firebase dengan lebih andal."""
    url = f"{FIREBASE_URL}control/isMonitoring.json"
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = urequests.put(url, data=json.dumps(status))
            if response.status_code == 200:
                print(f"Status kontrol berhasil diatur ke {status}.")
                response.close()
                return
            else:
                print(f"Percobaan {attempt + 1} gagal. Kode Status: {response.status_code}")
                response.close()
        except Exception as e:
            print(f"Percobaan {attempt + 1} gagal karena error: {e}")
        time.sleep(1)
    print("Gagal total mengatur status kontrol setelah beberapa percobaan.")

def send_history_to_firebase(bpm_value, timestamp):
    url = f"{FIREBASE_URL}history.json"
    data_payload = {"bpm": bpm_value, "timestamp": timestamp, "status": "normal" if 60 <= bpm_value <= 100 else "warning"}
    print(f"Mengirim data riwayat: {data_payload}")
    try:
        response = urequests.post(url, data=json.dumps(data_payload))
        response.close()
    except Exception as e:
        print(f"Error Firebase: {e}")

def sensor_monitor_loop():
    print("Memulai thread monitoring sensor...")
    while True:
        is_monitoring_active = False
        try:
            url_control = f"{FIREBASE_URL}control/isMonitoring.json"
            response = urequests.get(url_control)
            if response.status_code == 200:
                is_monitoring_active = json.loads(response.text)
            response.close()
        except Exception:
            time.sleep(2)
            continue

        if is_monitoring_active:
            print("\nPerintah 'Mulai' diterima. Mengukur BPM selama 15 detik...")
            start_time = time.ticks_ms()
            beats = 0
            beat_detected = False
            
            while time.ticks_diff(time.ticks_ms(), start_time) < 15000:
                sensor_value = adc.read()
                if sensor_value > PULSE_THRESHOLD and not beat_detected:
                    beat_detected = True
                    beats += 1
                elif sensor_value < PULSE_THRESHOLD:
                    beat_detected = False
                time.sleep_ms(20)
            
            bpm = beats * 4
            print(f"BPM terhitung: {bpm}")
            
            send_history_to_firebase(int(bpm), time.time())
            
            print("Pengukuran selesai. Mengembalikan status ke 'NONAKTIF'.")
            set_monitoring_status(False)  # Ensure status is set to False after measurement
            print("-" * 30)
            time.sleep(1)
        else:
            time.sleep(2)

def start_web_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    print('Web server berjalan di port 80')
    while True:
        try:
            cl, addr = s.accept()
            request = cl.recv(1024)
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(HTML_CODE)
            cl.close()
        except OSError as e:
            cl.close()


# === PROGRAM UTAMA ===
if connect_wifi():
    sync_time()
    set_monitoring_status(False)  # Ensure monitoring is off initially
    _thread.start_new_thread(sensor_monitor_loop, ())  # Start the sensor monitoring thread
    start_web_server()  # Start the web server to handle requests
else:
    print("Gagal memulai. Periksa koneksi WiFi.")
