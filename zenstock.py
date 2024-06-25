import tkinter as tk
from tkinter import *
from tkinter import font 
from PIL import ImageTk, Image
from tkinter import ttk, messagebox

#from tkcalendar import Calendar
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from tkinter import filedialog
import subprocess
import webbrowser
#import json
import os
import re


#----------------------------------------------------------------------------------------------------
    #Creamos una clase para la barra botones de control
#----------------------------------------------------------------------------------------------------
class Botones:
    def __init__(self, func_Agregar,func_Eliminar,func_Actualizar,func_navegar, func_Salir):
        #Funciones que van llamar los botones
        self.func_Agregar=func_Agregar
        self.func_Actualizar=func_Actualizar
        self.func_Eliminar=func_Eliminar
        self.func_navegar=func_navegar
        self.func_salir=func_Salir
        
        #Botones
        self.btn_agregar=None
        self.btn_eliminar=None
        self.btn_actualizar=None
        self.btn_primero=None
        self.btn_anterior=None
        self.btn_siguiente=None
        self.btn_ultimo=None
        self.btn_cerrar=None
        #Imagnes
        self.img_agregar=None
        self.img_guardar=None
        self.img_eliminar=None
        self.img_actualizar=None
        self.img_primero=None
        self.img_anterior=None
        self.img_siguiente=None
        self.img_ultimo=None
        self.img_cerrar=None
        self.img_deshacer=None

    def crear_botones(self,parent,n_col=0,n_row=0,solo_navegar=False):
        
        frm_botones = ttk.Frame(parent)
        frm_botones.grid(row=n_row,column=n_col,padx=5,pady=5)
        #--------------------------------------------------------------------------------------
            #Botones para manejo de acciones de la ventana (agregar-eliminar-actualizar-navegar-salir)
        #--------------------------------------------------------------------------------------
        try: 
            if not solo_navegar:
                self.img_agregar=ImageTk.PhotoImage(Image.open("icons/agregar.png").resize((32,32)))
                self.img_guardar=ImageTk.PhotoImage(Image.open("icons/guardar.png").resize((32,32)))
                self.btn_agregar=ttk.Button(frm_botones,image=self.img_agregar,command=self.func_Agregar)
                self.btn_agregar.grid(column=0,row=0)#Agregar      
            
                self.img_eliminar=ImageTk.PhotoImage(Image.open("icons/eliminar.png").resize((32,32)))
                self.btn_eliminar=ttk.Button(frm_botones, image=self.img_eliminar,command=self.func_Eliminar)
                self.btn_eliminar.grid(column=1,row=0)#Eliminar

                self.img_actualizar=ImageTk.PhotoImage(Image.open("icons/actualizar.png").resize((32,32)))
                self.btn_actualizar=ttk.Button(frm_botones,image=self.img_actualizar,command=self.func_Actualizar)
                self.btn_actualizar.grid(column=2,row=0)#Actualizar
            
            #Botones de navegacion
            self.img_primero=ImageTk.PhotoImage(Image.open("icons/primero.png").resize((32,32)))
            self.btn_primero=ttk.Button(frm_botones,image=self.img_primero,command=lambda:self.func_navegar('Primero'))
            self.btn_primero.grid(column=3,row=0)#Primero

            self.img_anterior=ImageTk.PhotoImage(Image.open("icons/anterior.png").resize((32,32)))
            self.btn_anterior=ttk.Button(frm_botones,image=self.img_anterior,command=lambda:self.func_navegar('Anterior'))
            self.btn_anterior.grid(column=4,row=0)#Anterior

            self.img_siguiente=ImageTk.PhotoImage(Image.open("icons/siguiente.png").resize((32,32)))
            self.btn_siguiente=ttk.Button(frm_botones,image=self.img_siguiente,command=lambda:self.func_navegar('Siguiente'))
            self.btn_siguiente.grid(column=5,row=0)#Siguiente

            self.img_ultimo=ImageTk.PhotoImage(Image.open("icons/ultimo.png").resize((32,32)))
            self.btn_ultimo=ttk.Button(frm_botones,image=self.img_ultimo,command=lambda:self.func_navegar('Ultimo'))
            self.btn_ultimo.grid(column=6,row=0)#Ultimo

            self.img_cerrar=ImageTk.PhotoImage(Image.open("icons/cerrar.png").resize((32,32)))
            self.img_deshacer=ImageTk.PhotoImage(Image.open("icons/deshacer.png").resize((32,32)))
            self.btn_cerrar=ttk.Button(frm_botones,image=self.img_cerrar,command=self.func_salir)
            self.btn_cerrar.grid(column=7,row=0)#Salir

        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
            print(f"Ocurrió un error de E/S: {e}")
    
    def cambiar_imagenes_al_agregar(self):
        self.btn_agregar.config(image=self.img_guardar)
        self.btn_cerrar.config(image=self.img_deshacer)
        
        self.btn_actualizar.config(state=DISABLED)
        self.btn_eliminar.config(state=DISABLED)
        self.btn_primero.config(state=DISABLED)
        self.btn_anterior.config(state=DISABLED)
        self.btn_siguiente.config(state=DISABLED)
        self.btn_ultimo.config(state=DISABLED) 

    def cambiar_imagenes_al_navegar(self):
        self.btn_agregar.config(image=self.img_agregar)
        self.btn_cerrar.config(image=self.img_cerrar)

        self.btn_actualizar.config(state=NORMAL)
        self.btn_eliminar.config(state=NORMAL)
        self.btn_primero.config(state=NORMAL)
        self.btn_anterior.config(state=NORMAL)
        self.btn_siguiente.config(state=NORMAL)
        self.btn_ultimo.config(state=NORMAL)
    
   

