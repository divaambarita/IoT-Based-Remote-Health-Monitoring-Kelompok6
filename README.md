# Diagaram Blok Sistem

![Diagram Blok Sistem](DiagramBlokSistem_Kel6.jpg)
# IoT-Based Health Monitoring System (Kelompok 6)

Sistem ini menggunakan sensor detak jantung dan sensor suhu tubuh yang terhubung dengan modul ESP32 untuk memantau kondisi kesehatan pasien secara real-time. Data yang dikumpulkan akan dikirim melalui koneksi Wi-Fi ke platform cloud seperti Blynk atau Firebase, dan dapat dipantau melalui dashboard web yang menampilkan informasi detak jantung dan suhu tubuh pasien secara langsung.

## Tujuan Proyek
- Memantau detak jantung dan suhu tubuh pasien secara real-time.  
- Mengirimkan data sensor ke platform cloud untuk analisis dan pemantauan.  
- Memberikan visualisasi data kesehatan pasien melalui dashboard web.  
- Membantu meningkatkan kualitas pemantauan kesehatan pasien.

## Skema Sistem

### Input
- Pulse sensor (sensor detak jantung)  
- LM35 sensor (sensor suhu tubuh)

### Proses
- Data sensor dikirim ke ESP32 (microcontroller).  
- ESP32 menerima daya dari baterai atau laptop (power source).  
- Data dikirim melalui koneksi Wi-Fi ke platform cloud.

### Output
- Data disimpan dan dianalisis di platform cloud (Blynk atau Firebase).  
- Dashboard web menampilkan data real-time berupa detak jantung dan suhu tubuh pasien.

## Komponen Utama
- **ESP32:** Microcontroller dengan Wi-Fi terintegrasi.  
- **Pulse sensor:** Sensor detak jantung.  
- **LM35 sensor:** Sensor suhu tubuh.  
- **Power source:** Baterai atau laptop sebagai sumber daya.  
- **Platform cloud:** Blynk atau Firebase sebagai media pengumpulan data dan visualisasi.

## Manfaat dan Keterkaitan SDG
- Mendukung **SDG 3: Good Health and Well-Being** dengan menyediakan teknologi pemantauan kesehatan yang praktis dan efisien untuk semua usia.

## Cara Penggunaan
1. Hubungkan pulse sensor dan LM35 sensor ke ESP32 sesuai skema.  
2. Pastikan ESP32 terhubung dengan sumber daya (baterai/laptop).  
3. Konfigurasikan ESP32 agar terkoneksi ke jaringan Wi-Fi.  
4. Integrasikan ESP32 dengan platform Blynk atau Firebase untuk pengiriman data.  
5. Pantau data kesehatan secara real-time melalui dashboard web.
