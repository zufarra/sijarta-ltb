-- TK 1
-- Kelas Basdat B
--
-- Lapis Talas Bogor
--
-- Akhdan Taufiq Syofyan (2306152475)
-- M. Rafli Esa Pradana (2306207480)
-- Yudayana Arif Prasojo (2306215160)
-- Zufar Romli Amri (2306202694)

-- Disclaimer : Kami tidak menggunakan set search_path to sijarta karena tabel user menyebabkan conflict 
--              dengan keyword user sql dan untuk menjaga konsistensi penulisan.

-- Membuat Schema
CREATE SCHEMA SIJARTA;

------------------------------------------------------------------------------------------------------------------------------------

-- Membuat tabel
CREATE TABLE SIJARTA.USER (
    id UUID NOT NULL,
    nama VARCHAR(255),
    jenis_kelamin CHAR(1) CHECK (jenis_kelamin IN ('L', 'P')),
    no_hp VARCHAR(50),
    pwd VARCHAR(255),
    tgl_lahir DATE,
    alamat VARCHAR(255),
    saldo_mypay DECIMAL,
    PRIMARY KEY (id)
);

CREATE TABLE SIJARTA.PELANGGAN (
    id UUID NOT NULL,
    level VARCHAR(50),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES SIJARTA.USER(id)
);

CREATE TABLE SIJARTA.PEKERJA (
    id UUID NOT NULL,
    nama_bank VARCHAR(255),
    nomor_rekening VARCHAR(50),
    npwp VARCHAR(50),
    link_foto VARCHAR(255),
    rating FLOAT,
    jml_pesanan_selesai INT,
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES SIJARTA.USER(id)
);

CREATE TABLE SIJARTA.KATEGORI_TR_MYPAY (
    id UUID NOT NULL,
    nama VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE TABLE SIJARTA.TR_MYPAY (
    id UUID NOT NULL,
    user_id UUID,
    tgl DATE,
    nominal DECIMAL,
    kategori_id UUID,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES SIJARTA.USER(id),
    FOREIGN KEY (kategori_id) REFERENCES SIJARTA.KATEGORI_TR_MYPAY(id)
);

CREATE TABLE SIJARTA.KATEGORI_JASA (
    id UUID NOT NULL,
    nama_kategori VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE TABLE SIJARTA.PEKERJA_KATEGORI_JASA (
    pekerja_id UUID,
    kategori_jasa_id UUID,
    FOREIGN KEY (pekerja_id) REFERENCES SIJARTA.PEKERJA(id),
    FOREIGN KEY (kategori_jasa_id) REFERENCES SIJARTA.KATEGORI_JASA(id),
    PRIMARY KEY (pekerja_id, kategori_jasa_id)
);

CREATE TABLE SIJARTA.SUBKATEGORI_JASA (
    id UUID NOT NULL,
    nama_subkategori VARCHAR(255),
    deskripsi TEXT,
    kategori_jasa_id UUID,
    PRIMARY KEY (id),
    FOREIGN KEY (kategori_jasa_id) REFERENCES SIJARTA.KATEGORI_JASA(id)
);

CREATE TABLE SIJARTA.SESI_LAYANAN (
    subkategori_id UUID NOT NULL,
    sesi INT NOT NULL,
    harga DECIMAL,
    PRIMARY KEY (subkategori_id, sesi),
    FOREIGN KEY (subkategori_id) REFERENCES SIJARTA.SUBKATEGORI_JASA(id)
);

CREATE TABLE SIJARTA.DISKON (
    kode VARCHAR(50) NOT NULL,
    potongan DECIMAL NOT NULL CHECK (potongan >= 0),
    min_tr_pemesanan INT NOT NULL CHECK (min_tr_pemesanan >= 0),
    PRIMARY KEY (kode)
);

CREATE TABLE SIJARTA.VOUCHER (
    kode VARCHAR(50) NOT NULL,
    jml_hari_berlaku INT NOT NULL CHECK (jml_hari_berlaku >= 0),
    kuota_penggunaan INT,
    harga DECIMAL NOT NULL CHECK (harga >= 0),
    PRIMARY KEY (kode),
    FOREIGN KEY (kode) REFERENCES SIJARTA.DISKON(kode)
);

CREATE TABLE SIJARTA.PROMO (
    kode VARCHAR(50) NOT NULL,
    tgl_akhir_berlaku DATE NOT NULL,
    PRIMARY KEY (kode),
    FOREIGN KEY (kode) REFERENCES SIJARTA.DISKON(kode)
);

CREATE TABLE SIJARTA.METODE_BAYAR (
    id UUID NOT NULL,
    nama VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE SIJARTA.TR_PEMBELIAN_VOUCHER (
    id UUID NOT NULL,
    tgl_awal DATE NOT NULL,
    tgl_akhir DATE NOT NULL,
    telah_digunakan INT NOT NULL CHECK (telah_digunakan >= 0),
    id_pelanggan UUID,
    id_voucher VARCHAR(50),
    id_metode_bayar UUID,
    PRIMARY KEY (id),
    FOREIGN KEY (id_pelanggan) REFERENCES SIJARTA.PELANGGAN(id),
    FOREIGN KEY (id_voucher) REFERENCES SIJARTA.VOUCHER(kode),
    FOREIGN KEY (id_metode_bayar) REFERENCES SIJARTA.METODE_BAYAR(id)
);

CREATE TABLE SIJARTA.STATUS_PESANAN (
    id UUID NOT NULL,
    status VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE SIJARTA.TR_PEMESANAN_JASA (
    id UUID NOT NULL,
    tgl_pemesanan DATE NOT NULL,
    tgl_pekerjaan DATE NOT NULL,
    waktu_pekerjaan TIMESTAMP NOT NULL,
    total_biaya DECIMAL NOT NULL CHECK(total_biaya >= 0),
    id_pelanggan UUID,
    id_pekerja UUID,
    id_kategori_jasa UUID,
    sesi INT,
    id_diskon VARCHAR(50),
    id_metode_bayar UUID,
    PRIMARY KEY (id),
    FOREIGN KEY (id_pelanggan) REFERENCES SIJARTA.PELANGGAN(id),
    FOREIGN KEY (id_pekerja) REFERENCES SIJARTA.PEKERJA(id),
    FOREIGN KEY (id_kategori_jasa, sesi) REFERENCES SIJARTA.SESI_LAYANAN(subkategori_id, sesi),
    FOREIGN KEY (id_diskon) REFERENCES SIJARTA.DISKON(kode),
    FOREIGN KEY (id_metode_bayar) REFERENCES SIJARTA.METODE_BAYAR(id)
);

CREATE TABLE SIJARTA.TR_PEMESANAN_STATUS (
    id_tr_pemesanan UUID NOT NULL,
    id_status UUID NOT NULL,
    tgl_waktu TIMESTAMP NOT NULL,
    FOREIGN KEY (id_tr_pemesanan) REFERENCES SIJARTA.TR_PEMESANAN_JASA(id),
    FOREIGN KEY (id_status) REFERENCES SIJARTA.STATUS_PESANAN(id),
    PRIMARY KEY (id_tr_pemesanan, id_status)
);

CREATE TABLE SIJARTA.TESTIMONI (
    id_tr_pemesanan UUID NOT NULL,
    tgl DATE,
    teks TEXT,
    rating INT NOT NULL DEFAULT 0,
    FOREIGN KEY (id_tr_pemesanan) REFERENCES SIJARTA.TR_PEMESANAN_JASA(id),
    PRIMARY KEY (id_tr_pemesanan, tgl)
);
