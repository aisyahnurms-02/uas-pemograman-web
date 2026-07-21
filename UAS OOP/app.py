from flask import Flask, request, redirect, url_for, render_template, session
from cafe import Pelanggan, daftar_menu  # Mengimpor class & data dari cafe.py
from datetime import datetime
import os
import uuid
import mysql.connector

app = Flask(__name__)
app.secret_key = "kunci_rahasia_kafe_oop_modern_12345"

# ==========================================
# KONFIGURASI PENGAMAN SESI
# ==========================================
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

# Dictionary global untuk menyimpan objek Pelanggan di memori web server sementara
session_data = {}


# ==========================================
# FUNGSI KONEKSI DATABASE FILES.IO (MySQL)
# ==========================================
def get_db_connection():
    return mysql.connector.connect(
        host="mtjytz.h.filess.io",      
        user="db_pelanggan_surpriseam",              
        password="d1c5a1ff4b77367e2c3bec4a774727f339dc0e50",          
        database="db_pelanggan_surpriseam",              
        port=3307                        
    )


# ==========================================
# RUTE 1: GERBANG UTAMA (LOGIN & PILIH MENU)
# ==========================================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nama = request.form.get("nama")
        action = request.form.get("action") # Menangkap value dari tombol (order / reservasi)
        
        # Membuat ID Sesi unik untuk melacak user ini
        user_id = str(uuid.uuid4())
        session['user_id'] = user_id
        session['nama_user'] = nama # Simpan nama ke session untuk auto-fill di form reservasi
        
        # Instansiasi objek Pelanggan secara OOP dan simpan di memori
        session_data[user_id] = Pelanggan(nama)
        session.modified = True
        
        # Pisahkan alur berdasarkan tombol yang diklik di login.html
        if action == "reservasi":
            return redirect(url_for("form_reservasi"))
        else:
            return redirect(url_for("order_menu"))
            
    return render_template("login.html")


# ==========================================
# RUTE 2: FITUR RESERVASI (CRUD DATABASE ONLINE)
# ==========================================

# CREATE - FORM TAMBAH RESERVASI
@app.route("/reservasi", methods=["GET", "POST"])
def form_reservasi():
    if request.method == "POST":
        nama = request.form.get("nama_pelanggan")
        tanggal = request.form.get("tanggal_reservasi")
        meja = request.form.get("no_meja")
        jumlah = request.form.get("jumlah_orang")
        pesanan = request.form.get("pesanan")
        
        db = get_db_connection()
        cursor = db.cursor()
        
        sql = """
            INSERT INTO reservasi (nama_pelanggan, tanggal_reservasi, no_meja, jumlah_orang, pesanan) 
            VALUES (%s, %s, %s, %s, %s)
        """
        val = (nama, tanggal, meja, jumlah, pesanan)
        
        cursor.execute(sql, val)
        db.commit()
        
        cursor.close()
        db.close()
        
        # Setelah sukses menyimpan, arahkan ke daftar reservasi
        return redirect(url_for("daftar_reservasi"))
        
    # Ambil nama default dari session login (jika ada)
    nama_default = session.get('nama_user', '')
    return render_template("reservasi.html", nama_default=nama_default)


# READ - HALAMAN TAMPIL DAFTAR RESERVASI
@app.route("/daftar_reservasi")
def daftar_reservasi():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True) 
    
    # Menampilkan data urut dari jadwal terdekat ke terjauh
    cursor.execute("SELECT * FROM reservasi ORDER BY tanggal_reservasi ASC")
    data_reservasi = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return render_template("daftar_reservasi.html", reservasi=data_reservasi)


