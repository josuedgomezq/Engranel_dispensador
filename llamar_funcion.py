# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 23:56:03 2021

@author: josue
"""

import sys
from PyQt5.QtWidgets import QDialog, QApplication
from envaseqr import *
import os
import io
import cv2
import numpy as np
import serial
from pyzbar.pyzbar import decode
from collections import Counter
import sqlite3
from firebase import firebase
db= firebase.FirebaseApplication("https://ejemplo2diplomado-a0e98-default-rtdb.firebaseio.com/")

class Inicio(QDialog):
    def __init__(self):
        super().__init__()
        self.dialogo=Ui_MainWindow()
        self.dialogo.setupUi(self)
        self.cont=0
        
        self.dialogo.btn_crear.clicked.connect(self.guardar)
        self.dialogo.btn_leer.clicked.connect(self.leer)
        self.dialogo.btn_completar.clicked.connect(self.completar)
    
    
    
    def completar(self):

        cliente=self.dialogo.obj_cliente
        clave=cliente[2]
        try:
            conexion = sqlite3.connect('base_de_datos.db')
            
                    
        except sqlite3.Error as error:
            print('Se ha producido un error al crear la conexión:', error)


        sql = "SELECT * FROM usuario WHERE clave = ?;"

        cursor = conexion.cursor()
        cursor.execute(sql, (clave,))
    
        registros = cursor.fetchall()
    
        for r in registros:
            print(r)

        
        cantidad=self.dialogo.spin_cj.value()
        litros=r[3]
        acum=float(litros)+self.dialogo.spin_cj.value()
        reutilizar=int(r[5])+1
        nombre=r[1]

        self.dialogo.lbl_cliente.setText(str(r[1]))
        self.dialogo.lbl_acum.setText(str(acum/1000))
        self.dialogo.lbl_reutilizacion.setText(str(reutilizar))
        pc400=r[6];pc500=r[7];pc600=r[8];pc700=r[9];pc800=r[10];pc900=r[11];pc1000=r[12];pc1100=r[13];pc1200=r[14];pc1300=r[15];pc1400=r[16];pc1500=r[17]

        if cantidad==400:
            pc400+=400
            print(pc400)
        if cantidad==500:
            pc500+=500
        if cantidad==600:
            pc600+=600
        if cantidad==700:
            pc700+=700
        if cantidad==800:
            pc800+=800
        if cantidad==900:
            pc900+=900
        if cantidad==1000:
            pc1000+=1000
        if cantidad==1100:
            pc1100+=1100
        if cantidad==1200:
            pc1200+=1200
        if cantidad==1300:
            pc1300+=1300
        if cantidad==1400:
            pc1400+=1400
        if cantidad==1500:
            pc1500+=1500
        
        band=0
        
        try:
            ser=serial.Serial("COM4",9600)

            while True:
                
                n_c=str(str(nombre)+","+str(cantidad))
                ser.write(str(n_c).encode())
            
                
                band=band+1
                if band==8:
                    ser.close()
                    break
        except TimeoutError:
            print('error')
                
        finally:
                print('done')
               
        sql = 'UPDATE usuario SET acumulado = ?, puntos = ?, reutilizacion = ?, p400=?,p500=?,p600=?,p700=?,p800=?,p900=?,p1000=?,p1100=?,p1200=?,p1300=?,p1400=?,p1500=? WHERE clave = ?;'
        cursor = conexion.cursor()
        
        cursor.execute(sql, (acum,1,reutilizar,pc400,pc500,pc600,pc700,pc800,pc900,pc1000,pc1100,pc1200,pc1300,pc1400,pc1500,clave))
        conexion.commit()
        
        if conexion:
            conexion.close()
        self.dialogo.spin_cj.setValue(0)

    def leer(self):
        
        lista=[]
        
        
        #conexion con la base de datos
        try:
            conexion = sqlite3.connect('base_de_datos.db')
    
            
        except sqlite3.Error as error:
            print('Se ha producido un error al crear la conexión:', error)
            
        cap = cv2.VideoCapture(0) # cuand se da crear se abre el lector qr
        cap.set(3,640)
        cap.set(4,480)
        myData=0
        x=0
        while x<=21:
            success, img = cap.read()
            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')
                print(myData)
                
                myOutput = 'Detectado'
                myColor = (0,255,0)
                lista.append(myData)
                x=len(lista)
                if x==20:
                    c = Counter(lista)
                    codigo=max(c, key=c.get)

        
                pts = np.array([barcode.polygon],np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(img,[pts],True,myColor,5)
                pts2 = barcode.rect
                cv2.putText(img,myOutput,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,myColor,2)
        
            cv2.imshow('Result',img)
            if cv2.waitKey(1) & 0xFF== ord('q'):
                brea
            
            
        cap.release()
        cv2.destroyAllWindows()
        
        clave=codigo
        
        sql = "SELECT * FROM usuario WHERE clave = ?;" # selecciono el valor clave de la base de datos, para realizar una busqueda de una lista especifica

        cursor = conexion.cursor()
        cursor.execute(sql, (clave,))
    
        registros = cursor.fetchall()
    
        for r in registros:
            print(r)
            
        
        sql = "SELECT * FROM usuario"
        cursor = conexion.cursor()
        cursor.execute(sql)

        clientes=cursor.fetchall()

        #inicializo variables
        clientes_registrados=0
        envases_reutilizados=0
        litros_vendidos=0
        clientes_reutilizaron=0
        porcentaje_reutilizacion=0
        stock=50
        sum400=0;sum500=0;sum600=0;sum700=0;sum800=0;sum900=0;sum1000=0;sum1100=0;sum1200=0;sum1300=0;sum1400=0;sum1500=0;

        #clculo valores de la base de datos y recorro toda la base de datos guardando cada lista de valores en x
        for x in clientes:
            clientes_registrados=clientes_registrados+1
            envases_reutilizados=envases_reutilizados+int(x[5])
            print(envases_reutilizados)
            litros_vendidos=litros_vendidos+float(x[3])/1000
            if int(x[5])>1:# a partir de dos me cuenta los clintes que reutilizan
                clientes_reutilizaron=clientes_reutilizaron+1
            # sumar cada valor de los formatos para determinar cual es el mayor
            sum400+=x[6]/400;sum500+=x[7]/500;sum600+=x[8]/600;sum700+=x[9]/700;sum800+=x[10]/800;sum900+=x[11]/900;sum1000+=x[12]/1000;sum1100+=x[13]/1100;sum1200+=x[14]/1200;sum1300+=x[15]/1300;sum1400+=x[16]/1400;sum1500+=x[17]/1500;

        lista_mayor=[sum400,sum500,sum600,sum700,sum800,sum900,sum1000,sum1100,sum1200,sum1300,sum1400,sum1500]
        formato=0
        if lista_mayor.index(max(lista_mayor))==0:
            formato=400
        if lista_mayor.index(max(lista_mayor))==1:
            formato=500
        if lista_mayor.index(max(lista_mayor))==2:
            formato=600
        if lista_mayor.index(max(lista_mayor))==3:
            formato=700
        if lista_mayor.index(max(lista_mayor))==4:
            formato=800
        if lista_mayor.index(max(lista_mayor))==5:
            formato=900
        if lista_mayor.index(max(lista_mayor))==6:
            formato=1000
        if lista_mayor.index(max(lista_mayor))==7:
            formato=1100
        if lista_mayor.index(max(lista_mayor))==8:
            formato=1200
        if lista_mayor.index(max(lista_mayor))==9:
            formato=1300
        if lista_mayor.index(max(lista_mayor))==10:
            formato=1400
        if lista_mayor.index(max(lista_mayor))==11:
            formato=1500

        print(formato)

        porcentaje_reutilizacion=(clientes_reutilizaron/clientes_registrados)*100 # porcentaje de reutilizacion de envases
        
        porcentaje_stock=(litros_vendidos/stock)*100 #porcentaje de inventario restante
        if porcentaje_stock>=60:
            ban_inventario=1
        else:
            ban_inventario=0

        print(ban_inventario)
        acum_litros=0

        acum_litros=float(r[3])/1000
        print(acum_litros)
        #paso parametros a qt y envio el objeto cliente a la funcion completar
        self.dialogo.obj_cliente=r
        self.dialogo.lbl_cliente.setText(str(r[1]))
        self.dialogo.lbl_acum.setText(str(acum_litros))
        self.dialogo.lbl_reutilizacion.setText(r[5])

        inventario_tienda=stock - litros_vendidos
        """
        db.put("/Nodemcu","CantidadDeEmbasesReutilizados",envases_reutilizados)
        db.put("/Nodemcu","ClientesRegistrados",clientes_registrados)
        db.put("/Nodemcu","Litros_Vendidos",litros_vendidos)
        db.put("/Nodemcu","PorcentajeDeClientesQueReutilizanEmvases",porcentaje_reutilizacion)
        db.put("/Nodemcu","PresentacionqueMasSeVendio",formato)
        db.put("/Nodemcu","TiendaAsociadaPocoInventario",inventario_tienda)
        """

        if conexion:
            conexion.close()
        
	
            
    
    def guardar(self):
        lista=[]
        print('base1')
        try:
            conexion = sqlite3.connect('base_de_datos.db')
    
            
        except sqlite3.Error as error:
            print('Se ha producido un error al crear la conexión:', error)
        
        
        """sql = 
        CREATE TABLE usuario(
            id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
           clave TEXT NOT NULL,
            acumulado TEXT NOT NULL,
            puntos TEXT NOT NULL,
            reutilizacion TEXT NOT NULL,
            p400 INTEGER NOT NULL,
            p500 INTEGER NOT NULL,
            p600 INTEGER NOT NULL,
            p700 INTEGER NOT NULL,
            p800 INTEGER NOT NULL,
            p900 INTEGER NOT NULL,
            P1000 INTEGER NOT NULL,
            p1100 INTEGER NOT NULL,
            p1200 INTEGER NOT NULL,
            p1300 INTEGER NOT NULL,
            p1400 INTEGER NOT NULL,
            p1500 INTEGER NOT NULL
        );
        
      
        
        cursor = conexion.cursor()
        cursor.execute(sql)
        conexion.commit()"""
        
    
        nombre=self.dialogo.line_nombre.text() #  guardo el nombre y el id
        id=str(self.dialogo.line_id.text())
        
        cap = cv2.VideoCapture(0) # cuand se da crear se abre el lector qr
        cap.set(3,640)
        cap.set(4,480)
        myData=0
        x=0
        while x<=21:
            success, img = cap.read()
            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')
                print(myData)
                
                myOutput = 'Detectado'
                myColor = (0,255,0)
                lista.append(myData)
                x=len(lista)
                if x==20:
                    c = Counter(lista)
                    codigo=max(c, key=c.get)

        
                pts = np.array([barcode.polygon],np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(img,[pts],True,myColor,5)
                pts2 = barcode.rect
                cv2.putText(img,myOutput,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,myColor,2)
        
            cv2.imshow('Result',img)
            if cv2.waitKey(1) & 0xFF== ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        
        
        acum=0
        puntos=0
        reutilizacion=0
        P400=0
        P500=0
        P600=0
        P700=0
        P800=0
        P900=0
        P1000=0
        P1100=0
        P1200=0
        P1300=0
        P1400=0
        P1500=0
        
        sql = 'INSERT INTO usuario VALUES (?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?);'

        cursor = conexion.cursor()
        cursor.execute(sql, (id, nombre, codigo,acum,puntos, reutilizacion,P400,P500,P600,P700,P800,P900,P1000,P1100,P1200,P1300,P1400,P1500))
    
        conexion.commit()
            
        if conexion:
            conexion.close()
	
if __name__== '__main__':
	app=QApplication(sys.argv)
	miapp= Inicio()
	miapp.show()
	sys.exit(app.exec_())
