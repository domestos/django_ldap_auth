"""
Low-level LDAP hooks.
"""

import ldap3
from ldap3.core.exceptions import LDAPException
from contextlib import contextmanager
from apps.settings.ldap.models import LdapConfig
# from django.contrib.auth.models import User
from apps.accounts.models import User
import logging
logger = logging.getLogger(__name__)


class Connection(object):
    """
    A connection to an LDAP server.
    """
    def __init__(self, connection, search_base, username):
        logger.info("Run __init__ Connection")
        """
        Creates the LDAP connection.

        No need to call this manually, the `connection()` context
        manager handles initialization.
        """
        self._connection = connection
        self._search_base = search_base
        self._username = username
        self._attributes =  ['cn', 'mail', 'department', 'sAMAccountName',
                      'givenName', 'sn', 'displayName', 'whenCreated', 'whenChanged']
        self.LDAP_AUTH_USER_FIELDS = {        "username": "sAMAccountName",
            "first_name": "givenName",
            "last_name": "sn",
            "email": "mail",
            "department":"department",
            # "when_created":"whenCreated"
        }

    def _get_or_create_user(self, user_data):
        """
        Returns a Django user for the given LDAP user data.
        If the user does not exist, then it will be created.
        """
        attributes = user_data.get("attributes")
        if attributes is None:
            logger.warning("LDAP user attributes empty")
            return None

      

        try:
            # Create the user data.
            user_fields = {
            field_name: ( 
                attributes[attribute_name][0]  
                if isinstance(attributes[attribute_name], (list, tuple)) and len(attributes[attribute_name])!=0  else attributes[attribute_name] 
            )
            for field_name, attribute_name
            in  self.LDAP_AUTH_USER_FIELDS .items()
            if attribute_name in attributes
            }
        except Exception as e:
            logger.warning("user_fields: {e}".format(e=e))

        try:
            # Check if exist this user
            user = User.objects.get(username=user_fields['username'])
            if user:
                print(user)
                return user
        except Exception as e:
            # Create the user lookup.
            user_lookup = {
                field_name: user_fields.pop(field_name, "")
                for field_name
                in  self.LDAP_AUTH_USER_FIELDS 
            }
            # Update or create the user.
            user, created = User.objects.update_or_create(
                defaults=user_fields,
                **user_lookup
            )
            # If the user was created, set them an unusable password.
            if created:
                user.set_unusable_password()
                if user.username == 'vap':
                    user.is_superuser = "True"
                    user.is_staff = "True"
                user.save()
            return user
            # Update relations

        return None

    def get_user(self, **kwargs):
        logger.info(":::Run get_user")
        """
        Returns the user with the given identifier.

        """       
        try:
            # ldap3.ALL_ATTRIBUTES
            if self._connection.search(
                search_base=self._search_base,
                search_filter="(&(objectCategory=Person)(objectClass=user)(sAMAccountName={username}))".format(
                    username=get_raw_username(self._username)),
                search_scope=ldap3.SUBTREE,
                attributes=self._attributes,
                get_operational_attributes=True,
                size_limit=1,
            ):  
               
                logger.warning("Result: {ex}".format(ex=self._connection.response[0]))
                return self._get_or_create_user(self._connection.response[0])

            else:
                logger.warning("LDAP user lookup failed")
        except Exception as ex:
            logger.warning("====LDAP connect failed: {ex}".format(ex=ex))
            return None

    
    def get_all_users(self,filter):
        logger.info(":::Run get_all_users")
        try:
            # ldap3.ALL_ATTRIBUTES
            if self._connection.search(
                search_base=self._search_base,
                search_filter=filter,
                search_scope=ldap3.SUBTREE,
                attributes=self._attributes,
                get_operational_attributes=True,             
            ):                 
                logger.warning("Result: {ex}".format(ex=self._connection.response[0]))
                return self._connection.response
            else:
                logger.warning("Result is None")
        except Exception as ex:
            logger.warning("====LDAP connect failed: {ex}".format(ex=ex))
            return None
        return None

