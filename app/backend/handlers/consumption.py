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
            period=b["Obdobje"],
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


def create_apartment_consumption_entries(
    consumption_table: pd.DataFrame, season: str, month: str):
    
    consumption_table["apartment_id"] = consumption_table.apply(lambda x: "{}/{}".format(x["Št. Objekta"], x["Št. Stan."]), axis=1)
    cons_table_list = consumption_table.to_dict("records")
    
    apartment_records = []
    
    for a in cons_table_list:
        
        try:
            
            apartment_records.append(
                ConsumptionReport(
                apartment_id=a["apartment_id"],
                building_id=a["Št. Objekta"],
                type="Apartment",
                season=season,
                month=month,
                period=a["Obdobje"],
                ogr_povrs=Decimal(a["Stan. - ogr. površina:"].replace(",", ".")),
                del_ogr_pov=Decimal(a["Stan. - delež ogr. pov.:"].replace(",", ".")),
                poraba=Decimal(a["Stan. - poraba enot:"].replace(",", ".")),
                kor_fakt=Decimal(a["Stan. - korekcijski faktor"].replace(",", ".")),
                osn_pd_13_clen=Decimal(a["Stan. - osnovni PD - 13.člen"].replace(",", ".")),
                korig_pd_15_1_clen=Decimal(a["Stan. - korigirani PD - 15.(1)člen"].replace(",", ".")),
                korig_pd_povrs_15_4_clen=Decimal(a["Stan. - korigirani PD na površino - 15.(4)člen"].replace(",", ".")),
                pod_40_nad_300_18_clen=Decimal(a["Stan. - pod 40% / nad 300% - 18.člen"].replace(",", ".")),
                prer_pd_100_19_clen=Decimal(a["Stan. - preračunan PD na 100% - 19.člen"].replace(",", ".")),
                var_del=Decimal(a["Stan. - variabilni delež"].replace(",", ".")),
                fiks_del=Decimal(a["Stan. - fiksni delež"].replace(",", ".")),
                skp_del_poraba=Decimal(a["Stan. - skupni delež / poraba"].replace(",", "."))
            ))
              
        except:
            # TODO: implement logging
            pass
            
    
    return apartment_records

