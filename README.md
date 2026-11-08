# Tugas 3 - Sistem Pakar Diagnosis Gangguan Internet

Implementasi **Rule Based System** (materi Minggu ke-10, Inteligensi Buatan) untuk kasus
diagnosis gangguan internet, menggunakan bahasa pemrograman **Python** (tanpa library
eksternal).

## Basis Pengetahuan

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

## Cara Menjalankan

```bash
python tugas3_sistem_pakar.py
```

## Jawaban

### (a) Forward chaining - semua kesimpulan dari Fakta Awal

Mesin inferensi data-driven memilih aturan dari conflict set tiap iterasi, dengan
refractoriness aktif (aturan yang sudah fire tidak diaktifkan lagi). Jejaknya dicetak
program dalam bentuk tabel: iterasi, conflict set, rule dipilih, dan perubahan working memory.

Kesimpulan baru yang ditarik dari 3 Fakta Awal:

1. **Gangguan Provider** (iterasi 1, via R5)
2. **Lapor ke Provider** (iterasi 2, via R4)
3. **Cek Router** (iterasi 3, via R1)
4. **Gunakan Tethering Sementara** (iterasi 4, via R7)

Yang tidak dapat ditarik: *Masalah pada Laptop* (R6 butuh fakta "Hanya Laptop Ini Bermasalah")
dan *Matikan Router 10 Menit* (R8 butuh fakta "Router Terasa Panas").

### (b) Backward chaining - buktikan goal "Lapor ke Provider"

Penalaran goal-driven menelusuri mundur sesuai algoritma FindOut/Monitor:

```
Lapor ke Provider  (goal)
└─ R4: Gangguan Provider DAN Tagihan Sudah Dibayar
   ├─ Tagihan Sudah Dibayar  -> ada di fakta awal  ✔
   └─ Gangguan Provider      -> sub-goal
      ├─ R2: butuh "Lampu Internet Router Merah"        -> tidak diketahui, GAGAL
      ├─ R3: butuh "Kecepatan Sangat Lambat"            -> tidak diketahui, GAGAL
      └─ R5: butuh "Perangkat Lain Juga Offline"        -> fakta awal, OK
         -> Gangguan Provider terbukti (via R5)

=> goal "Lapor ke Provider" TERBUKTI
```

### (c) Conflict resolution

Urutan pertimbangan: **(1) prioritas/salience, (2) spesifisitas (jumlah premis),
(3) urutan nomor aturan**, dengan refractoriness berlaku sepanjang proses.
Iterasi ketika lebih dari satu aturan siap jalan:

| Iterasi | Conflict set | Yang dipilih | Kriteria penentu |
|---------|--------------|--------------|------------------|
| 1 | {R1, R5} | R5 | salience: Sedang(2) > Rendah(1) — walau berpola urut nomor |
| 2 | {R1, R4, R7} | R4 | salience: Tinggi(3) tertinggi |
| 3 | {R1, R7} | R1 | salience seri (Rendah=1), spesifisitas seri (1 premis) → **urutan nomor** (R1 < R7) |

## Struktur Program

- `Rule` (dataclass): merepresentasikan 1 aturan produksi, dengan properti
  `salience`, `specificity`, dan `nomor` untuk conflict resolution.
- `urutkan_conflict_set()`  : strategi pemilihan aturan (salience → specificity → rule order).
- `forward_chaining()`      : inferensi data-driven + jejak iterasi + refractoriness.
- `backward_chaining()`     : inferensi goal-driven (FindOut/Monitor) dengan penanganan
  antar-sirkularitas dan asumsi closed-world (fakta yang tidak diketahui dijawab TIDAK).
- `jelaskan_konflik()`      : menampilkan urutan pemilihan pada iterasi yang konflik.
