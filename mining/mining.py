import hashlib
import time
import os
import random

def rng():
  rngd = os.urandom(32)
  sharng = hashlib.sha256(rngd).digest()
  return sharng

def diff():
  ranges = random.randint(1, 32)
  drn = os.urandom(ranges)
  diff256 = hashlib.sha256(drn).hexdigest()
  return int(diff256, 16)

t = (2**256 - 1) / diff()
target = t.to_bytes(32, byteorder="big")
prevHash = rng()
merkle = rng()
ti = time.time()
timestamp = int(ti).to_bytes(8, byteorder="big")
v = 1
version = v.to_bytes(4, byteorder="big")
difficulty = diff()
targ = target


def pseudoblock():
  nun = random.randint(1, 2**32)
  nonce = nun.to_bytes(4, byteorder="big")
  blockHash = hashlib.sha256(prevHash + merkle + timestamp + version + difficulty + target + nonce).hexdigest()
  return blockHash

def mine():
  yourHash = pseudoblock()
  while yourHash > target:
    yourHash = pseudoblock()
    mine()
  print("SOLVED")
  
  
  