def main():

    

    id_usuario_en_session=None
    root=None
    imagenes={}
    indice_actual=0

    agregando_producto= False
    agregando_entrada= False
    agregando_salida= False
    agregando_merma= False
    agregando_usuario= False
    agregando_categoria= False
    agregando_subcategoria= False
    agregando_proveedor= False
    agregando_departamento= False

        
    diccionario_productos={}
    diccionario_entradas={}
    diccionario_salidas={}
    diccionario_mermas={}
    diccionario_usuarios={}
    diccionario_categorias={}
    diccionario_subcategorias={}
    diccionario_proveedores={}
    diccionario_departamentos={}    
    
    lista_productos=[]
    lista_entradas=[]
    lista_salidas=[]
    lista_mermas=[]
    lista_usuarios=[]
    lista_categorias=[]
    lista_subcategorias=[]
    lista_proveedores=[]
    lista_departamentos=[]

    lista_nombres_productos=[]
    lista_nombres_categorias=[]
    lista_nombres_subcategorias=[]
    lista_nombres_proveedores=[]
    lista_nombres_departamentos=[]


    lista_id_productos=[]
    lista_id_entradas=[]
    lista_id_salidas=[]
    lista_id_mermas=[]
    lista_id_usuarios=[]
    lista_id_categorias=[]
    lista_id_subcategorias=[]
    lista_consec_id_subcategorias=[]
    lista_id_proveedores=[]
    lista_id_departamentos=[]

    lista_temp_id_productos_entrada=[]
    lista_temp_id_productos_salida=[]
    lista_temp_id_productos_merma=[]

    id_producto_actual=''
    id_entrada_actual=''
    id_salida_actual=''
    id_merma_actual=''
    id_usuario_actual=''
    id_categoria_actual=''
    id_subcategoria_actual=''
    id_proveedor_actual=''
    id_departamento_actual=''
    precio_costo=0
    img_path=''

    vent_consulta_producto=None
        
    #-------------------------------------------------------------------------------------------------
        #Creamos algunas funciones de uso general
    #-------------------------------------------------------------------------------------------------
   
    
    def validar_fecha(fecha):
        # Expresión regular que verifica el formato y los rangos básicos de día, mes y año.
        patron_fecha = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/([0-9]{4})$"
        if re.match(patron_fecha, fecha):
            return True
        
        return False

  
    def centrar_ventana(vent):
        vent.update_idletasks()
        vent_width = vent.winfo_width()
        vent_height = vent.winfo_height()
        screen_width = vent.winfo_screenwidth()
        screen_height = vent.winfo_screenheight()
        x = int((screen_width - vent_width) // 2)
        y = int((screen_height - vent_height) // 2)
        vent.geometry(f"{vent_width}x{vent_height}+{x}+{y}")
    
    def generar_codigo(lista,n):
        temp_codigos=[]
        identificador=lista[0][:1]
        for item in lista:
            temp_codigos.append(int(item[1:]))

        next_cod=str(max(temp_codigos)+1)
        codigo_formato=identificador + next_cod.zfill(n)
        
        return codigo_formato
  
    def validar_patron_correo(correo):
        # Expresión regular para validar una dirección de correo electrónico
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Utilizar re.match para verificar si el correo coincide con el patrón
        if re.match(patron, correo):
            return True
        else:
            return False
        
    def contiene_letras_numeros(cadena):
        return bool(re.search(r'[a-zA-Z]', cadena)) and bool(re.search(r'\d', cadena))
    

    #==========================================================================================================
        #FUNCIONES DE CARGA DE ARCHIVOS
    #==========================================================================================================
    def cargar_productos():# Recuperamos los datos del archivo de usuarios para mostrarlos
        nonlocal indice_actual,lista_id_productos,lista_nombres_productos,diccionario_productos
        try:                
            with open("Archivos/Productos.txt", "r") as archivo:# Cargamosla categorias
                # Leer cada línea del archivo
                lista_productos=[]
                for linea in archivo:
                    nueva_linea=linea.rstrip('\n')
                    lista_productos.append(nueva_linea.split('|'))

            lista_nombres_productos=[]

            for item in lista_productos:
                diccionario_productos.update({item[0]:{'SKU':item[1],'Id_categoria':item[2],'Id_subcategoria':item[3],
                                                        'Id_proveedor':item[4],'Descripcion':item[5],'Unidad':item[6],
                                                        'Factor_conversion':item[7],'Minimo':item[8],'Existencia':item[9],
                                                        'Precio_costo':item[10],'img_path':item[11]}})
                lista_nombres_productos.append(item[5])

            
            if diccionario_productos!={}:
                lista_id_productos=list(diccionario_productos.keys())
                indice_actual=len(lista_id_productos)-1
            
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
                print(f"Ocurrió un error de E/S: {e}")    

    
    def cargar_entradas():# Recuperamos los datos del archivo de usuarios para mostrarlos
        nonlocal indice_actual, lista_entradas,lista_id_entradas, diccionario_entradas    
        try:                
            with open("Archivos/Entradas.txt", "r") as archivo:# Cargamosla categorias
                # Leer cada línea del archivo
                lista_entradas=[]
                for linea in archivo:
                    nueva_linea=linea.rstrip('\n')
                    lista_entradas.append(nueva_linea.split('|'))
                
            
            for item in lista_entradas:
                if item[0] not in diccionario_entradas:
                        diccionario_entradas[item[0]]={}    

                diccionario_entradas[item[0]][item[1]]={'Id_usuario':item[2],'Id_producto':item[3],'Num_doc_entrada':item[4],
                                                        'Fecha_entrada':item[5],'Tipo_entrada':item[6],'Detalle_entrada':item[7],
                                                        'Cantidad_entrada':item[8],'Precio_entrada':item[9]}
            
            if diccionario_entradas!={}:
                lista_id_entradas=list(diccionario_entradas.keys())
                indice_actual=len(lista_id_entradas)-1
                
            
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
                print(f"Ocurrió un error de E/S: {e}")  
    
    def cargar_salidas():# Recuperamos los datos del archivo de usuarios para mostrarlos
        nonlocal indice_actual, lista_salidas,lista_id_salidas, diccionario_salidas       
            
        try:                
            with open("Archivos/Salidas.txt", "r") as archivo:# Cargamosla categorias
                # Leer cada línea del archivo
                lista_salidas=[]
                for linea in archivo:
                    nueva_linea=linea.rstrip('\n')
                    lista_salidas.append(nueva_linea.split('|'))
                
            for item in lista_salidas:
                if item[0] not in diccionario_salidas:
                        diccionario_salidas[item[0]]={}    

                diccionario_salidas[item[0]][item[1]]={'Id_usuario':item[2],'Id_producto':item[3],'Id_departamento':item[4],'Num_doc_salida':item[5],
                                                        'Fecha_salida':item[6],'Tipo_salida':item[7],'Detalle_salida':item[8],
                                                        'Cantidad_salida':item[9],'Precio_salida':item[10]}
            
            if diccionario_salidas!={}:
                lista_id_salidas=list(diccionario_salidas.keys())
                indice_actual=len(lista_id_salidas)-1
                
            
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
                print(f"Ocurrió un error de E/S: {e}")  
    
    def cargar_mermas():# Recuperamos los datos del archivo de usuarios para mostrarlos
        nonlocal indice_actual, lista_mermas,lista_id_mermas, diccionario_mermas   
        try:                
            with open("Archivos/Mermas.txt", "r") as archivo:# Cargamosla categorias
                # Leer cada línea del archivo
                lista_mermas=[]
                for linea in archivo:
                    nueva_linea=linea.rstrip('\n')
                    lista_mermas.append(nueva_linea.split('|'))
                
            for item in lista_mermas:
                if item[0] not in diccionario_mermas:
                        diccionario_mermas[item[0]]={}    

                diccionario_mermas[item[0]][item[1]]={'Id_usuario':item[2],'Id_producto':item[3],'Num_doc_merma':item[4],
                                                        'Fecha_merma':item[5],'Tipo_merma':item[6],'Detalle_merma':item[7],
                                                        'Cantidad_merma':item[8],'Precio_merma':item[9]}
            
            if diccionario_mermas!={}:
                lista_id_mermas=list(diccionario_mermas.keys())
                indice_actual=len(lista_id_mermas)-1
                
            
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
                print(f"Ocurrió un error de E/S: {e}")  

    def cargar_usuarios():# Recuperamos los datos del archivo de usuarios para validar la session
        nonlocal indice_actual, lista_usuarios,lista_id_usuarios, diccionario_usuarios          
        try:                
            with open("Archivos/Usuarios.txt", "r") as archivo:
                # Leer cada línea del archivo
                lista_usuarios=[]
                for linea in archivo:
                    nueva_linea=linea.rstrip('\n')
                    lista_usuarios.append(nueva_linea.split('|'))
                
                for item in lista_usuarios:
                    print(type(item[0]))
                    diccionario_usuarios.update({item[0]:{'Nombre':item[1], 'Correo':item[2],'Telefono':item[3],
                                'Usuario':item[4], 'Contrasena':item[5],
                                'Pin':item[6], 'Rol':item[7],'Estado':item[8]}})
                    
                if diccionario_usuarios!={}:
                    lista_id_usuarios=list(diccionario_usuarios.keys())
                    indice_actual=len(lista_id_usuarios)-1
        
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
                print(f"Ocurrió un error de E/S: {e}")     
        
    
    def cargar_categorias(caller=''):# Recuperamos los datos del archivo de usuarios para mostrarlos
        nonlocal indice_actual, id_categoria_actual,lista_categorias,lista_id_categorias,lista_nombres_categorias, diccionario_categorias   
        try:                
            with open("Archivos/Categorias.txt", "r") as archivo:
                # Leer cada línea del archivo
                lista_categorias=[]
                for linea in archivo:
                    nueva_linea=linea.rstrip('\n')
                    lista_categorias.append(nueva_linea.split('|'))

                lista_nombres_categorias=[]

                for item in lista_categorias:
                    diccionario_categorias.update({item[0]:{'Nombre':item[1]}})
                    lista_nombres_categorias.append(item[1])
                
                if diccionario_categorias!={} and caller=='vent_categorias':
                    lista_id_categorias=list(diccionario_categorias.keys())
                    indice_actual=len(lista_id_categorias)-1
                elif caller=='vent_subcategorias':
                    lista_id_categorias=list(diccionario_categorias.keys())
                    id_categoria_actual=lista_id_categorias[len(lista_id_categorias)-1]


        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
                print(f"Ocurrió un error de E/S: {e}")   

    
    def cargar_subcategorias(caller=''):# Recuperamos los datos del archivo de usuarios para mostrarlos
        nonlocal indice_actual, lista_subcategorias,lista_id_subcategorias,lista_consec_id_subcategorias,lista_nombres_subcategorias, diccionario_entradas   
        try:                
            
            with open("Archivos/Subcategorias.txt", "r") as archivo:# Cargamos las subcategorias
                # Leer cada línea del archivo
                lista_subcategorias=[]
                for linea in archivo:
                    nueva_linea=linea.rstrip('\n')
                    lista_subcategorias.append(nueva_linea.split('|'))
                
            lista_nombres_subcategorias=[]

            for item in lista_subcategorias:
                if item[0] not in diccionario_subcategorias:
                    diccionario_subcategorias[item[0]]={}
                        
                diccionario_subcategorias[item[0]][item[1]]={'Nombre':item[2]}
                lista_nombres_subcategorias.append(item[2])
   

            if diccionario_subcategorias!={} and caller=='vent_subcategorias':
                lista_id_subcategorias=list(diccionario_subcategorias[item[0]].keys())
                indice_actual=len(lista_id_subcategorias)-1
                lista_consec_id_subcategorias.append(lista_id_subcategorias[indice_actual])

        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
                print(f"Ocurrió un error de E/S: {e}")   

    def cargar_proveedores(caller=''):# Recuperamos los datos del archivo de usuarios para mostrarlos
        nonlocal indice_actual, lista_proveedores,lista_id_proveedores,lista_nombres_proveedores, diccionario_entradas           
        try:                
            with open("Archivos/Proveedores.txt", "r") as archivo:
                # Leer cada línea del archivo
                lista_proveedores=[]
                for linea in archivo:
                    nueva_linea=linea.rstrip('\n')
                    lista_proveedores.append(nueva_linea.split('|'))
                
                lista_nombres_proveedores=[]

                for item in lista_proveedores:
                    diccionario_proveedores.update({item[0]:{'Nombre':item[1], 'Correo':item[2],'Telefono':item[3],
                                'Tipo':item[4], 'Cedula':item[5]}})
                    lista_nombres_proveedores.append(item[1])

                if diccionario_proveedores!={} and caller=='vent_proveedores':
                    lista_id_proveedores=list(diccionario_proveedores.keys())
                    indice_actual=len(lista_id_proveedores)-1
                   
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
                print(f"Ocurrió un error de E/S: {e}")
        
    def cargar_departamentos(caller=''):# Recuperamos los datos del archivo de usuarios para mostrarlos
        nonlocal indice_actual, lista_departamentos,lista_id_departamentos,lista_nombres_departamentos, diccionario_departamentos   
        try:                
            with open("Archivos/Departamentos.txt", "r") as archivo:
                # Leer cada línea del archivo
                lista_departamentos=[]
                for linea in archivo:
                    nueva_linea=linea.rstrip('\n')
                    lista_departamentos.append(nueva_linea.split('|'))
                
                lista_nombres_departamentos=[]
                
                for item in lista_departamentos :
                    diccionario_departamentos.update({item[0]:{'Nombre':item[1]}})
                    lista_nombres_departamentos.append(item[1])

                if diccionario_departamentos!={} and caller=='vent_departamentos':
                    lista_id_departamentos=list(diccionario_departamentos.keys())
                    indice_actual=len(lista_id_departamentos)-1    
            
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
                print(f"Ocurrió un error de E/S: {e}")   
        

     #==========================================================================================================
        #FUNCIONES PARA ACTUALIZAR ARCHIVOS
    #==========================================================================================================
    
    
    def actualizar_archivo_productos():  
        try: 
            with open("Archivos/Productos.txt", "w") as archivo:
                for clave,valor in diccionario_productos.items():
                    archivo.write(clave +'|'+ valor['SKU'] +'|'+ valor['Id_categoria']+'|'+ valor['Id_subcategoria'] 
                                    +'|'+ valor['Id_proveedor']+'|'+ valor['Descripcion']+'|'+ valor['Unidad']
                                    +'|'+ valor['Factor_conversion']+'|'+ valor['Minimo']+'|'+ valor['Existencia']
                                    +'|'+ valor['Precio_costo']+'|'+ valor['img_path']+'\n')
                    
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
            messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")   

    def actualizar_archivo_entradas():  
        try: 
            with open("Archivos/Entradas.txt", "w") as archivo:
                for clave1,valores in diccionario_entradas.items():
                    for clave2 ,valor in valores.items():
                        archivo.write(clave1 +'|'+ clave2 +'|'+ id_usuario_en_session +'|'+ valor['Id_producto']+'|'+ valor['Num_doc_entrada'] 
                                    +'|'+ valor['Fecha_entrada']+'|'+ valor['Tipo_entrada']+'|'+ valor['Detalle_entrada']
                                    +'|'+ str(valor['Cantidad_entrada'])+'|'+ str(valor['Precio_entrada'])+'\n')
                        
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
            messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}") 
    
    def actualizar_archivo_salidas():  
        try: 
            with open("Archivos/Salidas.txt", "w") as archivo:
                for clave1,valores in diccionario_salidas.items():
                    for clave2 ,valor in valores.items():
                        archivo.write(clave1 +'|'+ clave2 +'|'+ id_usuario_en_session +'|'+ valor['Id_producto']+'|'+ valor['Num_doc_salida'] 
                                    +'|'+ valor['Fecha_salida']+'|'+ valor['Tipo_salida']+'|'+ valor['Detalle_salida']
                                    +'|'+ str(valor['Cantidad_salida'])+'|'+ str(valor['Precio_salida'])+'\n')
                        
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
            messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")
    
    def actualizar_archivo_mermas():  
        try: 
            with open("Archivos/Mermas.txt", "w") as archivo:
                for clave1,valores in diccionario_mermas.items():
                    for clave2 ,valor in valores.items():
                        archivo.write(clave1 +'|'+ clave2 +'|'+ id_usuario_en_session +'|'+ valor['Id_producto']+'|'+ valor['Num_doc_merma'] 
                                    +'|'+ valor['Fecha_merma']+'|'+ valor['Tipo_merma']+'|'+ valor['Detalle_merma']
                                    +'|'+ str(valor['Cantidad_merma'])+'|'+ str(valor['Precio_merma'])+'\n')
                        
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
            messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")         

    def actualizar_archivo_usuarios():  
        try: 
            with open("Archivos/Usuarios.txt", "w") as archivo:
                for clave, item in diccionario_usuarios.items():
                    archivo.write(clave +'|'+item['Nombre']+'|'+item['Correo']+'|'+
                                    item['Telefono']+'|'+item['Usuario']+'|'+ 
                                    item['Contrasena']+'|'+item['Pin']+'|'+item['Rol']+'|'+item['Estado']+'\n')
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
            messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")
    
    
    def actualizar_archivo_categorias():  
        try: 
            with open("Archivos/Categorias.txt", "w") as archivo:
                for clave, item in diccionario_categorias.items():
                    archivo.write(clave +'|'+item['Nombre']+'\n')
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
            messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")   

    def actualizar_archivo_subcategorias():  
        try: 
            with open("Archivos/Subcategorias.txt", "w") as archivo:
                for id_cat,valores in diccionario_subcategorias.items():
                    for id_sub,valor in valores.items():
                        archivo.write(id_cat +'|'+ id_sub +'|'+ valor['Nombre'] +'\n')
                    
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
            messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")   

    
    def actualizar_archivo_proveedores():  
        try: 
            with open("Archivos/Proveedores.txt", "w") as archivo:
                for clave, item in diccionario_proveedores.items():
                    archivo.write(clave +'|'+item['Nombre'].replace('|',"")+'|'+item['Correo']+'|'+
                                    item['Telefono']+'|'+item['Tipo']+'|'+ 
                                    item['Cedula']+'\n')
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
            messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")

    def actualizar_archivo_departamentos():  
        try: 
            with open("Archivos/Departamentos.txt", "w") as archivo:
                for clave, item in diccionario_departamentos.items():
                    archivo.write(clave +'|'+item['Nombre'].replace('|',"")+'\n')
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") 
        except IOError as e:
            messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")
          

    #==========================================================================================================
        #CREAMOS LA VENTANA PRINCIPAL (ROOT)
    #==========================================================================================================
        
    def crear_vent_principal():
        nonlocal root
        

        def confirmar_salir():
            if messagebox.askokcancel("Cerrar la aplicación", "¿Seguro que quieres cerrar la aplicación?"):
                root.destroy()

        def ayuda_url():
            webbrowser.open('https://safetyculture.com/es/temas/manejo-de-inventario/control-de-inventarios/')

        root = Tk()
        root.title("ZendStock Alamcenes")
        root.option_add('*tearOff', FALSE)
        root.attributes('-zoomed', True)
        root.rowconfigure((0,3), weight=1)
        root.columnconfigure((0,2), weight=1)
        
        
        style = ttk.Style()
        style.configure("RoundedLabel.TLabel", borderwidth=1, relief="solid", bordercolor="blue", borderradius=10)
        img_portada=Image.open("images/images.jpg").resize((400,300))
        img_portada_tk=ImageTk.PhotoImage(img_portada)
        mi_fuente = font.Font(family="Arial", size=24, weight="bold")
        lbl_portada=ttk.Label(root,image=img_portada_tk, style="RoundedLabel.TLabel")
        lbl_portada.grid(row=0,column=1)
        lbl_name=ttk.Label(root,text='ZenStock Alacenes', font=mi_fuente).grid(row=2,column=1)
        
        
        img_cerrar_tk=ImageTk.PhotoImage(Image.open("icons/cerrar.png").resize((40,40)))       
        btn_cerrar=ttk.Button(root,text='Cerrar', image=img_cerrar_tk,compound=TOP,command=confirmar_salir).grid(row=3,column=1)
        
        #Menu pricnipal
        menubar = Menu(root)
            
        menubar.add_command(label='Gestion Producto', command=crear_vent_productos)
        
        menubar.add_command(label='Entradas',command=crear_vent_entradas)
        
        menubar.add_command(label='Salidas',command=crear_vent_salidas)
        
        menubar.add_command(label='Merma',command=crear_vent_mermas)
        
        menubar.add_command(label='Consultar',command=crear_vent_consulta_producto)

        menubar.add_command(label='Reporte',command=crear_vent_reportes)

        menubar.add_command(label='SendList',command=crear_vent_sendlist)

        menu_mantenimiento=Menu(menubar)
        menubar.add_cascade(menu=menu_mantenimiento, label='Mantenimiento')
        menu_mantenimiento.add_command(label='Usuarios', command=crear_vent_usuarios)
       
        menu_mantenimiento.add_command(label='Categorias',command=crear_vent_categorias)
        menu_mantenimiento.add_command(label='Subcategorias',command=crear_vent_subcategorias)
        menu_mantenimiento.add_command(label='Provedores',command=crear_vent_proveedores)
        menu_mantenimiento.add_command(label='Departamentos',command=crear_vent_departamentos)
        menubar.add_command(label='Ayuda', command=ayuda_url)
        
        menubar.add_command(label='Salir', command=confirmar_salir)
    
        #menu_file.add_command(label='Open', underline=0)
        #menu_file.entryconfigure('Open', accelerator='Command+V')
        #menu_file.entryconfigure('Close', state=DISABLED)
    
        #root['menu'] = menubar
        root.protocol("WM_DELETE_WINDOW", confirmar_salir)
        root.config(menu=menubar)
        
        
        root.mainloop()

    

    #==========================================================================================================
        #CREAMOS LA VENTANA DE GETION DE PRODUCTOS
    #==========================================================================================================
    def crear_vent_productos():
        # nonlocal root
                
        def abrir_archivo():
            nonlocal img_path,imagenes

            # Mostrar el cuadro de diálogo para seleccionar un archivo
            img_path = filedialog.askopenfilename()
            desc_producto.set(os.path.basename(img_path))
            if len(img_path):
                if img_path.endswith(('.png', '.jpg', '.jpeg', '.gif','webp','jfif')):

                    try:
                        img_articulo=ImageTk.PhotoImage(Image.open(img_path).resize((100,100)))
                        lbl_img_producto.config(image=img_articulo)
                        #lbl_img_producto['image']=img_articulo
                        imagenes[vent_productos] = img_articulo
                    except FileNotFoundError as e: 
                        print('Error, Imagen no cargada',e)
                else: 
                    img_path=''
                    messagebox.showwarning('Error','Archivo imagen no valida.') 
        
                
        def actualizar_diccionario_productos():
            nonlocal diccionario_productos

            if id_producto.get() not in diccionario_productos:
                diccionario_productos[id_producto.get()]={}
                
            diccionario_productos.update({id_producto.get():{'SKU':sku_producto.get(),'Id_categoria':id_categoria_actual,'Id_subcategoria':id_subcategoria_actual,
                                                           'Id_proveedor':id_proveedor_actual,'Descripcion':desc_producto.get(),'Unidad':und_medida.get(),
                                                           'Factor_conversion':fact_conversion.get(),'Minimo':min_producto.get(),'Existencia':exist_producto.get(),
                                                           'Precio_costo':precio_costo.get(),'img_path':img_path}})
   
        def navegar(boton):
            nonlocal indice_actual
            if diccionario_productos!={}:
       
                if boton=='Primero':
                    indice_actual = 0
                elif boton=='Anterior':
                    indice_actual = (indice_actual - 1) % len(lista_id_productos)
                elif boton=='Siguiente':
                    indice_actual = (indice_actual + 1) % len(lista_id_productos)
                elif boton=='Ultimo':
                    indice_actual=len(lista_id_productos)-1
                
                mostrar_datos_producto()
        
        def mostrar_datos_producto():
            nonlocal img_path,imagenes,id_producto_actual,id_categoria_actual,id_subcategoria_actual,id_proveedor_actual

            if diccionario_productos!={}:
                id_producto_actual=lista_id_productos[indice_actual]
                
                id_categoria_actual=diccionario_productos[id_producto_actual]['Id_categoria']
                id_subcategoria_actual=diccionario_productos[id_producto_actual]['Id_subcategoria']
                id_proveedor_actual=diccionario_productos[id_producto_actual]['Id_proveedor']

                id_producto.set(id_producto_actual)
                sku_producto.set(diccionario_productos[id_producto_actual]['SKU'])
                desc_producto.set(diccionario_productos[id_producto_actual]['Descripcion'])
                und_medida.set(diccionario_productos[id_producto_actual]['Unidad'])
                fact_conversion.set(diccionario_productos[id_producto_actual]['Factor_conversion'])

                nombre_categoria.set(diccionario_categorias[id_categoria_actual]['Nombre'])
                nombre_subcategoria.set(diccionario_subcategorias[id_categoria_actual][id_subcategoria_actual]['Nombre'])
               
                actualizar_combo_subcategorias()

                nombre_proveedor.set(diccionario_proveedores[id_proveedor_actual]['Nombre'])


                min_producto.set(diccionario_productos[id_producto_actual]['Minimo'])
                exist_producto.set(diccionario_productos[id_producto_actual]['Existencia'])
                precio_costo.set(diccionario_productos[id_producto_actual]['Precio_costo'])

                img_path=diccionario_productos[id_producto_actual]['img_path']
               

                if len(img_path):
                    try:
                        img_articulo=img_articulo=ImageTk.PhotoImage(Image.open(img_path).resize((100,100)))
                        lbl_img_producto.config(image=img_articulo)
                        imagenes[vent_productos]=img_articulo
                    except :
                        pass
                else:
                    img_nofoto=ImageTk.PhotoImage(Image.open("icons/nofoto.png").resize((32,32)))
                    lbl_img_producto.config(image=img_nofoto)
                    imagenes[vent_productos]=img_nofoto
        
        def validar_datos_producto():    
            valor_desc_producto =desc_producto.get()
            valor_factor_conversion=fact_conversion.get()
            valor_min_producto=min_producto.get()
            
            if not len(valor_desc_producto) :
                messagebox.showinfo('Informacion','Debe ingresar un nombre de producto')
                entry_descripcion.focus()
                return False
            elif not len(valor_factor_conversion) :
                messagebox.showinfo('Informacion','Debe ingresar un factor de conversion.')
                entry_factor_producto.focus()
                return False
            elif not len(valor_min_producto) :
                messagebox.showinfo('Informacion','Debe ingresar un minimo de reorden')
                entry_min_producto.focus()
                return False
            
            else: return True
                
        def limpiar_widgets():
            nonlocal img_path

            id_producto.set('')
            sku_producto.set('')
            fact_conversion.set('1')
            desc_producto.set('')
            min_producto.set('1')
            lbl_img_producto.config(image=img_nofoto)
            exist_producto.set(0.0)
            precio_costo.set(0.0)
            img_path=''
            
            if diccionario_productos=={}: 
                nombre_categoria.set(lista_nombres_categorias[0])
                nombre_subcategoria.set(lista_nombres_subcategorias[0])
                capturar_opcion_categoria(event=None)
                nombre_proveedor.set(lista_nombres_proveedores[0])
                capturar_opcion_proveedor(event=None)
        
        def eliminar_producto():
            nonlocal indice_actual,lista_id_productos,diccionario_productos

            if diccionario_productos!={}:
                if messagebox.askokcancel("Eliminar", "¿Seguro que quieres eliminar este producto?"):
                    diccionario_productos.pop(id_producto_actual)
                    lista_id_productos.pop(indice_actual)
                    indice_actual-=1
                    actualizar_archivo_productos()
                    mostrar_datos_producto()
                    messagebox.showinfo('Info','Registro eliminado exitosamente.')

        def actualizar_producto():
            if diccionario_productos!={}:
                if validar_datos_producto():
                    actualizar_diccionario_productos()
                    actualizar_archivo_productos()
                    messagebox.showinfo('Informacion','Registro actualizado exitosamente.')

        def guardar_nuevo_producto():
                 
            try:
                with open('Archivos/Productos.txt','a') as archivo:
                    archivo.write(id_producto.get()+'|'+sku_producto.get().strip()+'|'+ id_categoria_actual+'|'+ id_subcategoria_actual
                                  +'|'+id_proveedor_actual+'|'+desc_producto.get().strip()+'|'+und_medida.get()+'|'+fact_conversion.get()
                                  +'|'+min_producto.get().strip()+'|'+exist_producto.get()+'|'+precio_costo.get().strip()+'|'+img_path+'\n')       
                
            except FileNotFoundError as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}") 
            except IOError as e:
                messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")
           
        def agregar_producto():
            nonlocal indice_actual,lista_id_productos,agregando_producto
            if agregando_producto: 
                if validar_datos_producto():    
                    guardar_nuevo_producto()
                    actualizar_diccionario_productos()
                    lista_id_productos=list(diccionario_productos)
                    indice_actual=len(lista_id_productos)-1
                    agregando_producto = not agregando_producto
                    botones.cambiar_imagenes_al_navegar() #Volvemos a activar los botones para navegar
                   
                    messagebox.showinfo('Informacion','Registro agregado exitosamente.')    
            else: 
                limpiar_widgets()

                if lista_id_productos!=[]:
                    id_producto.set(generar_codigo(lista_id_productos,4))
                else:
                    lista_id_productos.append('A0000') 
                    id_producto.set(generar_codigo(lista_id_productos,4)) 
                    
                agregando_producto =not agregando_producto                 
                #Desactivamos los bootones de navegacion y cambiamos sus imagenes               
                botones.cambiar_imagenes_al_agregar()
               
                entry_descripcion.focus()   
    
        def confirmar_salir():
            nonlocal agregando_producto

            if agregando_producto==False:
                vent_productos.destroy()
            else: 
                agregando_producto =not agregando_producto                 
                botones.cambiar_imagenes_al_navegar()
                if diccionario_productos!={}:
                    mostrar_datos_producto()
        
        def capturar_opcion_unidad(event):
            und_medida.set(cmb_unidad.get())
        
        def capturar_opcion_categoria(event):
            nonlocal id_categoria_actual

            nombre_categoria.set(cmb_categoria.get())

            for clave,valor in diccionario_categorias.items():
                if valor['Nombre']==nombre_categoria.get():
                    id_categoria_actual=clave
                    break
            actualizar_combo_subcategorias()
            
            nombre_subcategoria.set(lista_nombres_subcategorias[0])
            

        def actualizar_combo_subcategorias():
            nonlocal id_subcategoria_actual, lista_nombres_subcategorias

            lista_nombres_subcategorias=[]
            for item in lista_subcategorias:
                if item[0]==id_categoria_actual:
                    lista_nombres_subcategorias.append(item[2])
            
            cmb_subcategoria['values']=[]
            cmb_subcategoria['values']=lista_nombres_subcategorias
            vent_productos.update()
            
            if diccionario_subcategorias!={}:
                for id_cat,valores in diccionario_subcategorias.items():
                    for id_sub, valor in valores.items():
                        if valor['Nombre']==nombre_subcategoria.get():
                            id_subcategoria_actual=id_sub
                            return

            

        def capturar_opcion_subcategoria(event):
            nonlocal id_subcategoria_actual

            nombre_subcategoria.set(cmb_subcategoria.get())

            if diccionario_subcategorias!={}:
                for id_cat,valores in diccionario_subcategorias.items():
                    for id_sub, valor in valores.items():
                        if valor['Nombre']==nombre_subcategoria.get():
                            id_subcategoria_actual=id_sub
                            return
                        
        def capturar_opcion_proveedor(event):
            nonlocal id_proveedor_actual

            nombre_proveedor.set(cmb_proveedor.get())
            if diccionario_proveedores!={}:
                for clave,valor in diccionario_proveedores.items():
                    if valor['Nombre']==nombre_proveedor.get():
                        id_proveedor_actual=clave
                        break
             
        def validar_entrada_numerica(nuevo_valor):
            if nuevo_valor == "":
                return True
            try:
                float(nuevo_valor)
                return True
            except ValueError:
                return False
                
        vent_productos=Toplevel(root)
        
        vent_productos.title("Gestion producto.")
        vent_productos.resizable(0,0)
        vent_productos.geometry("660x300")
       
        #vent_productos.rowconfigure(0, weight=1)
        #vent_productos.columnconfigure(0, weight=1)
        
        frm = ttk.Frame(vent_productos,borderwidth=1, relief='solid',padding=5)
        frm.grid(column=0,row=0,pady=10,padx=10)
        frm.columnconfigure((2,3,4,5),weight=1) 
        frm.rowconfigure((0,1,2,3,4),weight=1)
         
                
        lbl_id_producto=ttk.Label(frm, text='Id_producto:')
        lbl_id_producto.grid(row=0, column=0, padx=2,pady=2,sticky='W')
        id_producto=StringVar()
        entry_id_producto=ttk.Entry(frm, textvariable=id_producto, width=10,state='readonly')
        entry_id_producto.grid(row=0, column=1, padx=2,pady=2, sticky='W')
        
        lbl_sku=ttk.Label(frm, text='SKU:',width=4)
        lbl_sku.grid(row=0, column=2, padx=0,pady=2,sticky='E')
        sku_producto=StringVar()
        entry_sku_producto=ttk.Entry(frm, textvariable=sku_producto, width=10)
        entry_sku_producto.grid(row=0, column=3, padx=0,pady=2, sticky='E')

        lbl_descripcion=ttk.Label(frm, text='Descripcion:')
        lbl_descripcion.grid(row=1, column=0, padx=2,pady=2,sticky='W')
        desc_producto=StringVar()
        entry_descripcion=ttk.Entry(frm, textvariable=desc_producto, width=32)
        entry_descripcion.grid(row=1, column=1, padx=2,pady=2,columnspan=3,sticky='W')
        
        try:
            img_buscar=ImageTk.PhotoImage(Image.open("icons/8415529.png").resize((16,16)))
            btn_buscar=ttk.Button(frm,image=img_buscar,width=32)
            btn_buscar.grid(column=4,row=1, sticky=W)#Boton Buscar
       
            
            img_nofoto=ImageTk.PhotoImage(Image.open("icons/nofoto.png").resize((32,32)))
            lbl_img_producto=tk.Label(frm,borderwidth=1,image=img_nofoto,relief="solid" ,width=100,height=100)
            lbl_img_producto.grid(row=0, column=5,rowspan=4, columnspan=2, padx=20,pady=2,sticky='W')

            img_add_foto=ImageTk.PhotoImage(Image.open("icons/agregarfoto.png").resize((16,16)))

        except FileNotFoundError as e: 
            print('Error, Imagen no cargada',e)
        
        ttk.Label(frm,text='Unidad:').grid(column=0,row=2, sticky=W)
        opcion_unidades=['Und','Caja','Paquete','Rollo','Bolsa']
        und_medida=StringVar()
        und_medida.set(opcion_unidades[0])
        #nombre_categoria.set(lista_nombres_categorias[len(lista_nombres_categorias)-1])
        cmb_unidad=ttk.Combobox(frm,width=9,textvariable=und_medida, values=opcion_unidades, state="readonly")
        cmb_unidad.grid(column=1,row=2,pady=2,sticky=W)
        cmb_unidad.bind("<<ComboboxSelected>>", capturar_opcion_unidad)
        
        lbl_factor=ttk.Label(frm, text='Fact. conv:',width=10)
        lbl_factor.grid(row=2, column=2, padx=0,pady=2,sticky='E')
        validate_cmd = vent_productos.register(validar_entrada_numerica)
        fact_conversion=StringVar()
        entry_factor_producto=ttk.Entry(frm, textvariable=fact_conversion, width=10,validate="key", validatecommand=(validate_cmd, "%P"))
        entry_factor_producto.grid(row=2, column=3, padx=0,pady=2, sticky='E')

        cargar_categorias()

        ttk.Label(frm,text='Categoria:').grid(column=0,row=3, sticky=W)
        nombre_categoria=StringVar()
        #nombre_categoria.set(lista_nombres_categorias[len(lista_nombres_categorias)-1])
        cmb_categoria=ttk.Combobox(frm,width=25,textvariable=nombre_categoria, values=lista_nombres_categorias, state="readonly")
        cmb_categoria.grid(column=1,row=3,pady=2,columnspan=3,sticky=W)
        cmb_categoria.bind("<<ComboboxSelected>>", capturar_opcion_categoria)
        
        cargar_subcategorias()
        
        ttk.Label(frm,text='Sub categoria:').grid(column=0,row=4, sticky=W)
        nombre_subcategoria=StringVar()
        #nombre_categoria.set(lista_nombres_categorias[len(lista_nombres_categorias)-1])
        cmb_subcategoria=ttk.Combobox(frm,width=25,textvariable=nombre_subcategoria, values=lista_nombres_subcategorias, state="readonly")
        cmb_subcategoria.grid(column=1,row=4,pady=2,columnspan=3,sticky=W)
        cmb_subcategoria.bind("<<ComboboxSelected>>", capturar_opcion_subcategoria)
        
        btn_buscar_img=ttk.Button(frm,image=img_add_foto,width=32,command=abrir_archivo)
        btn_buscar_img.grid(column=5,row=4)#Boton Buscar
        
        cargar_proveedores()
        
        ttk.Label(frm,text='Proveedor:').grid(column=0,row=5, sticky=W)
        nombre_proveedor=StringVar()
        #nombre_categoria.set(lista_nombres_categorias[len(lista_nombres_categorias)-1])
        cmb_proveedor=ttk.Combobox(frm,width=25,textvariable=nombre_proveedor, values=lista_nombres_proveedores, state="readonly")
        cmb_proveedor.grid(column=1,row=5,pady=2,columnspan=3,sticky=W)
        cmb_proveedor.bind("<<ComboboxSelected>>", capturar_opcion_proveedor)
        
        lbl_minimo=ttk.Label(frm, text='Minimo:',width=8)
        lbl_minimo.grid(row=6, column=0, padx=0,pady=2,sticky='W')
        validate_cmd = vent_productos.register(validar_entrada_numerica)
        min_producto=StringVar()
        entry_min_producto=ttk.Entry(frm, textvariable=min_producto, width=10,validate="key", validatecommand=(validate_cmd, "%P"))
        entry_min_producto.grid(row=6, column=1, padx=0,pady=2, sticky='W')

        lbl_exist=ttk.Label(frm, text='Existencia:',width=8)
        lbl_exist.grid(row=6, column=2, padx=0,pady=2,sticky='W')
        exist_producto=StringVar()
        entry_exist_producto=ttk.Entry(frm, textvariable=exist_producto, width=10,state="readonly")
        entry_exist_producto.grid(row=6, column=3, padx=0,pady=2, sticky='W')

        lbl_prec_costo=ttk.Label(frm, text='Precio costo:',width=10)
        lbl_prec_costo.grid(row=6, column=4, padx=0,pady=2,sticky='W')
        precio_costo=StringVar()
        entry_precio_costo=ttk.Entry(frm, textvariable=precio_costo, width=10,state="readonly")
        entry_precio_costo.grid(row=6, column=5, padx=0,pady=2, sticky='W')


        #--------------------------------------------------------------------------------------
            #Botones para manejo de acciones de la ventana (agregar-eliminar-actualizar-navegar-salir)
        #--------------------------------------------------------------------------------------
        botones=Botones(agregar_producto,eliminar_producto,actualizar_producto,navegar,confirmar_salir)
        botones.crear_botones(vent_productos,0,7)

        vent_productos.transient(root)  # Asociar la ventana hija a la ventana principal
        vent_productos.grab_set()  # Evitar que el usuario interactúe con la ventana principal mientras la ventana hija está abierta
        vent_productos.focus_set()  # Establecer el foco en la ventana hija

        cargar_productos()
        mostrar_datos_producto()
        
        centrar_ventana(vent_productos)
        vent_productos.mainloop()
        
    #=============================================================================================================
        #CREAR VENTANA ENTRADAS
    #=============================================================================================================
    
    def crear_vent_entradas(doc_referencia=''):
        doc_ref=doc_referencia
        
        
        def actualizar_diccionario_entradas():
            nonlocal lista_temp_id_productos_entrada, diccionario_entradas,diccionario_productos    
            
            if agregando_entrada==False:
                
                del diccionario_entradas[id_entrada.get()]
                
                for item in lista_temp_id_productos_entrada:
                    existencia_actual=float(diccionario_productos[item[0]]['Existencia'])
                    existencia_actual-=float(item[1])
                    diccionario_productos[item[0]]['Existencia']=str(existencia_actual)
            
            lista_temp_id_productos_entrada=[]

            filas = tree.get_children()
         
            # Iterar sobre las filas
            for fila in filas:
                 # Obtener los valores de cada celda en la fila
                linea=tree.item(fila)['text']
                
                valores = tree.item(fila)['values']                
                if id_entrada.get() not in diccionario_entradas:
                    diccionario_entradas[id_entrada.get()]={}

                diccionario_entradas[id_entrada.get()][linea]={'Id_usuario':id_usuario_en_session,'Id_producto':valores[0],'Num_doc_entrada':num_documento.get(),
                                                           'Fecha_entrada':fecha_documento.get(),'Tipo_entrada':tipo_entrada.get(),'Detalle_entrada':detalle_entrada.get(),
                                                           'Cantidad_entrada':valores[3],'Precio_entrada':valores[4]}
                
                existencia_actual=float(diccionario_productos[valores[0]]['Existencia'])
                existencia_actual+=float(valores[3])
                diccionario_productos[valores[0]]['Existencia']=str(existencia_actual)
                if agregando_entrada==True: diccionario_productos[valores[0]]['Precio_costo']=str(valores[4])

                lista_temp_id_productos_entrada.append([valores[0],valores[3]])
        
        def navegar(boton):
            nonlocal indice_actual,id_entrada_actual

            if diccionario_entradas!={}:
       
                if boton=='Primero':
                    indice_actual = 0
                elif boton=='Anterior':
                    indice_actual = (indice_actual - 1) % len(lista_id_entradas)
                elif boton=='Siguiente':
                    indice_actual = (indice_actual + 1) % len(lista_id_entradas)
                elif boton=='Ultimo':
                    indice_actual=len(lista_id_entradas)-1
                
                
           
                mostrar_datos_entrada()
        
        def mostrar_datos_entrada():
            nonlocal indice_actual, id_entrada_actual, lista_temp_id_productos_entrada,doc_ref

            if diccionario_entradas!={}:
                if doc_ref!="":
                    indice_actual=lista_id_entradas.index(doc_ref)
                    doc_ref=''
 
                #Datos de emcabezado
                id_entrada_actual=lista_id_entradas[indice_actual]
                id_entrada.set(id_entrada_actual)
                num_documento.set(diccionario_entradas[id_entrada_actual]['1']['Num_doc_entrada'])
                fecha_documento.set(diccionario_entradas[id_entrada_actual]['1']['Fecha_entrada'])
                cmb_tipo_entrada.set(diccionario_entradas[id_entrada_actual]['1']['Tipo_entrada'])
                detalle_entrada.set(diccionario_entradas[id_entrada_actual]['1']['Detalle_entrada'])
                
                for fila in tree.get_children():
                    tree.delete(fila)
                
                num_filas = 0
                lista_temp_id_productos_entrada=[]

                for clave1, valor in diccionario_entradas[id_entrada_actual].items():
                    num_filas+=1
                    tree.insert("", tk.END, text=str(num_filas),values=(valor['Id_producto'],diccionario_productos[valor['Id_producto']]['Descripcion'],
                                                                                   diccionario_productos[valor['Id_producto']]['Unidad'], valor['Cantidad_entrada'],
                                                                                   valor['Precio_entrada'],float(valor['Cantidad_entrada']) * float(valor['Precio_entrada'])))
                
                    lista_temp_id_productos_entrada.append([valor['Id_producto'],valor['Cantidad_entrada']])
                
                lbl_monto_total.config(text= "{:>10,.2f}".format(sumar_columna()))
                
               
        def validar_datos_entrada():

            valor_fecha_doc=fecha_documento.get()
            valor_num_doc=num_documento.get()
            
            if not len(valor_fecha_doc) :
                messagebox.showinfo('Informacion','Debe ingresar una fecha valida')
                entry_fecha.focus()
                return False
            elif not len(valor_num_doc) :
                messagebox.showinfo('Informacion','Debe ingresar un numero de documento.')
                entry_documento.focus()
                return False
            
            else: return True
                
        def limpiar_widgets():
            
            id_entrada.set('')
            fecha=datetime.now()
            fecha_documento.set(fecha.strftime('%d/%m/%Y'))
            num_documento.set('')
            detalle_entrada.set('')
            cantidad.set(1)
            precio_costo.set(0.00)
            lbl_monto_total.config(text='0.00')

            if id_producto.get()=='': 
                desc_producto.set(lista_nombres_productos[0])
                capturar_descripcion_producto(event=None)

            for fila in tree.get_children():
                tree.delete(fila)
            
                
        def eliminar_entrada():
            nonlocal indice_actual,lista_id_entradas,diccionario_entradas

            if diccionario_entradas!={}:
                if messagebox.askokcancel("Eliminar", "¿Seguro que quieres eliminar este entrada?"):
                    diccionario_entradas.pop(id_entrada_actual)
                    lista_id_entradas.pop(indice_actual)
                    indice_actual-=1
                    actualizar_archivo_entradas()
                    mostrar_datos_entrada()
                    messagebox.showinfo('Info','Registro eliminado exitosamente.')

        def actualizar_entrada():
            if diccionario_entradas!={}:
                if validar_datos_entrada():
                    actualizar_diccionario_entradas()
                    actualizar_archivo_entradas()
                    actualizar_archivo_productos()
                    messagebox.showinfo('Informacion','Registro actualizado exitosamente.')

        
        def guardar_nuevo_entrada():
                 
            try:
                with open('Archivos/Entradas.txt','a') as archivo:
                     # Obtener todas las filas del TreeView
                    filas = tree.get_children()

                    # Iterar sobre las filas
                    for fila in filas:
                        # Obtener los valores de cada celda en la fila
                        linea=tree.item(fila)['text']
                        valores = tree.item(fila)['values']
                        archivo.write(id_entrada.get().strip()+'|'+ linea +'|'+ id_usuario_en_session+'|'+ valores[0]
                                  +'|'+num_documento.get().strip()+'|'+fecha_documento.get().strip()+'|'+tipo_entrada.get()+'|'+detalle_entrada.get().strip()
                                  +'|'+str(valores[3])+'|'+str(valores[4])+'\n')       
                
            except FileNotFoundError as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}") 
            except IOError as e:
                messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")
           
        def agregar_entrada():
            nonlocal indice_actual, lista_id_entradas, agregando_entrada

            if agregando_entrada: 
                if validar_datos_entrada():    
                    guardar_nuevo_entrada()
                    actualizar_diccionario_entradas()
                    actualizar_archivo_productos()
                    lista_id_entradas=list(diccionario_entradas)
                    indice_actual=len(lista_id_entradas)-1
                    agregando_entrada = not agregando_entrada
                    botones.cambiar_imagenes_al_navegar() #Volvemos a activar los botones para navegar
                   
                    messagebox.showinfo('Informacion','Registro agregado exitosamente.')    
            else: 
                limpiar_widgets()

                if lista_id_entradas!=[]:
                    id_entrada.set(generar_codigo(lista_id_entradas,4))
                else:
                    lista_id_entradas.append('E0000') 
                    id_entrada.set(generar_codigo(lista_id_entradas,4)) 
                    
                agregando_entrada =not agregando_entrada                 
                #Desactivamos los bootones de navegacion y cambiamos sus imagenes               
                botones.cambiar_imagenes_al_agregar()
               
                entry_documento.focus()   
        
        def confirmar_salir():
            nonlocal agregando_entrada, vent_consulta_producto
            
            if agregando_entrada==False:
                if vent_consulta_producto is not None:
                    if vent_consulta_producto.winfo_exists():
                        vent_consulta_producto.grab_set()
                vent_entradas.destroy()
            else: 
                agregando_entrada =not agregando_entrada                 
                botones.cambiar_imagenes_al_navegar()
                if diccionario_entradas!={}:
                    mostrar_datos_entrada()
        
             
        def validar_entrada_numerica(nuevo_valor):
            if nuevo_valor == "":
                return True
            try:
                float(nuevo_valor)
                return True
            except ValueError:
                return False
            
        def capturar_tipo_entrada():        
            tipo_entrada.set(cmb_tipo_entrada.get())
        
        def capturar_descripcion_producto(event):
            
            desc_producto.set(cmb_desc_producto.get())

            for clave,valor in diccionario_productos.items():           
                if valor['Descripcion']==desc_producto.get():
                    id_producto.set(clave)

        def delete_selected_row(event):
            
            # Obtener el ID de la fila seleccionada
            
            if messagebox.askokcancel('Eliminar producto','Esta seguro de eliminar este producto?'):
                selected_item = tree.focus()
                if selected_item:
                    
                    tree.delete(selected_item)# Eliminar la fila seleccionada
                    num_lineas=0
                    for index, item_id in enumerate(tree.get_children()):
                    # Establece el nuevo nuemro de linea de la primera columna para cada elemento
                        
                        num_lineas+=1
                        tree.item(item_id, text=str(num_lineas))

                lbl_monto_total.config(text= "{:>10,.2f}".format(sumar_columna()))


        def agregar_producto(event):
            if id_producto.get() not in diccionario_productos:
                messagebox.showwarning('Infomarcio','Id producto no existe.')
                entry_id_producto.focus()
                entry_id_producto.select_range(0,'end')
                return False
            if not len(cantidad.get()):
                entry_cantidad.focus()
                entry_cantidad.select_range(0,'end')
                return False
            elif not len(precio_costo.get()):
                entry_precio_costo.focus()
                entry_precio_costo.select_range(0,'end')
                return False
            else: 
                # Obtener el número de filas actuales
                num_filas = len(tree.get_children())
                tree.insert("", tk.END, text=str(num_filas + 1), values=(id_producto.get(), diccionario_productos[id_producto.get()]['Descripcion'],
                                                diccionario_productos[id_producto.get()]['Unidad'],cantidad.get(),precio_costo.get(),
                                                (float(cantidad.get())*(float(precio_costo.get())))))

                lbl_monto_total.config(text= "{:>10,.2f}".format(sumar_columna()))
                entry_id_producto.focus()
        
        def on_enter_entry_documento(event):
            entry_fecha.focus()

        def on_enter_entry_fecha(event):
            entry_detalle.focus()
        
        def on_enter_cmb_tipo_entrada(event):
            entry_detalle.focus()

        def on_enter_entry_detalle(event):
            entry_id_producto.focus()

        def on_enter_entry_id_producto(event):
            if id_producto.get() not in diccionario_productos:
                messagebox.showwarning('Infomarcion','Id producto no existe.')
                entry_id_producto.focus()
                return
            else:
                desc_producto.set(diccionario_productos[id_producto.get()]['Descripcion'])
                entry_cantidad.focus()
        
        def on_enter_cmb_desc_producto(event):
            entry_cantidad.focus()

        def on_enter_entry_cantidad(event):
            entry_precio_costo.focus()

        def on_enter_entry_precio_costo(event):
            btn_add.focus()
        
        def sumar_columna():
            filas=tree.get_children()
            total=0
            for fila in filas:
                valores = tree.item(fila)['values']
                total+=float(valores[5])
            return total
        
        global vent_entradas
        vent_entradas=Toplevel(root)
        vent_entradas.title("Entradas.")
        vent_entradas.resizable(0,0)
        vent_entradas.geometry("725x525")
       
        #vent_entradas.rowconfigure(0, weight=1)
        #vent_entradas.columnconfigure(0, weight=1)
        
        frm = ttk.Frame(vent_entradas,borderwidth=1, relief='solid',padding=5)
        frm.grid(column=0,row=0,pady=10,padx=10)
        #frm.columnconfigure((2,3,4,5,6),weight=1) 
        #frm.rowconfigure((0,1,2,3,4),weight=1)
        frm.columnconfigure((0,2,3,4,5,6),weight=1) 
        frm.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        
                
        lbl_id_entrada=ttk.Label(frm, text='Id_entrada:')
        lbl_id_entrada.grid(row=0, column=0, padx=2,pady=2,sticky='W')
        id_entrada=StringVar()
        entry_id_entrada=ttk.Entry(frm, textvariable=id_entrada, width=10,state='readonly')
        entry_id_entrada.grid(row=0, column=1, padx=2,pady=2, sticky='W')
        
        lbl_documento=ttk.Label(frm, text='Documento:',width=10)
        lbl_documento.grid(row=1, column=0, padx=0,pady=2,sticky='W')
        num_documento=StringVar()
        entry_documento=ttk.Entry(frm, textvariable=num_documento, width=10)
        entry_documento.grid(row=1, column=1, padx=0,pady=2, sticky='W')
        entry_documento.bind('<Return>', on_enter_entry_documento)
        entry_documento.bind('<KP_Enter>', on_enter_entry_documento)

        lbl_detalle=ttk.Label(frm, text='Detalle:',width=10)
        lbl_detalle.grid(row=1, column=2, padx=10,pady=2,sticky='W')

        lbl_fecha=ttk.Label(frm, text='Fecha',width=10)
        lbl_fecha.grid(row=1, column=3, padx=0,pady=2,sticky='E')

        fecha_documento=StringVar()
        fecha_actual=datetime.now()
        fecha_actual=fecha_actual.strftime('%d/%m/%Y')
        fecha_documento.set(fecha_actual)
        entry_fecha=ttk.Entry(frm, textvariable=fecha_documento, width=12)
        entry_fecha.grid(row=1, column=4, padx=0,pady=2, sticky='W')
        entry_fecha.bind('<Return>', on_enter_entry_fecha)
        entry_fecha.bind('<KP_Enter>', on_enter_entry_fecha)


        
        ttk.Label(frm,text='Tipo entrada:').grid(column=0,row=2, sticky=W)
        opcion_entradas=['Compra','Ajuste','Donacion','Otro']
        tipo_entrada=StringVar()
        tipo_entrada.set(opcion_entradas[0])
        cmb_tipo_entrada=ttk.Combobox(frm,width=9,textvariable=tipo_entrada, values=opcion_entradas, state="readonly")
        cmb_tipo_entrada.grid(column=1,row=2,pady=2,sticky=W)
        cmb_tipo_entrada.bind("<<ComboboxSelected>>", capturar_tipo_entrada)
        cmb_tipo_entrada.bind('<Return>', on_enter_cmb_tipo_entrada)
        cmb_tipo_entrada.bind('<KP_Enter>', on_enter_cmb_tipo_entrada)


        detalle_entrada=StringVar()
        entry_detalle=ttk.Entry(frm, textvariable=detalle_entrada, width=41)
        entry_detalle.grid(row=2, column=2, padx=2,pady=2,columnspan=3,sticky='W')
        entry_detalle.bind('<Return>', on_enter_entry_detalle)
        entry_detalle.bind('<KP_Enter>', on_enter_entry_detalle)

        
        
        
        lbl_id_producto=ttk.Label(frm, text='Id_producto:',width=10)
        lbl_id_producto.grid(row=3, column=0, padx=0,pady=2,sticky='W')
        id_producto=StringVar()
        entry_id_producto=ttk.Entry(frm, textvariable=id_producto, width=10)
        entry_id_producto.grid(row=3, column=1, padx=0,pady=2, sticky='W')
        entry_id_producto.bind('<Return>', on_enter_entry_id_producto)
        entry_id_producto.bind('<KP_Enter>', on_enter_entry_id_producto)

        cargar_productos()

        desc_producto=StringVar()
        #desc_producto.set(lista_descripcion_productos[0])
        cmb_desc_producto=ttk.Combobox(frm,width=30,textvariable=desc_producto, values=lista_nombres_productos, state="readonly")
        cmb_desc_producto.grid(column=2,row=3,pady=2,columnspan=4,sticky=W)
        cmb_desc_producto.bind("<<ComboboxSelected>>", capturar_descripcion_producto)
        cmb_desc_producto.bind('<KP_Enter>', on_enter_cmb_desc_producto)

        
        try:
            img_buscar=ImageTk.PhotoImage(Image.open("icons/8415529.png").resize((16,16)))
            btn_buscar=ttk.Button(frm,image=img_buscar,width=32,command=lambda event=None: agregar_producto(event))
            btn_buscar.grid(column=5,row=3)#Boton Buscar
            btn_buscar.bind('<Return>', on_enter_entry_id_producto)
            btn_buscar.bind('<KP_Enter>', on_enter_entry_id_producto)
            #btn_buscar.bind("<Button-1>", on_enter_entry_id_producto)
 
          
        except: pass
        

        lbl_cantidad=ttk.Label(frm, text='Cantidad:',width=8)
        lbl_cantidad.grid(row=4, column=0, padx=0,pady=2,sticky='W')
        validate_cmd = vent_entradas.register(validar_entrada_numerica)
        cantidad=StringVar()
        entry_cantidad=ttk.Entry(frm, textvariable=cantidad, width=10,validate="key", validatecommand=(validate_cmd, "%P"))
        entry_cantidad.grid(row=4, column=1, padx=0,pady=2, sticky='W')
        entry_cantidad.bind('<Return>', on_enter_entry_cantidad)
        entry_cantidad.bind('<KP_Enter>', on_enter_entry_cantidad)
        
        lbl_precio_costo=ttk.Label(frm, text='Precio:',width=8)
        lbl_precio_costo.grid(row=4, column=2, padx=0,pady=2,sticky='E')
        validate_cmd = vent_entradas.register(validar_entrada_numerica)
        precio_costo=StringVar()
        entry_precio_costo=ttk.Entry(frm, textvariable=precio_costo, width=10,validate="key", validatecommand=(validate_cmd, "%P"))
        entry_precio_costo.grid(row=4, column=3, padx=0,pady=2, sticky='W')
        entry_precio_costo.bind('<Return>', on_enter_entry_precio_costo)
        entry_precio_costo.bind('<KP_Enter>', on_enter_entry_precio_costo)

        try:
            img_add=ImageTk.PhotoImage(Image.open("icons/8839040.png").resize((16,16)))
            btn_add=ttk.Button(frm,image=img_add,width=32,command=lambda event=None: agregar_producto(event))
            btn_add.grid(column=4,row=4)#Boton aagregar productos
            # Vincular la pulsación de tecla Enter al botón
            btn_add.bind("<Return>", agregar_producto)
            btn_add.bind('<KP_Enter>', agregar_producto)
            #btn_add.bind("<Button-1>", agregar_producto)
        except: pass
        
        #--------------------------------------------------------------------------------------
            #CONFIGURAMOS EL TREE VIEW
        #--------------------------------------------------------------------------------------    
        # Crear un Treeview
        tree = ttk.Treeview(frm)
        tree["columns"] = ("1","2","3","4","5","6")

        # Configurar las columnas
        tree.column("#0", width=40, minwidth=40,stretch=tk.NO)
        tree.column("1", width=80, minwidth=80, stretch=tk.NO)
        tree.column("2", width=200, minwidth=200, stretch=tk.NO)
        tree.column("3", width=80, minwidth=80, stretch=tk.NO)
        tree.column("4", width=80, minwidth=80, stretch=tk.NO,anchor=E)
        tree.column("5", width=100, minwidth=100, stretch=tk.NO,anchor=E)
        tree.column("6", width=100, minwidth=100, stretch=tk.NO,anchor=E)

        # Configurar las cabeceras de las columnas
        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("1", text="Id", anchor=tk.W)
        tree.heading("2", text="Descripcion", anchor=tk.W)
        tree.heading("3", text="Und", anchor=tk.W)
        tree.heading("4", text="Cantidad", anchor=tk.W)
        tree.heading("5", text="Precio", anchor=tk.W)
        tree.heading("6", text="Total", anchor=tk.W)

        #tree.tag_configure('right_align', anchor='e')
         
        # Mostrar el Treeview
        tree.grid(column=0,row=5,columnspan=6,pady=10,sticky="W")
        tree.bind("<Delete>", delete_selected_row)

        scrollbar = ttk.Scrollbar(frm, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=5, column=6, sticky="ns")

        lbl_total=ttk.Label(frm, text='TOTAL:',width=8,anchor='w',font=("Arial", 14, "bold"))
        lbl_total.grid(row=6, column=3, padx=0,pady=2,sticky='E')
        lbl_monto_total=ttk.Label(frm, text='0.00',width=20, anchor='e',font=("Arial", 14, "bold"),background='lightgreen')
        lbl_monto_total.grid(row=6, column=4,columnspan=2,padx=0,pady=2)
        
        #--------------------------------------------------------------------------------------
            #Botones para manejo de acciones de la ventana (agregar-eliminar-actualizar-navegar-salir)
        #--------------------------------------------------------------------------------------
        botones=Botones(agregar_entrada,eliminar_entrada,actualizar_entrada,navegar,confirmar_salir)
        botones.crear_botones(vent_entradas,0,7)

        cargar_entradas()
        mostrar_datos_entrada()
        centrar_ventana(vent_entradas)
        
        vent_entradas.transient(root)  # Asociar la ventana hija a la ventana principal
        vent_entradas.grab_set()  # Evitar que el usuario interactúe con la ventana principal mientras la ventana hija está abierta
        vent_entradas.focus_set()  # Establecer el foco en la ventana hija
        
        vent_entradas.mainloop()

    #=============================================================================================================
        #CREAR VENTANA SALIDAS
    #=============================================================================================================
    
    def crear_vent_salidas(doc_referencia=''):
        doc_ref=doc_referencia
        
        def actualizar_diccionario_salidas():
            nonlocal lista_temp_id_productos_salida,diccionario_salidas,diccionario_productos

            if agregando_salida==False:
                
                del diccionario_salidas[id_salida.get()]
                
                for item in lista_temp_id_productos_salida:
                    existencia_actual=float(diccionario_productos[item[0]]['Existencia'])
                    existencia_actual+=float(item[1])
                    diccionario_productos[item[0]]['Existencia']=str(existencia_actual)
            
            lista_temp_id_productos_salida=[]

            filas = tree.get_children()
         
            # Iterar sobre las filas
            for fila in filas:
                 # Obtener los valores de cada celda en la fila
                linea=tree.item(fila)['text']
                
                valores = tree.item(fila)['values']                
                if id_salida.get() not in diccionario_salidas:
                    diccionario_salidas[id_salida.get()]={}

                diccionario_salidas[id_salida.get()][linea]={'Id_usuario':id_usuario_en_session,'Id_producto':valores[0],'Id_departamento':id_departamento.get().strip(),'Num_doc_salida':num_documento.get(),
                                                           'Fecha_salida':fecha_documento.get(),'Tipo_salida':tipo_salida.get(),'Detalle_salida':detalle_salida.get(),
                                                           'Cantidad_salida':valores[3],'Precio_salida':valores[4]}
                
                existencia_actual=float(diccionario_productos[valores[0]]['Existencia'])
                existencia_actual-=float(valores[3])
                diccionario_productos[valores[0]]['Existencia']=str(existencia_actual)
                #if agregando_salida==True: diccionario_productos[valores[0]]['Precio_costo']=valores[4]

                lista_temp_id_productos_salida.append([valores[0],valores[3]])
        
        def navegar(boton):
            nonlocal indice_actual, id_salida_actual
            if diccionario_salidas!={}:
       
                if boton=='Primero':
                    indice_actual = 0
                elif boton=='Anterior':
                    indice_actual = (indice_actual - 1) % len(lista_id_salidas)
                elif boton=='Siguiente':
                    indice_actual = (indice_actual + 1) % len(lista_id_salidas)
                elif boton=='Ultimo':
                    indice_actual=len(lista_id_salidas)-1
          
                mostrar_datos_salida()
        
        def mostrar_datos_salida():
            nonlocal indice_actual, id_salida_actual, lista_temp_id_productos_salida, doc_ref
            
            if diccionario_salidas!={}:
                if doc_ref!="":
                    indice_actual=lista_id_salidas.index(doc_ref)
                    doc_ref=''

                id_salida_actual=lista_id_salidas[indice_actual] 
                #Datos de emcabezado
                id_salida.set(id_salida_actual)
                num_documento.set(diccionario_salidas[id_salida_actual]['1']['Num_doc_salida'])
                fecha_documento.set(diccionario_salidas[id_salida_actual]['1']['Fecha_salida'])
                cmb_tipo_salida.set(diccionario_salidas[id_salida_actual]['1']['Tipo_salida'])
                detalle_salida.set(diccionario_salidas[id_salida_actual]['1']['Detalle_salida'])
                id_departamento.set(diccionario_salidas[id_salida_actual]['1']['Id_departamento'])
                nombre_departamento.set(diccionario_departamentos[id_departamento.get()]['Nombre'])
                
                for fila in tree.get_children():
                    tree.delete(fila)
                
                num_filas = 0
                lista_temp_id_productos_salida=[]

                for clave1, valor in diccionario_salidas[id_salida_actual].items():
                    num_filas+=1
                    tree.insert("", tk.END, text=str(num_filas),values=(valor['Id_producto'],diccionario_productos[valor['Id_producto']]['Descripcion'],
                                                                                   diccionario_productos[valor['Id_producto']]['Unidad'], valor['Cantidad_salida'],
                                                                                   valor['Precio_salida'],float(valor['Cantidad_salida']) * float(valor['Precio_salida'])))
                
                    lista_temp_id_productos_salida.append([valor['Id_producto'],valor['Cantidad_salida']])
                
                lbl_monto_total.config(text= "{:>10,.2f}".format(sumar_columna()))
                
               
        def validar_datos_salida():

            valor_fecha_doc=fecha_documento.get()
            valor_num_doc=num_documento.get()
            
            if not len(valor_fecha_doc) :
                messagebox.showinfo('Informacion','Debe ingresar una fecha valida')
                entry_fecha.focus()
                return False
            elif not len(valor_num_doc) :
                messagebox.showinfo('Informacion','Debe ingresar un numero de documento.')
                entry_documento.focus()
                return False
            
            else: return True
                
        def limpiar_widgets():
            
            id_salida.set('')
            fecha=datetime.now()
            fecha_documento.set(fecha.strftime('%d/%m/%Y'))
            num_documento.set('')
            detalle_salida.set('')
            cantidad.set(1)

            if desc_producto.get()=='':
                desc_producto.set(lista_nombres_productos[0])
                capturar_descripcion_producto(event=None)
            if nombre_departamento.get()=='':
                nombre_departamento.set(lista_nombres_departamentos[0])
                capturar_descripcion_departamento(event=None)
            lbl_monto_total.config(text='0.00')

            for fila in tree.get_children():
                tree.delete(fila)
                
        def eliminar_salida():
            nonlocal indice_actual,lista_salidas,diccionario_salidas

            if diccionario_salidas!={}:
                if messagebox.askokcancel("Eliminar", "¿Seguro que quieres eliminar este salida?"):
                    diccionario_salidas.pop(id_salida_actual)
                    lista_id_salidas.pop(indice_actual)
                    indice_actual-=1
                    actualizar_archivo_salidas()
                    mostrar_datos_salida()
                    messagebox.showinfo('Info','Registro eliminado exitosamente.')

        def actualizar_salida():
            if diccionario_salidas!={}:
                if validar_datos_salida():
                    actualizar_diccionario_salidas()
                    actualizar_archivo_salidas()
                    actualizar_archivo_productos()
                    messagebox.showinfo('Informacion','Registro actualizado exitosamente.')

        
        def guardar_nuevo_salida():
                 
            try:
                with open('Archivos/Salidas.txt','a') as archivo:
                     # Obtener todas las filas del TreeView
                    filas = tree.get_children()

                    # Iterar sobre las filas
                    for fila in filas:
                        # Obtener los valores de cada celda en la fila
                        linea=tree.item(fila)['text']
                        valores = tree.item(fila)['values']
                        archivo.write(id_salida.get().strip()+'|'+ linea +'|'+id_usuario_en_session+'|'+ valores[0]+'|'+id_departamento.get().strip()
                                  +'|'+num_documento.get().strip()+'|'+fecha_documento.get().strip()+'|'+tipo_salida.get()+'|'+detalle_salida.get().strip()
                                  +'|'+str(valores[3])+'|'+str(valores[4])+'\n')       
                
            except FileNotFoundError as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}") 
            except IOError as e:
                messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")
           
        def agregar_salida():
            nonlocal indice_actual, lista_id_salidas,agregando_salida

            if agregando_salida: 
                if validar_datos_salida():    
                    guardar_nuevo_salida()
                    actualizar_diccionario_salidas()
                    actualizar_archivo_productos()
                    lista_id_salidas=list(diccionario_salidas)
                    indice_actual=len(lista_id_salidas)-1
                    agregando_salida = not agregando_salida
                    botones.cambiar_imagenes_al_navegar() #Volvemos a activar los botones para navegar
                   
                    messagebox.showinfo('Informacion','Registro agregado exitosamente.')    
            else: 
                limpiar_widgets()

                if lista_id_salidas!=[]:
                    id_salida.set(generar_codigo(lista_id_salidas,4))
                else:
                    lista_id_salidas.append('S0000') 
                    id_salida.set(generar_codigo(lista_id_salidas,4)) 
                    
                agregando_salida =not agregando_salida                 
                #Desactivamos los bootones de navegacion y cambiamos sus imagenes               
                botones.cambiar_imagenes_al_agregar()
               
                entry_documento.focus()   

        
        
        def confirmar_salir():
            nonlocal agregando_salida,vent_consulta_producto
            
            if agregando_salida==False:
                if vent_consulta_producto is not None:
                    if vent_consulta_producto.winfo_exists():
                        vent_consulta_producto.grab_set()
                vent_salidas.destroy()
            else: 
                agregando_salida =not agregando_salida                 
                botones.cambiar_imagenes_al_navegar()
                if diccionario_salidas!={}:
                    mostrar_datos_salida()
        
             
        def validar_salida_numerica(nuevo_valor):
            if nuevo_valor == "":
                return True
            try:
                float(nuevo_valor)
                return True
            except ValueError:
                return False
            
        def capturar_tipo_salida():        
            tipo_salida.set(cmb_tipo_salida.get())
        
        def capturar_descripcion_producto(event):
           
            desc_producto.set(cmb_desc_producto.get())

            for clave,valor in diccionario_productos.items():    
                if valor['Descripcion']==desc_producto.get():
                    id_producto.set(clave)

        def delete_selected_row(event):
            
            # Obtener el ID de la fila seleccionada
           
            if messagebox.askokcancel('Eliminar producto','Esta seguro de eliminar este producto?'):
                selected_item = tree.focus()
                if selected_item:
                    #if agregando_salida==False:
                    #    lista_id_producto_eliminar.append([tree.item(selected_item, "text"),tree.item(selected_item)['values'][3]])
                    tree.delete(selected_item)# Eliminar la fila seleccionada
                    num_lineas=0
                    for index, item_id in enumerate(tree.get_children()):
                    # Establece el nuevo nuemro de linea de la primera columna para cada elemento         
                        num_lineas+=1
                        tree.item(item_id, text=str(num_lineas))

                lbl_monto_total.config(text= "{:>10,.2f}".format(sumar_columna()))


        def agregar_producto(event):
            nonlocal precio_costo

            if id_producto.get() not in diccionario_productos:
                messagebox.showwarning('Infomarcion','Id producto no existe.')
                entry_id_producto.focus()
                entry_id_producto.select_range(0,'end')
                return False
            
            elif not len(cantidad.get()):
                messagebox.showwarning('Infomarcion','Cantidad no valida.')
                entry_cantidad.focus()
                entry_cantidad.select_range(0,'end')
                return False
            else:
                cantidad_actual=float(diccionario_productos[id_producto.get()]['Existencia'])
                if float(cantidad_actual)<float(cantidad.get()):
                     messagebox.showwarning('Infomarcion',f'Existencia actual del articulo {desc_producto.get()}, '
                                            f'insuficiente para cubrir la solicitud: existentencia actual: {cantidad_actual}, solicitada: {cantidad.get()}' )
                     entry_cantidad.focus()
                     return
                else: 
                    precio_costo=diccionario_productos[id_producto.get()]['Precio_costo']

                    # Obtener el número de filas actuales
                    num_filas = len(tree.get_children())
                    tree.insert("", tk.END, text=str(num_filas + 1), values=(id_producto.get(), diccionario_productos[id_producto.get()]['Descripcion'],
                                                    diccionario_productos[id_producto.get()]['Unidad'],cantidad.get(),precio_costo,
                                                    (float(cantidad.get())*float(precio_costo))))

                    lbl_monto_total.config(text= "{:>10,.2f}".format(sumar_columna()))
                    entry_id_producto.focus()
        
        def on_enter_entry_documento(event):
            entry_fecha.focus()

        def on_enter_entry_fecha(event):
            entry_detalle.focus()
        
        def on_enter_cmb_tipo_salida(event):
            entry_detalle.focus()

        def on_enter_entry_detalle(event):
            entry_id_departamento.focus()

        def on_enter_entry_id_producto(event):
            if id_producto.get() not in diccionario_productos:
                messagebox.showwarning('Infomarcion','Id producto no existe.')
                entry_id_producto.focus()
                return
            else:
                desc_producto.set(diccionario_productos[id_producto.get()]['Descripcion'])
                entry_cantidad.focus()

        def on_enter_cmb_desc_producto(event):
            entry_cantidad.focus()

        
        def sumar_columna():
            filas=tree.get_children()
            total=0
            for fila in filas:
                valores = tree.item(fila)['values']
                total+=float(valores[5])
            return total
        
        def on_enter_entry_id_departamento(event):
            if id_departamento.get() not in diccionario_departamentos:
                messagebox.showwarning('Infomarcion','Id departamento no existe.')
                entry_id_departamento.focus()
                return
            else:
                nombre_departamento.set(diccionario_departamentos[id_departamento.get()]['Nombre'])
                entry_id_producto.focus()

        def on_enter_cmb_desc_departamento(event):
            entry_cantidad.focus()
        
        def capturar_descripcion_departamento(event):
            
            nombre_departamento.set(cmb_desc_departamento.get())

            for clave,valor in diccionario_departamentos.items():      
                if valor['Nombre']==nombre_departamento.get():
                    id_departamento.set(clave)
        
        def on_enter_entry_cantidad(event):
            btn_add.focus()

        global vent_salidas
        vent_salidas=Toplevel(root)
        vent_salidas.title("Salidas.")
        vent_salidas.resizable(0,0)
        vent_salidas.geometry("725x550")
       
        #vent_salidas.rowconfigure(0, weight=1)
        #vent_salidas.columnconfigure(0, weight=1)
        
        frm = ttk.Frame(vent_salidas,borderwidth=1, relief='solid',padding=5)
        frm.grid(column=0,row=0,pady=10,padx=10)
        frm.columnconfigure((0,2,3,4,5,6),weight=1) 
        frm.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        frm.grid(column=0,row=0,pady=10,padx=10)
         
                
        lbl_id_salida=ttk.Label(frm, text='Id_salida:')
        lbl_id_salida.grid(row=0, column=0, padx=2,pady=2,sticky='W')
        id_salida=StringVar()
        entry_id_salida=ttk.Entry(frm, textvariable=id_salida, width=10,state='readonly')
        entry_id_salida.grid(row=0, column=1, padx=2,pady=2, sticky='W')
        
        lbl_documento=ttk.Label(frm, text='Documento:',width=10)
        lbl_documento.grid(row=1, column=0, padx=0,pady=2,sticky='W')
        num_documento=StringVar()
        entry_documento=ttk.Entry(frm, textvariable=num_documento, width=10)
        entry_documento.grid(row=1, column=1, padx=0,pady=2, sticky='W')
        entry_documento.bind('<Return>', on_enter_entry_documento)
        entry_documento.bind('<KP_Enter>', on_enter_entry_documento)

        lbl_detalle=ttk.Label(frm, text='Detalle:',width=10)
        lbl_detalle.grid(row=1, column=2, padx=10,pady=2,sticky='W')

        lbl_fecha=ttk.Label(frm, text='Fecha',width=10)
        lbl_fecha.grid(row=1, column=3, padx=0,pady=2,sticky='E')

        fecha_documento=StringVar()
        fecha_actual=datetime.now()
        fecha_actual=fecha_actual.strftime('%d/%m/%Y')
        fecha_documento.set(fecha_actual)
        entry_fecha=ttk.Entry(frm, textvariable=fecha_documento, width=12)
        entry_fecha.grid(row=1, column=4, padx=0,pady=2, sticky='W')
        entry_fecha.bind('<Return>', on_enter_entry_fecha)
        entry_fecha.bind('<KP_Enter>', on_enter_entry_fecha)


        
        ttk.Label(frm,text='Tipo salida:').grid(column=0,row=2, sticky=W)
        opcion_salidas=['Consumo','Venta','Ajuste','Donacion','Otro']
        tipo_salida=StringVar()
        tipo_salida.set(opcion_salidas[0])
        cmb_tipo_salida=ttk.Combobox(frm,width=9,textvariable=tipo_salida, values=opcion_salidas, state="readonly")
        cmb_tipo_salida.grid(column=1,row=2,pady=2,sticky=W)
        cmb_tipo_salida.bind("<<ComboboxSelected>>", capturar_tipo_salida)
        cmb_tipo_salida.bind('<Return>', on_enter_cmb_tipo_salida)
        cmb_tipo_salida.bind('<KP_Enter>', on_enter_cmb_tipo_salida)


        detalle_salida=StringVar()
        entry_detalle=ttk.Entry(frm, textvariable=detalle_salida, width=42)
        entry_detalle.grid(row=2, column=2, padx=2,pady=2,columnspan=3,sticky='W')
        entry_detalle.bind('<Return>', on_enter_entry_detalle)
        entry_detalle.bind('<KP_Enter>', on_enter_entry_detalle)

        
        
        lbl_id_departamento=ttk.Label(frm, text='Id_departamento:',width=12)
        lbl_id_departamento.grid(row=3, column=0, padx=0,pady=2,sticky='W')
        id_departamento=StringVar()
        entry_id_departamento=ttk.Entry(frm, textvariable=id_departamento, width=10)
        entry_id_departamento.grid(row=3, column=1, padx=0,pady=2, sticky='W')
        entry_id_departamento.bind('<Return>', on_enter_entry_id_departamento)
        entry_id_departamento.bind('<KP_Enter>', on_enter_entry_id_departamento)

        cargar_departamentos()

        nombre_departamento=StringVar()
        #desc_departamento.set(lista_descripcion_departamentos[0])
        cmb_desc_departamento=ttk.Combobox(frm,width=30,textvariable=nombre_departamento, values=lista_nombres_departamentos, state="readonly")
        cmb_desc_departamento.grid(column=2,row=3,pady=2,columnspan=4,sticky=W)
        cmb_desc_departamento.bind("<<ComboboxSelected>>", capturar_descripcion_departamento)
        cmb_desc_departamento.bind('<KP_Enter>', on_enter_cmb_desc_departamento)

        lbl_id_producto=ttk.Label(frm, text='Id_producto:',width=10)
        lbl_id_producto.grid(row=4, column=0, padx=0,pady=2,sticky='W')
        id_producto=StringVar()
        entry_id_producto=ttk.Entry(frm, textvariable=id_producto, width=10)
        entry_id_producto.grid(row=4, column=1, padx=0,pady=2, sticky='W')
        entry_id_producto.bind('<Return>', on_enter_entry_id_producto)
        entry_id_producto.bind('<KP_Enter>', on_enter_entry_id_producto)

        cargar_productos()

        desc_producto=StringVar()
        #desc_producto.set(lista_descripcion_productos[0])
        cmb_desc_producto=ttk.Combobox(frm,width=30,textvariable=desc_producto, values=lista_nombres_productos, state="readonly")
        cmb_desc_producto.grid(column=2,row=4,pady=2,columnspan=4,sticky=W)
        cmb_desc_producto.bind("<<ComboboxSelected>>", capturar_descripcion_producto)
        cmb_desc_producto.bind('<KP_Enter>', on_enter_cmb_desc_producto)

        
        try:
            img_buscar=ImageTk.PhotoImage(Image.open("icons/8415529.png").resize((16,16)))
            btn_buscar_producto=ttk.Button(frm,image=img_buscar,width=32)
            btn_buscar_producto.grid(column=4,row=4)#Boton Buscar
            btn_buscar_producto.bind('<Return>', on_enter_entry_id_producto)
            btn_buscar_producto.bind('<KP_Enter>', on_enter_entry_id_producto)
            btn_buscar_producto.bind("<Button-1>", lambda event=None:on_enter_entry_id_producto(event))
 
          
        except: pass
        

        lbl_cantidad=ttk.Label(frm, text='Cantidad:',width=8)
        lbl_cantidad.grid(row=5, column=0, padx=0,pady=2,sticky='W')
        validate_cmd = vent_salidas.register(validar_salida_numerica)
        cantidad=StringVar()
        entry_cantidad=ttk.Entry(frm, textvariable=cantidad, width=10,validate="key", validatecommand=(validate_cmd, "%P"))
        entry_cantidad.grid(row=5, column=1, padx=0,pady=2, sticky='W')
        entry_cantidad.bind('<Return>', on_enter_entry_cantidad)
        entry_cantidad.bind('<KP_Enter>', on_enter_entry_cantidad)
        
      
        try:
            img_add=ImageTk.PhotoImage(Image.open("icons/8839040.png").resize((16,16)))
            btn_add=ttk.Button(frm,image=img_add,width=32,command=lambda event=None: agregar_producto(event))
            btn_add.grid(column=2,row=5)#Boton aagregar productos
            # Vincular la pulsación de tecla Enter al botón
            btn_add.bind("<Return>", agregar_producto)
            btn_add.bind('<KP_Enter>', agregar_producto)
            #btn_add.bind("<Button-1>", agregar_producto)
        except: pass
        
        #--------------------------------------------------------------------------------------
            #CONFIGURAMOS EL TREE VIEW
        #--------------------------------------------------------------------------------------    
        # Crear un Treeview
        tree = ttk.Treeview(frm)
        tree["columns"] = ("1","2","3","4","5","6")

        # Configurar las columnas
        tree.column("#0", width=40, minwidth=40,stretch=tk.NO)
        tree.column("1", width=80, minwidth=80, stretch=tk.NO)
        tree.column("2", width=200, minwidth=200, stretch=tk.NO)
        tree.column("3", width=80, minwidth=80, stretch=tk.NO)
        tree.column("4", width=80, minwidth=80, stretch=tk.NO,anchor=E)
        tree.column("5", width=100, minwidth=100, stretch=tk.NO,anchor=E)
        tree.column("6", width=100, minwidth=100, stretch=tk.NO,anchor=E)

        # Configurar las cabeceras de las columnas
        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("1", text="Id", anchor=tk.W)
        tree.heading("2", text="Descripcion", anchor=tk.W)
        tree.heading("3", text="Und", anchor=tk.W)
        tree.heading("4", text="Cantidad", anchor=tk.W)
        tree.heading("5", text="Precio", anchor=tk.W)
        tree.heading("6", text="Total", anchor=tk.W)

        tree.tag_configure('right_align', anchor='e')
         
        # Mostrar el Treeview
        tree.grid(column=0,row=6,columnspan=6,pady=10,sticky="W")
        tree.bind("<Delete>", delete_selected_row)

        scrollbar = ttk.Scrollbar(frm, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=6, column=6, sticky="ns")

        lbl_total=ttk.Label(frm, text='TOTAL:',width=15,anchor='w',font=("Arial", 14, "bold"))
        lbl_total.grid(row=7, column=3, padx=0,pady=2,sticky='E')
        lbl_monto_total=ttk.Label(frm, text='0.00',width=20,anchor='e',font=("Arial", 14, "bold"),background='lightgreen')
        lbl_monto_total.grid(row=7, column=4,padx=0,pady=2)
        
        
        #--------------------------------------------------------------------------------------
            #Botones para manejo de acciones de la ventana (agregar-eliminar-actualizar-navegar-salir)
        #--------------------------------------------------------------------------------------
        botones=Botones(agregar_salida,eliminar_salida,actualizar_salida,navegar,confirmar_salir)
        botones.crear_botones(vent_salidas,0,8)

        

        cargar_salidas()
        mostrar_datos_salida()
        centrar_ventana(vent_salidas)
        
        vent_salidas.transient(root)  # Asociar la ventana hija a la ventana principal
        vent_salidas.grab_set()  # Evitar que el usuario interactúe con la ventana principal mientras la ventana hija está abierta
        vent_salidas.focus_set()  # Establecer el foco en la ventana hija
        
        vent_salidas.mainloop()

    #=============================================================================================================
        #CREAR VENTANA MERMAS
    #=============================================================================================================
    
    def crear_vent_mermas(doc_referencia=''):
        doc_ref=doc_referencia

        def actualizar_diccionario_mermas():
            nonlocal agregando_merma,lista_temp_id_productos_merma,diccionario_mermas,diccionario_productos
            if agregando_merma==False:
                
                del diccionario_mermas[id_merma.get()]
                
                for item in lista_temp_id_productos_merma:
                    existencia_actual=float(diccionario_productos[item[0]]['Existencia'])
                    existencia_actual+=float(item[1])
                    diccionario_productos[item[0]]['Existencia']=str(existencia_actual)
            
            lista_temp_id_productos_merma=[]

            filas = tree.get_children()
         
            # Iterar sobre las filas
            for fila in filas:
                 # Obtener los valores de cada celda en la fila
                linea=tree.item(fila)['text']
                
                valores = tree.item(fila)['values']                
                if id_merma.get() not in diccionario_mermas:
                    diccionario_mermas[id_merma.get()]={}

                diccionario_mermas[id_merma.get()][linea]={'Id_usuario':id_usuario_en_session,'Id_producto':valores[0],'Num_doc_merma':num_documento.get(),
                                                           'Fecha_merma':fecha_documento.get(),'Tipo_merma':tipo_merma.get(),'Detalle_merma':detalle_merma.get(),
                                                           'Cantidad_merma':valores[3],'Precio_merma':valores[4]}
                
                existencia_actual=float(diccionario_productos[valores[0]]['Existencia'])
                existencia_actual-=float(valores[3])
                diccionario_productos[valores[0]]['Existencia']=str(existencia_actual)
                #if agregando_merma==True: diccionario_productos[valores[0]]['Precio_costo']=valores[4]

                lista_temp_id_productos_merma.append([valores[0],valores[3]])
        
        def navegar(boton):
            nonlocal indice_actual
            if diccionario_mermas!={}:
       
                if boton=='Primero':
                    indice_actual = 0
                elif boton=='Anterior':
                    indice_actual = (indice_actual - 1) % len(lista_id_mermas)
                elif boton=='Siguiente':
                    indice_actual = (indice_actual + 1) % len(lista_id_mermas)
                elif boton=='Ultimo':
                    indice_actual=len(lista_id_mermas)-1
             
           
                mostrar_datos_merma()
        
        def mostrar_datos_merma():
            nonlocal indice_actual,lista_temp_id_productos_merma,doc_ref

            if diccionario_mermas!={}:
                if doc_ref!="":
                    indice_actual=lista_id_mermas.index(doc_ref)
                    doc_ref=''

                id_merma_actual=lista_id_mermas[indice_actual]
                #Datos de emcabezado
                id_merma.set(id_merma_actual)
                num_documento.set(diccionario_mermas[id_merma_actual]['1']['Num_doc_merma'])
                fecha_documento.set(diccionario_mermas[id_merma_actual]['1']['Fecha_merma'])
                cmb_tipo_merma.set(diccionario_mermas[id_merma_actual]['1']['Tipo_merma'])
                detalle_merma.set(diccionario_mermas[id_merma_actual]['1']['Detalle_merma'])
                
                for fila in tree.get_children():
                    tree.delete(fila)
                
                num_filas = 0
                lista_temp_id_productos_merma=[]

                for clave1, valor in diccionario_mermas[id_merma_actual].items():
                    num_filas+=1
                    tree.insert("", tk.END, text=str(num_filas),values=(valor['Id_producto'],diccionario_productos[valor['Id_producto']]['Descripcion'],
                                                                                   diccionario_productos[valor['Id_producto']]['Unidad'], valor['Cantidad_merma'],
                                                                                   valor['Precio_merma'],float(valor['Cantidad_merma']) * float(valor['Precio_merma'])))
                
                    lista_temp_id_productos_merma.append([valor['Id_producto'],valor['Cantidad_merma']])
                
                lbl_monto_total.config(text= "{:>10,.2f}".format(sumar_columna()))
        
        def validar_datos_merma():
            valor_fecha_doc=fecha_documento.get()
            valor_num_doc=num_documento.get()
            
            if not len(valor_fecha_doc) :
                messagebox.showinfo('Informacion','Debe ingresar una fecha valida')
                entry_fecha.focus()
                return False
            elif not len(valor_num_doc) :
                messagebox.showinfo('Informacion','Debe ingresar un numero de documento.')
                entry_documento.focus()
                return False
            else: return True
                
        def limpiar_widgets():
            
            id_merma.set('')
            fecha=datetime.now()
            fecha_documento.set(fecha.strftime('%d/%m/%Y'))
            num_documento.set('')
            detalle_merma.set('')
            
            if id_producto.get()=='':
                desc_producto.set(lista_nombres_productos[0])
                capturar_descripcion_producto(event=None)
            
            cantidad.set(1)
        

            lbl_monto_total.config(text='0.00')

            for fila in tree.get_children():
                tree.delete(fila)
                
        def eliminar_merma():
            nonlocal indice_actual,lista_id_mermas, diccionario_mermas

            if diccionario_mermas!={}:
                if messagebox.askokcancel("Eliminar", "¿Seguro que quieres eliminar este merma?"):
                    diccionario_mermas.pop(id_merma_actual)
                    lista_id_mermas.pop(indice_actual)
                    indice_actual-=1
                    actualizar_archivo_mermas()
                    mostrar_datos_merma()
                    messagebox.showinfo('Info','Registro eliminado exitosamente.')

        def actualizar_merma():
            if diccionario_mermas!={}:
                if validar_datos_merma():
                    actualizar_diccionario_mermas()
                    actualizar_archivo_mermas()
                    actualizar_archivo_productos()
                    messagebox.showinfo('Informacion','Registro actualizado exitosamente.')

        def guardar_nuevo_merma():
                 
            try:
                with open('Archivos/Mermas.txt','a') as archivo:
                     # Obtener todas las filas del TreeView
                    filas = tree.get_children()

                    # Iterar sobre las filas
                    for fila in filas:
                        # Obtener los valores de cada celda en la fila
                        linea=tree.item(fila)['text']
                        valores = tree.item(fila)['values']
                        archivo.write(id_merma.get().strip()+'|'+ linea +'|'+id_usuario_en_session+'|'+ valores[0]
                                  +'|'+num_documento.get().strip()+'|'+fecha_documento.get().strip()+'|'+tipo_merma.get()+'|'+detalle_merma.get().strip()
                                  +'|'+str(valores[3])+'|'+str(valores[4])+'\n')       
                
            except FileNotFoundError as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}") 
            except IOError as e:
                messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")
           
        def agregar_merma():
            nonlocal indice_actual, lista_id_mermas,agregando_merma
            if agregando_merma: 
                if validar_datos_merma():    
                    guardar_nuevo_merma()
                    actualizar_diccionario_mermas()
                    actualizar_archivo_productos()
                    lista_id_mermas=list(diccionario_mermas)
                    indice_actual=len(lista_id_mermas)-1
                    agregando_merma = not agregando_merma
                    botones.cambiar_imagenes_al_navegar() #Volvemos a activar los botones para navegar
                   
                    messagebox.showinfo('Informacion','Registro agregado exitosamente.')    
            else: 
                limpiar_widgets()

                if lista_id_mermas!=[]:
                    id_merma.set(generar_codigo(lista_id_mermas,4))
                else:
                    lista_id_mermas.append('M0000') 
                    id_merma.set(generar_codigo(lista_id_mermas,4)) 
                    
                agregando_merma =not agregando_merma                 
                #Desactivamos los bootones de navegacion y cambiamos sus imagenes               
                botones.cambiar_imagenes_al_agregar()
               
                entry_documento.focus()   

        def confirmar_salir():
            nonlocal agregando_merma,vent_consulta_producto
 
            if agregando_merma==False:
                if vent_consulta_producto is not None:
                    if vent_consulta_producto.winfo_exists():
                        vent_consulta_producto.grab_set()
                vent_mermas.destroy()
            else: 
                agregando_merma =not agregando_merma                 
                botones.cambiar_imagenes_al_navegar()
                if diccionario_mermas!={}:
                    mostrar_datos_merma()
             
        def validar_merma_numerica(nuevo_valor):
            if nuevo_valor == "":
                return True
            try:
                float(nuevo_valor)
                return True
            except ValueError:
                return False
            
        def capturar_tipo_merma():        
            tipo_merma.set(cmb_tipo_merma.get())
        
        def capturar_descripcion_producto(event):
           
            desc_producto.set(cmb_desc_producto.get())

            for clave,valor in diccionario_productos.items():    
                if valor['Descripcion']==desc_producto.get():
                    id_producto.set(clave)

        def delete_selected_row(event):
            
            # Obtener el ID de la fila seleccionada
            
            if messagebox.askokcancel('Eliminar producto','Esta seguro de eliminar este producto?'):
                selected_item = tree.focus()
                if selected_item:
                    #if agregando_merma==False:
                    #    lista_id_producto_eliminar.append([tree.item(selected_item, "text"),tree.item(selected_item)['values'][3]])
                    tree.delete(selected_item)# Eliminar la fila seleccionada
                    num_lineas=0
                    for index, item_id in enumerate(tree.get_children()):
                    # Establece el nuevo nuemro de linea de la primera columna para cada elemento         
                        num_lineas+=1
                        tree.item(item_id, text=str(num_lineas))

                lbl_monto_total.config(text= "{:>10,.2f}".format(sumar_columna()))


        def agregar_producto(event):
            nonlocal precio_costo

            if id_producto.get() not in diccionario_productos:
                messagebox.showwarning('Infomarcion','Id producto no existe.')
                entry_id_producto.focus()
                entry_id_producto.select_range(0,'end')
                return False
            
            elif not len(cantidad.get()):
                messagebox.showwarning('Infomarcion','Cantidad no valida.')
                entry_cantidad.focus()
                entry_cantidad.select_range(0,'end')
                return False
            else:
                cantidad_actual=diccionario_productos[id_producto.get()]['Existencia']
                
                if float(cantidad_actual)<float(cantidad.get()):
                     messagebox.showwarning('Infomarcion',f'Existencia actual del articulo {desc_producto.get()}, '
                                            f'insuficiente para cubrir la solicitud: existentencia actual: {cantidad_actual}, solicitada: {cantidad.get()}' )
                     entry_cantidad.focus()
                     return
                else: 
                    precio_costo=diccionario_productos[id_producto.get()]['Precio_costo']

                    # Obtener el número de filas actuales
                    num_filas = len(tree.get_children())
                    tree.insert("", tk.END, text=str(num_filas + 1), values=(id_producto.get(), diccionario_productos[id_producto.get()]['Descripcion'],
                                                    diccionario_productos[id_producto.get()]['Unidad'],cantidad.get(),precio_costo,
                                                    (float(cantidad.get())*float(precio_costo))))

                    lbl_monto_total.config(text= "{:>10,.2f}".format(sumar_columna()))
                    entry_id_producto.focus()
        
        def on_enter_entry_documento(event):
            entry_fecha.focus()

        def on_enter_entry_fecha(event):
            entry_detalle.focus()
        
        def on_enter_cmb_tipo_merma(event):
            entry_detalle.focus()

        def on_enter_entry_detalle(event):
            entry_id_producto.focus()

        def on_enter_entry_id_producto(event):
            if id_producto.get() not in diccionario_productos:
                messagebox.showwarning('Infomarcion','Id producto no existe.')
                entry_id_producto.focus()
                return
            else:
                desc_producto.set(diccionario_productos[id_producto.get()]['Descripcion'])
                entry_cantidad.focus()

        def on_enter_cmb_desc_producto(event):
            entry_cantidad.focus()
        
        def sumar_columna():
            filas=tree.get_children()
            total=0
            for fila in filas:
                valores = tree.item(fila)['values']
                total+=float(valores[5])
            return total
        
        def on_enter_entry_cantidad(event):
            btn_add.focus()

        vent_mermas=Toplevel(root)
        vent_mermas.title("Mermas.")
        vent_mermas.resizable(0,0)
        vent_mermas.geometry("725x550")
       
        #vent_mermas.rowconfigure(0, weight=1)
        #vent_mermas.columnconfigure(0, weight=1)
        
        frm = ttk.Frame(vent_mermas,borderwidth=1, relief='solid',padding=5)
        frm.grid(column=0,row=0,pady=10,padx=10)
        frm.columnconfigure((0,2,3,4,5,6),weight=1) 
        frm.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        frm.grid(column=0,row=0,pady=10,padx=10)
         
                
        lbl_id_merma=ttk.Label(frm, text='Id_merma:')
        lbl_id_merma.grid(row=0, column=0, padx=2,pady=2,sticky='W')
        id_merma=StringVar()
        entry_id_merma=ttk.Entry(frm, textvariable=id_merma, width=10,state='readonly')
        entry_id_merma.grid(row=0, column=1, padx=2,pady=2, sticky='W')
        
        lbl_documento=ttk.Label(frm, text='Documento:',width=10)
        lbl_documento.grid(row=1, column=0, padx=0,pady=2,sticky='W')
        num_documento=StringVar()
        entry_documento=ttk.Entry(frm, textvariable=num_documento, width=10)
        entry_documento.grid(row=1, column=1, padx=0,pady=2, sticky='W')
        entry_documento.bind('<Return>', on_enter_entry_documento)
        entry_documento.bind('<KP_Enter>', on_enter_entry_documento)

        lbl_detalle=ttk.Label(frm, text='Detalle:',width=10)
        lbl_detalle.grid(row=1, column=2, padx=10,pady=2,sticky='W')

        lbl_fecha=ttk.Label(frm, text='Fecha',width=10)
        lbl_fecha.grid(row=1, column=3, padx=0,pady=2,sticky='E')

        fecha_documento=StringVar()
        fecha_actual=datetime.now()
        fecha_actual=fecha_actual.strftime('%d/%m/%Y')
        fecha_documento.set(fecha_actual)
        entry_fecha=ttk.Entry(frm, textvariable=fecha_documento, width=12)
        entry_fecha.grid(row=1, column=4, padx=0,pady=2, sticky='W')
        entry_fecha.bind('<Return>', on_enter_entry_fecha)
        entry_fecha.bind('<KP_Enter>', on_enter_entry_fecha)
        
        ttk.Label(frm,text='Tipo merma:').grid(column=0,row=2, sticky=W)
        opcion_mermas=['Deterioro o dano','Obsolescencia','Robo o Pérdida','Muestreo o Pruebas','Devoluciones a Proveedores','Otro']
        tipo_merma=StringVar()
        tipo_merma.set(opcion_mermas[0])
        cmb_tipo_merma=ttk.Combobox(frm,width=12,textvariable=tipo_merma, values=opcion_mermas, state="readonly")
        cmb_tipo_merma.grid(column=1,row=2,pady=2,sticky=W)
        cmb_tipo_merma.bind("<<ComboboxSelected>>", capturar_tipo_merma)
        cmb_tipo_merma.bind('<Return>', on_enter_cmb_tipo_merma)
        cmb_tipo_merma.bind('<KP_Enter>', on_enter_cmb_tipo_merma)

        detalle_merma=StringVar()
        entry_detalle=ttk.Entry(frm, textvariable=detalle_merma, width=42)
        entry_detalle.grid(row=2, column=2, padx=2,pady=2,columnspan=3,sticky='W')
        entry_detalle.bind('<Return>', on_enter_entry_detalle)
        entry_detalle.bind('<KP_Enter>', on_enter_entry_detalle)
        
        
        lbl_id_producto=ttk.Label(frm, text='Id_producto:',width=10)
        lbl_id_producto.grid(row=3, column=0, padx=0,pady=2,sticky='W')
        id_producto=StringVar()
        entry_id_producto=ttk.Entry(frm, textvariable=id_producto, width=10)
        entry_id_producto.grid(row=3, column=1, padx=0,pady=2, sticky='W')
        entry_id_producto.bind('<Return>', on_enter_entry_id_producto)
        entry_id_producto.bind('<KP_Enter>', on_enter_entry_id_producto)

        cargar_productos()

        desc_producto=StringVar()
        #desc_producto.set(lista_descripcion_productos[0])
        cmb_desc_producto=ttk.Combobox(frm,width=30,textvariable=desc_producto, values=lista_nombres_productos, state="readonly")
        cmb_desc_producto.grid(column=2,row=3,pady=2,columnspan=4,sticky=W)
        cmb_desc_producto.bind("<<ComboboxSelected>>", capturar_descripcion_producto)
        cmb_desc_producto.bind('<KP_Enter>', on_enter_cmb_desc_producto)
        
        try:
            img_buscar=ImageTk.PhotoImage(Image.open("icons/8415529.png").resize((16,16)))
            btn_buscar_producto=ttk.Button(frm,image=img_buscar,width=32)
            btn_buscar_producto.grid(column=4,row=3)#Boton Buscar
            btn_buscar_producto.bind('<Return>', on_enter_entry_id_producto)
            btn_buscar_producto.bind('<KP_Enter>', on_enter_entry_id_producto)
            btn_buscar_producto.bind("<Button-1>", lambda event=None:on_enter_entry_id_producto(event))
          
        except: pass
        
        lbl_cantidad=ttk.Label(frm, text='Cantidad:',width=8)
        lbl_cantidad.grid(row=4, column=0, padx=0,pady=2,sticky='W')
        validate_cmd = vent_mermas.register(validar_merma_numerica)
        cantidad=StringVar()
        entry_cantidad=ttk.Entry(frm, textvariable=cantidad, width=10,validate="key", validatecommand=(validate_cmd, "%P"))
        entry_cantidad.grid(row=4, column=1, padx=0,pady=2, sticky='W')
        entry_cantidad.bind('<Return>', on_enter_entry_cantidad)
        entry_cantidad.bind('<KP_Enter>', on_enter_entry_cantidad)
      
        try:
            img_add=ImageTk.PhotoImage(Image.open("icons/8839040.png").resize((16,16)))
            btn_add=ttk.Button(frm,image=img_add,width=32,command=lambda event=None: agregar_producto(event))
            btn_add.grid(column=2,row=4)#Boton aagregar productos
            # Vincular la pulsación de tecla Enter al botón
            btn_add.bind("<Return>", agregar_producto)
            btn_add.bind('<KP_Enter>', agregar_producto)
            #btn_add.bind("<Button-1>", agregar_producto)
        except: print('hola');pass
        
        #--------------------------------------------------------------------------------------
            #CONFIGURAMOS EL TREE VIEW
        #--------------------------------------------------------------------------------------    
        # Crear un Treeview
        tree = ttk.Treeview(frm)
        tree["columns"] = ("1","2","3","4","5","6")

        # Configurar las columnas
        tree.column("#0", width=40, minwidth=40,stretch=tk.NO)
        tree.column("1", width=80, minwidth=80, stretch=tk.NO)
        tree.column("2", width=200, minwidth=200, stretch=tk.NO)
        tree.column("3", width=80, minwidth=80, stretch=tk.NO)
        tree.column("4", width=80, minwidth=80, stretch=tk.NO,anchor=E)
        tree.column("5", width=100, minwidth=100, stretch=tk.NO,anchor=E)
        tree.column("6", width=100, minwidth=100, stretch=tk.NO,anchor=E)

        # Configurar las cabeceras de las columnas
        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("1", text="Id", anchor=tk.W)
        tree.heading("2", text="Descripcion", anchor=tk.W)
        tree.heading("3", text="Und", anchor=tk.W)
        tree.heading("4", text="Cantidad", anchor=tk.W)
        tree.heading("5", text="Precio", anchor=tk.W)
        tree.heading("6", text="Total", anchor=tk.W)

        tree.tag_configure('right_align', anchor='e')
         
        # Mostrar el Treeview
        tree.grid(column=0,row=5,columnspan=6,pady=10,sticky="W")
        tree.bind("<Delete>", delete_selected_row)

        scrollbar = ttk.Scrollbar(frm, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=5, column=6, sticky="ns")

        lbl_total=ttk.Label(frm, text='TOTAL:',width=15,anchor='w',font=("Arial", 14, "bold"))
        lbl_total.grid(row=6, column=3, padx=0,pady=2,sticky='E')
        lbl_monto_total=ttk.Label(frm, text='0.00',width=20,anchor='e',font=("Arial", 14, "bold"),background='lightgreen')
        lbl_monto_total.grid(row=6, column=4,padx=0,pady=2)
        
        
        #--------------------------------------------------------------------------------------
            #Botones para manejo de acciones de la ventana (agregar-eliminar-actualizar-navegar-salir)
        #--------------------------------------------------------------------------------------
        botones=Botones(agregar_merma,eliminar_merma,actualizar_merma,navegar,confirmar_salir)
        botones.crear_botones(vent_mermas,0,7)
        
               
        cargar_mermas()
        mostrar_datos_merma()
        centrar_ventana(vent_mermas)
        
        vent_mermas.transient(root)  # Asociar la ventana hija a la ventana principal
        vent_mermas.grab_set()  # Evitar que el usuario interactúe con la ventana principal mientras la ventana hija está abierta
        vent_mermas.focus_set()# Establecer el foco en la ventana hija 

        
        vent_mermas.mainloop()

        
    #=============================================================================================================
        #CREAR VENTANA CONSULTA DE ARTICULO
    #=============================================================================================================
    
    def crear_vent_consulta_producto():
        
        nonlocal vent_consulta_producto

        def confirmar_salir():
            vent_consulta_producto.destroy()
        
        def sumar_columna():
            filas=tree.get_children()
            total=0
            for fila in filas:
                valores = tree.item(fila)['values']
                total+=float(valores[5])
            return total
        
        
        def navegar(boton):
            nonlocal indice_actual,id_merma_actual
            if diccionario_mermas!={}:
       
                if boton=='Primero':
                    indice_actual = 0
                elif boton=='Anterior':
                    indice_actual = (indice_actual - 1) % len(lista_id_productos)
                elif boton=='Siguiente':
                    indice_actual = (indice_actual + 1) % len(lista_id_productos)
                elif boton=='Ultimo':
                    indice_actual=len(lista_id_productos)-1
             
           
                mostrar_datos_producto()
        
        def mostrar_datos_producto():
            nonlocal img_path,imagenes,id_producto_actual,id_categoria_actual,id_subcategoria_actual,id_proveedor_actual

            if diccionario_productos!={}:
                id_producto_actual=lista_id_productos[indice_actual]
                
                id_categoria_actual=diccionario_productos[id_producto_actual]['Id_categoria']
                id_subcategoria_actual=diccionario_productos[id_producto_actual]['Id_subcategoria']
                id_proveedor_actual=diccionario_productos[id_producto_actual]['Id_proveedor']

                id_producto.set(id_producto_actual)
                sku_producto.set(diccionario_productos[id_producto_actual]['SKU'])
                desc_producto.set(diccionario_productos[id_producto_actual]['Descripcion'])
                
                lbl_categoria.config(text=diccionario_categorias[id_categoria_actual]['Nombre'])
                lbl_subcategoria.config(text=diccionario_subcategorias[id_categoria_actual][id_subcategoria_actual]['Nombre'])
                lbl_proveedor.config(text=diccionario_proveedores[id_proveedor_actual]['Nombre'])

                img_path=diccionario_productos[id_producto_actual]['img_path']
                

                if len(img_path):
                    try:
                        img_articulo=img_articulo=ImageTk.PhotoImage(Image.open(img_path).resize((100,100)))
                        lbl_img_producto.config(image=img_articulo)
                        imagenes[vent_consulta_producto]=img_articulo
                    except :
                        pass
                else:
                    img_nofoto=ImageTk.PhotoImage(Image.open("icons/nofoto.png").resize((32,32)))
                    lbl_img_producto.config(image=img_nofoto)
                    imagenes[vent_consulta_producto]=img_nofoto                
                
                for fila in tree.get_children():
                    tree.delete(fila)
                
                
                
                dic_filtro_producto_entradas={}
                for clave1, linea in diccionario_entradas.items():
                    for clave2, valores in linea.items():
                        if isinstance(valores, dict) and valores.get('Id_producto') == id_producto_actual:
                            dic_filtro_producto_entradas[clave1] = linea
       
                dic_filtro_producto_salidas={}
                for clave1, linea in diccionario_salidas.items():
                    for clave2, valores in linea.items():
                        if isinstance(valores, dict) and valores.get('Id_producto') == id_producto_actual:
                            dic_filtro_producto_salidas[clave1] = linea
                
                dic_filtro_producto_mermas={}
                for clave1, linea in diccionario_mermas.items():
                    for clave2, valores in linea.items():
                        if isinstance(valores, dict) and valores.get('Id_producto') == id_producto_actual:
                            dic_filtro_producto_mermas[clave1] = linea
                
                lista_detalle_entradas=[]
                for clave1, linea in dic_filtro_producto_entradas.items():
                    for clave2, valores in dic_filtro_producto_entradas[clave1].items():
                        lista_detalle_entradas.append([clave1, clave2,list(valores.values())])
                
                lista_detalle_salidas=[]
                for clave1, linea in dic_filtro_producto_salidas.items():
                    for clave2, valores in dic_filtro_producto_salidas[clave1].items():
                        lista_detalle_salidas.append([clave1, clave2,list(valores.values())])
                
                lista_detalle_mermas=[]
                for clave1, linea in dic_filtro_producto_mermas.items():
                    for clave2, valores in dic_filtro_producto_mermas[clave1].items():
                        lista_detalle_mermas.append([clave1, clave2,list(valores.values())])
                
                

                for elemento in lista_detalle_entradas:
                    elemento.extend(elemento.pop(2))
                
                for elemento in lista_detalle_salidas:
                    elemento.extend(elemento.pop(2))

                for elemento in lista_detalle_mermas:
                    elemento.extend(elemento.pop(2))
                
                for sublista in lista_detalle_salidas:
                    # Eliminar el elemento en el índice 3
                    sublista.pop(4)  # Esto eliminará el elemento 'D0002' en cada sublista

                # Función para convertir la fecha de string a objeto datetime para comparar correctamente
                def convertir_fecha(sublista):
                    fecha_str = sublista[5]  # Asumiendo que el índice 5 es donde se encuentra la fecha
                    return datetime.strptime(fecha_str, '%d/%m/%Y')

                lista_unida=lista_detalle_entradas + lista_detalle_salidas + lista_detalle_mermas
                
                # Ordenar la lista unida por la fecha
                lista_movimientos = sorted(lista_unida, key=convertir_fecha)
                #print(lista_movimientos)
                
                saldo=0
                total_entradas=0
                total_salidas=0
                total_mermas=0

                for i in range(len(lista_movimientos)):
                    tipo_doc= lista_movimientos[i][0][:1]
                    total_movimiento=float(lista_movimientos[i][8]) * float(lista_movimientos[i][9])
                    if tipo_doc=='E':
                        total_entradas+=total_movimiento
                        saldo+=float(lista_movimientos[i][8])
                        tree.insert("", tk.END, text=str(lista_movimientos[i][1]), values=(lista_movimientos[i][5], lista_movimientos[i][6],lista_movimientos[i][0],diccionario_productos[id_producto_actual]['Unidad'],
                                                                                            lista_movimientos[i][8], '',saldo,lista_movimientos[i][9],total_movimiento))
                    elif tipo_doc=='S' or tipo_doc=='M':
                        if tipo_doc=='S':
                            total_salidas+=total_movimiento
                        elif tipo_doc=='M': 
                            total_mermas+=total_movimiento
                        saldo-=float(lista_movimientos[i][8])
                        tree.insert("", tk.END, text=str(lista_movimientos[i][1]), values=(lista_movimientos[i][5], lista_movimientos[i][6],lista_movimientos[i][0],diccionario_productos[id_producto_actual]['Unidad'],
                                                                                                     '',float(lista_movimientos[i][8])*-1,saldo,lista_movimientos[i][9],total_movimiento*-1))
                
                lbl_total_entradas.config(text= "Entradas: "+"{:>10,.2f}".format(total_entradas))
                lbl_total_salidas.config(text= "Salidas: "+"{:>10,.2f}".format(total_salidas))
                lbl_total_mermas.config(text= "Mermas: "+"{:>10,.2f}".format(total_mermas))

        def on_double_click(event):
            nonlocal vent_consulta_producto

            item = tree.selection()[0]  # Obtener el ítem seleccionado
            values = tree.item(item, "values")  # Obtener los valores del ítem
            valor_columna = values[2]  # Obtener el valor de la segunda columna
            tipo_doc= valor_columna[:1]
            
            vent_consulta_producto.grab_release()
            
            if tipo_doc=='E':
                crear_vent_entradas(doc_referencia=valor_columna)
            elif tipo_doc=='S':
                crear_vent_salidas(doc_referencia=valor_columna)
            elif tipo_doc=='M':
                crear_vent_mermas(doc_referencia=valor_columna)   
     
        vent_consulta_producto=Toplevel(root)
        vent_consulta_producto.title("Consulta_producto.")
        vent_consulta_producto.resizable(0,0)
        vent_consulta_producto.geometry("925x525")

       
        frm = ttk.Frame(vent_consulta_producto,borderwidth=1, relief='solid',padding=5)
        frm.grid(column=0,row=0,pady=10,padx=10)
        frm.columnconfigure((1,2,3,4,5,6),weight=1) 
        frm.rowconfigure((0,1,2,3,4),weight=1)
         
                
        ttk.Label(frm, text='Id_producto:').grid(row=0, column=0, padx=2,pady=2,sticky='W')
        id_producto=StringVar()
        lbl_id_producto=ttk.Label(frm, textvariable=id_producto, width=10,borderwidth=1,relief='solid')
        lbl_id_producto.grid(row=0, column=1, padx=2,pady=2, sticky='W')
        
        ttk.Label(frm, text='SKU:',width=4).grid(row=0, column=2, padx=0,pady=2,sticky='E')
        sku_producto=StringVar()
        lbl_sku_producto=ttk.Label(frm, textvariable=sku_producto, width=10,borderwidth=1,relief='solid')
        lbl_sku_producto.grid(row=0, column=3, padx=0,pady=2, sticky='W')

        ttk.Label(frm, text='Descripcion:').grid(row=1, column=0, padx=2,pady=2,sticky='W')
        desc_producto=StringVar()
        lbl_descripcion=ttk.Label(frm, textvariable=desc_producto, width=40,borderwidth=1,relief='solid')
        lbl_descripcion.grid(row=1, column=1, padx=2,pady=2,columnspan=3,sticky='W')
        
        try:
            img_buscar=ImageTk.PhotoImage(Image.open("icons/8415529.png").resize((16,16)))
            btn_buscar=ttk.Button(frm,image=img_buscar,width=32)
            btn_buscar.grid(column=4,row=1, sticky='W')#Boton Buscar
       
            
            img_nofoto=ImageTk.PhotoImage(Image.open("icons/nofoto.png").resize((32,32)))
            lbl_img_producto=tk.Label(frm,borderwidth=1,image=img_nofoto,relief="solid" ,width=100,height=100)
            lbl_img_producto.grid(row=0, column=4,rowspan=4,  padx=2,pady=2,sticky='E')

        except: pass
        
        
       
        tk.Label(frm,text='Categoria: ').grid(column=0,row=2, sticky=W)
        lbl_categoria=ttk.Label(frm,text='',width=40,borderwidth=1,relief='solid')
        lbl_categoria.grid(column=1,row=2,columnspan=3, sticky=W)
        
        
        ttk.Label(frm,text='Sub categoria: ').grid(column=0,row=3, sticky=W)
        lbl_subcategoria=ttk.Label(frm,text='',width=40,borderwidth=1,relief='solid')
        lbl_subcategoria.grid(column=1,row=3,columnspan=3, sticky=W)
        
        
        ttk.Label(frm,text='Proveedor: ').grid(column=0,row=4, sticky=W)
        lbl_proveedor=ttk.Label(frm,text='',width=40,borderwidth=1,relief='solid')
        lbl_proveedor.grid(column=1,row=4,columnspan=3, sticky=W)
        
         
        
        #--------------------------------------------------------------------------------------
            #CONFIGURAMOS EL TREE VIEW
        #--------------------------------------------------------------------------------------    
        # Crear un Treeview
        tree = ttk.Treeview(frm)
        tree["columns"] = ("1","2","3","4","5","6","7","8","9")

        # Configurar las columnas
        tree.column("#0", width=40, minwidth=40,stretch=tk.NO)
        tree.column("1", width=80, minwidth=80, stretch=tk.NO)
        tree.column("2", width=80, minwidth=80, stretch=tk.NO)
        tree.column("3", width=80, minwidth=80, stretch=tk.NO)
        tree.column("4", width=100, minwidth=80, stretch=tk.NO,anchor=E)
        tree.column("5", width=100, minwidth=80, stretch=tk.NO,anchor=E)
        tree.column("6", width=100, minwidth=80, stretch=tk.NO,anchor=E)
        tree.column("7", width=100, minwidth=80, stretch=tk.NO,anchor=E)
        tree.column("8", width=100, minwidth=80, stretch=tk.NO,anchor=E)
        tree.column("9", width=100, minwidth=80, stretch=tk.NO,anchor=E)

        # Configurar las cabeceras de las columnas
        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("1", text="Fecha", anchor=tk.W)
        tree.heading("2", text="Tipo Mov.", anchor=tk.W)
        tree.heading("3", text="Ref.", anchor=tk.W)
        tree.heading("4", text="Und", anchor=tk.W)
        tree.heading("5", text="Cant. Entrada", anchor=tk.W)
        tree.heading("6", text="Cant. Salida", anchor=tk.W)
        tree.heading("7", text="Saldo", anchor=tk.W)
        tree.heading("8", text="Costo Unit.", anchor=tk.W)
        tree.heading("9", text="Costo Total.", anchor=tk.W)

        #tree.tag_configure('right_align', anchor='e')
         
        # Mostrar el Treeview
        tree.grid(column=0,row=5,columnspan=6,pady=10,sticky="W")
        # Enlazar la función al evento de doble clic
        tree.bind("<Double-1>", on_double_click)
        
        scrollbar = ttk.Scrollbar(frm, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=5, column=6, sticky="ns")


        lbl_total_entradas=ttk.Label(frm, text='Entradas: 0.00',width=20,anchor='e',font=("Arial", 14, "bold"),background='lightgreen')
        lbl_total_entradas.grid(row=6, column=2, padx=0,pady=2)
        
        lbl_total_salidas=ttk.Label(frm, text='Salidas: 0.00',width=20,anchor='e',font=("Arial", 14, "bold"),background='lightgreen')
        lbl_total_salidas.grid(row=6, column=3,padx=0,pady=2)
        
        lbl_total_mermas=ttk.Label(frm, text='Mermas: 0.00',width=20,anchor='e',font=("Arial", 14, "bold"),background='lightgreen')
        lbl_total_mermas.grid(row=6, column=4,padx=0,pady=2)
        
        
        #--------------------------------------------------------------------------------------
            #Botones para manejo de acciones de la ventana (agregar-eliminar-actualizar-navegar-salir)
        #--------------------------------------------------------------------------------------
        botones=Botones("","","",navegar,confirmar_salir)
        botones.crear_botones(vent_consulta_producto,0,6,True)
        

        vent_consulta_producto.transient(root)  # Asociar la ventana hija a la ventana principal
        vent_consulta_producto.grab_set()  # Evitar que el usuario interactúe con la ventana principal mientras la ventana hija está abierta
        vent_consulta_producto.focus_set()  # Establecer el foco en la ventana hija

        
        cargar_productos()
        cargar_entradas()
        cargar_salidas()
        cargar_mermas()
        cargar_categorias()
        cargar_subcategorias()
        cargar_proveedores()

        mostrar_datos_producto()
        
        centrar_ventana(vent_consulta_producto)
        vent_consulta_producto.mainloop()
    
    #=============================================================================================================
        #CREAR VENTANA DE REPORTES
    #=============================================================================================================
    
    def crear_vent_reportes():

        
        def capturar_tipo_reporte(event):
            tipo_reporte.set(cmb_reportes.get())

        def on_enter_cmb_reportes():pass


        def generar_reportes():
            fecha=datetime.now()
                
            # Crear un documento PDF
            
            nombre_reporte=f'Reportes/Reporte de {tipo_reporte.get()} al {fecha.strftime("%d-%m-%Y %H:%M:%S")}.pdf'
            doc = SimpleDocTemplate(nombre_reporte, pagesize=letter)
            styles = getSampleStyleSheet()

            # Contenido del reporte
            content = []

            # Título del reporte
            titulo =nombre_reporte[9:]
            titulo=titulo[:-4]
            titulo=Paragraph(titulo,styles["Title"])
            content.append(titulo)

            # Espacio antes de los datos
            content.append(Spacer(1, 12))

            if tipo_reporte.get()=='EXISTENCIAS':
                lista_existencias=[[clave,valor] for clave,valor in diccionario_productos.items()]
                
                valores_grandes_anidados = []

                for sublista_anidada in lista_existencias:
                    primer_elemento = sublista_anidada[0] #El id_producto
                    valores_anidados = [primer_elemento] + [valor for valor in sublista_anidada[1].values()]#los valores del diccionario anidado dentro de 
                    valores_grandes_anidados.append(valores_anidados)
                
                # Índices de los elementos a eliminar
                indices_a_eliminar = [1,2,3,4,7,8,10,11]
                
               
                # Eliminar elementos de la lista utilizando un ciclo for anidado con reversed()
                for indice1  in reversed(sorted(indices_a_eliminar)):
                    for indice2 in range(len(valores_grandes_anidados)): 
                            del valores_grandes_anidados[indice2][indice1]

                # Encabezados de la tabla
                encabezados = ["Id_producto", "Descripcion", "Unidad","Cantidad"]
                datos =valores_grandes_anidados

                # Crear una tabla y establecer estilos
                tabla_datos = Table([encabezados] + datos)
                tabla_datos.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.aqua),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('ALIGN',(1,0), (1,-1),'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
                ]))

                # Agregar tabla al contenido
                content.append(tabla_datos)
                content.append(Spacer(1, 12))

            elif tipo_reporte.get()=='EXISTENCIAS X CATEGORIAS':
                # Estilo para el texto del encabezado
                
                encabezado_style = styles["Heading4"]
                
                for id_cat, categoria in diccionario_categorias.items():
                    for producto  in diccionario_productos.values():
                        if producto['Id_categoria']==id_cat:
                            # Agregar el nombre de la categoría al documento
                            content.append(Paragraph(id_cat+' '+categoria['Nombre'], encabezado_style))
                            encabezados = ["Id_producto", "Descripcion", "Unidad","Cantidad"]
                           
                    
                            datos=[]
                            for id_prod, producto in diccionario_productos.items(): 
                                if producto['Id_categoria']==id_cat:
                                    datos.append([id_prod, producto["Descripcion"], producto["Unidad"], producto["Existencia"]])
                        
                            # Crear una tabla y establecer estilos
                            tabla_datos = Table([encabezados] + datos)
                            tabla_datos.setStyle(TableStyle([
                                ('BACKGROUND', (0, 0), (-1, 0), colors.aqua),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('ALIGN',(1,0), (1,-1),'LEFT'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ]))
                                #lista_productos_categoria = [[clave,producto["Descripcion"], diccionario_categorias[producto["Id_categoria"]]['Nombre'], 
                                #                              producto["Unidad"], producto["Existencia"]] for clave, producto in diccionario_productos.items()] 
                                #print(lista_productos_categoria)
                

                            # Agregar tabla al contenido
                            content.append(tabla_datos)
                            content.append(Spacer(1, 12)) 
                            break

            elif tipo_reporte.get()=='EXSISTENCIAS X SUBCATEGORIA':
                # Estilo para el texto del encabezado
                
                encabezado_style = styles["Heading4"]
               
                for id_cat, categoria in diccionario_categorias.items():
                    for  id_cat_madre,subcategoria  in diccionario_subcategorias.items():
                        if id_cat==id_cat_madre:
                            for  id_sub,valor  in subcategoria.items():
                                for id_prod, producto in diccionario_productos.items():
                                    if producto['Id_subcategoria']==id_sub:
                                         #Agregar el nombre de la categoría al documento
                                        content.append(Paragraph(id_cat+' '+categoria['Nombre'], encabezado_style))
                                        content.append(Paragraph(id_sub+' '+valor['Nombre'], ParagraphStyle(name='Normal', parent=styles["Heading3"],leftIndent=20)))
                                        encabezados = ["Id_producto", "Descripcion", "Unidad","Cantidad"]
                                
                                        datos=[]    
                                        for id_prod, producto in diccionario_productos.items():
                                            if producto['Id_subcategoria']==id_sub:
                                                datos.append([id_prod,producto['Descripcion'],producto['Unidad'],producto['Existencia']])
                                    
                    
                                    # Crear una tabla y establecer estilos
                                        tabla_datos = Table([encabezados] + datos,colWidths=[60,300,70.70])
                                        tabla_datos.setStyle(TableStyle([
                                            ('BACKGROUND', (0, 0), (-1, 0), colors.aqua),
                                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                            ('ALIGN',(1,0), (1,-1),'LEFT'),
                                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                            ('WORDWRAP', (0, 0), (-1, -1), True)
                                        ]))
                                                                

                                        # Agregar tabla al contenido
                                        content.append(tabla_datos)
                                        content.append(Spacer(1, 12)) 
                                        break
                                        

            elif tipo_reporte.get()=='CONSUMOS X DEPARTAMENTO':
                # Estilo para el texto del encabezado
                
                encabezado_style = styles["Heading4"]
                
                for id_dep, departamento in diccionario_departamentos.items():
                    lista_consumos_departamento=[]
                    for id_sal,lineas  in diccionario_salidas.items():
                        for linea in lineas.values():
                            if linea['Id_departamento']==id_dep:
                                lista_consumos_departamento.append([id_sal, id_dep, linea['Id_producto'], linea['Cantidad_salida'], linea['Precio_salida']])    
                
                
                    for item in lista_consumos_departamento:

                        # Agregar el nombre de la categoría al documento
                        content.append(Paragraph(item[1]+' '+diccionario_departamentos[item[1]]['Nombre'], encabezado_style))
                        encabezados = ["Id_salida","Id_producto", "Descripcion", "Unidad","Cantidad"]
                    
            
                        datos=[]
                        total_departamento=0
                        for item in lista_consumos_departamento:
                            datos.append([item[0],item[2], diccionario_productos[item[2]]["Descripcion"], diccionario_productos[item[2]]["Unidad"], item[3],item[4],float(item[3])*float(item[4])])
                        
                        total_departamento+=sum(datos[i][6] for i in range(len(datos))) 

                        datos.append(['Total', '','','','','', total_departamento])
    
                        # Crear una tabla y establecer estilos
                        tabla_datos = Table([encabezados] + datos)
                        tabla_datos.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.aqua),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('ALIGN',(1,0), (1,-1),'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Cambiar la fuente a negrita en la última fila
                            ('TEXTCOLOR', (0, -1), (-1, -1), colors.red),  # Cambiar el color del texto en la última fila
                            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey)  # Cambiar el color de fondo en la última fila

                        ]))
                            #lista_productos_categoria = [[clave,producto["Descripcion"], diccionario_categorias[producto["Id_categoria"]]['Nombre'], 
                        #                              producto["Unidad"], producto["Existencia"]] for clave, producto in diccionario_productos.items()] 
                        #print(lista_productos_categoria)


                        # Agregar tabla al contenido
                        content.append(tabla_datos)
                        content.append(Spacer(1, 12)) 
                        break

            elif tipo_reporte.get()=='ENTRADAS':

                encabezado_style = styles["Heading4"]
                datos=[]
                i=0
                for id_ent, lineas in diccionario_entradas.items():
                    for linea in lineas.values():
                    
                        #content.append(Paragraph(item[1]+' '+diccionario_departamentos[item[1]]['Nombre'], encabezado_style))
                        encabezados = ["Id_entrada","Doc_ref","Tipo","Fecha", "Proveedor","Monto"]
                        id_proveed=diccionario_productos[linea['Id_producto']]['Id_proveedor']
                        
                        datos.append([id_ent, linea['Num_doc_entrada'], linea['Tipo_entrada'], linea["Fecha_entrada"], diccionario_proveedores[id_proveed]['Nombre']])
                        
                        total_entrada=0
                        for linea in lineas.values():
                            total_entrada+=float(linea['Cantidad_entrada'])*float(linea['Precio_entrada'])
                        
                        datos[i].append(total_entrada)
                        
                        i+=1
                        break

                total_entradas=0

                print(datos)
                total_entradas+=sum(datos[i][5] for i in range(len(datos))) 

                datos.append(['Total', '','','','', total_entradas])

                # Crear una tabla y establecer estilos
                tabla_datos = Table([encabezados] + datos)
                tabla_datos.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.aqua),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('ALIGN',(1,0), (1,-1),'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Cambiar la fuente a negrita en la última fila
                    ('TEXTCOLOR', (0, -1), (-1, -1), colors.red),  # Cambiar el color del texto en la última fila
                    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey)  # Cambiar el color de fondo en la última fila

                ]))
                    #lista_productos_categoria = [[clave,producto["Descripcion"], diccionario_categorias[producto["Id_categoria"]]['Nombre'], 
                #                              producto["Unidad"], producto["Existencia"]] for clave, producto in diccionario_productos.items()] 
                #print(lista_productos_categoria)


                # Agregar tabla al contenido
                content.append(tabla_datos)
                content.append(Spacer(1, 12))
            
            elif tipo_reporte.get()=='SALIDAS':

                encabezado_style = styles["Heading4"]
                datos=[]
                i=0
                for id_sal, lineas in diccionario_salidas.items():
                    for linea in lineas.values():
                    
                        #content.append(Paragraph(item[1]+' '+diccionario_departamentos[item[1]]['Nombre'], encabezado_style))
                        encabezados = ["Id_salida","Doc_ref","Tipo","Fecha", "Departamento","Monto"]
                        id_depart=linea['Id_departamento']
                        
                        datos.append([id_sal, linea['Num_doc_salida'], linea['Tipo_salida'], linea["Fecha_salida"], diccionario_departamentos[id_depart]['Nombre']])
                        
                        total_salida=0
                        for linea in lineas.values():
                            total_salida+=float(linea['Cantidad_salida'])*float(linea['Precio_salida'])
                        
                        datos[i].append(total_salida)
                        
                        i+=1
                        break

                total_salidas=0

                print(datos)
                total_salidas+=sum(datos[i][5] for i in range(len(datos))) 

                datos.append(['Total', '','','','', total_salidas])

                # Crear una tabla y establecer estilos
                tabla_datos = Table([encabezados] + datos)
                tabla_datos.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.aqua),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('ALIGN',(1,0), (1,-1),'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Cambiar la fuente a negrita en la última fila
                    ('TEXTCOLOR', (0, -1), (-1, -1), colors.red),  # Cambiar el color del texto en la última fila
                    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey)  # Cambiar el color de fondo en la última fila

                ]))
                    #lista_productos_categoria = [[clave,producto["Descripcion"], diccionario_categorias[producto["Id_categoria"]]['Nombre'], 
                #                              producto["Unidad"], producto["Existencia"]] for clave, producto in diccionario_productos.items()] 
                #print(lista_productos_categoria)


                # Agregar tabla al contenido
                content.append(tabla_datos)
                content.append(Spacer(1, 12))

            elif tipo_reporte.get()=='MERMAS':

                encabezado_style = styles["Heading4"]
                datos=[]
                i=0
                for id_merm, lineas in diccionario_mermas.items():
                    for linea in lineas.values():
                    
                        #content.append(Paragraph(item[1]+' '+diccionario_departamentos[item[1]]['Nombre'], encabezado_style))
                        encabezados = ["Id_merma","Doc_ref","Tipo","Fecha", "Monto"]
                       
                        datos.append([id_merm, linea['Num_doc_merma'], linea['Tipo_merma'], linea["Fecha_merma"]])
                        
                        total_merma=0
                        for linea in lineas.values():
                            total_merma+=float(linea['Cantidad_merma'])*float(linea['Precio_merma'])
                        
                        datos[i].append(total_merma)
                        
                        i+=1
                        break

                total_mermas=0

                print(datos)
                total_mermas+=sum(datos[i][4] for i in range(len(datos))) 

                datos.append(['Total', '','','', total_mermas])

                # Crear una tabla y establecer estilos
                tabla_datos = Table([encabezados] + datos)
                tabla_datos.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.aqua),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('ALIGN',(1,0), (1,-1),'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Cambiar la fuente a negrita en la última fila
                    ('TEXTCOLOR', (0, -1), (-1, -1), colors.red),  # Cambiar el color del texto en la última fila
                    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey)  # Cambiar el color de fondo en la última fila

                ]))
                    #lista_productos_categoria = [[clave,producto["Descripcion"], diccionario_categorias[producto["Id_categoria"]]['Nombre'], 
                #                              producto["Unidad"], producto["Existencia"]] for clave, producto in diccionario_productos.items()] 
                #print(lista_productos_categoria)


                # Agregar tabla al contenido
                content.append(tabla_datos)
                content.append(Spacer(1, 12))
                            
            # Texto de pie de página-----------------------------------------------------------------------
            footer_text = "Zentock Reportes."
            footer = Paragraph(footer_text, styles["Normal"])
            content.append(footer)

            # Construir el reporte
            doc.build(content)


            # Ruta al archivo PDF
            ruta_pdf = nombre_reporte

            # Comando para abrir el archivo PDF con el visor predeterminado
            comando = ["xdg-open", ruta_pdf]

            # Abrir el archivo PDF con el visor predeterminado
            subprocess.Popen(comando)
                
                

               
    
        vent_reportes=Toplevel(root)
        vent_reportes.title("Reportes.")
        vent_reportes.geometry("450x200")
        vent_reportes.resizable(0,0)
        vent_reportes.columnconfigure(0,weight=1)
        vent_reportes.rowconfigure(0,weight=1)
        

        lista_reportes=['EXISTENCIAS','EXISTENCIAS X CATEGORIAS','EXSISTENCIAS X SUBCATEGORIA','CONSUMOS X DEPARTAMENTO','ENTRADAS','SALIDAS','MERMAS']
        
        frm=ttk.Frame(vent_reportes,borderwidth=1,relief='solid',height=300)
        frm.pack(fill='x',padx=5,pady=5)
        frm.columnconfigure((0,1,2),weight=1)

       
        ttk.Label(frm,text='Seleccione un reporte: ',font=("Helvetica", 14,'bold')).grid(column=1,row=0,padx=2,pady=10)
        
        
        # Crear el estilo para el Combobox
        style = ttk.Style()
        style.theme_use('clam')  # Puedes cambiar 'clam' por otro tema si lo deseas

        # Establecer el estilo del Combobox
        style.configure('TCombobox', background="lightblue", font=('Helvetica', 14,'bold'), fieldbackground="lightblue", selectbackground="lightblue", selectforeground="black")
       
        tipo_reporte=StringVar()
        tipo_reporte.set(lista_reportes[0])
        cmb_reportes=ttk.Combobox(frm,textvariable=tipo_reporte,values=lista_reportes,style='TCombobox',width=30)
        cmb_reportes.grid(column=1,row=1,padx=10,pady=10)
        cmb_reportes.bind("<<ComboboxSelected>>", capturar_tipo_reporte)
        cmb_reportes.bind('<KP_Enter>', on_enter_cmb_reportes)
        
        style.configure('TButton', font=('Helvetica', 14,'bold'))
        
        btn_generar=ttk.Button(vent_reportes,text='Generar Rporte',style='TButton',command=generar_reportes)
        btn_generar.pack(pady=10)
        
        cargar_productos()
        cargar_categorias()
        cargar_subcategorias()
        cargar_departamentos()
        cargar_entradas()
        cargar_salidas()
        cargar_mermas()
        cargar_proveedores()


        vent_reportes.transient(root)
        vent_reportes.grab_set()
        vent_reportes.focus_set()

        vent_reportes.wait_window()

    #==========================================================================================================
        #CREAMOS LA VENTANA SEND LIST
    #==========================================================================================================
    
    def crear_vent_sendlist():
        report_body=""
        attachment_path=""

        def validar_envio():
            if to_email.get()=='':
                messagebox.showwarning('Advertencia','Debe especificar un destinatario de correo')
                entry_to_email.focus()
                return False
            elif email_subject=='':
                messagebox.showwarning('Advertencia','Debe especificar un asunto.')
                entry_subject.focus()
                return False
            elif attachment_path=='':
                messagebox.showwarning('Advertencia','Debe generar un PDF para adjuntar.')
                btn_generar_pdf.focus()
                return False
            else: return True

            
        def send_email(subject, body, to_email, attachment_path):
            if validar_envio():
                # Set up the SMTP server
                smtp_server = 'smtp.gmail.com'
                smtp_port = 587
                smtp_username = 'hdelgados74@gmail.com'
                smtp_password = 'xckt muuk dbdi ztgi'
                
                # Create a multipart message
                msg = MIMEMultipart()
                msg['From'] = smtp_username
                msg['To'] = to_email
                msg['Subject'] = subject
                
                # Attach the body to the message
                msg.attach(MIMEText(body, 'plain'))
                
                # Attach the PDF file
                with open(attachment_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {attachment_path}")
                
                msg.attach(part)
                
                # Connect to the SMTP server
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(smtp_username, smtp_password)
                
                # Send the email
                server.sendmail(smtp_username, to_email, msg.as_string())
                
                # Close the connection
                server.quit()

        
        def generar_pdf():
            nonlocal  attachment_path
            fecha=datetime.now()
                
            # Crear un documento PDF
            
            nombre_reporte=f'Reportes/Reporte SEND-LIST al {fecha.strftime("%d-%m-%Y %H:%M:%S")}.pdf'
            
            attachment_path=nombre_reporte

            doc = SimpleDocTemplate(nombre_reporte, pagesize=letter)
            styles = getSampleStyleSheet()

            # Contenido del reporte
            content = []
            
            # Título del reporte
            titulo =nombre_reporte[9:]
            lbl_adjunto.config(text='Archivo adjunto: '+ titulo)
            
            titulo=titulo[:-4]
            titulo=Paragraph(titulo,styles["Title"])
            content.append(titulo)

            # Espacio antes de los datos
            content.append(Spacer(1, 12))

            #------------------------------------------------------------------
            # Encabezados de la tabla
            encabezados = ["Id_producto", "Descripcion", "Unidad","Cantidad"]
            
            datos=[[clave,valor['Descripcion'],valor['Unidad'],valor['Existencia']] for clave,valor in diccionario_productos.items() if float(valor['Existencia'])<= float(valor['Minimo'])]
            
            # Crear una tabla y establecer estilos
            tabla_datos = Table([encabezados] + datos)
            tabla_datos.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.aqua),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN',(1,0), (1,-1),'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
            ]))

            # Agregar tabla al contenido
            content.append(tabla_datos)
            content.append(Spacer(1, 12))
            #-----------------------------------------------------------
            # Texto de pie de página
            footer_text = "Zentock Reportes."
            footer = Paragraph(footer_text, styles["Normal"])
            content.append(footer)

            # Construir el reporte
            doc.build(content)

             # Ruta al archivo PDF
            ruta_pdf = nombre_reporte

            tamano=os.path.getsize(ruta_pdf) / 1024
                    
            lbl_adjunto.config(text=lbl_adjunto.cget("text") +' ('+ "{:,.2f}".format(tamano) +'KB'+')')

           
            # Comando para abrir el archivo PDF con el visor predeterminado
            comando = ["xdg-open", ruta_pdf]

            # Abrir el archivo PDF con el visor predeterminado
            subprocess.Popen(comando)

        
             
          
        vent_sendlist=Toplevel(root)
        vent_sendlist.title("sendlist.")
        vent_sendlist.geometry("675x400")
        vent_sendlist.resizable(0,0)
        vent_sendlist.columnconfigure(0,weight=1)
        vent_sendlist.rowconfigure(0,weight=1)
        
        # Crear el estilo para el Combobox
        style = ttk.Style()
        style.theme_use('clam')  # Puedes cambiar 'clam' por otro tema si lo deseas

        frm=ttk.Frame(vent_sendlist,borderwidth=1,relief='solid',height=300)
        frm.pack(fill='x',padx=5,pady=5)
        frm.columnconfigure((1,2,3),weight=1)

        cargar_usuarios()

        ttk.Label(frm,text='De: ',font=("Helvetica", 12,'bold')).grid(column=0,row=1,padx=2,pady=2,sticky='W')
        from_email=StringVar()
        from_email.set( diccionario_usuarios["U0001"]["Correo"])
        entry_from_email=ttk.Entry(frm,textvariable=from_email,width=30)
        entry_from_email.grid(column=1,row=1,sticky='W')

        ttk.Label(frm,text='Para: ',font=("Helvetica", 12,'bold')).grid(column=0,row=2,padx=2,pady=2,sticky='W')
        to_email=StringVar()
        entry_to_email=ttk.Entry(frm,textvariable=to_email,width=30)
        entry_to_email.grid(column=1,row=2,sticky='W')

        ttk.Label(frm,text='Asunto: ',font=("Helvetica", 12,'bold')).grid(column=0,row=3,padx=2,pady=2,sticky='W')
        email_subject=StringVar()
        email_subject.set('Send-List')
        entry_subject=ttk.Entry(frm,textvariable=email_subject,width=30)
        entry_subject.grid(column=1,row=3,sticky='W')

        
        text_report_body=tk.Text(frm, height=10, width=80 )
        text_report_body.grid(column=0,row=4,columnspan=3,padx=5)
        text_report_body.insert('1.0','Sr(es):\nLista de Reorden al '+ str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))

        lbl_adjunto=ttk.Label(frm,text='()',font=("Helvetica", 10,'bold'),foreground='blue')
        lbl_adjunto.grid(column=0,row=5,padx=5,pady=10,columnspan=4,sticky='W')

        btn_generar_pdf=ttk.Button(frm,text='Generar PDF ',style='TButton',command=generar_pdf)
        btn_generar_pdf.grid(column=1,row=6,sticky='W')

        btn_enviar=ttk.Button(frm,text='Enviar',style='TButton',command=lambda:  send_email(email_subject.get(), text_report_body.get("1.0", "end-1c"), to_email.get(),  attachment_path))
        btn_enviar.grid(column=2,row=6,sticky='W')

        ttk.Label(frm).grid(column=0,row=7,pady=20)



        cargar_productos()
        
        

        vent_sendlist.transient(root)
        vent_sendlist.grab_set()
        vent_sendlist.focus_set()

        vent_sendlist.wait_window()
    #==========================================================================================================
        #CREAMOS LA VENTANA USUARIOS
    #==========================================================================================================
    def crear_vent_usuarios():
       
        correo_actual=''
        usuario_actual=''
        contrasena_actual=''
        pin_actual=''
     
        
        def validar_correo(nuevo_correo):
            if correo_actual!=nuevo_correo or nuevo_correo=='':
                if not validar_patron_correo(nuevo_correo):
                    messagebox.showinfo('Informacion','El patron correo no valido, intente de nuevo.')
                    return False
                else:        
                    for item in diccionario_usuarios.values():#Verificar si el correo existe
                        if nuevo_correo==item['Correo']:
                            messagebox.showinfo('Informacion','El correo ya existe, intente de nuevo.')
                            return False
                    else: return True
            else: return True
        
        def validar_usuario(nuevo_usuario):
            if usuario_actual!=nuevo_usuario or nuevo_usuario=='':      
                if (len(nuevo_usuario)<8 or len(nuevo_usuario)>8) or  not contiene_letras_numeros(nuevo_usuario):
                    messagebox.showinfo('Informacion','Debe ingresar un usuario de 8 caracteres que contenga numeros y letras')
                    return False
                else:
                    for item in diccionario_usuarios.values():  #Verificar si usuario ya existe       
                        if nuevo_usuario==item['Usuario']:
                            messagebox.showinfo('Informacion','El usuario ya existe, intente de nuevo.')
                            return False
                    else: return True
            else: return True
                         
        def validar_contrasena1(nueva_contrasena):
            if contrasena_actual!=nueva_contrasena or nueva_contrasena=='':
                if (len(nueva_contrasena)<8 or len(nueva_contrasena)>8) or  not contiene_letras_numeros(nueva_contrasena):
                    messagebox.showinfo('Informacion','Debe ingresar una contrasena de 8 caracteres que contenga numeros y letras')
                    return False
                elif nueva_contrasena==usuario.get():
                    messagebox.showinfo('Informacion','La contrasena debe ser diferente del usuario.')
                    return False
                else:        
                    for item in diccionario_usuarios.values():#Verificar si contrasena ya existe
                        if nueva_contrasena==item['Contrasena']:
                            messagebox.showinfo('Informacion','La contrasena ya existe, intente de nuevo.')
                            return False
                    else: return True
            else: return True 
        
        def confirmar_contrasenas(nueva_contrasena):
            if contrasena_actual!=nueva_contrasena or nueva_contrasena=='':
                if nueva_contrasena!=contrasena2.get():
                    messagebox.showinfo('Informacion','Contrasenas no coinciden, intente de nuevo.')
                    return False
                else: return True
            else: return True
    
        def validar_pin(nuevo_pin):
            if pin_actual!=nuevo_pin or nuevo_pin=='':
                if (len(nuevo_pin)<4 or len(nuevo_pin)>4) or  not nuevo_pin.isdigit() :
                    messagebox.showinfo('Informacion','Debe ingresar un numerico de 4 caracteres')
                    return False   
                else:
                    for item in diccionario_usuarios.values(): #Verifica si pin ya existe
                        if nuevo_pin==item['Pin']:
                            messagebox.showinfo('Informacion','El pin ya existe, intente de nuevo.')
                            return False
                    else: return True
            else: return True

        def confirmar_eliminar():
            return messagebox.askokcancel("Eliminar usuario", "¿Seguro que quieres eliminar este usuario?")
                 
        def capturar_opcion_rol(event):
            rol_usuario = cmb_rol_usuario.get()
        
        def capturar_opcion_estado(event):
            estado_usuario = cmb_estado_usuario.get()
        
        def actualizar_diccionario_usuarios():
            nonlocal indice_actual, lista_id_usuarios, diccionario_usuarios

            diccionario_usuarios.update({id_usuario.get():{'Nombre':nombre_usuario.get().strip(), 'Correo':correo_usuario.get().strip(),'Telefono':telefono_usuario.get().strip(),
                                    'Usuario':usuario.get().strip(), 'Contrasena':contrasena1.get().strip(),
                                    'Pin':pin.get().strip(), 'Rol':cmb_rol_usuario.get().strip(),'Estado':cmb_estado_usuario.get().strip()}})
            
                
        def navegar(boton):
            nonlocal indice_actual

            if diccionario_usuarios!={}:
                if boton=='Primero':
                    indice_actual = 0
                elif boton=='Anterior':
                    indice_actual = (indice_actual - 1) % len(lista_id_usuarios)
                elif boton=='Siguiente':
                    indice_actual = (indice_actual + 1) % len(lista_id_usuarios)
                elif boton=='Ultimo':
                    indice_actual=len(lista_id_usuarios)-1
                
                

                limpiar_variables()# Variables que se utilizar para saber si una entrada cambio para validarla
                mostrar_datos()
        
        def mostrar_datos():
            
            if diccionario_usuarios!={}:
                id_usuario_actual=lista_id_usuarios[indice_actual]
                id_usuario.set(id_usuario_actual)
                nombre_usuario.set(diccionario_usuarios[id_usuario_actual]['Nombre'])
                correo_usuario.set(diccionario_usuarios[id_usuario_actual]['Correo'])
                telefono_usuario.set(diccionario_usuarios[id_usuario_actual]['Telefono'])
                usuario.set(diccionario_usuarios[id_usuario_actual]['Usuario'])
                contrasena1.set(diccionario_usuarios[id_usuario_actual]['Contrasena'])
                pin.set(diccionario_usuarios[id_usuario_actual]['Pin'])
                rol_usuario.set(diccionario_usuarios[id_usuario_actual]['Rol'])
                estado_usuario.set(diccionario_usuarios[id_usuario_actual]['Estado'])
                actualizar_banderas_de_validacion()
        
        def actualizar_banderas_de_validacion():
            nonlocal correo_actual, usuario_actual,contrasena_actual, pin_actual
            correo_actual=correo_usuario.get()
            usuario_actual=usuario.get()
            contrasena_actual=contrasena1.get()
            pin_actual=pin.get()

        def validar_datos_usuario():    
            valor_nombre_usuario=nombre_usuario.get()
            valor_correo_usuario=correo_usuario.get()
            valor_usuario=usuario.get()
            valor_contrasena1=contrasena1.get()
            valor_contrasena2=contrasena2.get()
            valor_pin=pin.get()

            if not len(valor_nombre_usuario):
                messagebox.showinfo('Informacion','Debe ingresar un nombre de usuario')
                entry_nombre_usuario.focus()
                return False
            elif not validar_correo(valor_correo_usuario):
                entry_correo.focus()
                return False
            elif not validar_usuario(valor_usuario):
                entry_usuario.focus()
                return False
            elif not validar_contrasena1(valor_contrasena1):
                entry_contrasena1.focus()
                return False
            elif not confirmar_contrasenas(valor_contrasena1):
                entry_contrasena2.focus()
                return False
            elif not validar_pin(valor_pin):
                entry_pin.focus()
                return False
            else: return True
                
        def limpiar_widgets():
            id_usuario.set('')
            nombre_usuario.set('')
            correo_usuario.set('')
            telefono_usuario.set('')
            usuario.set('')
            contrasena1.set('')
            contrasena2.set('')
            pin.set('')
            cmb_rol_usuario.set('Empleado')
            cmb_estado_usuario.set('Activo')

        def limpiar_variables():    #limpiamos la variables de navegacion que usamos para validar al actualizar
            nonlocal correo_actual,usuario_actual,contrasena_actual,pin_actual

            correo_actual=''
            usuario_actual=''
            contrasena_actual=''
            pin_actual=''
                
        def eliminar_usuario():
            nonlocal indice_actual, lista_id_usuarios, diccionario_usuarios

            if diccionario_usuarios!={}:
                resp=confirmar_eliminar()
                if resp:
                    diccionario_usuarios.pop(id_usuario_actual)
                    lista_id_usuarios.pop(indice_actual)
                    indice_actual-=1
                    actualizar_archivo_usuarios()
                    mostrar_datos()
                    messagebox.showinfo('Info','Registro eliminado exitosamente.')

        def actualizar_usuario():
            if diccionario_usuarios!={}:
                if validar_datos_usuario():
                    actualizar_diccionario_usuarios()
                    actualizar_archivo_usuarios()
                    actualizar_banderas_de_validacion()
                    messagebox.showinfo('Informacion','Registro actualizado exitosamente.')

        def guardar_nuevo_usuario():       
            try:
                with open('Archivos/Usuarios.txt','a') as archivo:
                    archivo.write(id_usuario.get().strip()+'|'+ nombre_usuario.get().strip() +'|'+ correo_usuario.get().strip() +'|'+ telefono_usuario.get().strip()+'|'+usuario.get().strip()+'|'+
                                    contrasena1.get().strip()+'|'+ pin.get().strip() +'|'+ rol_usuario.get().strip() +'|'+ estado_usuario.get().strip()+'\n')       
            except FileNotFoundError as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}") 
            except IOError as e:
                messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")
           
        def agregar_usuario():
            nonlocal indice_actual,lista_id_usuarios, agregando_usuario    
            if agregando_usuario:
                if validar_datos_usuario():    
                    guardar_nuevo_usuario()
                    actualizar_diccionario_usuarios()
                    lista_id_usuarios=(list(diccionario_usuarios))
                    indice_actual=len(lista_id_usuarios)-1
                    agregando_usuario=not agregando_usuario
                    actualizar_banderas_de_validacion()
                    botones.cambiar_imagenes_al_navegar()
                    messagebox.showinfo('Info','Registro agregado exitosamente.')    
            else: 
                limpiar_widgets()
                limpiar_variables()

                if lista_id_usuarios!=[]:
                    id_usuario.set(generar_codigo(lista_id_usuarios,4))
                else:
                    lista_id_usuarios.append('U0000') 
                    id_usuario.set(generar_codigo(lista_id_usuarios,4))

                agregando_usuario=not agregando_usuario
                #Desactivamos los bootones de navegacion y cambiamos sus imagenes               
                botones.cambiar_imagenes_al_agregar()
                entry_nombre_usuario.focus()   

        def confirmar_salir():
            nonlocal agregando_usuario

            if agregando_usuario==False:
                vent_usuarios.destroy()
            else: 
                agregando_usuario=not agregando_usuario
                botones.cambiar_imagenes_al_navegar()
                if diccionario_usuarios!={}:
                    mostrar_datos()

        #Creamos la ventana de usuarios
        global vent_usuarios
        vent_usuarios=Toplevel(root)
        vent_usuarios.title("Mantenimiento de usuarios.")
        vent_usuarios.geometry("500x350")
        vent_usuarios.resizable(0,0)

        #Creamos los frames que van a contener widget de entrada y botones
        frm = ttk.Frame(vent_usuarios,borderwidth=1, relief='solid',padding=5)
        frm.grid(row=0,column=0,padx=10,pady=10)
        frm.columnconfigure((0,1,2),weight=1)
        frm.rowconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
            
        frm_botones = ttk.Frame(vent_usuarios)
        frm_botones.grid(row=1,column=0,padx=5,pady=5)

        #--------------------------------------------------------------------------------------------
            # Creamos los widgets de entrada
        #---------------------------------------------------------------------------------------------
        ttk.Label(frm,text='Id Usuario:').grid(column=0,row=0, sticky=W)
        id_usuario=StringVar()
        entry_id_usuario=ttk.Entry(frm,width=12,textvariable=id_usuario,state=DISABLED)
        entry_id_usuario.grid(column=1,row=0,sticky=W)

        ttk.Label(frm,text='Nombre:').grid(column=0,row=1, sticky=W)
        nombre_usuario=StringVar()
        entry_nombre_usuario=ttk.Entry(frm,width=30,textvariable=nombre_usuario)
        entry_nombre_usuario.grid(column=1,row=1,sticky=W)
        
        
        img_buscar=ImageTk.PhotoImage(Image.open("icons/8415529.png").resize((16,16)))
        ttk.Button(frm,image=img_buscar,width=32).grid(column=2,row=1, sticky=W)#Boton Buscar

        validar_nuevo_correo = vent_usuarios.register(validar_correo)  
        ttk.Label(frm,text='Correo:').grid(column=0,row=3, sticky=W)
        correo_usuario=StringVar()
        entry_correo=ttk.Entry(frm,width=30,textvariable=correo_usuario,validate="focusout", validatecommand=(validar_nuevo_correo, "%P"))
        entry_correo.grid(column=1,row=3,sticky=W)
        
        ttk.Label(frm,text='Telefono:').grid(column=0,row=4, sticky=W)
        telefono_usuario=StringVar()
        entry_telefono=ttk.Entry(frm,width=30,textvariable=telefono_usuario)
        entry_telefono.grid(column=1,row=4,sticky=W)

        validar_nuevo_usuario = vent_usuarios.register(validar_usuario)
        ttk.Label(frm,text='Usuario:').grid(column=0,row=5, sticky=W)
        usuario=StringVar()
        entry_usuario=ttk.Entry(frm,width=30,textvariable=usuario)
        entry_usuario.grid(column=1,row=5,sticky=W)
        entry_usuario.config(validate="focusout", validatecommand=(validar_nuevo_usuario, "%P"))
        
        #entry_usuario.bind("<FocusOut>", on_focus_out)
       
        validar_nueva_contrasena= vent_usuarios.register(validar_contrasena1)
        ttk.Label(frm,text='Contrasena:').grid(column=0,row=6, sticky=W)
        contrasena1=StringVar()
        entry_contrasena1=ttk.Entry(frm,width=12,textvariable=contrasena1)
        entry_contrasena1.config(validate="focusout", validatecommand=(validar_nueva_contrasena, "%P"))
        entry_contrasena1.grid(column=1,row=6,sticky=W)
        
        #entry_contrasena1.bind("<FocusOut>", on_focus_out)
        
        confirmar_contrasena2=vent_usuarios.register(confirmar_contrasenas)
        ttk.Label(frm,text='Confirmar contrasena:').grid(column=0,row=7, sticky=W)
        contrasena2=StringVar()
        entry_contrasena2=ttk.Entry(frm,width=12,textvariable=contrasena2,validate="focusout", validatecommand=(confirmar_contrasena2))
        entry_contrasena2.grid(column=1,row=7,sticky=W)
       
        
        validar_nuevo_pin=vent_usuarios.register(validar_pin)
        ttk.Label(frm,text='Pin:').grid(column=0,row=8, sticky=W)
        pin=StringVar()
        entry_pin=ttk.Entry(frm,width=12,textvariable=pin,validate="focusout", validatecommand=(validar_nuevo_pin, "%P"))
        entry_pin.grid(column=1,row=8,sticky=W)
       
        
        ttk.Label(frm,text='Rol de usuario:').grid(column=0,row=9, sticky=W)
        opciones_rol=['Empleado','Administrador']
        rol_usuario=StringVar()
        rol_usuario.set(opciones_rol[0])
        cmb_rol_usuario=ttk.Combobox(frm,width=12,textvariable=rol_usuario, values=opciones_rol,state="readonly")
        cmb_rol_usuario.grid(column=1,row=9,sticky=W)
        cmb_rol_usuario.bind("<<ComboboxSelected>>", capturar_opcion_rol)
        
        
        ttk.Label(frm,text='Estado:').grid(column=0,row=10, sticky=W)
        opciones_estado=['Activo','Inactivo']
        estado_usuario=StringVar()
        estado_usuario.set(opciones_estado[0])
        cmb_estado_usuario=ttk.Combobox(frm,width=12,textvariable=estado_usuario,values=opciones_estado,state="readonly")
        cmb_estado_usuario.grid(column=1,row=10,sticky=W)
        cmb_estado_usuario.bind("<<ComboboxSelected>>", capturar_opcion_estado)
        
        widgets_hijos = frm.winfo_children()
    
        # Iterar sobre la lista de widgets hijos y aplicar propiedades
        for widget_hijo in widgets_hijos:
            # Establecer un padding
            widget_hijo.grid(padx=2,pady=2)

        #--------------------------------------------------------------------------------------
            #Instanciamos la clase Botones para manejo de acciones de la ventana (agregar-eliminar-actualizar-navegar-salir)
        #--------------------------------------------------------------------------------------
        botones=Botones(agregar_usuario,eliminar_usuario,actualizar_usuario,navegar,confirmar_salir)
        botones.crear_botones(vent_usuarios,0,1)

        
        vent_usuarios.transient(root)  # Asociar la ventana hija a la ventana principal
        vent_usuarios.grab_set()  # Evitar que el usuario interactúe con la ventana principal mientras la ventana hija está abierta
        vent_usuarios.focus_set()  # Establecer el foco en la ventana hija
        
        centrar_ventana(vent_usuarios)
        cargar_usuarios()
        mostrar_datos()

        vent_usuarios.mainloop()

    #==========================================================================================================
        #CREAMOS LA VENTANA PROVEEDORES
    #==========================================================================================================
    def crear_vent_proveedores():
        
        correo_actual=''
        
        
        def validar_correo_proveedor(nuevo_correo):
            if correo_actual!=nuevo_correo or nuevo_correo=='':
                if not validar_patron_correo(nuevo_correo):
                    messagebox.showinfo('Informacion','El patron correo no valido, intente de nuevo.')
                    return False
                else:        
                    for item in diccionario_proveedores.values():#Verificar si el correo existe
                        if nuevo_correo==item['Correo']:
                            messagebox.showinfo('Informacion','El correo ya existe, intente de nuevo.')
                            return False
                    else: return True
            else: return True

        def confirmar_eliminar():
            return messagebox.askokcancel("Eliminar", "¿Seguro que quieres eliminar este proveedor?")
        
        def capturar_opcion_tipo(event):
            tipo_proveedor = cmb_tipo_proveedor.get()
        
        def actualizar_diccionario_proveedores():
            nonlocal indice_actual, lista_id_proveedores, diccionario_proveedores

            diccionario_proveedores.update({id_proveedor.get():{'Nombre':nombre_proveedor.get().strip(), 'Correo':correo_proveedor.get().strip(),'Telefono':telefono_proveedor.get().strip(),
                                    'Tipo':tipo_proveedor.get().strip(), 'Cedula':cedula_proveedor.get().strip()}})
            
            lista_id_proveedores=(list(diccionario_proveedores))
            indice_actual=len(lista_id_proveedores)-1
            
        def navegar(boton):
            nonlocal indice_actual, id_proveedor_actual

            if diccionario_proveedores!={}:
                if boton=='Primero':
                    indice_actual = 0
                elif boton=='Anterior':
                    indice_actual = (indice_actual - 1) % len(lista_id_proveedores)
                elif boton=='Siguiente':
                    indice_actual = (indice_actual + 1) % len(lista_id_proveedores)
                elif boton=='Ultimo':
                    indice_actual=len(lista_id_proveedores)-1
                
                limpiar_variables()
                mostrar_datos_proveedor()
        
        def mostrar_datos_proveedor():
            nonlocal id_proveedor_actual,correo_actual

            if diccionario_proveedores!={}:
                id_proveedor_actual=lista_id_proveedores[indice_actual]
                id_proveedor.set(id_proveedor_actual)
                nombre_proveedor.set(diccionario_proveedores[id_proveedor_actual]['Nombre'])
                correo_proveedor.set(diccionario_proveedores[id_proveedor_actual]['Correo'])
                telefono_proveedor.set(diccionario_proveedores[id_proveedor_actual]['Telefono'])
                tipo_proveedor.set(diccionario_proveedores[id_proveedor_actual]['Tipo'])
                cedula_proveedor.set(diccionario_proveedores[id_proveedor_actual]['Cedula'])
                correo_actual=correo_proveedor.get()

        def validar_datos_proveedor():    
            valor_nombre_proveedor=nombre_proveedor.get()
            valor_correo_proveedor=correo_proveedor.get()
            
            if not len(valor_nombre_proveedor):
                messagebox.showinfo('Informacion','Debe ingresar un nombre de usuario')
                entry_nombre_proveedor.focus()
                return False
            elif not validar_correo_proveedor(valor_correo_proveedor):
                entry_correo_proveedor.focus()
                return False
            else: return True
                
        def limpiar_widgets():
            id_proveedor.set('')
            nombre_proveedor.set('')
            correo_proveedor.set('')
            telefono_proveedor.set('')
            cedula_proveedor.set('')
            tipo_proveedor.set('Juridico')
            
        def limpiar_variables():
            nonlocal correo_actual    #limpiamos la variables de navegacion que usamos para validar al actualizar
            correo_actual=''
                
        def eliminar_proveedor():
            nonlocal indice_actual, lista_id_proveedores, diccionario_proveedores

            if diccionario_proveedores!={}:
                resp=confirmar_eliminar()
                if resp:
                    diccionario_proveedores.pop(id_proveedor_actual)
                    lista_id_proveedores.pop(indice_actual)
                    indice_actual-=1
                    actualizar_archivo_proveedores()
                    mostrar_datos_proveedor()
                    messagebox.showinfo('Info','Registro eliminado exitosamente.')

        def actualizar_proveedor():
            if diccionario_proveedores!={}:
                actualizar_diccionario_proveedores()
                actualizar_archivo_proveedores()
                messagebox.showinfo('Informacion','Registro actualizado exitosamente.')

        def guardar_nuevo_proveedor():       
            try:
                with open('Archivos/Proveedores.txt','a') as archivo:
                    archivo.write(id_proveedor.get().strip()+'|'+ nombre_proveedor.get().strip() +'|'+ correo_proveedor.get().strip() +'|'+ 
                                  telefono_proveedor.get().strip()+'|'+ tipo_proveedor.get().strip()+'|'+
                                  cedula_proveedor.get().strip()+'\n')       
            except FileNotFoundError as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}") 
            except IOError as e:
                messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")
           
        def agregar_proveedor():
            nonlocal indice_actual, lista_id_proveedores, agregando_proveedor

            if agregando_proveedor:
                if validar_datos_proveedor():    
                    guardar_nuevo_proveedor()
                    actualizar_diccionario_proveedores()
                    lista_id_proveedores=(list(diccionario_proveedores))
                    indice_actual=len(lista_id_proveedores)-1
                    agregando_proveedor=not agregando_proveedor
                    botones.cambiar_imagenes_al_navegar() #Volvemos a activar los botones para navegar
                   
                    messagebox.showinfo('Info','Registro agregado exitosamente.')    
            else: 
                limpiar_widgets()
                limpiar_variables()

                if lista_id_proveedores!=[]:
                    id_proveedor.set(generar_codigo(lista_id_proveedores,4))
                else:
                    lista_id_proveedores.append('P0000') 
                    id_proveedor.set(generar_codigo(lista_id_proveedores,4))

                agregando_proveedor=not agregando_proveedor
                #Desactivamos los bootones de navegacion y cambiamos sus imagenes               
                botones.cambiar_imagenes_al_agregar()
               
                entry_nombre_proveedor.focus()   

        def confirmar_salir():
            nonlocal agregando_proveedor

            if agregando_proveedor==False:
                vent_proveedores.destroy()
            else: 
                agregando_proveedor=not agregando_proveedor
                botones.cambiar_imagenes_al_navegar()
                if diccionario_proveedores!={}:
                    mostrar_datos_proveedor()

        #Creamos la ventana de proveedores
        vent_proveedores=Toplevel(root)
        vent_proveedores.title("Mantenimiento de proveedores.")
        vent_proveedores.geometry("470x275")
        vent_proveedores.resizable(0,0)

        #Creamos los frames que van a contener widget de entrada y botones
        frm = ttk.Frame(vent_proveedores,borderwidth=1, relief='solid',padding=5)
        frm.grid(row=0,column=0,padx=10,pady=10)
        frm.columnconfigure((0,1,2),weight=1)
        frm.rowconfigure((0,1,2,3,4,5),weight=1)
            
        #--------------------------------------------------------------------------------------------
            # Creamos los widgets de entrada
        #---------------------------------------------------------------------------------------------
        ttk.Label(frm,text='Id proveedor:').grid(column=0,row=0, sticky=W)
        id_proveedor=StringVar()
        entry_id_proveedor=ttk.Entry(frm,width=12,textvariable=id_proveedor,state=DISABLED)
        entry_id_proveedor.grid(column=1,row=0,sticky=W)

        ttk.Label(frm,text='Nombre:').grid(column=0,row=1, sticky=W)
        nombre_proveedor=StringVar()
        entry_nombre_proveedor=ttk.Entry(frm,width=30,textvariable=nombre_proveedor)
        entry_nombre_proveedor.grid(column=1,row=1,sticky=W)
        
        
        try:
            img_buscar=ImageTk.PhotoImage(Image.open("icons/8415529.png").resize((16,16)))
            btn_buscar=ttk.Button(frm,image=img_buscar,width=32)
            btn_buscar.grid(column=2,row=1, sticky=W)#Boton Buscar
        except FileNotFoundError as e: 
            print('Error, Imagen no cargada',e)

        validar_nuevo_correo = vent_proveedores.register(validar_correo_proveedor)  
        ttk.Label(frm,text='Correo:').grid(column=0,row=2, sticky=W)
        correo_proveedor=StringVar()
        entry_correo_proveedor=ttk.Entry(frm,width=30,textvariable=correo_proveedor,validate="focusout", validatecommand=(validar_nuevo_correo, "%P"))
        entry_correo_proveedor.grid(column=1,row=2,sticky=W)
        
     
        ttk.Label(frm,text='Telefono:').grid(column=0,row=3, sticky=W)
        telefono_proveedor=StringVar()
        entry_tel_proveedor=ttk.Entry(frm,width=12,textvariable=telefono_proveedor)
        entry_tel_proveedor.grid(column=1,row=3,sticky=W)
        
        
        ttk.Label(frm,text='Tipo de proveedor:').grid(column=0,row=4, sticky=W)
        opciones_tipo=['Fisico','Juridico']
        tipo_proveedor=StringVar()
        tipo_proveedor.set(opciones_tipo[0])
        cmb_tipo_proveedor=ttk.Combobox(frm,width=12,textvariable=tipo_proveedor, values=opciones_tipo, state="readonly")
        cmb_tipo_proveedor.grid(column=1,row=4,sticky=W)
        cmb_tipo_proveedor.bind("<<ComboboxSelected>>", capturar_opcion_tipo)
        
        ttk.Label(frm,text='Cedula:').grid(column=0,row=5, sticky=W)
        cedula_proveedor=StringVar()
        entry_cedula_proveedor=ttk.Entry(frm,width=12,textvariable=cedula_proveedor)
        entry_cedula_proveedor.grid(column=1,row=5,sticky=W)
        
        
        widgets_hijos = frm.winfo_children()
    
        # Iterar sobre la lista de widgets hijos y aplicar propiedades
        for widget_hijo in widgets_hijos:
            # Establecer un padding
            widget_hijo.grid(padx=2,pady=2)

        #-----------------------------------------------------------------------------------------------
            #Botones para manejo de acciones de la ventana (agregar-eliminar-actualizar-navegar-salir)
        #-----------------------------------------------------------------------------------------------
        botones=Botones(agregar_proveedor,eliminar_proveedor,actualizar_proveedor,navegar,confirmar_salir)
        botones.crear_botones(vent_proveedores,0,1)

        vent_proveedores.transient(root)  # Asociar la ventana hija a la ventana principal
        vent_proveedores.grab_set()  # Evitar que el usuario interactúe con la ventana principal mientras la ventana hija está abierta
        vent_proveedores.focus_set()  # Establecer el foco en la ventana hija
        
        centrar_ventana(vent_proveedores)
        cargar_proveedores(caller='vent_proveedores')
        if diccionario_proveedores!={}: mostrar_datos_proveedor()

        vent_proveedores.mainloop()

    #==========================================================================================================
        #CREAMOS LA VENTANA DEPARTAMENTOS
    #==========================================================================================================
 
    def crear_vent_departamentos():
        
               
        def confirmar_eliminar():
            return messagebox.askokcancel("Eliminar", "¿Seguro que quieres eliminar esta departamento ")
                
        def actualizar_diccionario_departamentos():
            nonlocal diccionario_departamentos

            diccionario_departamentos.update({id_departamento.get():{'Nombre':nombre_departamento.get().strip()}})

        def navegar(boton):
            nonlocal indice_actual,id_departamento_actual
            if diccionario_departamentos!={}:
                if boton=='Primero':
                    indice_actual = 0
                elif boton=='Anterior':
                    indice_actual = (indice_actual - 1) % len(lista_id_departamentos)
                elif boton=='Siguiente':
                    indice_actual = (indice_actual + 1) % len(lista_id_departamentos)
                elif boton=='Ultimo':
                    indice_actual=len(lista_id_departamentos)-1
                
                
                mostrar_datos_departamento()
        
        def mostrar_datos_departamento():
            nonlocal id_departamento_actual

            if diccionario_departamentos!={}:                
                id_departamento_actual=lista_id_departamentos[indice_actual]
                id_departamento.set(id_departamento_actual)
                nombre_departamento.set(diccionario_departamentos[id_departamento_actual]['Nombre'])
       
        def validar_datos_departamento():    
            valor_nombre_departamento =nombre_departamento.get()
            
            if not len(valor_nombre_departamento) :
                messagebox.showinfo('Informacion','Debe ingresar un nombre de departamento')
                entry_nombre_departamento.focus()
                return False
            else: return True
                
        def limpiar_widgets():
            id_departamento.set('')
            nombre_departamento.set('')
                
        def eliminar_departamento():
            nonlocal indice_actual, lista_id_departamentos,diccionario_departamentos

            if diccionario_departamentos!={}:
                resp=confirmar_eliminar()
                if resp:
                    diccionario_departamentos.pop(id_departamento_actual)
                    lista_id_departamentos.pop(indice_actual)
                    indice_actual-=1
                    actualizar_archivo_departamentos()
                    mostrar_datos_departamento()
                    messagebox.showinfo('Info','Registro eliminado exitosamente.')

        def actualizar_departamento():
            if diccionario_departamentos!={}:
                actualizar_diccionario_departamentos()
                actualizar_archivo_departamentos()
                messagebox.showinfo('Informacion','Registro actualizado exitosamente.')

        def guardar_nuevo_departamento():       
            try:
                with open('Archivos/Departamentos.txt','a') as archivo:
                    archivo.write(id_departamento.get()+'|'+ nombre_departamento.get().strip()+'\n')       
            except FileNotFoundError as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}") 
            except IOError as e:
                messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")
           
        def agregar_departamento():
            nonlocal indice_actual, lista_id_departamentos,agregando_departamento

            if agregando_departamento: 
                if validar_datos_departamento():    
                    guardar_nuevo_departamento()
                    actualizar_diccionario_departamentos()
                    lista_id_departamentos=(list(diccionario_departamentos))
                    indice_actual=len(lista_id_departamentos)-1
                    agregando_departamento = not agregando_departamento                     
                    botones.cambiar_imagenes_al_navegar() #Volvemos a activar los botones para navegar
                   
                    messagebox.showinfo('Info','Registro agregado exitosamente.')    
            else: 
                limpiar_widgets()

                if lista_id_departamentos!=[]:
                    id_departamento.set(generar_codigo(lista_id_departamentos,4))
                else:
                    lista_id_departamentos.append('D0000') 
                    id_departamento.set(generar_codigo(lista_id_departamentos,4))

                agregando_departamento =not agregando_departamento                 
                #Desactivamos los bootones de navegacion y cambiamos sus imagenes               
                botones.cambiar_imagenes_al_agregar()
               
                entry_nombre_departamento.focus()   

        def confirmar_salir():
            nonlocal agregando_departamento

            if agregando_departamento==False:
                vent_departamentos.destroy()
            else: 
                agregando_departamento =not agregando_departamento                 
                botones.cambiar_imagenes_al_navegar()
                if diccionario_departamentos!={}:
                    mostrar_datos_departamento()
        
        #Creamos la ventana de departamentos
        vent_departamentos=Toplevel(root)
        vent_departamentos.title("Mantenimiento de departamentos.")
        vent_departamentos.geometry("445x190")
        vent_departamentos.resizable(0,0)

        #Creamos los frames que van a contener widget de entrada
        frm = ttk.Frame(vent_departamentos,borderwidth=1, relief='solid',padding=5)
        frm.grid(row=0,column=0,padx=10,pady=10)
        frm.columnconfigure((0,1,2),weight=1)
        frm.rowconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)

        #--------------------------------------------------------------------------------------------
            # Creamos los widgets de entrada
        #---------------------------------------------------------------------------------------------    
        ttk.Label(frm,text='Id departamento:').grid(column=0,row=0, sticky=W)
        id_departamento=StringVar()
        entry_id_departamento=ttk.Entry(frm,width=12,textvariable=id_departamento,state='readonly')
        entry_id_departamento.grid(column=1,row=0,sticky=W)

        ttk.Label(frm,text='Nombre:').grid(column=0,row=1, sticky=W)
        nombre_departamento=StringVar()
        entry_nombre_departamento=ttk.Entry(frm,width=30,textvariable=nombre_departamento)
        entry_nombre_departamento.grid(column=1,row=1,sticky=W)
        
        try:
            img_buscar=ImageTk.PhotoImage(Image.open("icons/8415529.png").resize((16,16)))
            btn_buscar=ttk.Button(frm,image=img_buscar,width=32)
            btn_buscar.grid(column=2,row=1, sticky=W)#Boton Buscar
        except FileNotFoundError as e: 
            print('Error, Imagen no cargada',e)

        #--------------------------------------------------------------------------------------
            #Botones para manejo de acciones de la ventana (agregar-eliminar-actualizar-navegar-salir)
        #--------------------------------------------------------------------------------------
        botones=Botones(agregar_departamento,eliminar_departamento,actualizar_departamento,navegar,confirmar_salir)
        botones.crear_botones(vent_departamentos,0,1)

        
        vent_departamentos.transient(root)  # Asociar la ventana hija a la ventana principal
        vent_departamentos.grab_set()  # Evitar que el usuario interactúe con la ventana principal mientras la ventana hija está abierta
        vent_departamentos.focus_set()  # Establecer el foco en la ventana hija
        
        centrar_ventana(vent_departamentos)
        cargar_departamentos(caller='vent_departamentos')
        if diccionario_departamentos!={}: mostrar_datos_departamento()
        vent_departamentos.mainloop()

    #==========================================================================================================
        #CREAMOS LA VENTANA CATEGORIAS
    #==========================================================================================================
 
    def crear_vent_categorias():
        
        
        
        def focus_in_nombre(event):
            entry_nombre_categoria.select_range(0,'end')
               
        def confirmar_eliminar():
            return messagebox.askokcancel("Eliminar", "¿Seguro que quieres eliminar esta categoria ")
        
                
        def actualizar_diccionario_categorias():
            nonlocal diccionario_categorias
        
            diccionario_categorias.update({id_categoria.get():{'Nombre':nombre_categoria.get().strip()}})
            
        def navegar(boton):
            nonlocal indice_actual

            if diccionario_categorias!={}:
                if boton=='Primero':
                    indice_actual = 0
                elif boton=='Anterior':
                    indice_actual = (indice_actual - 1) % len(lista_id_categorias)
                elif boton=='Siguiente':
                    indice_actual = (indice_actual + 1) % len(lista_id_categorias)
                elif boton=='Ultimo':
                    indice_actual=len(lista_id_categorias)-1

                
                mostrar_datos_categoria()
        
        def mostrar_datos_categoria():
            nonlocal id_categoria_actual
            if diccionario_categorias!={}:
                id_categoria_actual=lista_id_categorias[indice_actual]
                id_categoria.set(id_categoria_actual)
                nombre_categoria.set(diccionario_categorias[id_categoria_actual]['Nombre'])
  
        def validar_datos_categoria():    
            valor_nombre_categoria =nombre_categoria.get()
            
            if not len(valor_nombre_categoria) :
                messagebox.showinfo('Informacion','Debe ingresar un nombre de categoria')
                entry_nombre_categoria.focus()
                return False
            else: return True
                
        def limpiar_widgets():
            id_categoria.set('')
            nombre_categoria.set('')
                
        def eliminar_categoria():
            nonlocal indice_actual, lista_id_categorias, diccionario_categorias
            if diccionario_categorias!={}:
                resp=confirmar_eliminar()
                if resp:
                    diccionario_categorias.pop(id_categoria_actual)
                    lista_id_categorias.pop(indice_actual)
                    indice_actual-=1
                    actualizar_archivo_categorias()
                    mostrar_datos_categoria()
                    messagebox.showinfo('Info','Registro eliminado exitosamente.')

        def actualizar_categoria():
            if diccionario_categorias!={}:
                actualizar_diccionario_categorias()
                actualizar_archivo_categorias()
                messagebox.showinfo('Informacion','Registro actualizado exitosamente.')
        
        def guardar_nueva_categoria():       
            try:
                with open('Archivos/Categorias.txt','a') as archivo:
                    archivo.write(id_categoria.get()+'|'+ nombre_categoria.get().strip()+'\n')       
            except FileNotFoundError as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}") 
            except IOError as e:
                messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")
           
        def agregar_categoria():
            nonlocal indice_actual, lista_id_categorias,agregando_categoria
            if agregando_categoria: 
                if validar_datos_categoria():    
                    guardar_nueva_categoria()
                    actualizar_diccionario_categorias()
                    lista_id_categorias=(list(diccionario_categorias))
                    indice_actual=len(lista_id_categorias)-1
                    agregando_categoria = not agregando_categoria                     
                    botones.cambiar_imagenes_al_navegar() #Volvemos a activar los botones para navegar
                   
                    messagebox.showinfo('Info','Registro agregado exitosamente.')    
            else: 
                limpiar_widgets()

                if lista_id_categorias!=[]:
                    id_categoria.set(generar_codigo(lista_id_categorias,4))
                else:
                    lista_id_categorias.append('C0000') 
                    id_categoria.set(generar_codigo(lista_id_categorias,4))

                agregando_categoria =not agregando_categoria                 
                #Desactivamos los bootones de navegacion y cambiamos sus imagenes               
                botones.cambiar_imagenes_al_agregar()
               
                entry_nombre_categoria.focus()   

        def confirmar_salir():
            nonlocal agregando_categoria      
            if agregando_categoria==False:
                vent_categorias.destroy()
            else: 
                agregando_categoria =not agregando_categoria                 
                botones.cambiar_imagenes_al_navegar()
                if diccionario_categorias!={}:
                    mostrar_datos_categoria()
        
        #Creamos la ventana de categorias
        vent_categorias=Toplevel(root)
        vent_categorias.title("Mantenimiento de categorias.")
        vent_categorias.geometry("420x150")
        vent_categorias.resizable(0,0)

        #Creamos los frames que van a contener widget de entrada
        frm = ttk.Frame(vent_categorias,borderwidth=1, relief='solid',padding=5)
        frm.grid(row=0,column=0,padx=10,pady=10)
        frm.columnconfigure((0,1,2),weight=1)
        frm.rowconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)

        #--------------------------------------------------------------------------------------------
            # Creamos los widgets de entrada
        #---------------------------------------------------------------------------------------------    
        ttk.Label(frm,text='Id categoria:').grid(column=0,row=0, sticky=W)
        id_categoria=StringVar()
        entry_id_categoria=ttk.Entry(frm,width=12,textvariable=id_categoria,state=DISABLED)
        entry_id_categoria.grid(column=1,row=0,sticky=W)

        ttk.Label(frm,text='Nombre:').grid(column=0,row=1, sticky=W)
        nombre_categoria=StringVar()
        entry_nombre_categoria=ttk.Entry(frm,width=30,textvariable=nombre_categoria)
        entry_nombre_categoria.grid(column=1,row=1,sticky=W)
        entry_nombre_categoria.bind("<FocusIn>", focus_in_nombre)
        
        try:
            img_buscar=ImageTk.PhotoImage(Image.open("icons/8415529.png").resize((16,16)))
            btn_buscar=ttk.Button(frm,image=img_buscar,width=32)
            btn_buscar.grid(column=2,row=1, sticky=W)#Boton Buscar
        except FileNotFoundError as e: 
            print('Error, Imagen no cargada',e)

        #--------------------------------------------------------------------------------------
            #Botones para manejo de acciones de la ventana (agregar-eliminar-actualizar-navegar-salir)
        #--------------------------------------------------------------------------------------
        botones=Botones(agregar_categoria,eliminar_categoria,actualizar_categoria,navegar,confirmar_salir)
        botones.crear_botones(vent_categorias,0,1)

        
        vent_categorias.transient(root)  # Asociar la ventana hija a la ventana principal
        vent_categorias.grab_set()  # Evitar que el usuario interactúe con la ventana principal mientras la ventana hija está abierta
        vent_categorias.focus_set()  # Establecer el foco en la ventana hija
        
        centrar_ventana(vent_categorias)
        cargar_categorias(caller='vent_categorias')
        if diccionario_categorias!={}: mostrar_datos_categoria()
        vent_categorias.mainloop()

    #==========================================================================================================
        #CREAMOS LA VENTANA SUB-CATEGORIAS
    #==========================================================================================================
    def crear_vent_subcategorias():
       
        
        def focus_in_nombre(event):
            entry_nombre_subcategoria.select_range(0,'end')
                
        def actualizar_diccionario_subcategorias():
            nonlocal diccionario_subcategorias    
            
            if id_categoria.get() not in diccionario_subcategorias:
                diccionario_subcategorias[id_categoria.get()]={}
                
            diccionario_subcategorias[id_categoria.get()][id_subcategoria.get()]={'Nombre':nombre_subcategoria.get().strip()}
            
        def navegar(boton):
            nonlocal indice_actual
            if diccionario_subcategorias[id_categoria_actual]!={}:
                if boton=='Primero':
                    indice_actual = 0
                elif boton=='Anterior':
                    indice_actual = (indice_actual - 1) % len(lista_id_subcategorias)
                elif boton=='Siguiente':
                    indice_actual = (indice_actual + 1) % len(lista_id_subcategorias)
                elif boton=='Ultimo':
                    indice_actual=len(lista_id_subcategorias)-1
                
                mostrar_datos_subcategoria()
        
        def mostrar_datos_subcategoria():
            nonlocal id_subcategoria_actual
            #print(diccionario_subcategorias)
            if diccionario_subcategorias!={} and indice_actual>=0 and id_categoria_actual in diccionario_subcategorias:
                id_subcategoria_actual=lista_id_subcategorias[indice_actual]
                id_subcategoria.set(id_subcategoria_actual)
                nombre_subcategoria.set(diccionario_subcategorias[id_categoria_actual][id_subcategoria_actual]['Nombre'])
            else: limpiar_widgets()

        def validar_datos_subcategoria():    
            valor_nombre_subcategoria =nombre_subcategoria.get()
            
            if not len(valor_nombre_subcategoria) :
                messagebox.showinfo('Informacion','Debe ingresar un nombre de subcategoria')
                entry_nombre_subcategoria.focus()
                return False
            else: return True
                
        def limpiar_widgets():
            id_subcategoria.set('')
            nombre_subcategoria.set('')
                
        def eliminar_subcategoria():
            nonlocal indice_actual,lista_id_subcategorias, diccionario_subcategorias,lista_consec_id_subcategorias

            if diccionario_subcategorias!={}:
                if messagebox.askokcancel("Eliminar", "¿Seguro que quieres eliminar esta subcategoria "):
                    diccionario_subcategorias[id_categoria_actual].pop(id_subcategoria_actual)
                    ultimo=lista_id_subcategorias[-1]
                    eliminado=lista_id_subcategorias.pop(indice_actual)
                    indice_actual-=1
                    if ultimo==eliminado:lista_consec_id_subcategorias.pop()
                    actualizar_archivo_subcategorias()
                    mostrar_datos_subcategoria()
                    messagebox.showinfo('Info','Registro eliminado exitosamente.')

        def actualizar_subcategoria():
            if diccionario_subcategorias!={}:
                if validar_datos_subcategoria:
                    actualizar_diccionario_subcategorias()
                    actualizar_archivo_subcategorias()
                    messagebox.showinfo('Informacion','Registro actualizado exitosamente.')

        def guardar_nueva_subcategoria():       
            try:
                with open('Archivos/Subcategorias.txt','a') as archivo:
                    archivo.write(id_categoria.get()+'|'+ id_subcategoria. get().strip()+'|'+ nombre_subcategoria.get().strip()+'\n')       
            except FileNotFoundError as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}") 
            except IOError as e:
                messagebox.showerror("Error",f"Ocurrió un error de E/S: {e}")
           
        def agregar_subcategoria():
            nonlocal indice_actual, lista_id_subcategorias,agregando_subcategoria,lista_consec_id_subcategorias
            if agregando_subcategoria: 
                if validar_datos_subcategoria():    
                    guardar_nueva_subcategoria()
                    actualizar_diccionario_subcategorias()
                    lista_id_subcategorias=(list(diccionario_subcategorias[id_categoria.get()].keys()))
                    indice_actual=len(lista_id_subcategorias)-1
                    
                    agregando_subcategoria = not agregando_subcategoria                     
                    botones.cambiar_imagenes_al_navegar() #Volvemos a activar los botones para navegar
                   
                    messagebox.showinfo('Info','Registro agregado exitosamente.')    
            else: 
                limpiar_widgets()

                if lista_consec_id_subcategorias!=[]:
                    id_subcategoria.set(generar_codigo(lista_consec_id_subcategorias,4))
                    lista_consec_id_subcategorias.append(id_subcategoria.get())
                else:
                    lista_consec_id_subcategorias.append('S0000') 
                    id_subcategoria.set(generar_codigo(lista_consec_id_subcategorias,4))

                agregando_subcategoria =not agregando_subcategoria                 
                #Desactivamos los bootones de navegacion y cambiamos sus imagenes               
                botones.cambiar_imagenes_al_agregar()
               
                entry_nombre_subcategoria.focus()   

        def confirmar_salir():
            nonlocal agregando_subcategoria

            if agregando_subcategoria==False:
                vent_subcategorias.destroy()
            else: 
                agregando_subcategoria =not agregando_subcategoria                 
                botones.cambiar_imagenes_al_navegar()
                if diccionario_subcategorias!={}:
                    mostrar_datos_subcategoria()
        
        def capturar_opcion_categoria(event):
            nonlocal indice_actual,id_categoria_actual,lista_id_subcategorias

            nombre_categoria.set(cmb_categoria.get())

            for clave,valor in diccionario_categorias.items():
                if valor['Nombre']==nombre_categoria.get():
                    id_categoria_actual=clave
                    id_categoria.set(clave)
                    break

            if diccionario_subcategorias!={}:
                for clave,valor in diccionario_subcategorias.items():
                    if clave==id_categoria_actual:
                        lista_id_subcategorias=list(diccionario_subcategorias[clave].keys())
                        indice_actual=len(lista_id_subcategorias)-1
                        break
                else: id_subcategoria.set('');nombre_subcategoria.set(''); return
            
            mostrar_datos_subcategoria()
           
                            
        #Creamos la ventana de subcategorias
        vent_subcategorias=Toplevel(root)
        vent_subcategorias.title("Mantenimiento de subcategorias.")
        vent_subcategorias.geometry("480x215")
        vent_subcategorias.resizable(0,0)

        #Creamos los frames que van a contener widget de entrada
        frm = ttk.Frame(vent_subcategorias,borderwidth=1, relief='solid',padding=5)
        frm.grid(row=0,column=0,padx=10,pady=10)
        frm.columnconfigure((0,1,2),weight=1)
        frm.rowconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)

        #--------------------------------------------------------------------------------------------
            # Creamos los widgets de entrada
        #---------------------------------------------------------------------------------------------    
        cargar_categorias(caller='vent_subcategorias')
        
        ttk.Label(frm,text='Id_categoria:').grid(column=0,row=0, sticky=W)
        id_categoria=StringVar()
        id_categoria.set(id_categoria_actual)
        entry_id_categoria=ttk.Entry(frm,width=12,textvariable=id_categoria, state='readonly')
        entry_id_categoria.grid(column=1,row=0,pady=2,sticky=W)
        
        
        ttk.Label(frm,text='Categoria:').grid(column=0,row=1, sticky=W)
        nombre_categoria=StringVar()
        nombre_categoria.set(lista_nombres_categorias[len(lista_nombres_categorias)-1])
        cmb_categoria=ttk.Combobox(frm,width=25,textvariable=nombre_categoria, values=lista_nombres_categorias, state="readonly")
        cmb_categoria.grid(column=1,row=1,pady=2,sticky=W)
        cmb_categoria.bind("<<ComboboxSelected>>", capturar_opcion_categoria)
        
        
        ttk.Label(frm,text='Id subcategoria:').grid(column=0,row=2, sticky=W)
        id_subcategoria=StringVar()
        entry_id_subcategoria=ttk.Entry(frm,width=12,textvariable=id_subcategoria,state='readonly')
        entry_id_subcategoria.grid(column=1,row=2,pady=2,sticky=W)

        ttk.Label(frm,text='Nombre Subcategoria:').grid(column=0,row=3, sticky=W)
        nombre_subcategoria=StringVar()
        entry_nombre_subcategoria=ttk.Entry(frm,width=30,textvariable=nombre_subcategoria)
        entry_nombre_subcategoria.grid(column=1,row=3,pady=2,sticky=W)
        entry_nombre_subcategoria.bind("<FocusIn>", focus_in_nombre)
        
        try:
            img_buscar=ImageTk.PhotoImage(Image.open("icons/8415529.png").resize((16,16)))
            btn_buscar=ttk.Button(frm,image=img_buscar,width=32)
            btn_buscar.grid(column=2,row=3, sticky=W)#Boton Buscar
        except FileNotFoundError as e: 
            print('Error, Imagen no cargada',e)

        #--------------------------------------------------------------------------------------
            #Botones para manejo de acciones de la ventana (agregar-eliminar-actualizar-navegar-salir)
        #--------------------------------------------------------------------------------------
        botones=Botones(agregar_subcategoria,eliminar_subcategoria,actualizar_subcategoria,navegar,confirmar_salir)
        botones.crear_botones(vent_subcategorias,n_col=0,n_row=1)

        
        vent_subcategorias.transient(root)  # Asociar la ventana hija a la ventana principal
        vent_subcategorias.grab_set()  # Evitar que el usuario interactúe con la ventana principal mientras la ventana hija está abierta
        vent_subcategorias.focus_set()  # Establecer el foco en la ventana hija
        
        centrar_ventana(vent_subcategorias)
        cargar_subcategorias(caller='vent_subcategorias')
        if diccionario_subcategorias!={}: mostrar_datos_subcategoria()
        vent_subcategorias.mainloop()         
    #---------------------------------------------------------------------------------    
        # Creamos la ventana de login
    #---------------------------------------------------------------------------------
    def crear_vent_login():
        ver_contrasena=False
       
        
        def validar_sesion(usuario,contrasena,pin):
            nonlocal diccionario_usuarios, id_usuario_en_session

            for clave, valor in diccionario_usuarios.items():
                if usuario==valor['Usuario']:
                    if contrasena==valor['Contrasena']:
                        if pin==valor['Pin']:
                            if valor['Estado']=='Inactivo':
                                messagebox.showwarning('Informacion','Su usuario de encuentra inactivo, consulte al administrador del sistema.')
                                return
                            id_usuario_en_session=clave
                            
                            vent_login.destroy()
                            crear_vent_principal()
                            break
                        else:
                            messagebox.showinfo('Informacion','Pin no valido, intente de nuevo.')
                            entry_pin.focus()
                            entry_pin.select_range(0,'end')
                            break
                    else:
                        messagebox.showinfo('Informacion','Contrasena no valida, intente de nuevo.')
                        entry_contrasena.focus()
                        entry_contrasena.select_range(0,'end')
                        break
            else:
                messagebox.showinfo('Informacion','Usuario no valido, intente de nuevo.')
                entry_usuario.focus()
                entry_usuario.select_range(0,'end')
                
        def mostrar_contrasena():#Funcion para mostrar u ocultar la contrasena de ingreso
            ver_contrasena = not ver_contrasena
            if ver_contrasena:
                entry_contrasena.config(show="")
                btn_mostrar_contrasena.config(image=new_img_open_eye)
            else:
                entry_contrasena.config(show="*") 
                btn_mostrar_contrasena.config(image=new_img_close_eye)
        
        def usuario_on_enter(even):
            entry_contrasena.focus()

        def contrasena_on_enter(even):
            entry_pin.focus()

        def pin_on_enter(even):
            btn_iniciar.focus()

        def btn_iniciar_on_enter(even):
            validar_sesion(usuario.get(),contrasena.get(),pin.get())

        def usuario_on_focus(even):
            entry_usuario.select_range(0,'end')

        def contrasena_on_focus(even):
            entry_contrasena.select_range(0,'end')

        def pin_on_focus(even):
            entry_pin.select_range(0,'end')
            

            
        vent_login=Tk()
        vent_login.title("Iniciar sesion.")
        vent_login.geometry("305x200")
        vent_login.resizable(0,0)
       
        frm = ttk.Frame(vent_login,borderwidth=1, relief='solid',padding=5)
        frm.grid(column=0, row=0,padx=5,pady=5, sticky=(N, W, E, S))
        frm.columnconfigure((0,1,2),weight=1)
        frm.rowconfigure((0,1,2,3,4,5),weight=1)   
        
        vent_login.columnconfigure(0,weight=1)
        vent_login.rowconfigure(0,weight=1)

        #Usuario
        lbl_usuario=ttk.Label(frm, text='Usuario:')        
        lbl_usuario.grid(row=0, column=0, padx=2,pady=2,sticky='W')
        
        usuario=StringVar()
        entry_usuario=ttk.Entry(frm, textvariable=usuario, width=15)
        entry_usuario.grid(row=0, column=1, padx=2,pady=2, sticky='W')
        entry_usuario.bind('<Return>', usuario_on_enter)
        entry_usuario.bind('<KP_Enter>',usuario_on_enter)
        entry_usuario.bind("<FocusIn>", usuario_on_focus)
        
        #Contrasena
        lbl_contrasena=ttk.Label(frm, text='Contrasena')
        lbl_contrasena.grid(row=1, column=0, padx=2,pady=2,sticky='W')
        contrasena=StringVar()
        entry_contrasena=ttk.Entry(frm, textvariable=contrasena, width=15, show="*")
        entry_contrasena.grid(row=1, column=1, padx=2,pady=2,sticky='W')
        entry_contrasena.bind('<Return>', contrasena_on_enter)
        entry_contrasena.bind('<KP_Enter>',contrasena_on_enter)
        entry_contrasena.bind("<FocusIn>", contrasena_on_focus)

        #Pin    
        lbl_pin=ttk.Label(frm, text='Pin')
        lbl_pin.grid(row=2, column=0, padx=2,pady=2,sticky='W')
        pin=StringVar()
        entry_pin=ttk.Entry(frm, textvariable=pin, width=15)
        entry_pin.grid(row=2, column=1, padx=2,pady=2,sticky='W')
        entry_pin.bind('<Return>', pin_on_enter)
        entry_pin.bind('<KP_Enter>',pin_on_enter)
        entry_pin.bind("<FocusIn>", pin_on_focus)

        #Botones inicio y cerrar
        img_boton1 =Image.open("icons/7562743.png").resize((32,32))
        new_img_boton1 = ImageTk.PhotoImage(img_boton1)
        btn_iniciar=ttk.Button(frm, text="Iniciar",  image=new_img_boton1, compound=TOP,command=lambda: validar_sesion(usuario.get(),contrasena.get(),pin.get()))
        btn_iniciar.grid(column=0, row=5, sticky="E")
        btn_iniciar.bind('<Return>', btn_iniciar_on_enter)
        btn_iniciar.bind('<KP_Enter>',btn_iniciar_on_enter)
        
        img_boton2 =Image.open("icons/6460744.png").resize((32,32))
        new_img_boton2=ImageTk.PhotoImage(img_boton2)
        btn_cerrar=ttk.Button(frm, text="Cerrar", image=new_img_boton2, compound=TOP,command=vent_login.destroy)
        btn_cerrar.grid(column=1, row=5,sticky="E")
        
        #Boton ver contrasena
        img_close_eye =Image.open("icons/close_eye.png").resize((16,16))
        new_img_close_eye=ImageTk.PhotoImage(img_close_eye)
        
        img_open_eye =Image.open("icons/open_eye.png").resize((16,16))
        new_img_open_eye=ImageTk.PhotoImage(img_open_eye)

        s = ttk.Style()
        s.configure('BotonFlat.TButton', relief='flat')#Definimos un estilo plano para el boton
        btn_mostrar_contrasena=ttk.Button(frm, image=new_img_close_eye, command=mostrar_contrasena,style='BotonFlat.TButton')
        btn_mostrar_contrasena.grid(column=2, row=1)
        
        cargar_usuarios()
        centrar_ventana(vent_login)#Centramos la ventana
        entry_usuario.focus()
        
        vent_login.mainloop()
         
    #crear_vent_login()
    crear_vent_principal()   
if __name__=='__main__':
    main()
