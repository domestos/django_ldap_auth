"""
Django authentication backend.
"""

from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from .ldap_con import *
from apps.settings.ldap.models import LdapConfig


import logging
logger = logging.getLogger(__name__)

class LDAPBackend(ModelBackend):

    logger.info("Run backend LDAP AUTH")
    """
    An authentication backend that delegates to an LDAP
    server.

    User models authenticated with LDAP are created on
    the fly, and syncronised with the LDAP credentials.
    """

    def is_enabled_ldap_auth(self):
        """
        Return True if LDAP Auth is Enabled
        """
        try:
            return LdapConfig.objects.all().first().LDAP_AUTH
        except Exception as e:
            logger.info("Exception:::", str(e))
            return False


    def authenticate(self, *args, **kwargs):
        #need       
        if self.is_enabled_ldap_auth():
            return authenticate(*args, **kwargs)
        else:
            logger.info("LDAP AUTH is Disabled")
            return None



# class EmailAuthBackend(object):
#     """
#     Authenticate using e-mail account.
#     """

#     def authenticate(self, username=None, password=None):
#         try:
#             user = User.objects.get(email=username)
#             if user.check_password(password):
#                 return user
#             return None
#         except User.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None
