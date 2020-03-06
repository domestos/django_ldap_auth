from django.db import models
from django.core import signing

# from .util.encryptions_pass import encrypt_pass
# Create your models here.

# rename later as LdapCredentials
class LdapConfig(models.Model):
    LDAP_URL = models.CharField(max_length=50)
    LDAP_USER = models.CharField(max_length=30)
    LDAP_PASS = models.CharField(max_length=30)
    LDAP_BASE_DN = models.CharField(max_length=250)
    LDAP_AUTH = models.BooleanField(default='False')
    
    def __str__(self):            
            return self.LDAP_URL
    
    def encrypt_pass(self, raw_pass):
        hash_pass = signing.dumps({"password": raw_pass})
        print(hash_pass)
        return hash_pass


    def decrypt_pass(self, hash_pass):
        raw_pass = signing.loads(hash_pass)
        raw_pass = (raw_pass['password']).encode('utf-8').decode("utf-8")    
        return raw_pass


    def save(self, **kwargs):
        self.LDAP_PASS = self.encrypt_pass(self.LDAP_PASS)
        super(LdapConfig, self).save()


    # def get_absolute_url(self):
    #     return reverse("update_equipment_url", kwargs={'pk':self.pk} )