import os
import sqlite3
import html
from datetime import date, timedelta

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="SI-PUSTAKA Bangkalan", page_icon="📚", layout="wide")

# ---------- DATABASE ----------
DB = "pustaka.db"
os.makedirs("uploads", exist_ok=True)


def run(sql, params=()):
    with sqlite3.connect(DB) as con:
        con.execute(sql, params)


def read(sql, params=()):
    with sqlite3.connect(DB) as con:
        return pd.read_sql_query(sql, con, params=params)


def init_db():
    run("""CREATE TABLE IF NOT EXISTS buku(id INTEGER PRIMARY KEY AUTOINCREMENT,
        judul TEXT, penulis TEXT, kategori TEXT, stok INTEGER)""")
    run("""CREATE TABLE IF NOT EXISTS peminjaman(id INTEGER PRIMARY KEY AUTOINCREMENT,
        peminjam TEXT, buku_id INTEGER, tgl_pinjam TEXT, batas_kembali TEXT, status TEXT)""")
    run("""CREATE TABLE IF NOT EXISTS arsip(id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT, jenis TEXT, tahun INTEGER, status TEXT, file TEXT)""")
    if read("SELECT COUNT(*) AS n FROM buku")["n"][0] == 0:
        for b in [("Laskar Pelangi", "Andrea Hirata", "Novel", 5), ("Bumi Manusia", "Pramoedya A.T.", "Novel", 2),
                  ("Filosofi Teras", "Henry Manampiring", "Pengembangan Diri", 4),
                  ("Sejarah Madura", "Kuntowijoyo", "Sejarah", 3), ("Pemrograman Python", "Budi Raharjo", "Teknologi", 6),
                  ("Cerita Rakyat Bangkalan", "Tim DPK", "Budaya Lokal", 7)]:
            run("INSERT INTO buku(judul,penulis,kategori,stok) VALUES(?,?,?,?)", b)


init_db()

