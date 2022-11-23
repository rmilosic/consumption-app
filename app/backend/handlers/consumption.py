from decimal import Decimal

import pandas as pd

from ..models import ConsumptionReport, Measurment

def create_building_consumption_entries(
    buildings_consumption: pd.DataFrame, season: str, month: str):
    
    build_cons_list = buildings_consumption.to_dict("records")
    
    building_entires = [ConsumptionReport(
            # apartment=None,
            building_id=b["Št. Objekta"],
            type="Building",
            season=season,
            month=month,
            period="Obdobje",
            ogr_povrs=Decimal(b["Objekt - ogr. površina:"].replace(",", ".")),
            del_ogr_pov=Decimal(b["Objekt - delež ogr. pov.:"].replace(",", ".")),
            poraba=Decimal(b["Objekt - poraba enot:"].replace(",", ".")),
            # kor_fakt=None,
            osn_pd_13_clen=Decimal(b["Objekt - osnovni PD - 13.člen"].replace(",", ".")),
            korig_pd_15_1_clen=Decimal(b["Objekt - korigirani PD - 15.(1)člen"].replace(",", ".")),
            korig_pd_povrs_15_4_clen=Decimal(b["Objekt - korigirani PD na površino - 15.(4)člen"].replace(",", ".")),
            pod_40_nad_300_18_clen=Decimal(b["Objekt - pod 40% in nad 300% - 18.člen"].replace(",", ".")),
            prer_pd_100_19_clen=Decimal(b["Objekt - preračunan PD na 100% - 19.člen"].replace(",", ".")),
            var_del=Decimal(b["Objekt - variabilni delež"].replace(",", ".")),
            fiks_del=Decimal(b["Objekt - fiksni delež"].replace(",", ".")),
            skp_del_poraba=Decimal(b["Objekt - skupni delež"].replace(",", "."))
            
        ) for b in build_cons_list]
    
    return building_entires


def bulk_import_consumption_report(consumption_report_entries):
    return ConsumptionReport.objects.bulk_create(consumption_report_entries)