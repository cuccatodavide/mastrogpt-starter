#--kind python:default
#--web true
#--param OLLAMA_HOST $OLLAMA_HOST
#--param AUTH $AUTH
#--param STREAM_HOST $STREAM_HOST
#--param STREAM_PORT $STREAM_PORT
import api
def main(args):
  return { "body": api.api(args) }
