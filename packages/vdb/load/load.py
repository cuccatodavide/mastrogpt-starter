import packages.vdb.load.vdb_old as vdb_old
import requests
from bs4 import BeautifulSoup
import re

USAGE = f"""Welcome to the Vector DB Loader.
Write text to insert in the DB.
Start with * to do a vector search in the DB.
Start with ! to remove text with a substring.
"""

def concat_chunks(strings: list[str], x: int) -> list[str]:
    """
    Divide la lista `strings` in blocchi di lunghezza x e li unisce con uno spazio.
    Anche l'ultimo blocco (più corto di x) viene unito comunque.
    """
    return [' '.join(strings[i:i+x]) for i in range(0, len(strings), x)]


def tokenize(text):
    tokens = text.split()
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if re.match(r'\d{1,2}[/-]\d{1,2}[/-]\d{4}', token):
            pass
        
        elif re.match(r"\w+'s", token):
            token = re.sub(r"(\w+)'s", r"\1 's", token)
        
        elif re.match(r"\w+'\w+", token):
            token = token.replace("'", "")
        
        elif re.match(r"\w+-\w+", token):
            pass
        
        elif re.match(r"\d+(,\d+)*", token):
            pass
        
        else:
            token = re.sub(r"([^\w\s]+)", r" \1 ", token)
        
        token = re.sub(r"(\w+)\.", r"\1", token)
        token = re.sub(r"(\w+),", r"\1", token)
        token = re.sub(r"U\.S\.A\.", r"U.S.A.", token)
        
        tokens[i] = token
        i += 1
    
    return concat_chunks(tokens, 42)

def load(args):
  
  collection = args.get("COLLECTION", "default")
  out = f"{USAGE}Current colletion is {collection}"
  inp = str(args.get('input', ""))
  db = vdb_old.VectorDB(args)
  
  if inp.startswith("https://"):
    res = requests.get(inp)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    for script in soup(['script', 'style']):
       script.decompose()
    text = soup.get_text(separator=' ')
    tokens = tokenize(text.lower())
    ids = []
    for t in tokens:
      res = db.insert(t)
      ids.extend(res.get("ids", []))
    out = "Inserted: " 
    out += ", ".join([str(x) for x in set(ids)])
    
  elif inp.startswith("*"):
    if len(inp) == 1:
      out ="please specify a search string"
    else:
      res = db.vector_search(inp[1:])
      if len(res) > 0:
        out = f"Found:\n"
        for i in res:
          out += f"({i[0]:.2f}) {i[1]}\n"
      else:
        out = "Not found"
  elif inp.startswith("!"):
    count = db.remove_by_substring(inp[1:])
    out = f"Deleted {count} records."
  elif inp != '':
    res = db.insert(inp)
    out = "Inserted " 
    out += " ".join([str(x) for x in res.get("ids", [])])

  return {"output": out}
  
