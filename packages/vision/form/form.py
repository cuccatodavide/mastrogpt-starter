import vision2 as vision
from bucket import Bucket 
import base64
from datetime import datetime


USAGE = "Please upload a picture and I will tell you what I see"
FORM = [
  {
    "label": "Load Image",
    "name": "pic",
    "required": "true",
    "type": "file"
  },
]

def form(args):
  res = {}
  out = USAGE
  buc = Bucket(args)
  print(f"Bucket: {buc.bucket}")
  inp = args.get("input", "")

  if type(inp) is dict and "form" in inp:
    img = inp.get("form", {}).get("pic", "")
    img_key = datetime.now().strftime('%Y%m-%d%H-%M%S')
    print(f"Image key: {img_key}")
    ret = buc.write(img_key, base64.standard_b64decode(img))
    print(f"Upload result: {ret}")
    print(f"uploaded size {len(img)}")
    vis = vision.Vision(args)
    out = vis.decode(img)
    url = buc.exturl(img_key, 3600)
    res['html'] = f"<img src='{url}'>"
  res['form'] = FORM
  res['output'] = out
  print(res)
  return res
