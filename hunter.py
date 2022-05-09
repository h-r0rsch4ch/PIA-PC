import json
import requests
import logging

# Apikey Hunter (50 usos maximo = 7423f7ac035e69bd7552283469acf1f4f4bdd564)

def apiHunter(txt, key):
    logging.info('Busqueda de correos iniciada...')
    apikey = key
    
    
    correo = open(txt, "r")
    sitios = open("resultadosHunter.txt", "w")

    
    for line in correo:
        email = line
        # Verificamos el email con la api de hunter
        page = requests.get("https://api.hunter.io/v2/email-verifier?"
                            "email="+email+"&api_key="+apikey)
        # Registramos la conexión
        sitios.write("La respuesta HTTP para " + email + " es " +
                str(page.status_code) + "\n")
        # Revisamos los datos obtenidos
        hunter = json.loads(page.content)
        for key in hunter["data"]:
            # Buscamos las posibles fuentes donde se encuentre el email
            if key == "sources":
                sitios.write("El correo se encontró en " +
                        str(len(hunter["data"]["sources"]))+" sitios web:\n")
                # Registramos cada fuente
                for sourc in range(len(hunter["data"]["sources"])):
                    url = ("http://" +
                        hunter["data"]["sources"][sourc]["domain"])
                    pagestat = requests.get(url)
                    # Se revisa la conexion web con el servidor
                    if pagestat.status_code == 200:
                        sitios.write(str(sourc) + "\t" + url + "\tstatus: " +
                                str(pagestat.status_code) + "\n")
                    else:
                    #En caso de error se imprime el error de conexion 401
                        sitios.write(str(sourc) + "\t" + url + "\tstatus: " +
                                str(pagestat.status_code) +
                                " Falló en conexion" + "\n")
        sitios.write("\n")
    logging.info('Búsqueda de correos terminada')
    # Guardamos los txt
    correo.close()
    sitios.close()
    