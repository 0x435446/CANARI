import requests

x = requests.get('http://92.81.21.126/', params={"lenghtlenght":100 , "width":50})
print(x.status_code)