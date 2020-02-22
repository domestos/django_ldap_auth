from apps.user.models import *
from .ldap_connect import get_ldap_users
from datetime import datetime
# get all users from LDAP

# get all users from DataBase

# compare users  

def sync():
    ldap_users = get_ldap_users()
    print(type(ldap_users))
    db_users = User.objects.all()
    print(type(db_users))
    compare_obj(ldap_users)
    return ldap_users


def compare_obj(ldap_users):
    for ldap_user in ldap_users:
        if len(str(ldap_user.alias)) <= 3 and len(str(ldap_user.alias)) != 2:
            try:
                db_user = User.objects.get(alias__iexact=str(ldap_user.alias))
                # UPDATE USER
                if(str(db_user.display_name).lower().strip() != str(ldap_user.display_name).lower().strip() or
                    str(db_user.email).lower().strip() != str(ldap_user.email).lower().strip() or
                    str(db_user.department).lower().strip() != str(ldap_user.department).lower().strip() ):    
                        db_user.alias = ldap_user.alias
                        db_user.display_name=ldap_user.display_name
                        db_user.email = ldap_user.email
                        db_user.enabled = ldap_user.enabled
                        db_user.department = ldap_user.department
                        db_user.when_created = str(ldap_user.when_created)
                        db_user.when_changed = str(ldap_user.when_changed)
                        db_user.save()
                # NEED To Do Save Log
            except Exception as e:
                #ADD NEW USER
                ldap_user.when_created = str(ldap_user.when_created)
                ldap_user.when_changed = str(ldap_user.when_changed)
                ldap_user.save()
                # NEED To Do Save Log





# def compare(ldap_users, db_users):

#     for ldap_user in ldap_users:
#         print(ldap_user['sAMAccountName'])
#         try:
#             db_user = User.objects.get(
#                 alias__iexact=str(ldap_user['sAMAccountName']))
#             print(db_user)

#         except Exception as e:
#            user = User()
#            user.alias = ldap_user['sAMAccountName']
#            user.display_name = ldap_user['displayName']
#            user.department = ldap_user['department']
#         #    when_created = datetime.strptime(str(ldap_user['whenCreated']), "%Y-%m-%d %H:%M:%S%z")
#            user.when_created = datetime.strptime(
#                str(ldap_user['whenCreated']), "%Y-%m-%d %H:%M:%S%z")

#            user.when_changed = datetime.strptime(
#                str(ldap_user['whenChanged']), "%Y-%m-%d %H:%M:%S%z")
#            user.save()
#            print("user was not found in database: ",  str(e))



# def compare(ldap_users, db_users):
    
#     for ldap_user in ldap_users:        
#         print(ldap_user['sAMAccountName'])
#         try:
#             db_user = User.objects.get(
#                 alias__iexact=str(ldap_user['sAMAccountName']))           
#             print(db_user)

#         except Exception as e:
#            user = User()
#            user.alias = ldap_user['sAMAccountName']
#            user.display_name = ldap_user['displayName']
#            user.department = ldap_user['department']
#         #    when_created = datetime.strptime(str(ldap_user['whenCreated']), "%Y-%m-%d %H:%M:%S%z")
#            user.when_created = datetime.strptime(
#                str(ldap_user['whenCreated']), "%Y-%m-%d %H:%M:%S%z")
        
#            user.when_changed = datetime.strptime(
#                str(ldap_user['whenChanged']), "%Y-%m-%d %H:%M:%S%z")
#            user.save()
#            print("user was not found in database: ",  str(e)    )
