
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from random import randint, randrange


from backend.models import Building, Apartment
from backend.handlers import *
import os
import pathlib


class TestHandlers(TestCase):
    
    def test_handle_file_upload_import_users(self):
        with open(os.path.join(pathlib.Path(__file__).parent.resolve(), "sample.csv"), "rb") as f:
            bts = f.read()
            file = SimpleUploadedFile("mycsv.txt", bts)
            result = handle_file_upload_import_users(file)
            
        self.assertEqual(result, "ok")
            
    
    def test_load_csv(self):
        
        with open(os.path.join(pathlib.Path(__file__).parent.resolve(), "sample.csv"), "rb") as f:
            bts = f.read()
            file = SimpleUploadedFile("mycsv.txt", bts)
            import_table = load_csv(file)
        
            print(import_table.head())
            self.assertEqual("hello", "hello")
            
    def test_get_random_string(self):
        rand_str = get_random_string(8)
        self.assertEqual(len(rand_str), 8)
        
        
    def test_add_user_details(self):
        
        df = pd.DataFrame(data={
            "col1": [1, 2], "col2": [3,4]
        })
        
        df = add_user_details(df)
        print(df.head())
        self.assertEqual(len(df["username"].iloc[0]), 6)
        self.assertEqual(len(df["password"].iloc[0]), 12)
        
        
    def test_create_user_entries(self):

        df = pd.DataFrame(data={
            "username": ["12rad9aw", "rqwr12"], "password": ["rq3rh1o2i", "21489awads"], "Naziv stranke": ["Ime 1 asdadas", "Ime 2 asudbaofa"]
        })
        user_entries = create_user_entries(df)
        
        self.assertIsInstance(user_entries[0], User)
        
        
    def test_bulk_import_users(self):
        
        user_entries = [
            User(username="usrnm1", password=make_password("passwrd1"), first_name="First nm1"),
            User(username="usrnm2", password=make_password("passwrd2"), first_name="First nm2"),
            User(username="usrnm3", password=make_password("passwrd3"), first_name="First nm3")
        ]
        
        resp = bulk_import_users(user_entries)
        
        self.assertEqual(resp[0].username, "usrnm1")
        
        
    def test_create_building_records(self):
        
        df = pd.DataFrame(data={
            "Št. Objekta": [2, 2, 3, 3], "col2": [3,4, 4, 4]
        })
        
        result = create_building_records(df) 
        
        self.assertIsInstance(result[0], Building)
        
    def test_bulk_import_buildings(self):
        
        id_1 = randint(100,999)
        id_2 = randint(100,999)
        id_3 = randint(100,999)
        
        building_entries = [
            Building(id=id_1),
            Building(id=id_2),
            Building(id=id_3)
        ]
        
        response = bulk_import_buildings(building_entries)
        
        self.assertEqual(response[0].id, id_1)
        
        
    def test_create_apartment_records(self):
        
        df = pd.DataFrame(data={
            "Št. Objekta": [2, 3, 4, 5], "Št. Stan.": [1,2,3,4]
        })
        
        result = create_apartment_entries(df) 
        
        self.assertIsInstance(result[0], Apartment)
        
        
        
        
        
        
     