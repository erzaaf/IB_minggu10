from dataclasses import dataclass


SALIENCE = {"Rendah": 1, "Sedang": 2, "Tinggi": 3, "Tertinggi": 4}


@dataclass(frozen=True)
class Rule:
    id: str
    lhs: tuple
    rhs: str
    prioritas: str

    @property
    def salience(self):
        return SALIENCE[self.prioritas]

    @property
    def specificity(self):
        return len(self.lhs)

    @property
    def nomor(self):
        return int(self.id[1:])

    def __str__(self):
        return f"{self.id}: JIKA {' DAN '.join(self.lhs)} MAKA {self.rhs} [{self.prioritas}]"


RULES = [
    Rule("R1", ("Semua Situs Tidak Bisa Dibuka",), "Cek Router", "Rendah"),
    Rule("R2", ("Lampu Internet Router Merah",), "Gangguan Provider", "Sedang"),
    Rule("R3", ("Kecepatan Sangat Lambat",), "Gangguan Provider", "Sedang"),
    Rule("R4", ("Gangguan Provider", "Tagihan Sudah Dibayar"), "Lapor ke Provider", "Tinggi"),
    Rule("R5", ("Perangkat Lain Juga Offline",), "Gangguan Provider", "Sedang"),
    Rule("R6", ("Semua Situs Tidak Bisa Dibuka", "Hanya Laptop Ini Bermasalah"),
         "Masalah pada Laptop", "Tinggi"),
    Rule("R7", ("Gangguan Provider",), "Gunakan Tethering Sementara", "Rendah"),
    Rule("R8", ("Cek Router", "Router Terasa Panas"), "Matikan Router 10 Menit", "Tertinggi"),
]

FAKTA_AWAL = [
    "Semua Situs Tidak Bisa Dibuka",
    "Perangkat Lain Juga Offline",
    "Tagihan Sudah Dibayar",
]


def urutkan_conflict_set(cs):
    """Prioritas (salience) tertinggi -> spesifisitas terbesar -> nomor aturan terkecil."""
    return sorted(cs, key=lambda r: (-r.salience, -r.specificity, r.nomor))


def forward_chaining(rules, fakta_awal, verbose=True):
    wm = list(fakta_awal)
    sudah_fire = set()
    jejak = []
    iterasi = 0

    while True:
        iterasi += 1

        cs = [r for r in rules
              if r.id not in sudah_fire and all(k in wm for k in r.lhs)]
        if not cs:
            jejak.append((iterasi, [], None, "berhenti, tidak ada aturan yang cocok"))
            break

        terurut = urutkan_conflict_set(cs)
        dipilih = terurut[0]
        sudah_fire.add(dipilih.id)

        if dipilih.rhs in wm:
            perubahan = f"(tidak ada perubahan, '{dipilih.rhs}' sudah ada)"
        else:
            wm.append(dipilih.rhs)
            perubahan = f"+ {dipilih.rhs}"
        jejak.append((iterasi, terurut, dipilih, perubahan))

    if verbose:
        cetak_jejak(jejak)
        print("\nIsi Working Memory di akhir:")
        for f in wm:
            print(f"  - {f}")
        print("\nKesimpulan baru (bukan fakta awal):")
        for f in wm:
            if f not in fakta_awal:
                print(f"  * {f}")
    return wm, jejak


def cetak_jejak(jejak):
    print(f"{'Iter':<5}{'Conflict set (urut prioritas)':<42}{'Rule dipilih':<14}Perubahan WM")
    print("-" * 110)
    for it, cs, dipilih, perubahan in jejak:
        cs_str = "{" + ", ".join(r.id for r in cs) + "}"
        pilih = dipilih.id if dipilih else "-"
        print(f"{it:<5}{cs_str:<42}{pilih:<14}{perubahan}")


def jelaskan_konflik(jejak):
    print("\nIterasi dengan konflik (conflict set > 1 aturan):")
    for it, cs, dipilih, _ in jejak:
        if len(cs) > 1:
            print(f"\n  Iterasi {it}: conflict set = {{{', '.join(r.id for r in cs)}}}")
            for r in cs:
                print(f"     {r.id}: salience={r.salience} ({r.prioritas}), "
                      f"spesifisitas={r.specificity}")
            alasan = alasan_pilihan(cs)
            print(f"     -> dipilih {dipilih.id} karena {alasan}")


def alasan_pilihan(cs):
    terurut = urutkan_conflict_set(cs)
    menang, kedua = terurut[0], terurut[1]
    if menang.salience != kedua.salience:
        return f"salience tertinggi ({menang.prioritas})"
    if menang.specificity != kedua.specificity:
        return "salience sama, tetapi paling spesifik"
    return "salience & spesifisitas sama, nomor aturan terkecil"


def backward_chaining(rules, fakta, goal):
    """Pembuktian goal secara mundur. Fakta yang tidak ada di daftar dianggap tidak
    diketahui (closed-world): 'request' dijawab TIDAK."""
    log = []
    sedang_dibuktikan = set()

    def find_out(g, depth):
        pad = "    " * depth
        if g in fakta:
            log.append(f"{pad}FindOut({g}) -> ada di fakta awal  [OK]")
            return True
        if g in sedang_dibuktikan:
            log.append(f"{pad}FindOut({g}) -> sirkular  [GAGAL]")
            return False
        kandidat = [r for r in rules if r.rhs == g]
        if not kandidat:
            log.append(f"{pad}FindOut({g}) -> tidak ada rule yang menyimpulkan, "
                       f"bukan fakta awal (request: tidak diketahui)  [GAGAL]")
            return False
        log.append(f"{pad}FindOut({g}) -> rule kandidat {{{', '.join(r.id for r in kandidat)}}}")
        sedang_dibuktikan.add(g)
        for r in kandidat:
            if monitor(r, depth + 1):
                fakta.add(g)
                sedang_dibuktikan.discard(g)
                return True
        sedang_dibuktikan.discard(g)
        log.append(f"{pad}  => {g} tidak terbukti  [GAGAL]")
        return False

    def monitor(r, depth):
        pad = "    " * depth
        log.append(f"{pad}Monitor({r.id}): perlu {' DAN '.join(r.lhs)}")
        for kondisi in r.lhs:
            if not find_out(kondisi, depth + 1):
                log.append(f"{pad}  {r.id} gagal karena '{kondisi}' tidak terbukti")
                return False
        log.append(f"{pad}  {r.id} berhasil -> {r.rhs}  [OK]")
        return True

    hasil = find_out(goal, 0)
    return hasil, log


if __name__ == "__main__":
    print("=" * 110)
    print("Aturan Produksi")
    print("=" * 110)
    for r in RULES:
        print(" ", r)
    print("\nFakta awal:", ", ".join(FAKTA_AWAL))

    print("\n" + "=" * 110)
    print("(a) FORWARD CHAINING")
    print("=" * 110)
    wm, jejak = forward_chaining(RULES, FAKTA_AWAL)

    print("\n" + "=" * 110)
    print("(b) BACKWARD CHAINING, goal: Lapor ke Provider")
    print("=" * 110)
    ok, log = backward_chaining(RULES, set(FAKTA_AWAL), "Lapor ke Provider")
    print("\n".join(log))
    print(f"\nHasil: goal 'Lapor ke Provider' {'TERBUKTI' if ok else 'TIDAK TERBUKTI'}")

    print("\n" + "=" * 110)
    print("(c) CONFLICT RESOLUTION (salience -> specificity -> nomor aturan; refractoriness aktif)")
    print("=" * 110)
    jelaskan_konflik(jejak)