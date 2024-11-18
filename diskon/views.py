from django.shortcuts import render

# Create your views here.

def show_diskon(request):
    context = {
        "user": {
            "is_authenticated": True,
            "name": "John Doe",
            "is_pengguna": True,
            "email": "johndoe@mail.com",
            "phone": "123-456-7890",
            "address": "1234 Elm St",
        },
        "Voucher": [
            {
                "Kode": "ABC123",
                "Potongan": "10%",
                "Min_Transaksi_Pemesanan": 100000,
                "Jumlah_Hari_Berlaku": 30,
                "Kuota_Penggunaan": 100,
                "Harga": 50000,
            },
            {
                "Kode": "DEF456",
                "Potongan": "20%",
                "Min_Transaksi_Pemesanan": 200.000,
                "Jumlah_Hari_Berlaku": 60,
                "Kuota_Penggunaan": 50,
                "Harga": 75000,
            },
            {
                "Kode": "GHI789",
                "Potongan": "15%",
                "Min_Transaksi_Pemesanan": 150000,
                "Jumlah_Hari_Berlaku": 45,
                "Kuota_Penggunaan": 80,
                "Harga": 60000,
            }
        ],

        "Promo": [
            {
                "Kode": "PROMO123",
                "Tanggal_Akhir_Berlaku": "2024-12-31"
            },
            {
                "Kode": "PROMO456",
                "Tanggal_Akhir_Berlaku": "2024-11-30"
            },
            {
                "Kode": "PROMO789",
                "Tanggal_Akhir_Berlaku": "2025-01-15"
            }
        ]
    }
    return render(request, "show_diskon.html", context)
