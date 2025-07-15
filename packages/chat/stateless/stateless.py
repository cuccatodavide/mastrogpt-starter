import os, requests as req, json, socket

MODEL="llama3.1:8b"
#MODEL="deepseek-r1:32b"

def url(args):
  host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
  auth = args.get("AUTH", os.getenv("AUTH"))
  base = f"https://{auth}@{host}"
  return f"{base}/api/generate"

import json, socket, traceback
def stream(args, lines):
  sock = args.get("STREAM_HOST")
  port = int(args.get("STREAM_PORT"))
  out = ""
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((sock, port))
    try:
      for line in lines:
        #print(line, end='')     
        dec = json.loads(line.decode("utf-8")).get("response", "")
        msg = {"output": dec}
        out += dec
        s.sendall(json.dumps(msg).encode("utf-8"))
    except Exception as e:
      traceback.print_exc(e)
      out = str(e)
  return out

def stateless(args):
  llm = url(args)
  inp = args.get("input", "")
  if inp != "":
    model = "llama3.1:8b" if inp == 'llama' else "deepseek-r1:32b"
    inp = "who are you?"
    out = f"Welcome to {model}"
    #msg = { "model": model, "prompt": inp, "stream": True }
    #lines = req.post(llm, json=msg, stream=True).iter_lines()
    #out = stream(args, lines)
  else:
    out = "con chi vuoi parlare?"
  return { "output": out, "streaming": False}
