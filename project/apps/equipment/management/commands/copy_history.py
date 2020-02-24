from mysql.connector import Error
from django.core.management.base import BaseCommand
from apps.equipment.models import Equipment, Location, EquipmentType
from apps.accounts.models import User as Profile
import datetime
import mysql.connector


class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser.add_argument('file_name', type=str, help='This text file that contain the journal titels')
        pass

    def handle(self, *args, **kwargs):
        self.clean_history()

        try:
            connection = mysql.connector.connect(host='uasrv63.csia.net',
                                                 database='inventory_db',
                                                 user='inventory',
                                                 password='C$ia2o16')

            # ============SELECT HISTORY ===========

            sql_select_Device = "select `id`,`date_of_purchase`,`description`,`host_name`,`inventory_number`,`memory`,`model`,`part_number`,`qr_id`,`serial_number`,`state`,`history_id`,`history_date`,`history_change_reason`,`history_type`,`device_type_id_id`,`history_user_id`,`location_id_id`,`owner_id_id`,`status_inventory` from inventory_historicaldevice"
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql_select_Device)
            device_records = cursor.fetchall()
            print("Total number of rows in Laptop is: ")
            for row in device_records:
                # print(row)
                self.convert_to_history_equipment_obj(row)

            # =============================================
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")

                self.stdout.write(self.style.SUCCESS(
                    'Data was imported successfully'))

    def convert_to_history_equipment_obj(self, row):
        print(row.get('id'))
        sql = "INSERT INTO inventory_historicalequipment( id, inventory_number, history_id, history_date, history_change_reason, history_type,  device_type_id, history_relation_id, history_user_id, location_id, user_id, date_of_purchase, description, model, part_number, serial_number, host_name, memory, qr_id, state, status_inventory) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (
            row.get('id'),
            row.get('inventory_number'),
            row.get('history_id'),
            row.get('history_date'),
            row.get('history_change_reason'),
            row.get('history_type'),
            row.get('device_type_id_id'),
            row.get('id'),
            row.get('history_user_id'),
            row.get('location_id_id'),
            row.get('owner_id_id'),
            row.get('date_of_purchase'),
            row.get('description'),
            row.get('model'),
            row.get('part_number'),
            row.get('serial_number'),
            row.get('host_name'),
            row.get('memory'),
            row.get('qr_id'),
            row.get('state'),
            row.get('status_inventory')

        )
        self.insert_history(sql, val)

    def insert_history(self, sql, val):
        try:
            connection = mysql.connector.connect(host='uasrv63.csia.net',
                                                 database='inventory_db_react',
                                                 user='inventory',
                                                 password='C$ia2o16')
        
            cursor = connection.cursor()
            cursor.execute(sql, val)
            connection.commit()
            print(cursor.rowcount, "record(s) Inserted")
           
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")

                self.stdout.write(self.style.SUCCESS(
                    'INSERTED WAS successfully'))


    def clean_history(self):
        try:
            connection = mysql.connector.connect(host='uasrv63.csia.net',
                                                 database='inventory_db_react',
                                                 user='inventory',
                                                 password='C$ia2o16')
            sql_select_Device = "delete from inventory_historicalequipment"
            cursor = connection.cursor()
            cursor.execute(sql_select_Device)
            connection.commit()
            print(cursor.rowcount, "record(s) deleted")
            print("Delete successfully")
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")

                self.stdout.write(self.style.SUCCESS(
                    'DELETING WAS successfully'))