# ---------- STYLE ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
html, body, .stApp, .stMarkdown, label, input, textarea, button, p, h1, h2, h3, h4 { font-family: 'Poppins', sans-serif; }
.stApp { background: linear-gradient(160deg,#e6f0fb 0%,#f8fafc 45%,#e5f5f1 100%); }
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.6rem; max-width: 1200px; }
section[data-testid="stSidebar"] { background: linear-gradient(190deg,#0b2d4f 0%,#14588f 60%,#1b7fa8 100%); }
section[data-testid="stSidebar"] * { color: #fff !important; }
section[data-testid="stSidebar"] [role="radiogroup"] { gap: 6px; }
section[data-testid="stSidebar"] [role="radiogroup"] > label { background: rgba(255,255,255,.08); padding: 10px 14px; border-radius: 12px; transition: .2s; }
section[data-testid="stSidebar"] [role="radiogroup"] > label:hover { background: rgba(255,255,255,.22); }
.brand { display:flex; gap:12px; align-items:center; padding: 6px 0 16px; }
.brand .logo { width:46px; height:46px; border-radius:14px; background:rgba(255,255,255,.18); display:flex; align-items:center; justify-content:center; font-size:24px; }
.brand b { font-size:18px; letter-spacing:.5px; } .brand small { display:block; opacity:.8; font-size:11px; line-height:1.3; }
.side-card { background:rgba(255,255,255,.1); border-radius:14px; padding:12px 14px; font-size:12px; margin-top:24px; line-height:1.5; }
.hero { position:relative; overflow:hidden; background:linear-gradient(120deg,#0f3d66 0%,#1b6ca8 55%,#2a9d8f 100%);
  border-radius:22px; padding:30px 34px; margin-bottom:22px; box-shadow:0 12px 30px rgba(15,61,102,.25); }
.hero:before, .hero:after { content:""; position:absolute; border-radius:50%; background:rgba(255,255,255,.08); }
.hero:before { width:220px; height:220px; right:-50px; top:-80px; } .hero:after { width:140px; height:140px; right:150px; bottom:-70px; }
.hero h1, .hero p, .hero .chip { color:#fff !important; position:relative; z-index:1; }
.hero h1 { margin:0; font-size:28px; font-weight:700; } .hero p { margin:6px 0 0; opacity:.92; font-size:14px; }
.hero .chip { display:inline-block; background:rgba(255,255,255,.18); padding:4px 12px; border-radius:20px; font-size:12px; margin-bottom:10px; }
.kpi { background:#fff; border-radius:18px; padding:18px 20px; display:flex; gap:16px; align-items:center; box-shadow:0 6px 18px rgba(15,61,102,.08); transition:.2s; }
.kpi:hover { transform:translateY(-4px); box-shadow:0 12px 26px rgba(15,61,102,.16); }
.kpi .ico { width:52px; height:52px; border-radius:15px; display:flex; align-items:center; justify-content:center; font-size:26px; background:var(--g); }
.kpi .num { font-size:28px; font-weight:700; color:#0f3d66; line-height:1.1; } .kpi .lbl { font-size:13px; color:#6b7a8c; }
[data-testid="stVerticalBlockBorderWrapper"] { background:#fff; border-radius:18px; box-shadow:0 6px 18px rgba(15,61,102,.07); }
.sec { font-weight:600; color:#0f3d66; font-size:17px; margin:2px 0 8px; }
.book { background:#fff; border-radius:18px; overflow:hidden; box-shadow:0 6px 18px rgba(15,61,102,.08); transition:.2s; margin-bottom:18px; }
.book:hover { transform:translateY(-5px); box-shadow:0 14px 28px rgba(15,61,102,.17); }
.book .cover { height:96px; display:flex; align-items:center; justify-content:center; font-size:44px; background:var(--g); }
.book .info { padding:14px 16px 16px; } .book .t { font-weight:600; color:#0f3d66; font-size:15px; line-height:1.3; }
.book .a { color:#6b7a8c; font-size:12.5px; margin:2px 0 10px; }
.badge { display:inline-block; padding:3px 11px; border-radius:20px; font-size:11.5px; font-weight:600; color:#fff; background:var(--c); }
.kat { background:#eef3f9; color:#1b6ca8; padding:3px 10px; border-radius:20px; font-size:11.5px; font-weight:500; margin-right:6px; }
table.tbl { width:100%; border-collapse:collapse; font-size:13.5px; }
table.tbl th { background:#0f3d66; color:#fff; text-align:left; padding:10px 12px; font-weight:600; }
table.tbl th:first-child { border-radius:10px 0 0 0; } table.tbl th:last-child { border-radius:0 10px 0 0; }
table.tbl td { padding:10px 12px; border-bottom:1px solid #eef2f7; color:#2b3a4a; }
table.tbl tr:nth-child(even) td { background:#f8fafd; }
div.stButton > button, div[data-testid="stFormSubmitButton"] > button { border-radius:12px; font-weight:600; border:0;
  background:linear-gradient(120deg,#1b6ca8,#2a9d8f); color:#fff; padding:.5rem 1.4rem; }
.stTabs [data-baseweb="tab-list"] { gap:8px; border:0; }
.stTabs [data-baseweb="tab"] { background:#fff; border-radius:12px; padding:8px 18px; box-shadow:0 2px 8px rgba(15,61,102,.06); }
.stTabs [aria-selected="true"] { background:#1b6ca8 !important; } .stTabs [aria-selected="true"] p { color:#fff !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display:none; }
.foot { text-align:center; color:#8a94a6; font-size:12px; margin-top:34px; }

/* Label form di area utama: biru tua agar terbaca di latar terang */
.block-container [data-testid="stWidgetLabel"] p,
.block-container [data-testid="stWidgetLabel"] label { color:#0f3d66 !important; font-weight:500; }

/* Kotak Tambah Buku Baru: seluruhnya hitam */
.block-container [data-testid="stExpander"] details { background:#1a1a1f !important; border:0 !important; border-radius:14px; }
.block-container [data-testid="stExpander"] summary,
.block-container [data-testid="stExpander"] summary * { background:#1a1a1f; color:#fff !important; }
.block-container [data-testid="stExpander"] [data-testid="stForm"] { border:0 !important; }
.block-container [data-testid="stExpander"] [data-testid="stWidgetLabel"] p,
.block-container [data-testid="stExpander"] [data-testid="stWidgetLabel"] label { color:#fff !important; }
.block-container [data-testid="stExpander"] input { background:#2b2b33 !important; color:#fff !important; }
/* Tab Tambah Arsip dan Daftar Arsip: hitam penuh */
.st-key-arsip_box [data-baseweb="tab-panel"] { background:#1a1a1f; border-radius:14px; padding:20px 22px; margin-top:10px; }
.st-key-arsip_box [data-testid="stWidgetLabel"] p,
.st-key-arsip_box [data-testid="stWidgetLabel"] label { color:#fff !important; }
.st-key-arsip_box [data-testid="stForm"] { border:0 !important; padding:0; }
.st-key-arsip_box input { background:#2b2b33 !important; color:#fff !important; }
.st-key-arsip_box table.tbl td { background:#1a1a1f !important; color:#e8edf3; border-bottom:1px solid #2f3340; }
.st-key-arsip_box table.tbl tr:nth-child(even) td { background:#22232a !important; }
</style>
""", unsafe_allow_html=True)

# ---------- HELPER ----------
esc = html.escape
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
PAL = [("#74b9ff", "#0984e3"), ("#55efc4", "#00b894"), ("#ffeaa7", "#fdcb6e"), ("#fab1a0", "#e17055"), ("#a29bfe", "#6c5ce7"), ("#fd79a8", "#e84393")]
ICON = {"Novel": "📖", "Pengembangan Diri": "🧠", "Sejarah": "🏛️", "Teknologi": "💻", "Budaya Lokal": "🎭"}
BC = {"Dipinjam": "#e9a23b", "Dikembalikan": "#2a9d8f", "Terlambat": "#e76f51", "Aktif": "#2a9d8f", "Statis": "#1b6ca8", "Inaktif": "#8a94a6"}


def hero(chip, title, sub):
    d = date.today()
    st.markdown(f'<div class="hero"><span class="chip">{chip} &nbsp;•&nbsp; {HARI[d.weekday()]}, {d.day} {BULAN[d.month-1]} {d.year}</span>'
                f'<h1>{title}</h1><p>{sub}</p></div>', unsafe_allow_html=True)


def kpi(col, icon, num, label, g):
    col.markdown(f'<div class="kpi"><div class="ico" style="--g:{g}">{icon}</div>'
                 f'<div><div class="num">{num}</div><div class="lbl">{label}</div></div></div>', unsafe_allow_html=True)


def table(df):
    if df.empty:
        return '<p style="color:#8a94a6;padding:8px">Belum ada data.</p>'
    th = "".join(f"<th>{esc(str(c))}</th>" for c in df.columns)
    rows = ""
    for _, r in df.iterrows():
        tds = ""
        for c in df.columns:
            v = str(r[c])
            tds += (f'<td><span class="badge" style="--c:{BC[v]}">{esc(v)}</span></td>' if c == "Status" and v in BC else f"<td>{esc(v)}</td>")
        rows += f"<tr>{tds}</tr>"
    return f'<table class="tbl"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table>'


def footer():
    st.markdown('<div class="foot">© 2026 Dinas Perpustakaan dan Kearsipan Kabupaten Bangkalan</div>', unsafe_allow_html=True)


# ---------- SIDEBAR ----------
st.sidebar.markdown('<div class="brand"><div class="logo">📚</div><div><b>SI-PUSTAKA</b>'
                    '<small>Dinas Perpustakaan dan Kearsipan<br>Kabupaten Bangkalan</small></div></div>', unsafe_allow_html=True)
menu = st.sidebar.radio("Menu", ["🏠 Dashboard", "📖 Katalog Buku", "🔄 Peminjaman", "🗄️ Arsip Digital"], label_visibility="collapsed")
st.sidebar.markdown('<div class="side-card">📍 Jl. Durinan, Durinan, Bancaran, Bangkalan<br>🕗 Sistem Informasi Perpustakaan dan Arsip Digital</div>', unsafe_allow_html=True)

# ---------- DASHBOARD ----------
if menu == "🏠 Dashboard":
    hero("Dashboard", "Selamat Datang di SI-PUSTAKA", "Sistem Informasi Perpustakaan dan Arsip Digital Kabupaten Bangkalan")
    n_buku = int(read("SELECT COUNT(*) AS n FROM buku")["n"][0])
    stok = int(read("SELECT COALESCE(SUM(stok),0) AS n FROM buku")["n"][0])
    dipinjam = int(read("SELECT COUNT(*) AS n FROM peminjaman WHERE status='Dipinjam'")["n"][0])
    n_arsip = int(read("SELECT COUNT(*) AS n FROM arsip")["n"][0])
    n_pem = int(read("SELECT COUNT(DISTINCT peminjam) AS n FROM peminjaman")["n"][0])
    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "📚", stok, f"Stok Tersedia ({n_buku} judul)", "linear-gradient(135deg,#d6ebff,#9fd0ff)")
    kpi(c2, "🔄", dipinjam, "Sedang Dipinjam", "linear-gradient(135deg,#d5f5e3,#8fe0b5)")
    kpi(c3, "🗄️", n_arsip, "Arsip Digital", "linear-gradient(135deg,#fff0c9,#ffd77a)")
    kpi(c4, "👥", n_pem, "Peminjam Tercatat", "linear-gradient(135deg,#ffd9d2,#ffa99a)")
    st.write("")
    a, b = st.columns(2)
    with a.container(border=True):
        st.markdown('<div class="sec">📊 Stok per Kategori</div>', unsafe_allow_html=True)
        d = read("SELECT kategori, SUM(stok) AS stok FROM buku GROUP BY kategori")
        st.altair_chart(alt.Chart(d).mark_arc(innerRadius=58, cornerRadius=4).encode(
            theta="stok:Q", color=alt.Color("kategori:N", scale=alt.Scale(scheme="tableau10"), legend=alt.Legend(orient="bottom", title=None)),
            tooltip=["kategori", "stok"]).properties(height=290), width="stretch")
    with b.container(border=True):
        st.markdown('<div class="sec">📈 Status Peminjaman</div>', unsafe_allow_html=True)
        d = read("SELECT status, COUNT(*) AS jumlah FROM peminjaman GROUP BY status")
        if d.empty:
            st.info("Belum ada data peminjaman.")
        else:
            st.altair_chart(alt.Chart(d).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, size=60).encode(
                x=alt.X("status:N", title=None, axis=alt.Axis(labelAngle=0)), y=alt.Y("jumlah:Q", title=None),
                color=alt.Color("status:N", legend=None, scale=alt.Scale(domain=["Dipinjam", "Dikembalikan"], range=["#e9a23b", "#2a9d8f"])),
                tooltip=["status", "jumlah"]).properties(height=290), width="stretch")
    st.write("")
    x, y = st.columns(2)
    with x.container(border=True):
        st.markdown('<div class="sec">🕘 Peminjaman Terbaru</div>', unsafe_allow_html=True)
        st.markdown(table(read("""SELECT p.peminjam AS Peminjam, b.judul AS Buku, p.status AS Status FROM peminjaman p
                                   JOIN buku b ON b.id=p.buku_id ORDER BY p.id DESC LIMIT 5""")), unsafe_allow_html=True)
    with y.container(border=True):
        st.markdown('<div class="sec">🗂️ Arsip Terbaru</div>', unsafe_allow_html=True)
        st.markdown(table(read("SELECT nama AS Dokumen, jenis AS Jenis, status AS Status FROM arsip ORDER BY id DESC LIMIT 5")), unsafe_allow_html=True)

# ---------- KATALOG ----------
elif menu == "📖 Katalog Buku":
    hero("Katalog", "Katalog Buku", "Cari koleksi dan lihat ketersediaan stok secara langsung")
    with st.expander("➕ Tambah Buku Baru"):
        with st.form("form_buku", clear_on_submit=True):
            x, y = st.columns(2)
            judul, penulis = x.text_input("Judul"), y.text_input("Penulis")
            kategori, stok = x.text_input("Kategori"), y.number_input("Stok", min_value=0, value=1)
            if st.form_submit_button("Simpan Buku"):
                if judul.strip():
                    run("INSERT INTO buku(judul,penulis,kategori,stok) VALUES(?,?,?,?)", (judul, penulis, kategori, int(stok)))
                    st.success("Buku tersimpan di database.")
                    st.rerun()
                else:
                    st.warning("Judul wajib diisi.")
    f1, f2 = st.columns([2, 1])
    cari = f1.text_input("🔍 Cari judul atau penulis", placeholder="Ketik kata kunci...")
    buku = read("SELECT * FROM buku")
    kat = f2.selectbox("Kategori", ["Semua"] + sorted(buku["kategori"].dropna().unique()))
    data = buku[buku["judul"].str.contains(cari, case=False) | buku["penulis"].str.contains(cari, case=False)]
    if kat != "Semua":
        data = data[data["kategori"] == kat]
    st.caption(f"Menampilkan {len(data)} dari {len(buku)} judul buku")
    cols = st.columns(4)
    for i, (_, r) in enumerate(data.iterrows()):
        k = str(r["kategori"] or "Umum")
        g = PAL[sum(map(ord, k)) % len(PAL)]
        warna, teks = ("#2a9d8f", f"Tersedia · {r['stok']}") if r["stok"] > 0 else ("#e76f51", "Stok habis")
        cols[i % 4].markdown(
            f'<div class="book"><div class="cover" style="--g:linear-gradient(135deg,{g[0]},{g[1]})">{ICON.get(k, "📘")}</div>'
            f'<div class="info"><div class="t">{esc(str(r["judul"]))}</div><div class="a">{esc(str(r["penulis"]))}</div>'
            f'<span class="kat">{esc(k)}</span><span class="badge" style="--c:{warna}">{teks}</span></div></div>', unsafe_allow_html=True)

# ---------- PEMINJAMAN ----------
elif menu == "🔄 Peminjaman":
    hero("Transaksi", "Peminjaman Buku", "Catat peminjaman, pantau riwayat, dan proses pengembalian buku")
    t1, t2, t3 = st.tabs(["➕ Peminjaman Baru", "📋 Riwayat", "✅ Pengembalian"])
    tersedia = read("SELECT id, judul FROM buku WHERE stok > 0")
    with t1:
        with st.form("form_pinjam", clear_on_submit=True):
            x, y, z = st.columns(3)
            nama = x.text_input("Nama Peminjam")
            judul = y.selectbox("Judul Buku", tersedia["judul"])
            batas = z.date_input("Batas Pengembalian", date.today() + timedelta(days=7))
            if st.form_submit_button("Simpan Peminjaman"):
                if nama.strip() and not tersedia.empty:
                    bid = int(tersedia[tersedia["judul"] == judul]["id"].iloc[0])
                    run("INSERT INTO peminjaman(peminjam,buku_id,tgl_pinjam,batas_kembali,status) VALUES(?,?,?,?,?)",
                        (nama, bid, str(date.today()), str(batas), "Dipinjam"))
                    run("UPDATE buku SET stok = stok - 1 WHERE id = ?", (bid,))
                    st.success("Peminjaman tersimpan di database.")
                    st.rerun()
                else:
                    st.warning("Nama peminjam wajib diisi.")
    riwayat = read("""SELECT p.id, p.status AS raw, p.peminjam AS Peminjam, b.judul AS Buku, p.tgl_pinjam AS 'Tgl Pinjam',
                      p.batas_kembali AS 'Batas Kembali',
                      CASE WHEN p.status='Dipinjam' AND p.batas_kembali < date('now','localtime') THEN 'Terlambat' ELSE p.status END AS Status
                      FROM peminjaman p JOIN buku b ON b.id = p.buku_id ORDER BY p.id DESC""")
    with t2:
        st.markdown(table(riwayat.drop(columns=["id", "raw"])), unsafe_allow_html=True)
    with t3:
        aktif = riwayat[riwayat["raw"] == "Dipinjam"]
        if aktif.empty:
            st.info("Tidak ada peminjaman aktif.")
        else:
            pilih = st.selectbox("Pilih peminjaman", aktif["id"],
                                 format_func=lambda i: f"{aktif[aktif.id == i].Peminjam.iloc[0]} - {aktif[aktif.id == i].Buku.iloc[0]}")
            if st.button("✅ Tandai Dikembalikan"):
                bid = int(read("SELECT buku_id FROM peminjaman WHERE id=?", (int(pilih),))["buku_id"][0])
                run("UPDATE peminjaman SET status='Dikembalikan' WHERE id=?", (int(pilih),))
                run("UPDATE buku SET stok = stok + 1 WHERE id=?", (bid,))
                st.rerun()

# ---------- ARSIP ----------
else:
    hero("Kearsipan", "Arsip Digital", "Simpan dan kelola dokumen kearsipan secara digital")
    with st.container(key="arsip_box"):
        t1, t2 = st.tabs(["➕ Tambah Arsip", "🗂️ Daftar Arsip"])
        with t1:
            with st.form("form_arsip", clear_on_submit=True):
                x, y = st.columns(2)
                nama = x.text_input("Nama Dokumen")
                jenis = y.selectbox("Jenis", ["Surat", "Laporan", "Peta", "Notulen", "Foto", "Lainnya"])
                tahun = x.number_input("Tahun", 1900, 2100, date.today().year)
                status = y.selectbox("Status", ["Aktif", "Statis", "Inaktif"])
                berkas = st.file_uploader("Unggah dokumen", type=["pdf", "jpg", "png", "docx"])
                if st.form_submit_button("Simpan Arsip"):
                    if nama.strip():
                        path = ""
                        if berkas:
                            path = os.path.join("uploads", os.path.basename(berkas.name))
                            with open(path, "wb") as f:
                                f.write(berkas.getbuffer())
                        run("INSERT INTO arsip(nama,jenis,tahun,status,file) VALUES(?,?,?,?,?)", (nama, jenis, int(tahun), status, path))
                        st.success("Arsip tersimpan di database.")
                        st.rerun()
                    else:
                        st.warning("Nama dokumen wajib diisi.")
        with t2:
            arsip = read("SELECT nama AS 'Nama Dokumen', jenis AS Jenis, tahun AS Tahun, status AS Status, file AS Berkas FROM arsip ORDER BY id DESC")
            pilihan = st.multiselect("Filter jenis arsip", sorted(arsip["Jenis"].unique()), default=sorted(arsip["Jenis"].unique()))
            st.markdown(table(arsip[arsip["Jenis"].isin(pilihan)]), unsafe_allow_html=True)

footer()
