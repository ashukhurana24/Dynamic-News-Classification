
import requests
import json

class mydata:
    def getText(val):
        payload = {'text': val,
                   'token': '04eea67c6ea64ac6917ffd639995ad6d', 'model': '54cf2e1c-e48a-4c14-bb96-31dc11f84eac'}
        responseD = requests.post('https://api.dandelion.eu/datatxt/cl/v1', data=payload)

        print(responseD.json())


