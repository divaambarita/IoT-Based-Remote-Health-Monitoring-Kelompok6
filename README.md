# Diagaram Blok Sistem

![Diagram Blok Sistem](DiagramBlokSistem_Kel6.jpg)
# IoT-Based-Remote-Health-Monitoring-Kelompok6
Sistem ini dapat memantau detak jantung dan suhu tubuh pasien secara real-time, lalu mengirimkan data tersebut ke cloud untuk pemantauan lebih lanjut. Proyek ini dirancang untuk mempermudah monitoring kesehatan pasien .
Tujuan:
Memantau detak jantung dan suhu tubuh pasien secara real-time, mengirimkan data ke cloud untuk analisis dan notifikasi jika terjadi ketidaknormalan. Hal ini akan meningkatkan kualitas pemantauan kesehatan di rumah atau fasilitas kesehatan tanpa keterbatasan jarak.

•	SDG 3: Good Health and Well-Being – Memastikan kehidupan yang sehat dan mendukung kesejahteraan bagi semua usia.


Gambaran Skema Blok Sistem:

•	Input: Sensor detak jantung (pulse sensor) dan sensor suhu (LM35)

•	Proses: Data yang dikumpulkan oleh sensor dikirimkan ke ESP32, yang terhubung ke internet melalui Wi-Fi. Data kemudian diteruskan ke platform cloud untuk pemantauan lebih lanjut.

•	Output: Dashboard visualisasi data di cloud, yang menampilkan detak jantung dan suhu tubuh pasien secara real-time.

Daftar Komponen yang Diperlukan:

•	ESP32

•	Pulse sensor (untuk memantau detak jantung)

•	LM35 (sensor suhu tubuh)

•	Wi-Fi module (terintegrasi dalam ESP32)

•	Platform: Blynk atau Firebase

Platform yang Digunakan:
•	Blynk atau Firebase – untuk pengumpulan data secara real-time dan tampilan dashboard.
