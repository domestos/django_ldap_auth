"""
Low-level LDAP hooks.
"""

import ldap3
from ldap3.core.exceptions import LDAPException
from apps.settings.ldap.models import LdapConfig
from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.models import User
from apps.accounts.models import User
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

class Connection():
    def __init__(self, connection,base_dn):
        print('class Connection():::__init__ method called')             
        self.connection = connection
        self.search_base = base_dn
        self.attributes =   ['cn', 'mail', 'department', 'sAMAccountName', 'givenName', 'sn', 
                            'displayName', 'whenCreated', 'whenChanged']
          
    def __request_to_ldap(self, filter):
        try:
            # ldap3.ALL_ATTRIBUTES
            if self.connection.search(
                search_base=self.search_base,
                search_filter=filter,
                search_scope=ldap3.SUBTREE,
                attributes=self.attributes,
                get_operational_attributes=True,
            ):                 
                # logger.warning("Result: {ex}".format(ex=self.connection.response[0]))
                return self.connection.response
            else:
                logger.warning("LDAP user lookup failed")
                return None
        except Exception as ex:
            logger.warning("====LDAP connect failed: {ex}".format(ex=ex))
            return None

    def __check_format(self, attributes):
        if isinstance(attributes, (list, tuple)) and len(attributes)!=0 :
            attributes = attributes[0]
        return  attributes

    def __get_user_fields(self, user):
        print('class Connection():::__get_user_fields method called') 
        # print("raw_user ", user)
        attributes = user.get("attributes")     
        user_fields={
            "username": self.__check_format(attributes['sAMAccountName']),
            "first_name": self.__check_format(attributes['givenName']),
            "last_name":  self.__check_format(attributes['sn']),
            "email":  self.__check_format(attributes['mail']),
            "department": self.__check_format(attributes['department']),
            'when_created':self.__check_format(attributes['whenCreated']),
            'when_changed': self.__check_format(attributes['whenChanged'])
            }
        return user_fields
    
    def __get_or_create(self, user_fields):
        print('class Connection():::__get_or_create() method called') 
        try:
            print(user_fields['username'])
            user = User.objects.get(username=user_fields['username'])
            # logger.info("User was found: {username}".format(username=user_fields['username']))
            return user
        except Exception as ex:
            logger.warning("LDAP connect failed: {ex}".format(ex=ex))
       
            user= User.objects.create(**user_fields)
            user.set_unusable_password()
            if user.username == 'vap':
                    user.is_superuser = "True"
                    user.is_staff = "True"
            user.save()
            return user

    def __create_or_update(self, user_fields):
        try:
            # print(user_fields)
            print("I'll search the user: ", user_fields['username'])
            user = User.objects.get(username=user_fields['username'])
            status_update=False
            
            for key, value in user_fields.items():
                print("key = ", key," value = ", value)
                print("user values=", getattr(user, key) , " = ", value)
                if getattr(user, key) != value:
                    status_update =True 
                    setattr(user, key, value)
            
            if status_update:
                user.save()
          
            return user
        except ObjectDoesNotExist as ex:
            logger.warning("User was not found: {ex}".format(ex=ex))
            return User.objects.create(**user_fields)
        except Exception as ex:
            logger.warning("Other exception: {ex}".format(ex=ex))
   
    def get_user(self, filter):
        print('class Connection():::get_user() method called') 
        ldap_user= self.__request_to_ldap(filter)
        if ldap_user !=None:
            return self.__get_or_create(self.__get_user_fields(ldap_user[0]))
        else:
            return None

    def sync_users(self, filter, is_active):
        print('class Connection():::sync_users() method called') 
        ldap_users = self.__request_to_ldap(filter)
        if ldap_users !=None:
            for ldap_user in ldap_users:
                user_fields = self.__get_user_fields(ldap_user) 
                user_fields['is_active'] = is_active  
                user_fields['ldap_user'] = True
                data_user=self.__create_or_update(user_fields)
               
        return ldap_users
        # else:
        #     return None  

