from uuid import UUID
from django.http import JsonResponse
from django.shortcuts import render
from services_and_booking.services.category_service import CategoryAndSubcategoryService

# Create your views here.
def show_homepage(request):
    categories = CategoryAndSubcategoryService.get_all_categories()

    # Daftar kategori dan subkategori 
    category_subcategory_pairs = []
    for category in categories:
        subcategories = CategoryAndSubcategoryService.get_subcategories_by_category(category['id'])
        category_subcategory_pairs.append({
            'category': category,
            'subcategories': subcategories
        })
    
    search_results = []
    message = ''  
    category_id_filter = request.POST.get('category_filter')
    subcategory_name = request.POST.get('search_subcategory', '').lower()

    if request.method == 'POST':
        # kosongan gaada filter
        if not category_id_filter and not subcategory_name:
            category_subcategory_pairs = [{
                'category': category,
                'subcategories': CategoryAndSubcategoryService.get_subcategories_by_category(category['id'])
            } for category in categories]
            message = ''

        else:
            # Filter berdasarkan kategori jika ada
            if category_id_filter and category_id_filter != "Pilih Kategori...":
                try:
                    category_id_filter = UUID(category_id_filter)
                    category_subcategory_pairs = [{
                        'category': next(cat for cat in categories if cat['id'] == category_id_filter),
                        'subcategories': CategoryAndSubcategoryService.get_subcategories_by_category(category_id_filter)
                    }]
                except ValueError:
                    message = "ID kategori yang dimasukkan tidak valid."
                    category_subcategory_pairs = []

            # filter cuman kategori
            if subcategory_name:
                search_results = []
                for pair in category_subcategory_pairs:
                    filtered_subcategories = [
                        subcategory for subcategory in pair['subcategories'] 
                        if subcategory_name in subcategory['nama_subkategori'].lower()
                    ]
                    if filtered_subcategories:
                        search_results.append({
                            'category': pair['category'],
                            'subcategories': filtered_subcategories
                        })

                # Kalo gaada subkategori yang cocok
                if not search_results:
                    message = "Subkategori yang Anda cari tidak ditemukan."

            # Kalo kategori dan subkategori dicari bersama
            if category_id_filter and subcategory_name:
                search_results = []
                for pair in category_subcategory_pairs:
                    # Filter berdasarkan kategori
                    if pair['category']['id'] == category_id_filter:
                        filtered_subcategories = [
                            subcategory for subcategory in pair['subcategories']
                            if subcategory_name in subcategory['nama_subkategori'].lower()
                        ]
                        # kalo ada subkategori yang cocok
                        if filtered_subcategories:
                            search_results.append({
                                'category': pair['category'],
                                'subcategories': filtered_subcategories
                            })

                if not search_results:
                    message = "Tidak ada hasil yang cocok dengan pencarian Anda."

            # kategori ga di filter, tapi subnya iya
            if not category_id_filter or category_id_filter == "Pilih Kategori...":
                search_results = []
                for pair in category_subcategory_pairs:
                    filtered_subcategories = [
                        subcategory for subcategory in pair['subcategories']
                        if subcategory_name in subcategory['nama_subkategori'].lower()
                    ]
                    if filtered_subcategories:
                        search_results.append({
                            'category': pair['category'],
                            'subcategories': filtered_subcategories
                        })

                if not search_results:
                    message = "Subkategori yang Anda cari tidak ditemukan."

    context = {
        "user": request.user,
        "categories": categories,
        "category_subcategory_pairs": category_subcategory_pairs,
        "search_results": search_results,
        "message": message,
        "category_id_filter": category_id_filter, 
        "subcategory_name": subcategory_name,
    }

    return render(request, "homepage.html", context)


def search_subcategory(request):
    query = request.GET.get('query', '')
    if query:
        search_results = CategoryAndSubcategoryService.search_subcategory_by_name(query)
        results = [{'nama_subkategori': subcategory['subcategory_name']} for subcategory in search_results]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

def show_subkategori(request):
    context = {
        "user": {
            "is_authenticated": True,
            "name": "John Doe",
            "is_pengguna": True,
            "email": "johndoe@mail.com",
            "phone": "123-456-7890",
            "address": "1234 Elm St",
        },
        "pekerja_list": [
            {
                "id": 1,
                "nama": "Zufar Romli",
                "rating": 9.5,
                "jumlah_pesanan": 120,
                "no_hp": "081234567890",
                "tanggal_lahir": "1990-01-01",
                "alamat": "Jakarta",
            },
            {
                "id": 2,
                "nama": "Jane Smith",
                "rating": 8.9,
                "jumlah_pesanan": 85,
                "no_hp": "082123456789",
                "tanggal_lahir": "1992-03-15",
                "alamat": "Bandung",
            },
            {
                "id": 3,
                "nama": "Michael Johnson",
                "rating": 9.2,
                "jumlah_pesanan": 98,
                "no_hp": "081223344556",
                "tanggal_lahir": "1988-06-30",
                "alamat": "Surabaya",
            },
            {
                "id": 4,
                "nama": "Emily Davis",
                "rating": 8.5,
                "jumlah_pesanan": 76,
                "no_hp": "081987654321",
                "tanggal_lahir": "1993-12-20",
                "alamat": "Yogyakarta",
            },
            {
                "id": 5,
                "nama": "Chris Lee",
                "rating": 9.8,
                "jumlah_pesanan": 150,
                "no_hp": "082234567890",
                "tanggal_lahir": "1985-07-12",
                "alamat": "Semarang",
            },
            {
                "id": 6,
                "nama": "Jessica Wilson",
                "rating": 8.7,
                "jumlah_pesanan": 88,
                "no_hp": "081345678912",
                "tanggal_lahir": "1994-09-05",
                "alamat": "Denpasar",
            },
            {
                "id": 7,
                "nama": "David Brown",
                "rating": 9.1,
                "jumlah_pesanan": 105,
                "no_hp": "081223344567",
                "tanggal_lahir": "1989-04-18",
                "alamat": "Medan",
            },
            {
                "id": 8,
                "nama": "Sophia Martinez",
                "rating": 9.4,
                "jumlah_pesanan": 115,
                "no_hp": "082123456890",
                "tanggal_lahir": "1991-11-11",
                "alamat": "Makassar",
            },
        ],
    }

    return render(request, "subkategori.html", context)


def show_booking_view(request):
    context = {
        "user": request.user,
        "pesanan_list": [
            {
                "id": 1,
                "subkategori": "Reparasi Televisi",
                "sesi_layanan": "Perbaikan Layar Retak",
                "harga": "Rp 150.000",
                "nama_pekerja": "Jane Smith",
                "status": "Menunggu Pembayaran",
            },
            {
                "id": 2,
                "subkategori": "Reparasi Kulkas",
                "sesi_layanan": "Ganti Komponen Internal",
                "harga": "Rp 250.000",
                "nama_pekerja": "Sophia Martinez",
                "status": "Mencari Pekerja Terdekat",
            },
            {
                "id": 3,
                "subkategori": "Pengiriman Barang",
                "sesi_layanan": "Pindahan Rumah",
                "harga": "Rp 200.000",
                "nama_pekerja": "Zufar Romli",
                "status": "Pesanan Selesai",
            },
            {
                "id": 4,
                "subkategori": "Reparasi Televisi",
                "sesi_layanan": "Perbaikan Layar Retak",
                "harga": "Rp 150.000",
                "nama_pekerja": "Jane Smith",
                "status": "Sedang Diproses",
            },
        ],
    }

    return render(request, "booking_view.html", context)