# UPDATE - HALAMAN EDIT DATA RESERVASI
@app.route("/edit_reservasi/<int:id>", methods=["GET", "POST"])
def edit_reservasi(id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    if request.method == "POST":
        nama = request.form.get("nama_pelanggan")
        tanggal = request.form.get("tanggal_reservasi")
        meja = request.form.get("no_meja")
        jumlah = request.form.get("jumlah_orang")
        pesanan = request.form.get("pesanan")
        
        sql = """UPDATE reservasi 
                 SET nama_pelanggan=%s, tanggal_reservasi=%s, no_meja=%s, jumlah_orang=%s, pesanan=%s 
                 WHERE id=%s"""
        val = (nama, tanggal, meja, jumlah, pesanan, id)
        
        cursor.execute(sql, val)
        db.commit()
        
        cursor.close()
        db.close()
        
        return redirect(url_for('daftar_reservasi'))
        
    cursor.execute("SELECT * FROM reservasi WHERE id=%s", (id,))
    data = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    return render_template("edit_reservasi.html", data=data)


# DELETE - FUNGSI HAPUS RESERVASI
@app.route("/hapus_reservasi/<int:id>")
def hapus_reservasi(id):
    db = get_db_connection()
    cursor = db.cursor()
    
    cursor.execute("DELETE FROM reservasi WHERE id=%s", (id,))
    db.commit()
    
    cursor.close()
    db.close()
    
    return redirect(url_for('daftar_reservasi'))


# ==========================================
# RUTE 3: FITUR PESANAN LANGSUNG (MEMORI OOP)
# ==========================================

@app.route("/order")
def order_menu():
    user_id = session.get('user_id')
    if not user_id:
        print("[DEBUG ERROR] Cookie user_id tidak ditemukan di browser pelanggan!")
        return redirect(url_for("index"))
        
    if user_id not in session_data:
        print("[DEBUG ERROR] ID Sesi ada, tetapi objek Pelanggan hilang dari memori server!")
        return redirect(url_for("index"))
        
    pelanggan = session_data[user_id]
    return render_template("menu.html", pelanggan=pelanggan, daftar_menu=daftar_menu)


@app.route("/add/<int:menu_id>")
def add_menu(menu_id):
    user_id = session.get('user_id')
    if user_id and user_id in session_data:
        pelanggan = session_data[user_id]
        if 0 <= menu_id < len(daftar_menu):
            pelanggan.tambah_pesanan(daftar_menu[menu_id])
            session.modified = True
    return redirect(url_for("order_menu"))


@app.route("/checkout")
def checkout():
    user_id = session.get('user_id')
    if user_id and user_id in session_data:
        pelanggan = session_data[user_id]
        pesanan_raw = pelanggan.get_pesanan()
        
        if not pesanan_raw:
            return redirect(url_for("order_menu"))
            
        # Rekap pesanan untuk nota online
        rekap_pesanan = {}
        for item in pesanan_raw:
            if item.nama in rekap_pesanan:
                rekap_pesanan[item.nama]['qty'] += 1
                rekap_pesanan[item.nama]['sub'] += item.harga
            else:
                rekap_pesanan[item.nama] = {'qty': 1, 'harga_satuan': item.harga, 'sub': item.harga}
        
        subtotal = sum(data['sub'] for data in rekap_pesanan.values())
        pajak = int(subtotal * 0.10)
        total_akhir = subtotal + pajak
        
        no_nota = f"#TRX-{datetime.now().strftime('%Y%m%d%H%M')}"
        tgl_sekarang = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        return render_template(
            "nota_online.html", 
            pelanggan=pelanggan, 
            rekap_pesanan=rekap_pesanan,
            subtotal=subtotal,
            pajak=pajak,
            total_akhir=total_akhir,
            no_nota=no_nota,
            tgl=tgl_sekarang
        )
            
    return redirect(url_for("order_menu"))


@app.route("/reset")
def reset():
    user_id = session.get('user_id')
    if user_id in session_data:
        del session_data[user_id] # Bersihkan memori objek OOP
    session.clear()
    return redirect(url_for("index"))


# ==========================================
# JALANKAN SERVER APLIKASI
# ==========================================
if __name__ == "__main__":
    print("\n[!] Server Flask Berhasil Aktif.")
    print("[!] Silakan buka browser ke: http://127.0.0.1:5000\n")
    app.run(debug=True, use_reloader=False)
