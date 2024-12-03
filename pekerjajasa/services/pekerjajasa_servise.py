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
    sub.nama_subkategori as nama_subkategori
    """

    @staticmethod
    def get_tr_pemesanan_jasa_by_pekerja(pekerja_id : str) -> dict:
        '''Gets pemesanan jasa by id pekerja'''
        sql = f"""
        SELECT
            {PekerjaJasaService.TR_PEMESANAN_JASA_FIELDS}
        FROM sijarta.tr_pemesanan_jasa pj 
            JOIN sijarta.tr_pemesanan_status ps ON(pj.id = ps.id_tr_pemesanan)
            JOIN sijarta.status_pesanan s ON(ps.id_status = s.id)
            JOIN sijarta.user u ON(pj.id_pelanggan = u.id)
            JOIN sijarta.subkategori_jasa sub ON(pj.id_kategori_jasa = sub.id)
        WHERE pj.id_pekerja = %s;
        """

        result = fetch_dict_all(sql,[pekerja_id])
        if not result:
            return None
        return result