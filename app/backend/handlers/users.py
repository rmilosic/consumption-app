
from ..models import Apartment, Building

import pandas as pd
from django.core.files.uploadedfile import SimpleUploadedFile

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

import random
import string


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_letters+string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


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
    buildings = consumption_table[["Št. Objekta", "Naslov"]].drop_duplicates()
    buildings.rename({"Št. Objekta": "id"}, inplace=True, axis=1)
    buildings_object_list = buildings.to_dict("records")
    
    buildings_entries = [Building(id=b["id"], full_address=b["Naslov"]) for b in buildings_object_list]
    return buildings_entries


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
