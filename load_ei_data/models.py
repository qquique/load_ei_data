from functools import partial
from db import *

MoneyField = partial(DecimalField, decimal_places=2)


class BaseModel(Model):
    class Meta:
        database = db


class FormatA(BaseModel):
    id = AutoField()
    request_id = CharField(index=True)
    cnan = CharField(index=True)
    descrip = TextField()
    fecha = BigIntegerField()
    caduana = CharField()
    adua_desc = CharField()
    cpais = CharField()
    pais_desc = CharField()
    fob_dolpol = MoneyField()
    fle_dolar = MoneyField()
    seg_dolar = MoneyField()
    cif_dolar = MoneyField()
    peso_neto = DecimalField(decimal_places=2)
    peso_bruto = DecimalField(decimal_places=2)
    unid_fiqty = DecimalField(decimal_places=2)
    unid_fides = CharField()
    desc_com = TextField()
    puer_embar = CharField()
    puer_desc = CharField()
    fech_llega = CharField()
    nume_corre = CharField()
    nume_serie = CharField()
    via_transp = IntegerField()
    viat_desc = CharField()
    sest_merca = CharField()
    sest_desc = CharField()
    tipo_docum = CharField()
    libr_tribu = CharField()
    importador = CharField()
    cpais_proc = CharField()
    dpais_proc = CharField()

    class Meta:
        table_name = 'formata'


class FormatB(BaseModel):
    id = AutoField()
    request_id = CharField(index=True)
    cnan = CharField(index=True)
    descrip = CharField()
    fecha = IntegerField()
    caduana = CharField()
    adua_desc = CharField()
    cpais = CharField()
    pais_desc = CharField()
    fob_dolpol = MoneyField()
    peso_neto = DecimalField(decimal_places=2)
    peso_bruto = DecimalField(decimal_places=2)
    unid_fiqty = DecimalField(decimal_places=2)
    unid_fides = CharField()
    tipo_docu = CharField()
    nro_docu = CharField()
    puer_embar = CharField()
    exportador = CharField()
    puer_desc = CharField()
    desc_com = TextField()
    desc_adic = TextField()
    fec_num = IntegerField()
    fec_reg = IntegerField()
    ndcl = CharField()
    ndclreg = CharField()
    nume_serie = CharField()
    via_transp = CharField()
    viat_desc = CharField()
    cage = CharField()
    cage_desc = CharField()
    cemptra = CharField()
    cempt_desc = TextField()
    cadumanif = CharField()
    ann_manif = CharField()
    num_manif = CharField()

    class Meta:
        table_name = 'formatb'