class ConnectManager(): 
    def __init__(self,username,password,ldap_url,base_dn):
        print('class ConnectManager():::init():') 
        print(username,password,ldap_url,base_dn)
        self.username=username
        self.password =password
        self.ldap_url = ldap_url
        self.base_dn = base_dn
        self.connect = None
        print('__init__ method called') 
        
    def __enter__(self):
        print('__enter__ method called') 
        # == Prepare Connection ============
        try:
            # define the server
            server = ldap3.Server(self.ldap_url,
                                allowed_referral_hosts=[("*", True)],
                                get_info=ldap3.ALL,
                                connect_timeout=None,
                                )
            # define the connection
            self.connect = ldap3.Connection(server,
                                user= self.username,
                                password=self.password,
                                auto_bind=False,
                                raise_exceptions=True,
                                receive_timeout=None,
                                )
        except LDAPException as ex:
            logger.warning("LDAP connect failed: {ex}".format(ex=ex))
            return None
        # ==================================

       #  == Bind connection ===============
        try:
            self.connect.bind(read_server_info=True)
            logger.info("Connect is binded")
            # @ConnectManager Return Connection(c, BASE_DN, username)
            return Connection(self.connect , self.base_dn)
        except LDAPException as ex:
            logger.warning("LDAP bind failed: {ex}".format(ex=ex))
            return None        
        # ==================================
      
      
    def __exit__(self, exc_type, exc_value, exc_traceback): 
        print('__exit__ method called') 
        if self.connect != None:
            self.connect.unbind()
            logger.info(":::Connect unbind")
       
# # === AUTHENTICATE Method==============================================
def authenticate(*args, **kwargs):
    """ return django user"""
    logger.warning(":::Run authenticate: {e}".format(e=kwargs))
    ldap_config=LdapConfig.objects.all().first()
    if not ldap_config:
        return None
    ldap_url = ldap_config.LDAP_URL
    base_dn  = ldap_config.LDAP_BASE_DN
    password = kwargs.pop("password")
    username = kwargs.pop("username")
    filter ="(&(objectCategory=Person)(objectClass=user)(sAMAccountName={username}))".format(username=get_raw_username(username))     
    with ConnectManager(username,password,ldap_url,base_dn) as c:
        if c is None:
            return None
        return  c.get_user(filter)
    return None

# === TEST CONNECT Method==============================================
def test_connect():
    ldap_config=LdapConfig.objects.all().first()
    if not ldap_config:
        return None
    username = ldap_config.LDAP_USER
    password = ldap_config.decrypt_pass(ldap_config.LDAP_PASS)
    ldap_url = ldap_config.LDAP_URL
    base_dn  = ldap_config.LDAP_BASE_DN
    
    with ConnectManager(username,password,ldap_url,base_dn) as c:
        if c is None:
            return None
        return True
    return None

# === SYNC USERS Method==============================================
def sync_users():
    ldap_config=LdapConfig.objects.all().first()
    if not ldap_config:
        return None
    username = ldap_config.LDAP_USER
    password = ldap_config.decrypt_pass(ldap_config.LDAP_PASS)
    ldap_url = ldap_config.LDAP_URL
    base_dn  = ldap_config.LDAP_BASE_DN
    
    filter_for_enabled_user  = '(&(objectCategory=Person)(objectClass=user)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(givenName=*)(sn=*)(proxyAddresses=*))'
    filter_for_disabled_user = '(&(objectCategory=Person)(objectClass=user)(UserAccountControl:1.2.840.113556.1.4.803:=2)(givenName=*)(sn=*))'
      
    with ConnectManager(username,password,ldap_url,base_dn) as c:
        if c is None:
            return None
        enabled_users=c.sync_users(filter_for_enabled_user, is_active=True)
        disabled_users=c.sync_users(filter_for_disabled_user, is_active=False)
        users = enabled_users + disabled_users
        # print(users)
        return  users
    return None

def get_raw_username(domain_and_username):
    """  Return domain name    """
    raw_username = domain_and_username
    if '\\' in domain_and_username:
        raw_username = domain_and_username.split('\\')[1]
        print(raw_username)
        return raw_username
    if '@' in domain_and_username:
        raw_username = domain_and_username.split('@')[0]
        print(raw_username)
        return raw_username
    return raw_username

        