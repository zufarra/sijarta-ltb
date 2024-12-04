from datetime import datetime
import uuid
from db.utils.query_helpers import execute_query, fetch_dict_all, fetch_dict_one

class PekerjaJasaService:
    TR_PEMESANAN_JASA_FIELDS = """
    pj.id as id,
    pj.tgl_pemesanan as tanggal_pemesanan,
    pj.tgl_pekerjaan as tanggal_pekerjaan,
    pj.waktu_pekerjaan as waktu_pekerjaan,
    pj.total_biaya as total_biaya,
    pj.id_pelanggan as id_pelanggan,
    pj.id_pekerja as id_pekerja,
    pj.id_kategori_jasa as id_kategori_jasa,
    pj.sesi as sesi,
    pj.id_diskon as id_diskon,
    pj.id_metode_bayar as metode_bayar,
    u.nama as nama_pelanggan,
    s.status as status,
    ps.id_status as id_status,
    sub.nama_subkategori as nama_subkategori
    """

    @staticmethod
    def get_tr_pemesanan_jasa_by_pekerja(pekerja_id : str, match = None, status = None) -> dict:
        where_clause =  f"pj.id_pekerja = %s"
        param = [pekerja_id]

        if match :
            match += "%"
            where_clause +=  f" AND sub.nama_subkategori LIKE %s"
            param.append(match)
        
        if status :
            where_clause += f" AND s.id = %s"
            param.append(status)
        
        '''Gets pemesanan jasa by id pekerja'''
        sql = f"""
        SELECT
            {PekerjaJasaService.TR_PEMESANAN_JASA_FIELDS}
        FROM sijarta.tr_pemesanan_jasa pj 
            JOIN sijarta.tr_pemesanan_status ps ON(pj.id = ps.id_tr_pemesanan)
            JOIN sijarta.status_pesanan s ON(ps.id_status = s.id)
            JOIN sijarta.user u ON(pj.id_pelanggan = u.id)
            JOIN sijarta.subkategori_jasa sub ON(pj.id_kategori_jasa = sub.id)
        WHERE {where_clause} ORDER BY s.id;
        """


        result = fetch_dict_all(sql,param)
        if not result:
            return None
        return result
    
    @staticmethod
    def get_tr_pemesanan_jasa_by_id(id : str) -> dict:
        '''Gets pemesanan jasa by id'''
        sql = f"""
        SELECT
            {PekerjaJasaService.TR_PEMESANAN_JASA_FIELDS}
        FROM sijarta.tr_pemesanan_jasa pj 
            JOIN sijarta.tr_pemesanan_status ps ON(pj.id = ps.id_tr_pemesanan)
            JOIN sijarta.status_pesanan s ON(ps.id_status = s.id)
            JOIN sijarta.user u ON(pj.id_pelanggan = u.id)
            JOIN sijarta.subkategori_jasa sub ON(pj.id_kategori_jasa = sub.id)
        WHERE pj.id = %s;
        """

        result = fetch_dict_one(sql,[id])
        if not result:
            return None
        return result
    
    @staticmethod
    def update_status(id_transaksi : str) :
        transaksi = PekerjaJasaService.get_tr_pemesanan_jasa_by_id(id_transaksi)
        next_status = PekerjaJasaService.status_cycle(transaksi["id_status"])
        time_stamp = datetime.now()
        
        sql = f"""
            UPDATE sijarta.tr_pemesanan_status
            SET id_status = %s,
                tgl_waktu = %s
            WHERE id_tr_pemesanan = %s;
            """
        
        execute_query(
            sql,[next_status, time_stamp, id_transaksi]
        )


    @staticmethod
    def status_cycle(id_status : str) :
        mencari_pekerja_terdekat = str(PekerjaJasaService.get_id_by_status("Mencari Pekerja Terdekat"))
        pekerja_dalam_perjalanan = str(PekerjaJasaService.get_id_by_status("Pekerja Dalam Perjalanan"))
        pekerjaan_dimulai = str(PekerjaJasaService.get_id_by_status("Pekerjaan Dimulai"))
        pekerjaan_selesai = str(PekerjaJasaService.get_id_by_status("Pekerjaan Selesai"))

        if str(id_status) == mencari_pekerja_terdekat :
            return pekerja_dalam_perjalanan
        
        if str(id_status) == pekerja_dalam_perjalanan :
            return pekerjaan_dimulai
        
        if str(id_status) == pekerjaan_dimulai :
            return pekerjaan_selesai
        
        return None
    
    @staticmethod
    def get_id_by_status(nama : str) -> str :
        """Fetches the order status ID based on the given status name from the database."""
        sql = f"""
        SELECT id FROM sijarta.status_pesanan
        WHERE status LIKE %s;
        """

        result = fetch_dict_one(sql, [nama])
        return str(result['id'])
    

    @staticmethod
    def get_statuses_for_pekerja() -> dict :
        """Fetches all statuses"""
        sql = f"""
        SELECT * FROM sijarta.status_pesanan
        WHERE status NOT IN ('Menunggu Pembayaran','Mencari Pekerja Terdekat','Dibatalkan');
        """

        result = fetch_dict_all(sql)
        return result