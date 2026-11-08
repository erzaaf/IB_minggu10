# Tugas Kelompok Berbasis Kasus 03 — Rule Based System

## Kasus: Sistem Pakar Diagnosis Gangguan Internet

Mendiagnosis penyebab gangguan internet dari sejumlah Fakta Awal menggunakan **8 aturan
produksi IF-THEN** yang masing-masing memiliki prioritas (salience), lalu membuktikan goal
tertentu dengan penalaran mundur. Semuat aturan dievaluasi oleh mesin inferensi sederhana
yang ditulis dalam **Python**.

---

## 1. Basis Pengetahuan

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

**Fakta Awal (dari soal):**

> Semua Situs Tidak Bisa Dibuka, Perangkat Lain Juga Offline, Tagihan Sudah Dibayar

Konversi label prioritas ke angka salience (semakin besar = semakin tinggi): Rendah = 1,
Sedang = 2, Tinggi = 3, Tertinggi = 4.

---

## 2. Penyelesaian
Diselesaikan dengan:

1. **Forward Chaining** (data-driven) — menarik semua kesimpulan yang bisa ditarik dari Fakta Awal
2. **Backward Chaining** (goal-driven) — pembuktian goal "Lapor ke Provider"
3. **Conflict Resolution** — prioritas (salience) → spesifisitas → urutan nomor aturan, dengan refractoriness aktif
