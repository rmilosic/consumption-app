from django.contrib.auth.models import User


from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    
    help = "Removes users that don't have an apartment"
    
    
    def handle(self, *args, **options):
        
        # get users without apartment
        
        users_no_apt = User.objects.filter(apartment__id = None, is_staff=False).delete()
        # users_no_apt = User.objects.filter(apartment__id = None).prefetch_related("apartment_set")
             
        return