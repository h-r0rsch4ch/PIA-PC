import smtplib 
import getpass 
import imghdr 
import logging
import os

from email.message import EmailMessage

def enviarcorreo():
	logging.info("Envio de Correo Iniciado...")
	try:
		subject = input("Introduzca el asunto del correo: ")
		sender_email = "prueba105pc@gmail.com"
		receiver_email = input("Introduzca el destinatario: ")
		password = getpass.getpass("Introduzca la contraseña:")

		message = EmailMessage()
		message["From"] = sender_email
		message["To"] = receiver_email
		message["Subject"] = subject

		#Se necesita ingresar la ruta completa de las imagenes
		Files = ["C:\\Users\\Jair\\Desktop\\Tareas\\PC\\PIA\\PIA-PC-main\\img1.jpg",
		"C:\\Users\\Jair\\Desktop\\Tareas\\PC\\PIA\\PIA-PC-main\\img2.jpg",
		"C:\\Users\\Jair\\Desktop\\Tareas\\PC\\PIA\\PIA-PC-main\\img3.jpg",
		"C:\\Users\\Jair\\Desktop\\Tareas\\PC\\PIA\\PIA-PC-main\\img4.jpg",
		"C:\\Users\\Jair\\Desktop\\Tareas\\PC\\PIA\\PIA-PC-main\\img5.jpg",
		"C:\\Users\\Jair\\Desktop\\Tareas\\PC\\PIA\\PIA-PC-main\\img6.jpg",
		"C:\\Users\\Jair\\Desktop\\Tareas\\PC\\PIA\\PIA-PC-main\\img7.jpg"] 

		#asigna el nombre a los archivos a enviar
		cont = 1	
		for file in Files: 
			with open(file, "rb") as f:
				file_data = f.read()
				file_type = imghdr.what(f.name)
				file_name = "img" + str(cont) + ".jpg"
				cont+=1   
			message.add_attachment(file_data, maintype="image", subtype=file_type, filename=file_name)

		# Aqui se envia el correo electronico 
		with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
			server.login(sender_email, password)
			server.send_message(message)
		print("Correo enviado con exito a: %s" % (receiver_email))
	except:
		()
		logging.warning("Error en enviar correo...")
	logging.info("Envio de Correo Terminado...")
