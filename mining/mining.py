from bip32utils import BIP32Key
from Crypto.Hash import RIPEMD
from mnemonic import Mnemonic
from termcolor import colored
import hashlib
import base58
import random
import ecdsa
import json
import time
import os

mnemonics = Mnemonic("english")
signingkey = ""

diff = 2**32 / (1000 * 31536000)
target = (2**224) * ((2**32) - 1) // diff

def addresses():
  global signingkey
  entropy = os.urandom(16)
  phrase = mnemonics.to_mnemonic(entropy)
  seed = mnemonics.to_seed(phrase, passphrase="")

  master = BIP32Key.fromEntropy(seed)
  public = master.PublicKey()
  private = master.PrivateKey().hex()
  signingkey = ecdsa.SigningKey.from_string(bytes.fromhex(private), curve=ecdsa.SECP256k1)
  version = bytes([ord("T")])
  ripemd = RIPEMD.new(master.PublicKey())
  publicHash = ripemd.digest()
  checksum = hashlib.sha256(hashlib.sha256(version + publicHash).digest()).digest()[:4]
  pre = base58.b58encode(version + publicHash + checksum).decode()

  extract = base58.b58decode(pre)
  versions = extract[0:1]
  publichash = extract[1:21]
  checkSum = extract[21:25]

  if hashlib.sha256(hashlib.sha256(versions + publichash).digest()).digest()[:4] == checkSum:
    return "bit" + pre + "annual"
  else:
    return None

def transaction():
  toAddress = addresses()
  fromAddress = addresses()
  amount = random.randint(1, 500)
  timestamp = str(time.time())
  fee = (len(toAddress) + len(fromAddress) + len(str(amount)) + len(timestamp)) * 0.001
  signature = signingkey.sign_digest(hashlib.sha256(toAddress.encode("utf-8") + fromAddress.encode("utf-8") + str(amount).encode("utf-8") + timestamp.encode("utf-8") + str(fee).encode("utf-8")).digest())
  txid = hashlib.sha256(toAddress.encode("utf-8") + fromAddress.encode("utf-8") + str(amount).encode("utf-8") + timestamp.encode("utf-8") + str(fee).encode("utf-8") + signature).digest()
  lengthoftransaction = (len(toAddress) + len(fromAddress) + len(str(amount)) + len(timestamp) + len(str(fee)) + len(signature) + len(txid)) / 8
  metadata = {"to": toAddress, "from": fromAddress, "amount": amount, "time": timestamp, "fee": fee, "signature": signature.hex(), "txid": txid.hex()}
  return txid, lengthoftransaction, metadata

def block():
  max = (2**32) - 1
  version = 1
  height = 0
  if os.path.exists("blockchain.json"):
    with open("blockchain.json", "r") as r:
      heights = json.load(r)
    latest = list(heights.keys())[-1]
    height = read[latest]["height"] + 1
  else:
    height = 1
  nonce = 0
  extraNonce = 0
  timestamp = str(time.time())
  difficultyTarget = target.to_bytes(32, "big")
  prevHash = "0"*64
  lengthofblock = ((64*2) + 1 + len(str(nonce)) + len(timestamp) + len(str(target)) + 1) / 8
  amountoftrans = (2147483648 - lengthofblock) // (transaction()[1] / 8)
  hashes = [transaction()[0] for _ in range(round(amountoftrans))]
  while len(hashes) > 1:
      if len(hashes) % 2 == 1:
          hashes.append(hashes[-1])
      merkles = []
      for h in range(0, len(hashes), 2):
          merkles.append(hashlib.sha256(hashes[h] + hashes[h+1]).digest())
      hashes = merkles
  merkleRoot = hashes[0]
  while nonce < max:
    blockHash = hashlib.sha256(hashlib.sha256(version.to_bytes(4, "big") + height.to_bytes(4, "big") + nonce.to_bytes(32, "big") + extraNonce.to_bytes(32, "big") + timestamp.encode("utf-8") + difficultyTarget + bytes.fromhex(prevHash) + merkleRoot).digest()).hexdigest()
    if int(blockHash, 16) <= target:
      print(colored("Block Has Been Mined After A Whole Year!", "green", attrs=["bold"]))
      blockdata = 
      {
        "header": {"version": version, "prevHash": prevHash, "merkle": merkleRoot.hex(), "timestamp": timestamp, "difficultyTarget": difficultyTarget.hex(), "nonce": nonce, "blockHash": blockHash},
        "body": [transaction()[0] for _ in range(amountoftrans)]
      }
      if os.path.exists("blockchain.json"):
        with open("blockchain.json", "w") as w:
          json.dump(blockData, w, indent=4)
      else:
        with open("blockchain.json", "w") as w:
          json.dump(blockData, w, indent=4)
      block()
  nonce += 1
  if nonce >= max:
    extraNonce += 1

block()
