from ldap3.core.exceptions import LDAPBindError, LDAPSocketOpenError
from apps.settings.ldap.models import LdapConfig
from apps.user.models import User
from ldap3 import Server, Connection, SIMPLE, SYNC, ASYNC, SUBTREE, ALL
import json
from .encryptions_pass import decrypt_pass
  
import logging
logger = logging.getLogger(__name__)    
LOG_FILENAME = 'mylog.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)


def get_ldap_credential():
    """        
        Get credential from the DataBase and return credential in the dictionary
    """
    cred = LdapConfig.objects.all().first()  
    if not cred:
        print("Cann't get credential from DB. DataBase is empty.")
        # raise Exception("ERROR: Please set credential")
        return None

    credential={
            'LDAP_URL' : (cred.LDAP_URL).replace(' ', ''),
            'LDAP_URL': (cred.LDAP_URL).replace(' ', ''),
            'LDAP_PASS': decrypt_pass((cred.LDAP_PASS).replace(' ', '')),
            'LDAP_BASE_DN' : (cred.LDAP_BASE_DN).replace(' ', ''),
    }
    return credential

def get_ldap_connect():
    """        
        Return connect.
        Warning! Don't forget to close the connection in other functions
    """
    credential=get_ldap_credential()
    if not credential:
        # raise Exception("ERROR: Please set credential")
        return None

    # define the server
    server = Server(credential.get('LDAP_URL'))
    # define the connection
    connect = Connection(server, user=credential.get('LDAP_URL'), password=credential.get('LDAP_PASS'))
    print("get_ldap_connect: ", connect)
    return connect

def get_status_connect():
    """
        check LDAP connect and return his status
    """    
 
    connect = get_ldap_connect()
    if not connect:
        #  raise Exception("ERROR: Please set credential")
        logger.error('Credential is empty')
        return None

    print(connect)
    try:
        connect.bind()
        status = connect.result
    except Exception as e:
        # Raises an exception when LDAP server unavailable
        status= str(e)        
        logger.error(status)
    finally:
        connect.unbind()
        return status


def get_ldap_users():
    """
        LDAP_BASE_DN it is an OU where will searching users       
    """
    print("get_ldap_users")    
    connect = get_ldap_connect()
    if not connect:
        #  raise Exception("ERROR: Please set credential")
        return None
    users = None
    try:
        if connect.bind():
            #  https://social.technet.microsoft.com/wiki/contents/articles/8077.active-directory-ldap-ru-ru.aspx
            LDAP_BASE_DN = get_ldap_credential().get('LDAP_BASE_DN')
            # attributes=['cn', 'proxyAddresses', 'department', 'description', 'sAMAccountName', 'displayName', 'telephoneNumber', 'ipPhone', 'streetAddress','title', 'manager', 'objectGUID', 'company', 'lastLogon','whenCreated', 'msRTCSIP-UserEnabled']
            attributes = ['cn', 'mail', 'department',
                          'sAMAccountName', 'displayName', 'whenCreated', 'whenChanged']
            # search_filter= '(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(givenName=*)(sn=*))'
            # Все пользователи с заполненными именем и фамилией,e-mail .  => (& (objectCategory=person) (objectClass=user) (givenName=*)(sn=*)(proxyAddresses=*) )
            # Все пользователи с указанным e-mail  =>  ( & (objectCategory=person) (objectClass=user) ( | (proxyAddresses=*: jsmith@company.com) (mail=jsmith@company.com)))
            enable_user_search_filter = '(&(objectCategory=Person)(objectClass=user)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(givenName=*)(sn=*)(proxyAddresses=*))'
            disable_user_search_filter = '(&(objectCategory=Person)(objectClass=user)(UserAccountControl:1.2.840.113556.1.4.803:=2)(givenName=*)(sn=*)(proxyAddresses=*))'
            all_search_filter = "(& (objectCategory=person) (objectClass=user) (givenName=*)(sn=*)(proxyAddresses=*) )"
           #======== GET Disabled users ============
            connect.search(LDAP_BASE_DN, disable_user_search_filter, SUBTREE, attributes=attributes)
            disabled_users_dicts = convert_to_dict3(connect.entries, False)
            #======== GET Enabled users ============          
            connect.search(LDAP_BASE_DN, enable_user_search_filter,SUBTREE, attributes=attributes)
            enabled_users_dicts = convert_to_dict3(connect.entries, True)
            #======== Join dicts ============
            # print(str(dict(disabled_users_dicts)))
            # print(str(dict(enabled_users_dicts)))
            users = disabled_users_dicts+enabled_users_dicts
            connect.unbind()
    except LDAPBindError as e:
        # Raises an exception when LDAP server unavailable
        status=str(e) 
        logger.error(str(e))
    except LDAPSocketOpenError as e:
        logger.error('invalid search tree')       
        status =str(e) 
        users = "Error - " + str(e)
        print(status)
    finally:
        connect.unbind()
    # print(str(dir(users)))   
    return users


#========HELPER FUN=============
def convert_to_dict3(entries, enabled):
    users = []
    for ldap_user in entries:
        user = User()
        user.ldap_user = True
        user.display_name = ldap_user.displayName
        user.email = ldap_user.mail     
        user.alias = ldap_user.sAMAccountName
        user.department = ldap_user.department
        user.when_created = ldap_user.whenCreated
        user.when_changed = ldap_user.whenChanged
        user.enabled = enabled
        users.append(user)
    return users

def convert_to_dict2(entries, enabled):
    users = []
    for user in entries:      
        user_dict ={
            'cn':user.cn   , 
            'department':user.department   ,
            'sAMAccountName': user.sAMAccountName,
            'displayName':user.displayName   ,
            'whenCreated':user.whenCreated   ,
            'whenChanged': user.whenChanged,
            'Enabled': enabled
        }
        users.append(user_dict)
    return users

def convert_to_dict(entries, enabled):
    users=[]
    for user in entries:
        user_dict = json.loads(user.entry_to_json())
        user_dict['attributes']['Enabled'] = enabled
        print(user_dict)
        users.append(user_dict)
    return users
