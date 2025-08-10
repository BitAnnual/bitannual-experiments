import os
import hashlib
import ecdsa
import base58

private = ""
public = ""
wallet = ""

def generate():
  privbyte = os.urandom(32)
  private = privbyte.hex()

  signing = ecdsa.SigningKey.from_string(privbyte, curve=ecdsa.SECP256k1)
  verifying = signing.verifying_key
  pubbyte = verifying.to_string()
  public = pubbyte.hex()

  salt = os.urandom(10)
  sha = hashlib.sha256(pubbyte + salt).digest()
  b58 = base58.b58encode(sha).decode()

  wallet = "Ba" + b58 + "aB"
