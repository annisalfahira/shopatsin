# ShopAtSin

**Tugas Pemrograman Berbasis Platform - PBP F**

> **ShopAtSin** merupakan proyek Django sederhana berbentuk e-commerce football shop berbasis website untuk memenuhi Tugas Individu mata kuliah PBP Gasal 2025/2026

[ ⚽️ Kunjungi Website ShopAtSin at (link) ]

## **Penjelasan Tugas**

<details>
<summary> <b> Tugas 2: Implementasi Model-View-Template (MVT) pada Django </b> </summary>

## **Implementasi Checklist**

* ### Inisiasi Proyek Django

Setelah saya membuat direktori baru dengan nama ShopAtSin, nama toko saya, saya membuat dependencies pada berkas 'requirements.txt' yang berisi

```
django
gunicorn
whitenoise
psycopg2-binary
requests
urllib3
```

Lalu melakukan instalasi dependencies setelah menjalankan virtual environment dengan perintah `pip install -r requirements.txt` dan membuat proyek Django dengan perintah `django-admin startproject shopatsin .`

* ### Menjalankan Server

Setelah membuat proyek Django, saya menambahkan string `ALLOWED_HOSTS = ["localhost", "127.0.0.1"]` untuk keperluan deployment dan menjalankan server Django dengan perintah `python3 manage.py runserver`

* ### Membuat  aplikasi `main`

Saya menjalankan perintah `python manage.py startapp main` untuk membuat aplikasi baru bernama main. Lalu saya menambahkan `main` ke `INSTALLED_APPS` pada berkas `settings.py` 


* ### Membuat model aplikasi `main`

Saya membuat berkas `models.py` pada direktori `main` yang berisikan

```
from django.db import models

class ItemInShopAtSin(models.Model):
    name = models.CharField(max_length=255) 
    price = models.IntegerField()  
    description = models.TextField()  
    thumbnail = models.URLField()  
    is_featured = models.BooleanField(default=False)  

    stock = models.IntegerField(default=0)  
    brand = models.CharField(max_length=100, blank=True, null=True)  
    rating = models.FloatField(default=0.0)  
    date_added = models.DateField(auto_now_add=True) 

    def __str__(self):
        return f"{self.name} - {self.category}"
```

Lalu saya mengimigrasikan model yang sudah saya buat dengan menjalankan perintah `python3 manage.py makemigrations` dan mengimigrasikannya ke basis data lokal dengan menjalankan perintah `python manage.py migrate`

* ### Membuat template dan view aplikasi `main`

Template untuk merender pada file `views.py` berisikan

```
from django.shortcuts import render

def show_main(request):
    context = {
        "app_name": "ShopAtSin",              
        "student_name": "Annisa Muthia Alfahira",  
        "student_class": "F"   
    }
    return render(request, "main.html", context)

```

dan template pada file `html.main` berisi 

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ app_name }}</title>
</head>
<body>
    <h1>Welcome to {{ app_name }} 👋</h1>
    <p>Nama: {{ student_name }}</p>
    <p>Kelas: {{ student_class }}</p>
</body>
</html>

```

* ### Melakukan routing pada aplikasi `main`

Untuk mengatur URL pada aplikasi `main`, saya membuat berkas `urls.py` pada aplikasi `main` berisikan

```
from django.urls import path
from .views import show_main

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
]
```

Dengan begitu, saya dapat melihat `main` dengan perintah `python manage.py runserver`

## **Jawaban Tugas 2**

* ### Bagan request client ke web aplikasi berbasis Django

![bagan request client ke web](images/baganTugas2.JPG)

Client (Browser/User) mengirimkan request HTTP ke server, kemudian memprosesnya dengan melakukan pemetaan URL melalui `urls.py`. Setelah URL ditemukan dan dipetakan, fungsi yang sesuai dalam `views.py` dijalankan berdasarkan permintaan URL tersebut. Selanjutnya, fungsi view mengembalikan HTTP response dalam bentuk halaman HTML. Dalam proses ini, `views.py` mengambil data yang dibutuhkan dari `models.py`, lalu data tersebut disajikan menggunakan template main.html.


* ### Jelaskan peran `settings.py` dalam project Django!

File `settings.py` dalam proyek Django berfungsi sebagai pusat konfigurasi yang mengatur bagaimana aplikasi berjalan. Semua pengaturan inti, mulai dari aplikasi apa saja yang digunakan, koneksi ke database, hingga lokasi template HTML dan file statis seperti CSS atau JavaScript, didefinisikan di dalamnya. Selain itu, `settings.py` juga memuat pengaturan keamanan, misalnya `SECRET_KEY` untuk enkripsi, `DEBUG` untuk menentukan mode pengembangan atau produksi, serta `ALLOWED_HOSTS` yang menentukan domain mana saja yang diperbolehkan mengakses aplikasi. Tidak hanya itu, file ini juga mengatur bahasa, zona waktu, serta berbagai middleware yang akan memproses request dan response. Dengan kata lain, `settings.py` adalah jantung dari proyek Django, karena tanpa file ini server tidak akan tahu bagaimana cara menjalankan dan mengatur seluruh komponen aplikasi.

* ### Bagaimana cara kerja migrasi database di Django?

Migrasi database di Django adalah proses untuk menerjemahkan perubahan yang dibuat pada model Python menjadi perubahan pada struktur tabel di database. Saat seorang pengembang menambahkan, mengubah, atau menghapus atribut pada sebuah model di `models.py`, Django tidak langsung mengubah database, melainkan menyimpan perubahan itu sebagai berkas migrasi dengan perintah `python manage.py makemigrations`. Berkas migrasi ini berisi instruksi yang mendeskripsikan apa saja perubahan yang perlu dilakukan pada database. Setelah itu, perintah `python manage.py migrate` dijalankan untuk mengeksekusi instruksi tersebut sehingga database diperbarui sesuai dengan definisi model terbaru. Dengan sistem migrasi ini, pengembang dapat melacak riwayat perubahan database, berpindah antar versi struktur tabel, serta menjaga konsistensi antara kode program dengan basis data yang digunakan.

* ### Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?

Django sering dijadikan permulaan dalam pembelajaran pengembangan perangkat lunak karena sifatnya yang lengkap, terstruktur, dan begineer friendly. Framework ini menganut prinsip “batteries included”, artinya banyak fitur penting seperti autentikasi pengguna, manajemen database, sistem template, hingga pengaturan keamanan sudah tersedia secara bawaan tanpa harus menambahkan modul tambahan. Hal ini membuat mahasiswa atau pengembang pemula bisa lebih fokus memahami konsep dasar pengembangan aplikasi web daripada pusing pada detail teknis kecil. Selain itu, Django menggunakan bahasa Python yang dikenal dengan sintaks yang sederhana dan mudah dibaca, sehingga membantu pemula untuk cepat memahami logika program. Struktur proyek Django yang rapi juga memperkenalkan mahasiswa pada praktik best practice dalam pengembangan perangkat lunak, seperti pemisahan model, view, dan template. Dengan kombinasi kemudahan penggunaan dan kelengkapan fitur, Django menjadi pilihan yang ideal sebagai titik awal sebelum mempelajari framework lain yang mungkin lebih kompleks.

* ### Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?

Tidak ada, all good!!

</details>