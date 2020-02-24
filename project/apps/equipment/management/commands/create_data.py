from django.core.management.base import BaseCommand
from apps.inventory.models import Person, Location, TypeDevice, Device
import random
import datetime

locations = ['Lviv','Kyiv','Monako','Balivia']
persons=['John', 'Michael', 'Luke', 'Sally', 'Joe', 'Dude', 'Guy', 'Barbara']
type_devices=['Monitor', 'Computer', 'Laptop']

def isNotEmptyTable(obj):
    return obj.objects.all().exists()
    
def generate_person():
    index = random.randint(0,7)
    return persons[index]

def generate_inventorynumber():
    number = random.randint(10000,90000)
    return number

def return_obj(obj):
    objs =obj.objects.all();        
    return random.choice(objs)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='This argument is Count of rows in data base witch need to create')
    
    def handle(self, *args, **kwargs):
        # Insert Location
        if  not isNotEmptyTable(Location):            
            for location in locations:
               Location(location=location).save()
               print(location)
            
        # Insert Persons
        if not isNotEmptyTable(Person):
            for x in range(0, 50):
                Person(fname=generate_person(), sname=generate_person()).save()
              

        if not isNotEmptyTable(TypeDevice):
            for type in type_devices:
                TypeDevice(dtype=type).save()
                print(type)
          
        count = kwargs['count']
        for x in range(0, count):
            device = Device(
                inventory_number=generate_inventorynumber(),
                person_id = return_obj(Person),
                type_id=return_obj(TypeDevice),
                location_id=return_obj(Location)
            )
            # print(device)
            device.save()
        self.stdout.write(self.style.SUCCESS('Data was imported successfully'))