import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")   #pagina para acceder a la API REST de openFDA
conn.request("GET", "/drug/label.json", None, headers)   #recurso al que se quiere acceder
r1 = conn.getresponse() #respuesta de la info
print(r1.status, r1.reason)  #200 OK   #comprobar que funciona
informacion_label = r1.read().decode("utf-8")  #guardamos en una variable toda la información consultada
conn.close()

label_mejorada = json.loads(informacion_label)  #mejoramos la info obtenida
medicamento=label_mejorada['results'][0]   #nos quedamos solo con la info del apartado results, quitando meta

print('ID: ', medicamento['id'])   #seleccionamos la informacion requerida fijándonos en la indexacion en el archivo
print('Proposito: ', medicamento['purpose'][0])
print('Fabricante(s): ', medicamento['openfda']['manufacturer_name'][0])



