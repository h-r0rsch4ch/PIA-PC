from correos import *
from webScrapping import *
from hunter import *
from metadatos import *
from vTotal import *

import argparse
import os
import logging

logging.basicConfig(filename="historialMain.log",level=logging.INFO, format="%(levelname)s:%(asctime)s:%(message)s")

parser = argparse.ArgumentParser(description="***Se muestran los comandos necesarios para ejecutar las herramientas de CiberSeguridad***")

#Realizar WebScrapping de un sitio web y descargar imagenes
parser.add_argument("-w", "--webScrapping", help="Iniciar WebScrapping de imagenes y descargarlas \n", action="store_true")

#Mandar correo con las imagenes descargadas de WebScrapping
parser.add_argument("-c","--correos", help="Enviar correo con las imagenes descargadas de WebScrapping \n", action="store_true")

#Guardar en txt el cache del cliente DNS
parser.add_argument("-d","--dns", type=str, help="Dirrecion IP a escanear")

#Checar correos con ApiHunter
parser.add_argument("-k","--keyHunter", type=str, help="Ingresar la key de Hunter")
parser.add_argument("-t", "--txtHunter", type=str, help="Archivo txt con los correos a buscar" )

#Metadata de imagenes y archivos pdf
parser.add_argument("-m","--metadatos", type=str, help="Ingrese la ruta de la carpeta con los archivos a analizar")


#Herramienta de VirusTotal
parser.add_argument('-a', '--analisis', type=str, help="Llave api de VirusTotal para analizar urls")
parser.add_argument('-tv','--txtvirus', type=str,help="Nombre del archivo con las urls")


parser = parser.parse_args()

#Opciones
if __name__=="__main__":

    if parser.webScrapping:
        print("Realizando WebScrapping...")
        Imagenes(url="https://www.uanl.mx/noticias/" ,carpeta="ImagenesWeb")
    
    elif parser.correos:
        print("Enviando correo con imagenes descargadas...")
        enviarcorreo()

    elif parser.keyHunter:
        print("Buscando correos electronicos en sitios web...")
        apiHunter(parser.txtHunter, parser.keyHunter)
        print("Archivo txt con resultados creado...")

    elif parser.dns:
        logging.info("Chequeo de DNS Iniciado...")
        directory = os.getcwd()
        os.system(f"powershell -ExecutionPolicy ByPass ./dns.ps1 -TargetFolder \"{directory}\"")
        logging.info("Chequeo de DNS Terminado...")

    elif parser.metadatos:
        logging.info("Analisis de metadatos Iniciado...")
        print("Analizando documentos dentro de la carpeta..")
        metadatosPdf(parser.metadatos)
        metadatosImg(parser.metadatos)
        print("Proceso terminado")
        logging.info("Analisis de metadatos Finalizado...")

    elif parser.analisis:
        print("Iniciando analisis de urls...")
        analizarUrl(parser.txtvirus, parser.analisis)
        print("Analisis de urls terminado...")
