from tkinter import Tk,Label,Button,Entry,Frame, Text

from abc import ABC, abstractmethod

import requests

import fireworks.client
from fireworks.client.image import ImageInference, Answer
import matplotlib.pyplot as plt
from PIL import Image



class Generador:
    def __init__(self, contenido_inicial):
        self.contenidoInicial = contenido_inicial
        
    @abstractmethod   
    def generar(apartir_de):
        pass


class GeneradorTexto(Generador): #objeto de la clase generador
    def __init__ (self):
        pass
        
    def generar(self, apartir_de):
        
        texto_generado = aPIdeappcreadoradetextos().generarnuevotexto(apartir_de)
        return texto_generado
    
class GeneradorImagen(Generador): #objeto de la clase generador
    def __init__ (self):
        pass
        
    def generar(self, apartir_de): 
        aPIdeappcreadoradeimagenes().generar(apartir_de)
        

class aPIdeappcreadoradeimagenes():
    def __init__(self):
        # Aquí puedes inicializar cualquier atributo necesario para tu API
        pass

    def generar(self, contenidoinicial):
        return self.realizarsolicitud(contenidoinicial)
        
    def realizarsolicitud(self,contenidoinicial):
                        # Initialize the ImageInference client
        fireworks.client.api_key = "fw_3ZdtsSEDfyVWWLMy8E9T77tq"

        inference_client = ImageInference(model="stable-diffusion-xl-1024-v1-0")

        # Generate an image using the text_to_image method
        answer : Answer = inference_client.text_to_image(
            prompt= contenidoinicial,
            cfg_scale=7,
            height=1024,
            width=1024,
            sampler=None,
            steps=30,
            seed=0,
            safety_check=False,
            output_image_format="JPG",
            # Add additional parameters here
        )

        if answer.image is None:
          raise RuntimeError(f"No return image, {answer.finish_reason}")
        else:
          answer.image.save("output4.jpg")

        # Carga la imagen generada
        image_path = "output4.jpg"
        image = Image.open(image_path)

        # Muestra la imagen en un marco
        plt.imshow(image)
        plt.axis("off")  # Oculta los ejes
        plt.show()


class aPIdeappcreadoradetextos():
    def __init__(self):
        
        pass

    def generarnuevotexto(self, contenidoinicial):
        return self.realizarsolicitud(contenidoinicial)
        
    def realizarsolicitud(self,contenidoinicial):
        url = "https://www.learnitive.com/api/v1/contents"
        headers = {
            "content-type": "application/json",
            "Accept": "application/json",
            "api-key": ""  
        }

        data = {
            "input": contenidoinicial,
            "model": "balanced",
           "keywords": [],
            "max_tokens": "100",
            "temperature": "0.65"
        }

        response = requests.post(url, json=data, headers=headers)

        # Verifica si la solicitud fue exitosa
        if response.status_code == 200:
            result = response.json()
             #Accede al campo 'text' dentro de la lista 'message'
            texto = result['message'][0]['text']
            print(texto)
            print(type(texto))
            return texto
        else:
            print(f"Error en la solicitud (código {response.status_code}):")
            print(response.text)
                


    
class FrAI(Frame):

    def __init__(self, master=None):
        super().__init__(master,width=720, height=570)
        self.master = master
        self.pack()
        self.create_widgets()
        self.generadortexto = GeneradorTexto()
        self.generadorimagen = GeneradorImagen()

    def EnviarSolicitudTexto(self):
         
        n1 = self.generadortexto.generar(self.txtNum1.get("1.0", "end-1c"))
        print(n1)
        print(type(n1))
        if isinstance(n1, str):
        # Inserta el texto en el widget de texto
            print(type(n1))
            self.txtNum3.delete("1.0", "end")
            self.txtNum3.insert("1.0", n1)
            self.txtNum1.delete("1.0", "end")
        else:
            print("Error: El resultado no es una cadena de texto válida.")
            
    def enviarSolicitudImagen(self):
        textodesolicitud = self.txtNum1.get("1.0", "end-1c")
        self.txtNum1.delete("1.0", "end")
        self.generadorimagen.generar(textodesolicitud)
        
    def enviarSolicitudImagenyTexto(self):
        pass
        

               
 

    def create_widgets(self):

        
        self.lblTitle = Label(self,text="ProgramArte", fg="black",font= "consolas 20 bold",
        bd=2,
        padx=10, pady=10)
        
        self.lblTitle.pack( padx=10, pady=10)
        self.lblTitle.place(x=10,y=10,width=700, height=100)
        
        #AI dice:
        self.lblNum3 = Label(self,text="AI dice:",bg="yellow")
        self.txtNum3=Text(self,bg="cyan")
        
        
        
        #Aca se ingresa el texto y el label de "escribe algo"
        self.lblNum1 = Label(self,text="Escribe Algo: ",bg="white")
        self.txtNum1= Text(self,bg="white", height=1)
        self.lblNum1.place(x=20,y=200,width=100, height=10)
        self.txtNum1.place(x=120,y=200,width=200, height=30)

        #botones
        self.btn1=Button(self,text="GTexto", command=self.enviarSolicitudImagen)
        self.btn1.place(x=340,y=200,width=80, height=20)
        
        self.btn2=Button(self,text="GImagen", command=self.enviarSolicitudImagen)
        self.btn2.place(x=340,y=230,width=80, height=20)
        
        self.btn3=Button(self,text="GImagenyTexto", command=self.enviarSolicitudImagenyTexto)
        self.btn3.place(x=340,y=260,width=80, height=20)

        #Aca aparece el texto de resultado
        self.lblNum3.place(x=20,y=300,width=100, height=10)
        self.txtNum3.place(x=220,y=300,width=440, height=200)



root = Tk()
root.wm_title("ProgramArte")
app = FrAI(root) 
app.mainloop()
