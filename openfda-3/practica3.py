import http.server
import socketserver
import http.client
import json


PORT = 8011


lista_medicamentos = []
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)

r1 = conn.getresponse()
print(r1.status, r1.reason)
informacion_label = r1.read().decode("utf-8")
conn.close()

label_mejorada = json.loads(informacion_label)
for i in range(len(label_mejorada['results'])):
    medicamento = label_mejorada['results'][i]
    if (medicamento['openfda']):
        print('El nombre genérico del medicamento es: ', medicamento['openfda']['generic_name'][0])
        lista_medicamentos.append(medicamento['openfda']['generic_name'][0])
        #creamos una lista vacía a la que le añadiremos la información requerida, en este caso, el nombre
        #genérico de los 10 primeros medicamentos


#Creamos nuestro manejador a partir de la herencia de un manejador ya completo
#Podremos añadir al nuestro aquellas funciones que nos sean necesarias
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    # GET. Este metodo se invoca automaticamente cada vez que hay una
    # peticion GET por HTTP. El recurso que nos solicitan se encuentra
    # en self.path
    def do_GET(self):
        #establecemos la línea de estado de la respuesta
        self.send_response(200)

        #colocaremos aquí las cabeceras de la respuesta al cliente para que se pueda entender la
        #comunicación en lenguaje HTML
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content="<html><body style='background-color: orange'>"

        for e in lista_medicamentos:  #por cada medicamento vamos a mandar una respuesta en lenguaje html
            content += e+"<br>"       #que contenga su nombre genérico, separados por un salto de línea

        content+="</body></html>"

        self.wfile.write(bytes(content, "utf8"))
        return


# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("Ya está completa la lista de medicamentos")

