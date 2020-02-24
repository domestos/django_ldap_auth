from mysql.connector import Error
from django.core.management.base import BaseCommand
from apps.equipment.models import Equipment, Location, EquipmentType
from apps.accounts.models import User as Profile
import datetime


class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser.add_argument('file_name', type=str, help='This text file that contain the journal titels')
        pass

    def handle(self, *args, **kwargs):
        import mysql.connector
        Equipment.objects.all().delete()
        EquipmentType.objects.all().delete()
        Location.objects.all().delete()
        Profile.objects.all().delete()
      
        try:
            connection = mysql.connector.connect(host='uasrv63.csia.net',
                                                 database='inventory_db',
                                                 user='inventory',
                                                 password='C$ia2o16')


             # ============SELECT OWNER ===========
            user = Profile.objects.create_superuser('valera', password='vQsece4b')
            user.save()
            sql_select_Owner = "select `id`,`alias`,`name` from inventory_owner"
            # user_records = self.sqlQuery(connection, sql_select_Owner)
            cursor = connection.cursor()
            cursor.execute(sql_select_Owner)
            user_records = cursor.fetchall()
            print("Total number of Profile rows are: ")
            for row in user_records:
                print(row)
                self.convert_to_user_obj(row)
           
            #=============================================


            #  # ============SELECT LOCATION ===========
            sql_select_Location = "select * from inventory_location"
            # user_records = self.sqlQuery(connection, sql_select_Owner)
            cursor = connection.cursor()
            cursor.execute(sql_select_Location)
            location_records = cursor.fetchall()
            print("Total number of Profile rows are: ")
            for row in location_records:
                print(row)
                self.convert_to_location_obj(row)
           
            # #=============================================

              #  # ============SELECT EquipmentType ===========
            sql_select_Type = "select * from inventory_DeviceType"
            # user_records = self.sqlQuery(connection, sql_select_Owner)
            cursor = connection.cursor()
            cursor.execute(sql_select_Type)
            type_records = cursor.fetchall()
            print("Total number of Profile rows are: ")
            for row in type_records:
                print(row)
                self.convert_to_device_type_obj(row)
           
            # #=============================================


            # ============SELECT DEVICE ===========
       
            sql_select_Device = "select `id`,`date_of_purchase`,`description`,`host_name`,`inventory_number`,`memory`,`model`,`part_number`,`qr_id`,`seller`,`serial_number`,`state`,`warranty`,`device_type_id_id`,`location_id_id`,`owner_id_id`,`status_inventory` from inventory_device"
            cursor = connection.cursor()
            cursor.execute(sql_select_Device)
            device_records = cursor.fetchall()
            print("Total number of rows in Laptop is: ")
            for row in device_records:
                print(row)
                self.convert_to_equipment_obj(row)
           
            #=============================================




              # ============SELECT HISTORY ===========
       
            sql_select_Device = "select * from inventory_historicaldevice"
            cursor = connection.cursor()
            cursor.execute(sql_select_Device)
            device_records = cursor.fetchall()
            print("Total number of rows in Laptop is: ")
            for row in device_records:
                print(row)
                self.convert_to_history_equipment_obj(row)
           
            #=============================================
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")

                self.stdout.write(self.style.SUCCESS(
                    'Data was imported successfully'))


    def convert_to_equipment_obj(self, row):
        print(  'user=',row[15])
        if row[4] == "" or row[4] ==None:
            inventory_number = "None {}".format(str(row[0]))
        else:
            inventory_number = row[4]
            try:
                Equipment.objects.get(inventory_number=inventory_number)
                print ("=================================DUPLICATE ++++++")
                inventory_number = inventory_number+"_is_duplicate"+str(row[0])
            except Exception as identifier:
                pass               
        try:           
            user = Profile.objects.get(pk= str(row[15]).replace('/', '-'))
        except Exception as identifier:
            # 2316 - is id Itroom
            user =  Profile.objects.get(pk=2316)
       
        try:
            location = Location.objects.get(pk=row[14])
        except Exception as identifier:
            # 1 - is id Undefined
            location = Location.objects.get(pk=1)
        try:
            type = EquipmentType.objects.get(pk=row[13])
        except Exception as identifier:
            # 1 - is id IS_EMPTY
            type = EquipmentType.objects.get(pk=5)
      
        equipment = Equipment.objects.create( 
            id=row[0],
            date_of_purchase=row[1],
            description=row[2],
            host_name=row[3],
            inventory_number=inventory_number,
            memory=row[5],
            model=row[6],
            part_number=row[7],
            qr_id=row[8],
            serial_number=row[10],
            state=row[11],
            device_type=type,
            location=location,
            user=user,
            status_inventory=row[16]
        )
        equipment.save_without_historical_record()

    def convert_to_user_obj(self, row):
        profile = Profile.objects.create(
            id=row[0],
            username=str(row[1]).replace('/', '-'),
          
        )
        profile.set_unusable_password()
        profile.save_without_historical_record()

    def convert_to_location_obj(self, row):
        location = Location.objects.create(
            id=row[0],
            name=row[1]
        )
        location.save()

    def convert_to_device_type_obj(self, row):
        type = EquipmentType.objects.create(
            id=row[0],
            name=row[1]
        )
        type.save()            
        # 0 `id`, 
        # 1 `date_of_purchase`,
        # 2 `description`,
        # 3 `host_name`,
        # 4 `inventory_number`,
        # 5 `memory`,
        # 6 `model`,
        # 7 `part_number`,
        # 8 `qr_id`,
        # 9 `seller`,
        # 10`serial_number`,
        # 11`state`,
        # 12`warranty`,
        # 13`device_type_id_id`,
        # 14`location_id_id`,
        # 15`owner_id_id`,
        #16`status_inventory`


    def convert_to_history_equipment_obj(self, row):
        print(row)