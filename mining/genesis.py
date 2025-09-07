def gdiff():
  global gdifficulty, gtarget
  gdifficulty = hex(1000000000 * 31536000)
  gtarget = hex(2**256 // gdifficulty)
