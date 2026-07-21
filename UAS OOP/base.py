from abc import ABC, abstractmethod

# ==========================
# BASE CLASS
# ==========================
class Menu:
    def __init__(self, nama, harga):
        self.nama = nama
        self.harga = harga
        
    def tampil_menu(self):
        # Method ini akan di-override oleh class anak (Polymorphism)
        pass