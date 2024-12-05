from django.shortcuts import render, redirect
from django.http import HttpResponse
from diskon.services.diskon_service import DiscountService
from django.db import IntegrityError
from django.http import JsonResponse
import uuid


# Create your views here.


def show_diskon(request):
    voucher = DiscountService.get_all_vouchers()
    promo = DiscountService.get_all_promo()
    metode_bayar = DiscountService.get_all_metode_bayar()
    context = {
        "user": request.user,
        "voucher" : voucher,
        "promo": promo,
        "metode_bayar": metode_bayar,
    }
    return render(request, "show_diskon.html", context)


def beli_voucher(request):
    promo = DiscountService.get_all_promo()
    if request.method == "POST":
        # Ambil data dari form yang dikirim
        kode_voucher = request.POST.get('kode_voucher')
        harga_voucher = float(request.POST.get('harga_voucher'))
        metode_pembayaran_id = request.POST.get('metode_pembayaran')
        user_id = str(request.user["id"])  # Ambil ID pengguna yang sedang login
        metode_pembayaran_nama = DiscountService.get_metode_bayar(metode_pembayaran_id)
        if metode_pembayaran_nama == "MyPay":
            # Cek saldo MyPay pengguna
            saldo = DiscountService.check_saldo_mypay(user_id)
            # Cek apakah saldo mencukupi untuk pembelian
            if saldo < harga_voucher:
                # Jika saldo tidak mencukupi, tampilkan modal gagal
                return render(request, 'show_diskon.html', {
                    'status_modal': 'gagal',
                    'message': 'Saldo MyPay Anda tidak mencukupi untuk melakukan pembelian.',
                    'voucher': DiscountService.get_all_vouchers(),
                    "promo": promo,
                    'metode_bayar': DiscountService.get_all_metode_bayar(),
                })

            # Cek apakah voucher valid (kuota dan masa berlaku)
            is_valid = DiscountService.check_voucher_validity(kode_voucher)
            if not is_valid:
                # Jika voucher tidak valid, tampilkan modal gagal
                return render(request, 'show_diskon.html', {
                    'status_modal': 'gagal',
                    'message': 'Voucher tidak valid atau sudah habis kuotanya.',
                    'voucher': DiscountService.get_all_vouchers(),
                    "promo": promo,
                    'metode_bayar': DiscountService.get_all_metode_bayar(),
                })

            # Update saldo MyPay pengguna
            DiscountService.update_saldo_mypay(harga_voucher, user_id)
            # Record pembelian voucher
            # Misalkan ID transaksi voucher dibuat secara otomatis
            # Simulasi ID transaksi, misalnya ID baru dari DB
            id_transaksi_voucher = uuid.uuid4()  # Ganti dengan mekanisme ID transaksi yang sesuai di aplikasi Anda
            id_transaksi_mypay = uuid.uuid4()  # Ganti dengan mekanisme ID transaksi yang sesuai di aplikasi Anda
            DiscountService.record_voucher_purchase(id_transaksi_voucher, 0, user_id, kode_voucher, metode_pembayaran_id)
            DiscountService.record_mypay_purchase(id_transaksi_mypay, user_id, harga_voucher, DiscountService.get_id_category_voucher("Pembelian Voucher"))
            return render(request, 'show_diskon.html', {
                'status_modal': 'sukses',
                'message': f'Pembelian voucher {kode_voucher} berhasil!',
                'voucher': DiscountService.get_all_vouchers(),
                'metode_bayar': DiscountService.get_all_metode_bayar(),
                "promo": promo,
            })
        else:
            id_transaksi_voucher = uuid.uuid4()  # Ganti dengan mekanisme ID transaksi yang sesuai di aplikasi Anda
            DiscountService.record_voucher_purchase(id_transaksi_voucher, 0, user_id, kode_voucher, metode_pembayaran_id)
            return render(request, 'show_diskon.html', {
                'status_modal': 'sukses',
                'message': f'Pembelian voucher {kode_voucher} berhasil!',
                'voucher': DiscountService.get_all_vouchers(),
                'metode_bayar': DiscountService.get_all_metode_bayar(),
                "promo": promo,
            })





