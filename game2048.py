"""
Game 2048 - Versi Terminal (Python)
Tugas Mata Kuliah Kecerdasan Buatan
"""

import random
import os

SIZE = 4  # ukuran grid (4x4)


def buat_grid_kosong():
    """Buat grid SIZE x SIZE, semua isinya 0 (kosong)."""
    return [[0 for _ in range(SIZE)] for _ in range(SIZE)]


def spawn_tile(grid):
    """Munculkan angka baru (2 atau 4) di posisi kosong secara acak."""
    kosong = [(r, c) for r in range(SIZE) for c in range(SIZE) if grid[r][c] == 0]
    if not kosong:
        return
    r, c = random.choice(kosong)
    grid[r][c] = 2 if random.random() < 0.9 else 4


def cetak_grid(grid, skor):
    """Tampilkan grid ke layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"SKOR: {skor}\n")
    for row in grid:
        baris = ""
        for val in row:
            if val == 0:
                baris += ".".rjust(6)
            else:
                baris += str(val).rjust(6)
        print(baris)
    print("\nGerakan: W(atas) A(kiri) S(bawah) D(kanan)  |  Q untuk keluar")


def geser_baris_kiri(baris, skor):
    """
    Geser satu baris ke kiri + gabungkan angka yang sama.
    Mengembalikan (baris_baru, skor_baru).
    """
    angka = [v for v in baris if v != 0]  # buang angka 0
    hasil = []
    i = 0
    while i < len(angka):
        if i + 1 < len(angka) and angka[i] == angka[i + 1]:
            gabung = angka[i] * 2
            hasil.append(gabung)
            skor += gabung
            i += 2  # lompat dua angka karena sudah digabung
        else:
            hasil.append(angka[i])
            i += 1
    while len(hasil) < SIZE:
        hasil.append(0)
    return hasil, skor


def putar_grid(grid):
    """Putar grid 90 derajat searah jarum jam."""
    return [list(row) for row in zip(*grid[::-1])]


def gerakkan(grid, arah, skor):
    """
    Gerakkan seluruh grid ke satu arah.
    Trik: putar grid supaya arah yang diminta 'menjadi' kiri,
    proses geser-kiri, lalu putar balik ke posisi semula.
    """
    rotasi = {"kiri": 0, "atas": 3, "kanan": 2, "bawah": 1}[arah]

    g = grid
    for _ in range(rotasi):
        g = putar_grid(g)

    sebelum = [row[:] for row in g]
    baris_baru = []
    for row in g:
        hasil, skor = geser_baris_kiri(row, skor)
        baris_baru.append(hasil)
    g = baris_baru

    berubah = g != sebelum

    for _ in range((4 - rotasi) % 4):
        g = putar_grid(g)

    return g, skor, berubah


def masih_bisa_gerak(grid):
    """Cek apakah masih ada sel kosong atau pasangan sama (belum game over)."""
    for r in range(SIZE):
        for c in range(SIZE):
            if grid[r][c] == 0:
                return True
            if c < SIZE - 1 and grid[r][c] == grid[r][c + 1]:
                return True
            if r < SIZE - 1 and grid[r][c] == grid[r + 1][c]:
                return True
    return False


def main():
    grid = buat_grid_kosong()
    skor = 0
    spawn_tile(grid)
    spawn_tile(grid)

    tombol_ke_arah = {
        "w": "atas", "a": "kiri", "s": "bawah", "d": "kanan"
    }

    while True:
        cetak_grid(grid, skor)

        if not masih_bisa_gerak(grid):
            print("\nGAME OVER!")
            break

        tombol = input("Masukkan gerakan: ").strip().lower()

        if tombol == "q":
            print("Keluar dari game.")
            break

        if tombol not in tombol_ke_arah:
            continue  # input tidak dikenali, minta lagi

        arah = tombol_ke_arah[tombol]
        grid, skor, berubah = gerakkan(grid, arah, skor)

        if berubah:
            spawn_tile(grid)


if __name__ == "__main__":
    main()
