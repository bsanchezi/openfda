import http.client
import json

headers = {'User-Agent': 'http-client'}
numero_salto = 0
while True:

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", '/drug/label.json?limit=100&skip=' +str(numero_salto)+'&search=substance_name:"ASPIRIN"', None, headers)
    #con la función skip, selecciono de 100 en 100 los medicamentos gracias al bucle while
    #el bucle sólo para cuando hay menos de 100, es decir, cuando ya no hay más después
    #con la función search selecciono la información que debe contener el medicamento
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    informacion_label = r1.read().decode("utf-8")
    conn.close()


    label_mejorada = json.loads(informacion_label)
    print(label_mejorada)
    for i in range(len(label_mejorada['results'][0])):
        medicamento=label_mejorada['results'][i]
        print('ID: ', medicamento['id'])

        if (medicamento['openfda']):
            print('Fabricante: ', medicamento['openfda']['manufacturer_name'][0])
    if (len(label_mejorada['results'])<100):
        break
    numero_salto= numero_salto + 100 #esta variable nos ayuda a leer los medicamentos de 100
                                   #de manera que, al leerse los 100 primeros, se salta estos y pasa
                                   #a los 100 siguientes hasta que no quedan más y cae en el break
