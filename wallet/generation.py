from bip32utils import BIP32Key
from Crypto.Hash import RIPEMD
from mnemonic import Mnemonic
from termcolor import colored
import hashlib
import base58
import time
import os

wallet = ""
private = ""
public = ""
seedphrase = ""
obj = Mnemonic("english")

def gen():
  global wallet, private, public, seedphrase

  entropy = os.urandom(16)
  seedphrase = obj.to_mnemonic(entropy)
  seed = obj.to_seed(seedphrase, passphrase="")

  master = BIP32Key.fromEntropy(seed)
  private = master.PrivateKey().hex()
  public = master.PublicKey().hex()

  testnet = bytes([0x54])
  #mainnet = bytes([0x4D])
  ripemd = RIPEMD.new(master.PublicKey())
  publicHash = ripemd.digest()
  checksum = hashlib.sha256(hashlib.sha256(testnet + publicHash).digest()).digest()[:4]

  prewallet = base58.b58encode(testnet + publicHash + checksum).decode()

  extraction = base58.b58decode(prewallet)
  version = extraction[0:1]
  publichash = extraction[1:21]
  checkSum = extraction[21:25]
  if hashlib.sha256(hashlib.sha256(version + publichash).digest()).digest()[:4] == checkSum:
    wallet = "bit" + prewallet + "annual"
    return "Valid"
  else:
    return "Invalid"

gen()

if gen() == "Valid":
        print(colored(f"PRIVATE KEY: {private}", "green", attrs=["bold"]))
        print(colored(f"PUBLIC KEY: {public}", "green", attrs=["bold"]))
        print(colored(f"WALLET ADDRESS: {wallet}", "green", attrs=["bold"]))
        print(colored(f"MNEMONIC PHRASE: {seedphrase}", "green", attrs=["bold"]))
else:
    print(colored("INVALID CHECKSUM, REGENERATING...", "red", attrs=["bold"]))
    time.sleep(2)
    gen()
