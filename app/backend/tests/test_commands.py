from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command



from backend.models import Building, Apartment, ConsumptionReport, Measurment

import pandas as pd

import os
import pathlib


class TestCommands(TestCase):
    
    def test_cleanusers(self):
        
        build = Building(id=34, full_address="example address")
        build.save()
        
        user_1 = User(username="user1", password="pass1")
        user_1.save()
        user_2 = User(username="user2", password="pass2")
        user_2.save()
        
        user_3 = User(username="staff_usr", password="pass3", is_staff=True)
        user_3.save()
        
        apartment = Apartment(id="34/1", owner_id=user_1.id, number=1, building_id=build.id).save()
        
        call_command("cleanusers")
        
        deleted_users = User.objects.filter(id__in=[user_2.id]).all()
        available_users = User.objects.filter(id__in=[user_1.id, user_3.id]).all()
        self.assertEqual(len(deleted_users), 0)
        self.assertEqual(len(available_users), 2)
        