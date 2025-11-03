"""
TUGAS 1: APLIKASI PENDAFTARAN MAHASISWA
Nama  : Ade Nugroho
NIM   : 235150700111006
Kelas : Data Sains TI - A
"""

import streamlit as st
from dataclasses import dataclass, asdict
from typing import Dict
import pandas as pd

# =====================================================================
# TUGAS 1: APLIKASI PENDAFTARAN MAHASISWA
# =====================================================================

@dataclass
class Mahasiswa:
    nama: str
    prodi: str
    ipk: float

DatabaseMahasiswa = Dict[str, Mahasiswa]

def page_tambah_mahasiswa():
    """Halaman untuk Menu 1: Tambah Mahasiswa"""
    st.subheader("Tambah Mahasiswa Baru")

    with st.form(key="form_tambah"):
        nim = st.text_input("NIM")
        nama = st.text_input("Nama Lengkap")
        prodi = st.text_input("Program Studi")
        
        ipk = st.number_input("IPK", min_value=0.0, max_value=4.0, value=3.0, step=0.01, format="%.2f")
        
        submit_button = st.form_submit_button(label="Tambahkan")

    if submit_button:
        if not nim or not nama or not prodi:
            st.error("Error: NIM, Nama, dan Prodi tidak boleh kosong.")
        elif nim in st.session_state.db_mahasiswa:
            st.error(f"Error: NIM {nim} sudah terdaftar.")
        else:
            st.session_state.db_mahasiswa[nim] = Mahasiswa(nama=nama, prodi=prodi, ipk=ipk)
            st.success(f"Sukses: Mahasiswa '{nama}' (NIM: {nim}) berhasil ditambahkan.")

def page_tampilkan_semua():
    """Halaman untuk Menu 2: Tampilkan Semua Mahasiswa"""
    st.subheader("Daftar Semua Mahasiswa")

    db: DatabaseMahasiswa = st.session_state.db_mahasiswa
    
    if not db:
        st.info("Database masih kosong. Belum ada data mahasiswa.")
        return

    data_list = []
    for nim, mhs in db.items():
        data_list.append({
            "NIM": nim,
            "Nama": mhs.nama,
            "Prodi": mhs.prodi,
            "IPK": mhs.ipk
        })
    
    df = pd.DataFrame(data_list).set_index("NIM")
    st.dataframe(df, use_container_width=True)
    
    st.markdown(f"**Total Mahasiswa:** `{len(db)}`")

def page_cari_mahasiswa():
    """Halaman untuk Menu 3: Cari Mahasiswa"""
    st.subheader("Cari Mahasiswa berdasarkan NIM")

    db: DatabaseMahasiswa = st.session_state.db_mahasiswa
    
    nim_cari = st.text_input("Masukkan NIM yang dicari:")

    if st.button("Cari"):
        if not nim_cari:
            st.warning("Silakan masukkan NIM.")
            return

        mahasiswa = db.get(nim_cari)
        
        if mahasiswa:
            st.success(f"Data ditemukan untuk NIM: **{nim_cari}**")
            st.markdown(f"""
            - **Nama  :** `{mahasiswa.nama}`
            - **Prodi :** `{mahasiswa.prodi}`
            - **IPK   :** `{mahasiswa.ipk:.2f}`
            """)
        else:
            st.error(f"Error: Mahasiswa dengan NIM '{nim_cari}' tidak ditemukan.")

def page_hapus_mahasiswa():
    """Halaman untuk Menu 4: Hapus Mahasiswa"""
    st.subheader("Hapus Mahasiswa berdasarkan NIM")
    
    db: DatabaseMahasiswa = st.session_state.db_mahasiswa

    nim_hapus = st.text_input("Masukkan NIM yang akan dihapus:")

    if st.button("Hapus Data", type="primary"):
        if not nim_hapus:
            st.warning("Silakan masukkan NIM.")
            return
            
        if db.get(nim_hapus):
            mahasiswa_dihapus = db.pop(nim_hapus)
            st.success(f"Sukses: Mahasiswa '{mahasiswa_dihapus.nama}' (NIM: {nim_hapus}) telah dihapus.")
        else:
            st.error(f"Error: Mahasiswa dengan NIM '{nim_hapus}' tidak ditemukan.")

def main():
    st.set_page_config(page_title="Data Mahasiswa", layout="centered")
    st.title("🎓 Sistem Pendaftaran Mahasiswa")
    st.write("---")
    st.write("Dibuat oleh: **Ade Nugroho (235150700111006)** - Kelas TI-A")

    if 'db_mahasiswa' not in st.session_state:
        st.session_state.db_mahasiswa = {}

    st.sidebar.header("Menu Navigasi")
    pilihan_menu = st.sidebar.radio(
        "Pilih Aksi:",
        ("Tampilkan Semua", "Tambah Mahasiswa", "Cari Mahasiswa", "Hapus Mahasiswa")
    )
    
    st.sidebar.info("Data akan tersimpan selama aplikasi berjalan (menggunakan Session State).")

    if pilihan_menu == "Tampilkan Semua":
        page_tampilkan_semua()
    elif pilihan_menu == "Tambah Mahasiswa":
        page_tambah_mahasiswa()
    elif pilihan_menu == "Cari Mahasiswa":
        page_cari_mahasiswa()
    elif pilihan_menu == "Hapus Mahasiswa":
        page_hapus_mahasiswa()

if __name__ == "__main__":
    main()