import re, os, requests as req
#MODEL = "llama3.1:8b"
MODEL = "phi4:14b"

USAGE="""Let me generate a chess puzzle for you, what do you want in it?"""

FORM = [
  {
    "name": "pieces",
    "label": "What pieces do you want in the puzzle?",
    "type": "radio",
    "required": "true",
    "options": ["Queen", "Rook", "Knight", "Bishop"]
  }
]


def chat(args, inp):
  host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
  auth = args.get("AUTH", os.getenv("AUTH"))
  url = f"https://{auth}@{host}/api/generate"
  msg = { "model": MODEL, "prompt": inp, "stream": False}
  res = req.post(url, json=msg).json()
  out = res.get("response", "error")
  return  out
 
def extract_fen(out):
  pattern = r"([rnbqkpRNBQKP1-8]+\/){7}[rnbqkpRNBQKP1-8]+"
  fen = None
  m = re.search(pattern, out, re.MULTILINE)
  if m:
    fen = m.group(0)
  return fen

def puzzle(args):
  inp = args.get("input", "")
  res = {}
  if inp == "":
     out = USAGE
     res['form'] = FORM
  
  elif type(inp) is dict and "form" in inp:
    data = inp["form"]
    for field in data.keys():
      print(data[field])

    inp = f"""generate a chess puzzle in FEN format, put the following piece in the puzzle: a white {data['pieces']}."""
    print(inp)
    out = chat(args, inp)
    fen = extract_fen(out)
    if fen:
       print(fen)
       res['chess'] = fen
    else:
      out = "Bad FEN position."

  elif inp != "":
    out = chat(args, inp)

  res['output'] = out
  print(res)
  return res
