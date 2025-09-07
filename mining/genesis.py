gdifficulty = 0
gtarget = 0

def gdiff():
  global gdifficulty, gtarget
  gdifficulty = 1000000000 * 31536000
  gtarget = 2**256 // gdifficulty
