from django.core import signing
def encrypt_pass(raw_pass):
    hash_pass = signing.dumps({"password": raw_pass})
    print(hash_pass)
    return hash_pass


def decrypt_pass(hash_pass):
    raw_pass = signing.loads(hash_pass)
    raw_pass = (raw_pass['password']).encode('utf-8').decode("utf-8")
  
    return raw_pass
