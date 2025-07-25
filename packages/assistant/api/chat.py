import os
import openai
import json, socket, traceback

MODEL = "llama3.1:8b"
ROLE = "system:You are an helpful assistant."

class Chat:
    def __init__(self, args):
        
        host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
        api_key = args.get("AUTH", os.getenv("AUTH"))
        base_url = f"https://{api_key}@{host}/v1"
        
        self.client = openai.OpenAI(
            base_url = base_url,
            api_key = api_key,
        )
        
        self.sock = args.get("STREAM_HOST",  os.getenv("STREAM_HOST", 'localhost'))
        self.port = int(args.get("STREAM_PORT", os.getenv("STREAM_PORT", '8000')))
        self.messages = []
        self.add(ROLE)
    
    def stream(self, lines):
        out = ""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.sock, self.port))
            try:
                for line in lines:
                    msg = {"output": line.choices[0].delta.content}
                    s.sendall(json.dumps(msg).encode("utf-8"))
                    out += str(line)
            except Exception as e:
                traceback.print_exc(e)
                out = str(e)
        return out

    def add(self, msg):
        [role, content] = msg.split(":", maxsplit=1)
        self.messages.append({
            "role": role,
            "content": content,
        })
    
    def complete(self):
        res = self.client.chat.completions.create(
            model=MODEL,
            messages=self.messages,
            stream=True,
        )
        try: 
            out = self.stream(res)
            self.add(f"assistant:{out}")
        except Exception as e:
            out =  "error: " + str(e)
        return out
    
