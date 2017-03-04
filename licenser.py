import rsa
import requests
import datetime
import hashlib
PUBKEY=rsa.PublicKey.load_pkcs1('''
-----BEGIN RSA PUBLIC KEY-----
MEgCQQCkp2ERxNrz43WtDzRJueL21zBfK3sCcThSUOhlcZv54C0ogTbM/ca9oP6X
mTqqyL/AcFTntdMOl9EPhXHrEz2LAgMBAAE=
-----END RSA PUBLIC KEY-----
''')

SERVER='http://xmcp-playground.azurewebsites.net/xkmad_signer'
#SERVER='http://127.0.0.1/xkmad_signer'
APIVER='1'

s=requests.Session()
s.trust_env=False

def sha(data):
    return hashlib.new('sha256',data).hexdigest()

def sign(username,data):
    res=s.post(SERVER,params={'ver':APIVER},json={'username':username,'data':sha(data)})
    return res.content
    
def verify(sign,data):
    return rsa.verify(sha(data).encode(),sign,PUBKEY)
    
    