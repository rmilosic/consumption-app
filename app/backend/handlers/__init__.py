import pandas as pd
from django.core.files.uploadedfile import SimpleUploadedFile




from . import users, consumption, measurment, context


def load_csv(f: SimpleUploadedFile):
    f.file.seek(0)
    
    df = pd.read_csv(f.file, delimiter=";", na_values="", skip_blank_lines=True, dtype={
        "Št. Stan.": "Int64",
        "Št. Objekta": "Int64"
    })
    
    df.dropna(inplace=True, how="all")
    return df




def handle_file_upload_import_users(file: SimpleUploadedFile):
    
    
    # load CSV
    consumption_table = load_csv(file)
    
    # TODO: validate columns


    # TODO: stop if first apartment already exists in DB
    
    # get user details
        # Naziv stranke - first name
        # username - generate
        # password - generate
    consumption_table = users.add_user_details(consumption_table)
    
    # get list of user objects
    user_entries = users.create_user_entries(consumption_table)
    
    # get response which contains user ID
    user_save_response_list = users.bulk_import_users(user_entries)
    
    user_save_response__df = pd.DataFrame([user.__dict__ for user in user_save_response_list])    
    
    # store correlation username - ID (For later use)
    consumption_table = pd.merge(
        left=consumption_table,
        right=user_save_response__df,
        on="username",
        how="left")
    

    # get building details
    building_entries = users.create_building_records(consumption_table)
        
    # save buildings
    building_res = users.bulk_import_buildings(building_entries)
    
    
    
    apartment_entries = users.create_apartment_entries(consumption_table)
    
    apartment_res = users.bulk_import_apartments(apartment_entries)
    # get apartment details
    # ID - format building no. / apt. no
    # Building FK - provided
    # Apt No - Provided
    # User ID - get from user bulk create response correlation table
        
    # save apartments

    # delete all variables from memory
    
    # return
        # message ok/not ok
        # no, % of users created
        # no, % of buildings created
        # no, % of aparments created
    
    return f"Ustvarjenih je bilo {len(user_save_response__df)} uporabnikov, {len(building_res)} stavb ter {len(apartment_res)} stanovanj."


def handle_file_upload_import_consumption(file: SimpleUploadedFile, month: str, season: str):
    
    
    # load CSV
    consumption_table = load_csv(file)
    
    # TODO: validate columns

    # BUILDING consumption
    # deduplicate rows
    # create entries for bulk import
    # save data for building
    
    
    buildings_consumption = consumption_table.drop_duplicates(["Št. Objekta"], inplace=False)
    building_entries = consumption.create_building_consumption_entries(buildings_consumption, season=season, month=month)
    
    building_cons_bi_resp = consumption.bulk_import_consumption_report(building_entries)
    
    
    
    
    # APARTMENT consumption
    # create entries for buld import
    # save data
    # get created IDs
    # save created IDs to consumption table
    
    
    apartment_entries = consumption.create_apartment_consumption_entries(
        consumption_table, season, month
    )
    
    apartment_cons_bi_resp = consumption.bulk_import_consumption_report(apartment_entries)
    
    
    # add id of consumptionreport to each row
    apartment_cons_bi_resp_df = pd.DataFrame([cr.__dict__ for cr in apartment_cons_bi_resp])    
    
    # store correlation username - ID (For later use)
    consumption_table = pd.merge(
        left=consumption_table,
        right=apartment_cons_bi_resp_df,
        on="apartment_id",
        how="left",
        suffixes=(None, "_cr"))
    
    # MEASURMENTS
    # For each row, transform measurments into table, each unit separate row,
    # attach measurment to apartment consumption report
    # create entries
    # save data
    
    measurment_entries = measurment.create_measurment_entries(consumption_table)
    
    measurment_cons_bi_resp = measurment.bulk_import_measurments(measurment_entries)  
    
    
    return f"Shranili smo porabo za {len(building_cons_bi_resp)} objektov ter {len(apartment_cons_bi_resp)} stanovanj"