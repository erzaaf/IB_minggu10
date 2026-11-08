| ID | Aturan Produksi (IF-THEN) | Prioritas (salience) |
|----|---------------------------|----------------------|
| R1 | JIKA (Semua Situs Tidak Bisa Dibuka) MAKA (Cek Router) | Rendah |
| R2 | JIKA (Lampu Internet Router Merah) MAKA (Gangguan Provider) | Sedang |
| R3 | JIKA (Kecepatan Sangat Lambat) MAKA (Gangguan Provider) | Sedang |
| R4 | JIKA (Gangguan Provider) DAN (Tagihan Sudah Dibayar) MAKA (Lapor ke Provider) | Tinggi |
| R5 | JIKA (Perangkat Lain Juga Offline) MAKA (Gangguan Provider) | Sedang |
| R6 | JIKA (Semua Situs Tidak Bisa Dibuka) DAN (Hanya Laptop Ini Bermasalah) MAKA (Masalah pada Laptop) | Tinggi |
| R7 | JIKA (Gangguan Provider) MAKA (Gunakan Tethering Sementara) | Rendah |
| R8 | JIKA (Cek Router) DAN (Router Terasa Panas) MAKA (Matikan Router 10 Menit) | Tertinggi |

**Fakta Awal:** Semua Situs Tidak Bisa Dibuka, Perangkat Lain Juga Offline, Tagihan Sudah Dibayar.