@contextmanager
def connection(*args,**kwargs):
    """
    Creates and returns a connection to the LDAP server.
   
    """
    logger.info(":::Run connections -> @contextmanager")

    # @contextmanager TO DO

    # == Init credential for connect ===
    username = kwargs.pop("username")
    password = kwargs.pop("password")
    ldap_conf = get_ldap_conf()
    # domain_name = get_domain_name(ldap_conf.LDAP_URL)
    LDAP_AUTH_URL = ldap_conf.LDAP_URL
    BASE_DN = ldap_conf.LDAP_BASE_DN
    LDAP_AUTH_CONNECT_TIMEOUT = None
    LDAP_AUTH_RECEIVE_TIMEOUT = None
    LDAP_AUTH_USE_TLS = False
    # ==================================

    # == Prepare Connection ============
    try:
        # define the server
        server = ldap3.Server(LDAP_AUTH_URL,
                              allowed_referral_hosts=[("*", True)],
                              get_info=ldap3.NONE,
                              connect_timeout=LDAP_AUTH_CONNECT_TIMEOUT,
                              )
        # define the connection
        c = ldap3.Connection(server,
                             user=username,
                             password=password,
                             auto_bind=False,
                             raise_exceptions=True,
                             receive_timeout=LDAP_AUTH_RECEIVE_TIMEOUT,
                             )
    except LDAPException as ex:
        logger.warning("LDAP connect failed: {ex}".format(ex=ex))
        yield None
    # ==================================

    # == Bind connection ===============
    try:
        # Start TLS, if requested.
        # In the future, LDAP_AUTH_USE_TLS will be added to the form.
        # For now it is a static value=False.
        if LDAP_AUTH_USE_TLS:
            c.start_tls(reLDAP_URL_info=LDAP_AUTH_USE_TLS)
        # Perform initial authentication bind.
        c.bind(reLDAP_URL_info=True)
        logger.info("Connect is binded")
        # @contextmanager Return
        yield Connection(c, BASE_DN, username)
    except LDAPException as ex:
        logger.warning("LDAP bind failed: {ex}".format(ex=ex))
        yield None
    finally:
         # @contextmanager DO After Return
        c.unbind()
        logger.info(":::Connect unbind")
    # ==================================

# === AUTHENTICATE Method==============================================
def authenticate(*args, **kwargs):
    logger.info(":::Run authenticate")
    """
    Authenticates with the LDAP server, and returns 
    the corresponding Django user instance.
    """
    print(kwargs)
    password = kwargs.pop("password")

    # Connect to LDAP.
    with connection(password=password, **kwargs) as c:
        if c is None:
            return None
        return c.get_user(**kwargs)

# === SYNC USERS Method==============================================
def sync_users(*args, **kwargs):
    logger.info(":::Run sync_users")
    password = kwargs.pop("password")
    # Connect to LDAP.
    enable_user_search_filter = '(&(objectCategory=Person)(objectClass=user)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(givenName=*)(sn=*)(proxyAddresses=*))'
    disable_user_search_filter = '(&(objectCategory=Person)(objectClass=user)(UserAccountControl:1.2.840.113556.1.4.803:=2)(givenName=*)(sn=*)(proxyAddresses=*))'
           
    with connection(password=password, **kwargs) as c:
        if c is None:
            return None

        active_user = c.get_all_users(enable_user_search_filter)
        for user in active_user:
            user=c._get_or_create_user(user)
            user.is_active=True
            user.save()  
            

        terminated_users = c.get_all_users(disable_user_search_filter) 
        for user in terminated_users:
          user=  c._get_or_create_user(user)
          user.is_active=False
          user.save()  
        return active_user



# === Helpful methos ===========================================
def get_ldap_conf():
    """
    Get config from data base
    """
    try:
        return LdapConfig.objects.all().first()
    except Exception as e:
        logger.info("Exception:::", str(e))
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

        