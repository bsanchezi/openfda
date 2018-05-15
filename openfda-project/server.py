import http.server
import http.client
import json
import socketserver

PORT=8000

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET

    def formulario(self): #creamos el formulario que constituye la página principal
        html = """
            <html>
                <head>
                    <title>OpenFDA App</title>
                </head>
                <body>
                    <h1>OpenFDA Client </h1>
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Drug List">
                        </input>
                    </form>
                    --------------------------------------------------
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Drug Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    --------------------------------------------------
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Company List">
                        </input>
                    </form>
                    --------------------------------------------------
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Company Search">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    --------------------------------------------------
                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Warnings List">
                        </input>
                    </form>
                </body>
            </html>
                """
        return html
    def web(self, lista):  #incluimos una lista de puntos con los items necesarios para cada petición
        list_html = """
                                <html>
                                    <head>
                                        <title>OpenFDA Cool App</title>
                                    </head>
                                    <body>   
                                        <ul>
                            """
        for item in lista:
            list_html += "<li>" + item + "</li>"

        list_html += """
                                        </ul>
                                    </body>
                                </html>
                            """
        return list_html
    def resultados_genericos(self, limit=10):  #hacemos una petición a openfda para que nos de todos los datos que los clientes
        conn = http.client.HTTPSConnection("api.fda.gov")  #pueden pedir a nuestro servidor
        conn.request("GET", "/drug/label.json" + "?limit="+str(limit))
        print ("/drug/label.json" + "?limit="+str(limit))
        r1 = conn.getresponse()
        informacion_label = r1.read().decode("utf8")  #tratamos la respuesta en json que nos envía la api para poder trabajar con ello
        label_mejorada = json.loads(informacion_label)
        resultados = label_mejorada['results']
        return resultados
    def do_GET(self):
        recurso_list = self.path.split("?")  #creamos una función que nos ayude a encontrar el número de elementos solicitados escogiendo
        if len(recurso_list) > 1:            #dentro de la información del recurso aquella que nos indica el límite
            recurso = recurso_list[1]
        else:
            recurso = ""

        limit = 1


        if recurso:
            parse_limit = recurso.split("=")
            if parse_limit[0] == "limit":
                limit = int(parse_limit[1])
                print("Limit: {}".format(limit))
        else:
            print("SIN PARAMETROS")



        #diferenciamos entre las opciones del formulario principal según la petición del cliente para enviar una otra información
        if self.path=='/':
            #Mandamos la respuesta de estado
            self.send_response(200)
            #Mandamos las cabeceras
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html=self.formulario()
            self.wfile.write(bytes(html, "utf8"))
        elif 'listDrugs' in self.path:   #para las opciones que son lista se cogen los medicamentos, precacuciones o compañías seleccionadas
            self.send_response(200)      #por el cliente de la lista de todos los resultados que obtenemos de openfda
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            medicamentos = []
            resultados = self.resultados_genericos(limit)
            for resultado in resultados:
                if('generic_name' in resultado['openfda']):
                    medicamentos.append(resultado['openfda']['generic_name'][0])
                else:
                    medicamentos.append('Desconocido')
            resultado_html = self.web(medicamentos)

            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'listCompanies' in self.path:
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            companies = []
            resultados = self.resultados_genericos(limit)
            for resultado in resultados:
                if ('manufacturer_name' in resultado['openfda']):
                    companies.append(resultado['openfda']['manufacturer_name'][0])
                else:
                    companies.append('Desconocido')
            resultado_html = self.web(companies)

            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'listWarnings' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            warnings = []
            resultados = self.resultados_genericos(limit)
            for resultado in resultados:
                if ('warnings' in resultado):
                    warnings.append(resultado['warnings'][0])
                else:
                    warnings.append('Desconocido')
            resultado_html = self.web(warnings)

            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'searchDrug' in self.path:   #para aquellos formularios donde el cliente selecciona un medicamento/compañía, se hace una petición
                                          #nueva a la api de openfda para que nos devuelva una lista con 10 elementos
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            #en este caso pedimos que sean 10 elemento en lugar de 1 como en las listas
            limit = 10
            drug=self.path.split('=')[1]

            drugs = []  #hacemos una petición a la api pidiéndole específicamente que contenga el ingrediente activo que escribe el cliente
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json" + "?limit="+str(limit) + '&search=active_ingredient:' + drug)
            r1 = conn.getresponse()
            data1 = r1.read()
            data = data1.decode("utf8")
            biblioteca_data = json.loads(data)  #analizamos la respuesta mejorando el json que nos envían
            medicamentos_event = biblioteca_data['results']
            for resultado in medicamentos_event:
                if ('generic_name' in resultado['openfda']):
                    drugs.append(resultado['openfda']['generic_name'][0])  #seleccionamos los medicamentos por su nombre genérico, pero
                else:                                                       #sólo los que contenga dicho ingrediente activo
                    drugs.append('Desconocido')

            resultado_html = self.web(drugs)
            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'searchCompany' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            limit = 10
            company=self.path.split('=')[1]
            companies = []
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json" + "?limit=" + str(limit) + '&search=openfda.manufacturer_name:' + company)
            r1 = conn.getresponse()
            data1 = r1.read()
            data = data1.decode("utf8")
            biblioteca_data = json.loads(data)
            medicamentos_event = biblioteca_data['results']

            for event in medicamentos_event:
                companies.append(event['openfda']['manufacturer_name'][0])
            resultado_html = self.web(companies)
            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'redirect' in self.path:
            print("Redirigimos a la página principal")
            self.send_response(301)
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()
        elif 'secret' in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(self.path).encode())
        return



socketserver.TCPServer.allow_reuse_address= True #nos aseguramos de poder reutilizar siempre el puerto 8000

Handler = testHTTPRequestHandler  #creamos nuestro manejador a partir de otra clase ya existente. este handler manejará las peticiones de tipo get

httpd =socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()  #el servidor arranca una vez está todoo configurado

