from django.http import JsonResponse
from django.shortcuts import redirect, render
from mypay.services.mypay_service import MyPayService
from mypay.forms import TopUpForm
from users.services.user_service import UserService


def mypay_view(request):
    uid = str(request.user['id'])
    tr_history = MyPayService.get_tr_mypay_from_user_id(uid)
    
    context = {
        "user": request.user,
        "riwayat" : tr_history
               }
    return render(request, "show_mypay.html", context)


def transaksi_mypay(request):
    uid = str(request.user['id'])
    pesanan = MyPayService.get_menunggu_pembayaran_pemesanan_by_user(uid)

    context = {
        "user": request.user,
        "pesanan" : pesanan
        }
    return render(request, "transaksi_mypay.html", context)

def topup(request) :
    if request.method == "POST":
        nominal = request.POST.get('nominal')
        uid = str(request.user['id'])
        
        try:
            nominal = int(nominal)
            if nominal <= 0:
                return JsonResponse({"message": "Nominal must be a positive number!"}, status=400)
        except ValueError:
            return JsonResponse({"message": "Invalid nominal format!"}, status=400)
        
        try :
            MyPayService.topup(uid, nominal)
        except Exception as e:
            return JsonResponse(
                {"message": "Failed to process the top-up", "error": str(e)}, status=500
            )
        
        return redirect('/mypay/transaksi')
    
    return JsonResponse({"message": "Invalid request method"}, status=405)
    
def withdrawal(request) :
    if request.method == "POST":
        nominal = request.POST.get('nominal')
        uid = str(request.user['id'])

        try:
            nominal = int(nominal)
            if nominal <= 0:
                return JsonResponse({"message": "Nominal harus bilangan positif"}, status=400)
        except ValueError:
            return JsonResponse({"message": "Nominal tidak valid"}, status=400)
        
        if int(request.user['mypay_balance']) < nominal :
            return JsonResponse({"message": "Saldo kurang"}, status=400)
            
        try :
            MyPayService.withdrawal(uid, nominal)
        except Exception as e:
            return JsonResponse(
                {"message": "Failed ", "error": str(e)}, status=500
            )

        return redirect('/mypay/transaksi')
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

def transfer(request) :
    if request.method == "POST" :
        nominal = request.POST.get('nominal')
        no_hp_penerima = request.POST.get('no_hp')
        uid = str(request.user['id'])

        if not UserService.get_user_by_phone_number(no_hp_penerima) :
            return JsonResponse({"message": "No hp penerima not found"}, status=400)

        try:
            nominal = int(nominal)
            if nominal <= 0:
                return JsonResponse({"message": "Nominal must be a positive number!"}, status=400)
        except ValueError:
            return JsonResponse({"message": "Invalid nominal format!"}, status=400)

        if no_hp_penerima == request.user['phone_number'] :
            return JsonResponse({"message": "Tidak bisa transfer ke diri sendiri!"}, status=400)

        if int(request.user['mypay_balance']) < nominal :
            return JsonResponse({"message": "Saldo kurang"}, status=400)
        
        try :
            MyPayService.transfer_mypay(uid, no_hp_penerima, nominal)
        except Exception as e:
            return JsonResponse(
                {"message": "Failed to process the transfer ", "error": str(e)}, status=500
            )

        return redirect('/mypay/transaksi')

    return JsonResponse({"message": "Invalid request method"}, status=405)

def bayar_jasa(request) :
    if request.method == "POST" :
        id_pesanan = request.POST.get('id_pesanan')
        uid = str(request.user['id'])
        harga_pesanan = int(request.POST.get('harga_pesanan'))

        if int(request.user['mypay_balance']) < harga_pesanan :
            return JsonResponse({"message": "Saldo kurang"}, status=400)
        
        try:
            MyPayService.bayar(id_pesanan, uid, harga_pesanan)
        except Exception as e:
            return JsonResponse(
                {"message": "Failed to process the payment", "error": str(e)}, status=500
            )
        
        return redirect('/mypay/transaksi')

    return JsonResponse({"message": "Invalid request method"}, status=405)