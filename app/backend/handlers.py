import pandas as pd
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Apartment, Building

import random
import string
from itertools import islice

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_letters+string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def load_csv(f: SimpleUploadedFile):
    f.file.seek(0)
    return pd.read_csv(f.file, delimiter=";")


def add_user_details(consumption_table: pd.DataFrame):
    
    # add username col (autogenerate)
    consumption_table["username"] = consumption_table.apply(lambda x: get_random_string(6), axis=1)
    
    # add password col (autogenerate)
    consumption_table["password"] = consumption_table.apply(lambda x: get_random_string(12), axis=1)
    
    return consumption_table


def create_user_entries(df: pd.DataFrame):
    
    user_object_list = df.to_dict("records")
    
    # TODO: add user group
    user_entries = [User(username=u["username"], password=make_password(u["password"]), first_name=u["Naziv stranke"]) for u in user_object_list]
   
    return user_entries


def bulk_import_users(user_entries):
    
    # save users
    # batch_size = 100
    
    # while True:
    #     batch = list(islice(user_entries, batch_size))
    #     if not batch:
    #         break
    return User.objects.bulk_create(user_entries)


def bulk_import_buildings(building_entries):
    
    return Building.objects.bulk_create(building_entries)
    

def create_building_records(consumption_table: pd.DataFrame):    
    
    ## to be deduplicated (duplicates present)
    # ID - set explicitly
    # TODO: name (TO be provided)

    buildings = consumption_table[["Št. Objekta"]].drop_duplicates()
    buildings.rename({"Št. Objekta": "id"}, inplace=True, axis=1)
    buildings_object_list = buildings.to_dict("records")
    
    buildings_entires = [Building(id=b["id"]) for b in buildings_object_list]
    return buildings_entires


def create_apartment_entries(consumption_table: pd.DataFrame):    
    
    # ID - set explicitly

    apartments = consumption_table[["Št. Objekta", "Št. Stan.", "id"]].drop_duplicates()
    apartments_object_list = apartments.to_dict("records")
    
    apartments_entires = [Apartment(
        id=f"{b['Št. Objekta']}/{b['Št. Stan.']}", 
        number=f"{b['Št. Stan.']}",
        building_id=f"{b['Št. Objekta']}",
        owner_id=f"{b['id']}") for b in apartments_object_list]
    return apartments_entires


def bulk_import_apartments(apartment_entries):
    return Apartment.objects.bulk_create(apartment_entries)

def handle_file_upload_import_users(file: SimpleUploadedFile):
    
    # load CSV
    consumption_table = load_csv(file)

    # get user details
        # Naziv stranke - first name
        # username - generate
        # password - generate
    consumption_table = add_user_details(consumption_table)
    
    # get list of user objects
    user_entries = create_user_entries(consumption_table)
    
    # get response which contains user ID
    user_save_response_list = bulk_import_users(user_entries)
    
    user_save_response__df = pd.DataFrame([user.__dict__ for user in user_save_response_list])    
    
    # store correlation username - ID (For later use)
    consumption_table = pd.merge(
        left=consumption_table,
        right=user_save_response__df,
        on="username",
        how="left")
    

    # get building details
    building_entries = create_building_records(consumption_table)
        
    # save buildings
    building_res = bulk_import_buildings(building_entries)
    
    
    
    apartment_entries = create_apartment_entries(consumption_table)
    
    apartment_res = bulk_import_apartments(apartment_entries)
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