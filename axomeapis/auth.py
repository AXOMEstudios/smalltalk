from requests import post

cache = {}

def login(token):
  if token in cache.keys(): return cache[token]
  x = post("https://auth.axome.repl.co/check",{"usr": token}).text
  if len(x) > 20:
    raise Exception("The AXOME server rejected the given token or did not find it.")
  cache[token] = x
  return x

def logout(token):
  x = cache[token]
  del cache[token]
  return x
  
def getUser(token):
  if token in cache.keys(): return cache[token]
  x = post("https://auth.axome.repl.co/check",{"usr": token}).text
  if len(x) > 20:
    raise Exception("The AXOME server rejected the given token or did not find it.")
  cache[token] = x
  return x