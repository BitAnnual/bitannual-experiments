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
  return diff256

t = (2**256 - 1) / diff()
target = t.to_bytes(32, bytesorder="big")
prevHash = rng()
merkle = rng()
ti = time.time()
timestamp = ti.to_bytes(32, bytesorder="big")
version = 1
difficulty = diff()
targ = target


def pseudoblock():
  nonce = random.randint(1, 2**32)
  blockHash = hashlib.sha256(prevHash + merkle + timestamp + version + difficulty + target + nonce).hexdigest()
  return blockHash

def mine():
  yourHash = pseudoblock()
  while yourHash > target:
    yourHash = pseudoblock()
    mine()
  print("SOLVED")
  
  
  
