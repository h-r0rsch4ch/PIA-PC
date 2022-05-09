from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image
from PyPDF2 import PdfFileReader
import os
import logging

#Saca metadatos de archivos pdf y jpg por igual
def metadatosPdf(carpeta):
    logging.info("Busqueda de Metadatos(PDF) Iniciada...")
    try:
        # Declaramos un path a la carpeta
        ruta = carpeta
        os.chdir(ruta)
        for root, dirs, files in os.walk(".", topdown=False):
            # Buscamos todos los archivos disponibles
            for name in files:
                # Obtenemos la extensión de su nombre
                ext = name.lower().rsplit('.', 1)[-1]
                if ext in ['pdf']:
                    # Buscando info en pdf
                    pdfFile = PdfFileReader(open(ruta+os.path.sep+name, 'rb'))
                    titlePdf = name.rsplit('.', 1)[0]
                    # Obtenemos el nombre del pdf para el reporte
                    titleTxt = (str(titlePdf) + ".txt")
                    docInfo = pdfFile.getDocumentInfo()
                    # Guardar informacion en txt
                    file = open(titleTxt, 'w')
                    file.write("Título: " + str(pdfFile.documentInfo.title))
                    file.write("\n")
                    file.write("Páginas: " + str(pdfFile.getNumPages()))
                    file.write("\n")
                    file.write("Tipo: " + str(type(docInfo)))
                    file.write("\n")
                    for metaItem in docInfo:
                        file.write('[+] ' + metaItem + ':' + docInfo[metaItem])
                        file.write("\n")
                    logging.info('Búsqueda de metadatos(pdf) terminada')
                    # Guardamos la información encontrada
                    file.close()
    except:
        logging.warning('Error en búsqueda de metadatos(pdf)')


def decode_gps_info(exif):
    gpsinfo = {}
    if 'GPSinfo' in exif:
        Nsec = exif['GPSInfo'][2][2]
        Nmin = exif['GPSInfo'][2][1]
        Ndeg = exif['GPSInfo'][2][0]
        Wsec = exif['GPSInfo'][4][2]
        Wmin = exif['GPSInfo'][4][1]
        Wdeg = exif['GPSInfo'][4][0]
        if exif['GPSInfo'][1] == 'N':
            Nmult = 1
        else:
            Nmult = -1
        if exif['GPSInfo'][1] == 'E':
            Wmult = 1
        else:
            Wmult = -1
        # Calculamos las coordenadas
        Lat = Nmult * (Ndeg + (Nmin + Nsec/60.0)/60.0)
        Lng = Wmult * (Wdeg + (Wmin + Wsec/60.0)/60.0)
        exif['GPSInfo'] = {"Lat": Lat, "Lng": Lng}


def get_exif_metadata(image_path):
    ret = {}
    # Analizamos la informacion de la etiqueta
    image = Image.open(image_path)
    if hasattr(image, '_getexif'):
        exifinfo = image._getexif()
        # Registramos los exif en ret
        if exifinfo is not None:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
    decode_gps_info(ret)
    return ret


def metadatosImg(carpeta):
    logging.info("Búsqueda de metadatos(img) Iniciada..")
    try:
        # Definimos un path a la carpeta
        ruta = carpeta
        os.chdir(ruta)
        for root, dirs, files in os.walk(".", topdown=False):
            # Revisamos los archivos disponibles
            for name in files:
                # Obtenemos la extensión de cada archivo
                ext = name.lower().rsplit('.', 1)[-1]
                if ext in ['jpg', 'png', 'img']:
                    # Obtenemos el nombre para el archivo
                    os.path.join(root, name)
                    titleImg = name.rsplit('.', 1)[0]
                    titleTxt = (str(titleImg) + ".txt")
                    # guardando informacion en txt
                    file = open(titleTxt, "w")
                    try:
                        # Intentamos obtener sus metadatos
                        exifData = {}
                        exif = get_exif_metadata(name)
                        for metadata in exif:
                            # Guardamos los metadatos en el reporte
                            file.write(
                                "Metadata: %s - Value: %s " % (
                                    str(metadata), str(exif[metadata])))
                            file.write("\n")
                        logging.info('Búsqueda de metadatos(img) Terminada..')
                    except:
                        logging.warning('Error en búsqueda de metadatos(img)')
    except:
        logging.warning('Error en búsqueda de metadatos(img)')
