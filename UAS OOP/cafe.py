from fpdf import FPDF
from datetime import datetime
from base import Menu   # Mengambil Parent Class dari base.py
import os
import uuid

# ==========================
# INHERITANCE + POLYMORPHISM
# ==========================
class Makanan(Menu):
    def tampil_menu(self):
        return "Makanan"

class Minuman(Menu):
    def tampil_menu(self):
        return "Minuman"


# ==========================
# ENCAPSULATION & OOP
# ==========================
class Pelanggan:
    def __init__(self, nama):
        self.__nama = nama        # Private Attribute
        self.__pesanan = []       # Private Attribute

    # Getter untuk Nama
    def get_nama(self):
        return self.__nama

    # Setter untuk Nama
    def set_nama(self, nama_baru):
        self.__nama = nama_baru

    # Method Menambahkan Pesanan
    def tambah_pesanan(self, menu):
        self.__pesanan.append(menu)

    # Getter untuk Pesanan
    def get_pesanan(self):
        return self.__pesanan

    # =========================================================
    # CETAK NOTA PDF - VERSI MODERN (STRUK KASIR KAFE KEKINIAN)
    # =========================================================
    def cetak_nota_pdf(self, user_id=None):
        
        # 1. Inisialisasi dokumen dengan ukuran struk kasir (lebar 120mm, tinggi dinamis)
        pdf = FPDF(orientation='P', unit='mm', format=(120, 200))
        pdf.add_page()
        
        # Set margin agar pas di tengah
        pdf.set_margins(left=10, top=10, right=10)
        
        # Gunakan font Courier (Monospace) agar jarak spasi antar teks konsisten seperti mesin kasir
        pdf.set_font("Courier", style="", size=11)
        
        # 2. HEADER NOTA (Nama Kafe & Alamat)
        pdf.set_font("Courier", style="B", size=16)
        pdf.cell(100, 6, "KAFE OOP", ln=1, align="C")
        
        pdf.set_font("Courier", style="", size=11)
        pdf.cell(100, 5, "Jl. Algoritma No. 404, Yogyakarta", ln=1, align="C")
        pdf.cell(100, 5, "Telp: 0812-3456-7890", ln=1, align="C")
        
        # Garis Pembatas Putus-putus
        pdf.cell(100, 5, "-" * 50, ln=1, align="C")
        
        # 3. METADATA TRANSAKSI (No Nota, Tanggal, Nama Pelanggan)
        no_nota = f"#TRX-{datetime.now().strftime('%Y%m%d%H%M')}"
        tgl_sekarang = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Baris Nota & Tanggal
        pdf.cell(50, 5, f"No. Nota:", ln=0)
        pdf.cell(50, 5, f"Tgl: {tgl_sekarang}", ln=1, align="R")
        pdf.cell(100, 5, f"{no_nota}", ln=1)
        
        # Baris Nama Pelanggan
        pdf.cell(25, 6, "Pelanggan: ", ln=0)
        pdf.set_font("Courier", style="B", size=11)
        pdf.cell(75, 6, self.get_nama(), ln=1) 
        pdf.set_font("Courier", style="", size=11)
        
        pdf.cell(100, 5, "-" * 50, ln=1, align="C")
        
        # 4. HEADER TABEL MENU
        pdf.set_font("Courier", style="B", size=11)
        pdf.cell(50, 5, "Menu", ln=0)
        pdf.cell(15, 5, "Qty", ln=0, align="C")
        pdf.cell(35, 5, "Harga", ln=1, align="R")
        pdf.cell(100, 4, "-" * 50, ln=1, align="C")
        pdf.set_font("Courier", style="", size=11)
        
        # 5. LOOPING DAFTAR PESANAN
        pesanan_raw = self.get_pesanan()
        rekap_pesanan = {}
        
        for item in pesanan_raw:
            if item.nama in rekap_pesanan:
                rekap_pesanan[item.nama]['qty'] += 1
                rekap_pesanan[item.nama]['sub'] += item.harga
            else:
                rekap_pesanan[item.nama] = {'qty': 1, 'harga_satuan': item.harga, 'sub': item.harga}
        
        subtotal = 0
        for nama_menu, data in rekap_pesanan.items():
            txt_harga = f"Rp {data['sub']:,}".replace(',', '.')
            
            pdf.cell(50, 6, nama_menu, ln=0)
            pdf.cell(15, 6, str(data['qty']), ln=0, align="C")
            pdf.cell(35, 6, txt_harga, ln=1, align="R")
            subtotal += data['sub']
            
        pdf.cell(100, 4, "-" * 50, ln=1, align="C")
        
        # 6. TOTAL & PAJAK
        pajak = int(subtotal * 0.10)
        total_akhir = subtotal + pajak
        
        txt_subtotal = f"Rp {subtotal:,}".replace(',', '.')
        txt_pajak = f"Rp {pajak:,}".replace(',', '.')
        txt_total = f"Rp {total_akhir:,}".replace(',', '.')
        
        # Subtotal
        pdf.cell(50, 5, "", ln=0)
        pdf.cell(20, 5, "Subtotal:", ln=0, align="R")
        pdf.cell(30, 5, txt_subtotal, ln=1, align="R")
        
        # Pajak (10%)
        pdf.cell(50, 5, "", ln=0)
        pdf.cell(20, 5, "Pajak(10%):", ln=0, align="R")
        pdf.cell(30, 5, txt_pajak, ln=1, align="R")
        
        # Total Akhir
        pdf.set_font("Courier", style="B", size=12)
        pdf.cell(40, 6, "", ln=0)
        pdf.cell(25, 6, "TOTAL:", ln=0, align="R")
        pdf.cell(35, 6, txt_total, ln=1, align="R")
        pdf.set_font("Courier", style="", size=11)
        
        pdf.cell(100, 5, "-" * 50, ln=1, align="C")
        
        # 7. FOOTER NOTA
        pdf.ln(2)
        pdf.set_font("Courier", style="B", size=11)
        pdf.cell(100, 5, "Terima Kasih Atas Kunjungan Anda!", ln=1, align="C")
        pdf.ln(1)
        pdf.set_font("Courier", style="", size=10)
        pdf.cell(100, 4, "Barang yang sudah dibeli tidak dapat", ln=1, align="C")
        pdf.cell(100, 4, "ditukar/dikembalikan.", ln=1, align="C")
        
        # PENAMAAN FILE DENGAN ID UNIK (Kompatibel untuk Local & Vercel /tmp)
        nama_bersih = self.get_nama().replace(' ', '_').lower()
        if user_id:
            suffix_id = user_id.split('-')[0]
            filename = f"nota_{nama_bersih}_{suffix_id}.pdf"
        else:
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"nota_{nama_bersih}_{timestamp}.pdf"
            
        # Jika dideploy ke cloud serverless yang ketat, bisa diarahkan ke /tmp/filename
        # Untuk penggunaan lokal, simpan langsung di folder project:
        pdf.output(filename)
        return filename

# ==========================
# INSTANCE DAFTAR MENU (Tema Pastelle Bakery)
# ==========================
daftar_menu = [
    # Makanan / Roti
    Makanan("Sourdough Country Loaf", 45000),
    Makanan("Almond Croissant", 35000),
    Makanan("Lavender Lemon Cake", 38000),
    Makanan("Raspberry Cheesecake", 40000),
    Makanan("Pistachio Rose Cake", 42000),
    Makanan("Pain au Chocolat", 32000),
    
    # Minuman
    Minuman("Matcha Premium Latte", 28000),
    Minuman("Lavender Earl Grey Tea", 26000),
    Minuman("Kopi Susu Gula Aren", 22000),
    Minuman("Cascara Fizz", 30000)
]
