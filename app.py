import streamlit as st
import pandas as pd

st.set_page_config(page_title="E-Pustaka Bangkalan Bangkalan", page_icon="📚", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp { background: #f4f7fb; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg,#0f3d66,#1b6ca8); }
section[data-testid="stSidebar"] * { color: #fff !important; }
.hero { background: linear-gradient(135deg,#0f3d66,#2a9d8f); padding: 28px 32px;
        border-radius: 18px; color: #fff; margin-bottom: 22px; }
.hero h1 { margin: 0; font-size: 28px; color: #fff; }
.hero p { margin: 6px 0 0; opacity: .9; }
.card { background: #fff; padding: 20px; border-radius: 16px;
        box-shadow: 0 4px 14px rgba(15,61,102,.08); border-left: 6px solid var(--c); }
.card .num { font-size: 30px; font-weight: 700; color: #0f3d66; }
.card .lbl { color: #6b7a8c; font-size: 14px; }
.book { background:#fff; padding:16px; border-radius:14px; height:100%;
        box-shadow: 0 4px 14px rgba(15,61,102,.08); }
.book .ic { font-size: 40px; }
.book b { color:#0f3d66; }
.tag { display:inline-block; padding:3px 10px; border-radius:20px; font-size:12px; color:#fff; }
</style>
""", unsafe_allow_html=True)


def hero(title, sub):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{sub}</p></div>', unsafe_allow_html=True)


def card(col, num, label, color):
    col.markdown(
        f'<div class="card" style="--c:{color}"><div class="num">{num}</div>'
        f'<div class="lbl">{label}</div></div>', unsafe_allow_html=True)


# ---------- DATA CONTOH ----------
buku = pd.DataFrame({
    "Judul": ["Laskar Pelangi", "Bumi Manusia", "Filosofi Teras", "Atomic Habits",
              "Sejarah Madura", "Pemrograman Python", "Cerita Rakyat Bangkalan", "Bumi"],
    "Penulis": ["Andrea Hirata", "Pramoedya A.T.", "Henry Manampiring", "James Clear",
                "Kuntowijoyo", "Budi Raharjo", "Tim DPK", "Tere Liye"],
    "Kategori": ["Novel", "Novel", "Pengembangan Diri", "Pengembangan Diri",
                 "Sejarah", "Teknologi", "Budaya Lokal", "Novel"],
    "Stok": [5, 2, 4, 0, 3, 6, 7, 1],
})
arsip = pd.DataFrame({
    "No. Arsip": ["ARS-001", "ARS-002", "ARS-003", "ARS-004", "ARS-005"],
    "Nama Dokumen": ["Surat Keputusan Bupati", "Laporan Keuangan 2023", "Peta Wilayah Lama",
                     "Notulen Rapat Dinas", "Foto Dokumentasi Kegiatan"],
    "Jenis": ["Surat", "Laporan", "Peta", "Notulen", "Foto"],
    "Tahun": [2021, 2023, 1998, 2024, 2022],
    "Status": ["Aktif", "Aktif", "Statis", "Aktif", "Statis"],
})
pinjam = pd.DataFrame({
    "Peminjam": ["Siti Aisyah", "Ahmad Fauzi", "Dewi Lestari", "Rizky Pratama"],
    "Buku": ["Laskar Pelangi", "Pemrograman Python", "Sejarah Madura", "Bumi Manusia"],
    "Tgl Pinjam": ["01 Nov 2026", "02 Nov 2026", "03 Nov 2026", "04 Nov 2026"],
    "Batas Kembali": ["08 Nov 2026", "09 Nov 2026", "10 Nov 2026", "11 Nov 2026"],
    "Status": ["Dipinjam", "Dipinjam", "Dikembalikan", "Dipinjam"],
})

# ---------- SIDEBAR ----------
st.sidebar.markdown("## 📚 E-Pustaka Bangkalan")
st.sidebar.caption("Dinas Perpustakaan dan Kearsipan\nKabupaten Bangkalan")
menu = st.sidebar.radio("Menu", ["🏠 Dashboard", "📖 Katalog Buku", "🔄 Peminjaman", "🗄️ Arsip Digital"])

# ---------- HALAMAN ----------
if menu == "🏠 Dashboard":
    hero("Selamat Datang di E-Pustaka Bangkalan", "Sistem Informasi Perpustakaan dan Arsip Digital Kabupaten Bangkalan")
    c1, c2, c3, c4 = st.columns(4)
    card(c1, "1.250", "Total Koleksi Buku", "#1b6ca8")
    card(c2, "86", "Sedang Dipinjam", "#2a9d8f")
    card(c3, "430", "Arsip Digital", "#e9a23b")
    card(c4, "312", "Anggota Aktif", "#e76f51")
    st.write("")
    a, b = st.columns(2)
    with a:
        st.subheader("Kunjungan per Bulan")
        st.line_chart(pd.DataFrame({"Pengunjung": [120, 150, 170, 140, 210, 260]},
                                   index=["Mei", "Jun", "Jul", "Agu", "Sep", "Okt"]))
    with b:
        st.subheader("Koleksi per Kategori")
        st.bar_chart(buku.groupby("Kategori")["Stok"].sum())

elif menu == "📖 Katalog Buku":
    hero("Katalog Buku", "Cari dan lihat ketersediaan koleksi perpustakaan")
    f1, f2 = st.columns([2, 1])
    cari = f1.text_input("🔍 Cari judul atau penulis")
    kat = f2.selectbox("Kategori", ["Semua"] + sorted(buku["Kategori"].unique()))
    data = buku[buku["Judul"].str.contains(cari, case=False) |
                buku["Penulis"].str.contains(cari, case=False)]
    if kat != "Semua":
        data = data[data["Kategori"] == kat]
    cols = st.columns(4)
    for i, (_, r) in enumerate(data.iterrows()):
        warna, teks = ("#2a9d8f", "Tersedia") if r["Stok"] > 0 else ("#e76f51", "Habis")
        cols[i % 4].markdown(
            f'<div class="book"><div class="ic">📘</div><b>{r["Judul"]}</b><br>'
            f'<small>{r["Penulis"]}</small><br><small>{r["Kategori"]}</small><br><br>'
            f'<span class="tag" style="background:{warna}">{teks} · {r["Stok"]}</span></div>',
            unsafe_allow_html=True)
        cols[i % 4].write("")

elif menu == "🔄 Peminjaman":
    hero("Peminjaman Buku", "Catat dan pantau peminjaman anggota")
    with st.expander("➕ Tambah Peminjaman Baru", expanded=True):
        x, y, z = st.columns(3)
        x.text_input("Nama Peminjam")
        y.selectbox("Judul Buku", buku["Judul"])
        z.date_input("Batas Pengembalian")
        if st.button("Simpan", type="primary"):
            st.success("Tampilan saja: data belum disimpan ke database.")
    st.subheader("Riwayat Peminjaman")
    st.dataframe(pinjam, use_container_width=True, hide_index=True)

else:
    hero("Arsip Digital", "Pengelolaan dokumen kearsipan secara digital")
    st.file_uploader("📤 Unggah dokumen arsip", type=["pdf", "jpg", "png", "docx"])
    jenis = st.multiselect("Filter jenis", arsip["Jenis"].unique(), default=list(arsip["Jenis"].unique()))
    st.dataframe(arsip[arsip["Jenis"].isin(jenis)], use_container_width=True, hide_index=True)
