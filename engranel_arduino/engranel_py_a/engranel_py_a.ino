
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);  // set the LCD address to 0x27 for a 16 chars and 2 line display
#include "HX711.h"
#define DOUT  A0
#define CLK  A1
#include <Separador.h>

Separador s;
const int inputPin = 6;

String data;
String elemento1, elemento2, cantidad,nombre;

int value = 0;

 

HX711 balanza(DOUT, CLK);
// Lo primero is inicializar la librería indicando los pins de la interfaz
int a,b,c,gramos;
// Arreglo de botones y último estado del botón
// Nota: Los siguientes "DEFINE" son únicamente para
// mejorar la lectura del código al momento de codificar.


// Este arreglo contiene los pines utilizados para los botones

// Este arreglo contiene el último estado conocido de cada línea





const int LED=13;


void setup() {

pinMode(LED,OUTPUT);
Serial.begin(9600);
 lcd.init(); 
 lcd.backlight();
 balanza.set_scale(417330); // Establecemos la escala
 balanza.tare(20);  //El peso actual es considerado Tara.

 digitalWrite(13, LOW);
  
   // Configurar como PULL-UP para ahorrar resistencias
 pinMode(inputPin,  INPUT_PULLUP);
hom();
 


}


// monitoreados. Asume la existencia de un arreglo button
// con la asignación actual de pines y un arreglo button_estate
// con los valores de línea
uint8_t flancoSubida(int btn) {
 
  
}

void hom() {

        int num_cifras,num;
        num_cifras=1;
        
        lcd.clear();
        lcd.setCursor(0,0);
        lcd.print("[ENGRANEL]");
        while(digitalRead(7)==1)
  {
   
       
       num=-balanza.get_units(1)*1000;
       while(num>=10){

          num=num/10;
          num_cifras++;
        
        }

      if(num_cifras=1){
       lcd.setCursor(0,1);
       lcd.print(int(-balanza.get_units(1)*1000));
       delay(100);
       lcd.setCursor(1,1);
       lcd.print("  ");
      }

       if(num_cifras=2){
       lcd.setCursor(0,1);
       lcd.print(int(-balanza.get_units(1)*1000));
       delay(100);
       lcd.setCursor(2,1);
       lcd.print("  ");
      }

       if(num_cifras=3){
       lcd.setCursor(0,1);
       lcd.print(int(-balanza.get_units(1)*1000));
       delay(100);
       lcd.setCursor(3,1);
       lcd.print("  ");
      }

       if(num_cifras=4){
       lcd.setCursor(0,1);
       lcd.print(int(-balanza.get_units(1)*1000));
       delay(100);
       lcd.setCursor(4,1);
       lcd.print("  ");
      }

       if(num_cifras=5){
       lcd.setCursor(0,1);
       lcd.print(int(-balanza.get_units(1)*1000));
       delay(100);
       lcd.setCursor(5,1);
       lcd.print("  ");
      }

       if(num_cifras=6){
       lcd.setCursor(0,1);
       lcd.print(int(-balanza.get_units(1)*1000));
       delay(100);
       lcd.setCursor(6,1);
       lcd.print("  ");
      }
  }       
}

void PESO(){
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("PESO EN GRAMOS");
  
  
  }
  void DISPENSADOR(){
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("DISPENSADOR");
  
  
  }

        

void loop() {

if(Serial.available()>0){
  data= Serial.readString(); //lee de python
  elemento1=s.separa(data,',',0); 
  elemento2=s.separa(data,',',1); 
  
  
 gramos=elemento2.toInt();
 nombre= elemento1;

  
          
        lcd.clear();
        lcd.setCursor(0,0);
        lcd.print(nombre);
 }
        
        value = digitalRead(inputPin); 
      if(value == LOW) { // Transición BTN_UP

        
        
       while((-balanza.get_units(1))*1000<gramos){
           
           lcd.setCursor(0,1);
           lcd.print(int(-balanza.get_units(1)*1000));
           
           lcd.setCursor(4,1);
           lcd.print("  ");
             digitalWrite(13, HIGH);
            }
            digitalWrite(13, LOW);
           lcd.clear();
        lcd.setCursor(0,0);
        lcd.print("gramos"); 
   
        lcd.setCursor(0,1);
       lcd.print(gramos); 
        
        
      }  
      
        
      
 
}
     
