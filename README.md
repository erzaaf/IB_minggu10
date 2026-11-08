# Tugas Kelompok Berbasis Kasus 03 — Rule Based System

## Kasus: Sistem Pakar Diagnosis Gangguan Internet

Mendiagnosis penyebab gangguan internet dari sejumlah Fakta Awal menggunakan **8 aturan
produksi IF-THEN** yang masing-masing memiliki prioritas (salience), lalu membuktikan goal
tertentu dengan penalaran mundur. Semuat aturan dievaluasi oleh mesin inferensi sederhana
yang ditulis dalam **Python**.

Diselesaikan dengan:

1. **Forward Chaining** (data-driven) — menarik semua kesimpulan yang bisa ditarik dari Fakta Awal
2. **Backward Chaining** (goal-driven) — pembuktian goal "Lapor ke Provider"
3. **Conflict Resolution** — prioritas (salience) → spesifisitas → urutan nomor aturan, dengan refractoriness aktif

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

## 2. (a) Forward Chaining

Jejak lengkap iterasi dari program (conflict set setelah refractoriness):

| Iter | Conflict set (urut prioritas) | Rule dipilih | Perubahan Working Memory |
|------|-------------------------------|--------------|--------------------------|
| 1 | {R5, R1} | R5 | + Gangguan Provider |
| 2 | {R4, R1, R7} | R4 | + Lapor ke Provider |
| 3 | {R1, R7} | R1 | + Cek Router |
| 4 | {R7} | R7 | + Gunakan Tethering Sementara |
| 5 | {} | – | berhenti, tidak ada aturan yang cocok |

> Catatan: R2 dan R3 tidak pernah masuk conflict set karena premisnya ("Lampu Internet
> Router Merah", "Kecepatan Sangat Lambat") tidak pernah ada di Working Memory. R6 dan R8
> juga tidak aktif (butuh fakta "Hanya Laptop Ini Bermasalah" dan "Router Terasa Panas"
> yang tidak diketahui).

**Kesimpulan semua yang bisa ditarik dari Fakta Awal (4 kesimpulan baru):**

1. **Gangguan Provider** — via R5 (iterasi 1)
2. **Lapor ke Provider** — via R4 (iterasi 2)
3. **Cek Router** — via R1 (iterasi 3)
4. **Gunakan Tethering Sementara** — via R7 (iterasi 4)

---

## 3. (b) Backward Chaining — goal "Lapor ke Provider"

Penelusuran mundur dari goal sampai ke Fakta Awal yang mendukungnya (FindOut/Monitor):

```
FindOut(Lapor ke Provider) -> rule kandidat {R4}
    Monitor(R4): perlu Gangguan Provider DAN Tagihan Sudah Dibayar
        FindOut(Gangguan Provider) -> rule kandidat {R2, R3, R5}
            Monitor(R2): perlu Lampu Internet Router Merah            -> GAGAL
            Monitor(R3): perlu Kecepatan Sangat Lambat                -> GAGAL
            Monitor(R5): perlu Perangkat Lain Juga Offline            -> ada di fakta awal [OK]
        FindOut(Tagihan Sudah Dibayar)                                -> ada di fakta awal [OK]
    R4 berhasil -> Lapor ke Provider [OK]
```

Jalur bukti yang mendukung goal:

> **Lapor ke Provider** ← R4 ← { Gangguan Provider ← R5 ← (Perangkat Lain Juga Offline = fakta
> awal), Tagihan Sudah Dibayar (fakta awal) }

**Hasil: goal `Lapor ke Provider` TERBUKTI.** R2 dan R3 gagal karena "Lampu Internet Router
Merah" dan "Kecepatan Sangat Lambat" bukan fakta awal dan tidak dapat diturunkan dari fakta
apa pun (asumsi closed-world: request dijawab TIDAK).

---

## 4. (c) Conflict Resolution

Urutan pertimbangan: **(1) prioritas/salience, (2) spesifisitas (jumlah premis),
(3) urutan nomor aturan**. Refractoriness berlaku sepanjang proses — aturan yang sudah
dijalankan tidak diaktifkan lagi dengan data yang sama.

Iterasi ketika lebih dari satu aturan siap jalan:

**Iterasi 1 — conflict set {R5, R1}**

| Kandidat | salience | spesifisitas | urutan |
|----------|----------|--------------|--------|
| R5 | Sedang = 2 | 1 premis | R5 |
| R1 | Rendah = 1 | 1 premis | R1 |

→ dipilih **R5** karena salience tertinggi (Sedang), meskipun R1 menurut urutan nomor.

**Iterasi 2 — conflict set {R4, R1, R7}**

| Kandidat | salience | spesifisitas | urutan |
|----------|----------|--------------|--------|
| R4 | Tinggi = 3 | 2 premis | R4 |
| R1 | Rendah = 1 | 1 premis | R1 |
| R7 | Rendah = 1 | 1 premis | R7 |

→ dipilih **R4** karena salience tertinggi (Tinggi).

**Iterasi 3 — conflict set {R1, R7}**

| Kandidat | salience | spesifisitas | urutan |
|----------|----------|--------------|--------|
| R1 | Rendah = 1 | 1 premis | R1 |
| R7 | Rendah = 1 | 1 premis | R7 |

→ salience seri, spesifisitas seri, sehingga penentu akhirnya **urutan nomor aturan**:
dipilih **R1** (R1 < R7).
