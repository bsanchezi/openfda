import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", '/drug/label.json?limit=100''&search=substance_name:"ASPIRIN"', None, headers)
#con la función search selecciono la información que debe contener el medicamento
r1 = conn.getresponse()
print(r1.status, r1.reason)
informacion_label = r1.read().decode("utf-8")
conn.close()

label_mejorada = json.loads(informacion_label)
for i in range(len(label_mejorada['results'][0])):
    medicamento=label_mejorada['results'][i]
    print('ID: ', medicamento['id'])

    if (medicamento['openfda']):
        print('Fabricante: ', medicamento['openfda']['manufacturer_name'][0])

