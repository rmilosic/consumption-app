from decimal import Decimal

import pandas as pd

from ..models import Measurment

def create_measurment_entries(consumption_table: pd.DataFrame):
    
    # vsak stolpec od Poraba Delilnika 1 do 10 je ena vrstica
    measurments_raw_df = pd.melt(consumption_table, id_vars=["id"], 
                                 value_vars=[
                                     "Poraba Delilnika 1",
                                     "Poraba Delilnika 2",
                                     "Poraba Delilnika 3",
                                     "Poraba Delilnika 4",
                                     "Poraba Delilnika 5",
                                     "Poraba Delilnika 6",
                                     "Poraba Delilnika 7",
                                     "Poraba Delilnika 8",
                                     "Poraba Delilnika 9",
                                     "Poraba Delilnika 10"], value_name="Poraba delilnika", var_name="Št. delilnika")
    
    only_full_rows = measurments_raw_df[measurments_raw_df["Poraba delilnika"].notnull()]
    
    only_full_rows[["space", "device_number", "initial_state", "final_state", "corr_factor", "used_units"]] = only_full_rows["Poraba delilnika"].str.split("/", expand=True)
    
    only_full_rows_list = only_full_rows.to_dict("records")
    
    
    measurment_records = []
    
    for m in only_full_rows_list:
        
        try:
            measurment_records.append(
                Measurment(
                    device_number=m["device_number"],
                    space=m["space"],
                    initial_state=int(m["initial_state"]),
                    final_state=int(m["final_state"]),
                    corr_factor=Decimal(m["corr_factor"].replace(",", ".")),
                    used_units=Decimal(m["used_units"].replace(",", ".")),
                    consumption_report_id=m["id"]
                )
            )
        except:
            # TODO: log error
            pass 
    
    return measurment_records


def bulk_import_measurments(measurment_entries):
    return Measurment.objects.bulk_create(measurment_entries)
    