from requests import get, post, delete, put
import json

print(put('http://127.0.0.1:8080/films/1').json())
