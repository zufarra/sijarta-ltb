from db.utils.query_helpers import execute_query, fetch_dict_all, fetch_dict_one

class TestimoniService:
    @staticmethod
    def get_all_testimoni(id_pemesanan_jasa):
        sql = """
        SELECT * 
        FROM sijarta.testimoni T, sijarta,tr_pemesanan_jasa TR
        WHERE TR.id = %s;
        """
        return fetch_dict_all(sql, [id_pemesanan_jasa])
    
    @staticmethod
    def check_valid_for_testimoni(id_tr_pemesanan):
        sql = """
        SELECT s.status 
        FROM sijarta.tr_pemesanan_jasa trj
        JOIN sijarta.tr_pemesanan_status trs ON trs.id_tr_pemesanan = trj.id
        JOIN sijarta.status_pesanan s ON trs.id_status = s.id
        WHERE trj.id = %s AND s.status = 'Pesanan Selesai'
        """
        result = fetch_dict_one(sql, [id_tr_pemesanan])
        return result['status'] if result else None
    
    @staticmethod
    def create_testimoni(id_tr_pemesanan, teks, rating):
        insert_testimoni_sql = """
        INSERT INTO sijarta.testimoni (id_tr_pemesanan, tgl, teks, rating)
        VALUES (%s, CURRENT_DATE, %s, %s);
        """
        execute_query(insert_testimoni_sql, [id_tr_pemesanan, teks, rating])