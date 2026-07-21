from base import Menu   # Mengambil Parent Class dari base.py

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
