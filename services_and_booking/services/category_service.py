from db.utils.query_helpers import execute_query, fetch_dict_all, fetch_dict_one

class CategoryAndSubcategoryService:
    @staticmethod
    def get_all_categories():
        sql = """
        SELECT id, nama_kategori FROM sijarta.kategori_jasa;
        """
        return fetch_dict_all(sql)
    
    @staticmethod
    def get_subcategories_by_category(category_id):
        sql = """
        SELECT id, nama_subkategori FROM sijarta.subkategori_jasa WHERE kategori_jasa_id = %s;
        """
        return fetch_dict_all(sql, [category_id])
    
    @staticmethod
    def search_subcategory_by_name(subcategory_name):
        sql = """
        SELECT s.id AS subcategory_id, s.nama_subkategori AS subcategory_name, k.id AS category_id, k.nama_kategori AS category_name
        FROM sijarta.subkategori_jasa s
        JOIN sijarta.kategori_jasa k ON s.kategori_jasa_id = k.id
        WHERE s.nama_subkategori ILIKE %s;
        """
        return fetch_dict_all(sql, ['%' + subcategory_name + '%'])