"""
TUGAS 2: KALKULATOR STATISTIK
Nama  : Ade Nugroho
NIM   : 235150700111006
Kelas : Data Sains TI - A
"""

import streamlit as st
from typing import Dict, List, Optional, Any

def parse_input_angka(input_str: str) -> List[float]:
    """Mengurai string input yang dipisahkan koma menjadi list angka (float)."""
    angka_bersih = []
    if not input_str:
        return []
        
    for item in input_str.split(','):
        try:
            angka_bersih.append(float(item.strip()))
        except ValueError:
            st.warning(f"Input '{item.strip()}' diabaikan karena bukan angka.")
    return angka_bersih

def hitung_statistik(angka: List[float]) -> Optional[Dict[str, Any]]:
    """Menghitung semua statistik yang diperlukan dari daftar angka."""
    if not angka:
        return None
        
    jumlah_data = len(angka)
    total_jumlah = sum(angka)
    angka_integer = (int(x) for x in angka if x % 1 == 0)
    list_integer = list(angka_integer)
    
    hasil = {
        "rata_rata": total_jumlah / jumlah_data,
        "maksimum": max(angka),
        "minimum": min(angka),
        "jumlah_total": total_jumlah,
        "jumlah_angka": jumlah_data,
        "angka_genap": sum(1 for x in list_integer if x % 2 == 0),
        "angka_ganjil": sum(1 for x in list_integer if x % 2 != 0),
    }
    return hasil


def run_kalkulator_gui():
    st.title("📊 Kalkulator Statistik Sederhana")
    st.write("Dibuat oleh: **Ade Nugroho (235150700111006)**")

    input_str = st.text_input("Masukkan daftar angka (pisahkan dengan koma):", "2, 7, 4, 10, 5")

    if st.button("Hitung Statistik"):
        list_angka = parse_input_angka(input_str)
        hasil_statistik = hitung_statistik(list_angka)
        
        if hasil_statistik:
            st.subheader("--- Hasil Kalkulasi Statistik ---")
            
            col1, col2, col3 = st.columns(3) # Bagi jadi 3 kolom
            col1.metric("Rata-rata", f"{hasil_statistik['rata_rata']:.2f}")
            col2.metric("Maksimum", f"{hasil_statistik['maksimum']}")
            col3.metric("Minimum", f"{hasil_statistik['minimum']}")

            st.write(f"**Jumlah Total**: {hasil_statistik['jumlah_total']}")
            st.write(f"**Jumlah Angka**: {hasil_statistik['jumlah_angka']}")
            st.write(f"**Angka Genap**: {hasil_statistik['angka_genap']} (dari angka integer)")
            st.write(f"**Angka Ganjil**: {hasil_statistik['angka_ganjil']} (dari angka integer)")
        else:
            st.error("Tidak ada data angka yang valid untuk dihitung.")

if __name__ == "__main__":
    run_kalkulator_gui()