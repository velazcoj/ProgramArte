from tkinter import Tk,Label,Button,Frame, Text
from PIL import Image, ImageTk
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
        )

        if answer.image is None:
            raise RuntimeError(f"No return image, {answer.finish_reason}")
        else:
            answer.image.save("output.jpg")

        # Carga la imagen generada
        image_path = "output.jpg"
        image = Image.open(image_path)

        # Muestra la imagen en un marco
        plt.imshow(image)
        plt.axis("off")
        plt.show()


class aPIdeappcreadoradetextos():
    def __init__(self):
        pass

    def generarnuevotexto(self, contenidoinicial):
        return self.realizarsolicitud(contenidoinicial)
        
    def realizarsolicitud(self, contenidoinicial):
        url = "https://www.learnitive.com/api/v1/contents"
        headers = {
            "content-type": "application/json",
            "Accept": "application/json",
            "api-key": "lzdXeMv24j"  # Asegúrate de usar tu clave API
        }
        data = {
            "input": contenidoinicial,   # El texto que quieres convertir
            "model": "balanced",         # Modelo según el ejemplo de la API
            "keywords": [],  # Puedes cambiar estas palabras clave si es necesario
            "max_tokens": 50,           # Número de tokens como número entero
            "temperature": 0.65,          # El nivel de aleatoriedad, como número flotante
            "target_lang":"es"
        }
        
        # Realizar la solicitud POST a la API
        response = requests.post(url, json=data, headers=headers)

        # Verifica si la solicitud fue exitosa
        if response.status_code == 200:
            result = response.json()
            print(result)  # Verifica qué devuelve la API
            if isinstance(result, dict) and 'message' in result:
                texto = result['message'][0]['text']
                return texto
            else:
                print(f"Estructura inesperada en la respuesta: {result}")
                return "Error: La respuesta no tiene el formato esperado."
        else:
            print(f"Error en la solicitud (código {response.status_code}):")
            print(response.text)
            return "Error: No se pudo completar la solicitud."
                


    
class Interfaz(Frame):
    def __init__(self, master=None):
        super().__init__(master,width=1080, height=720, bg ="#ffebc2")
        self.master = master
        self.pack()
        self.create_widgets()
        self.generadortexto = GeneradorTexto()
        self.generadorimagen = GeneradorImagen()
        self.master.bind('<Configure>', self.update_image_position)

    def EnviarSolicitudTexto(self):
        # Generar el texto utilizando el generador
        n1 = self.generadortexto.generar(self.inputPrompt.get("1.0", "end-1c"))
        print(n1)
        print(type(n1))

        if isinstance(n1, str):
            # El texto generado es válido, así que inicializa la posición actual
            self.posicion_actual = 0  # Inicializamos la variable de posición
            
            # Inserta el texto en el widget de texto
            self.output.delete("1.0", "end")
            self.texto_a_mostrar = n1  # Guardamos el texto a mostrar

            # Inicia el proceso de escritura del texto
            self.escribir_texto()

            # Borrar el contenido del input después de procesar
            self.inputPrompt.delete("1.0", "end")
        else:
            print("Error: El resultado no es una cadena de texto válida.")

    def escribir_texto(self):
        # Método para escribir el texto de manera secuencial con efecto de escritura
        if self.posicion_actual < len(self.texto_a_mostrar):
            self.output.insert("end", self.texto_a_mostrar[self.posicion_actual])
            self.posicion_actual += 1
            self.after(100, self.escribir_texto) 
    
    def enviarSolicitudImagen(self):
        textodesolicitud = self.inputPrompt.get("1.0", "end-1c")
        self.inputPrompt.delete("1.0", "end")
        self.generadorimagen.generar(textodesolicitud)
        
    def enviarSolicitudImagenyTexto(self):
        pass
        


    def create_widgets(self):

        # Cargar la imagen en memoria
        self.image = Image.open("titulo.png")  
        self.image = self.image.resize((600, 250))  # Ajusta el tamaño según sea necesario
        self.photo = ImageTk.PhotoImage(self.image)

        # Label con la imagen principal
        self.titulo = Label(self, image=self.photo, bg="#ffebc2", borderwidth=0)
        self.titulo.place(anchor="center")  # Usamos anchor="center" para centrar
        
        # Etiqueta del prompt y prompt
        self.etiquetaPrompt = Label(self,text="Covierte tu texto a poesía:", fg="black", bg="#ffebc2", height=2, font=("Segoe UI", 16, "bold"), relief="raised", borderwidth=0.5)
        self.etiquetaPrompt.place(x=60, y=200, height=35)
        self.inputPrompt= Text(self, bg="#dfc29e", font=("Segoe UI", 14))
        self.inputPrompt.place(x=120,y=250, width=810, height=100)
        
        # Cargar la imagen 'icon.png'
        self.icon_image = Image.open("icon.png")
        self.icon_image = self.icon_image.resize((50, 50))  # Redimensionar si es necesario
        self.icon_photo = ImageTk.PhotoImage(self.icon_image)
        
        # Label con la imagen y output
        self.icon = Label(self, image=self.icon_photo, bg="#2e2e2e", relief="raised", borderwidth=1)
        self.icon.place(x=60,y=450,width=50, height=50)
        self.output =Text(self,bg="#c4ac94",font=("Segoe UI", 14))
        self.output.place(x=120,y=450,width=810, height=200)
        
        #botones
        self.botonTexto=Button(self,text="Obtener texto", 
                                    command=self.EnviarSolicitudTexto, 
                                    cursor="hand2", 
                                    font=("Segoe UI", 16),
                                    activebackground="#924019",
                                    bg="#b2856c",
                                    fg="white")
        self.botonTexto.place(x=190,y=370,width=180, height=35)
        
        self.botonImagen=Button(self,text="Obtener imagen", 
                                    command=self.enviarSolicitudImagen, 
                                    cursor="hand2", 
                                    font=("Segoe UI", 16),
                                    activebackground="#924019",
                                    bg="#b2856c",
                                    fg="white")
        self.botonImagen.place(x=440,y=370,width=180, height=35)
        
        self.botonTextoEImagen=Button(self,text="Texto e imagen", 
                                    command=self.enviarSolicitudImagenyTexto, 
                                    cursor="hand2", 
                                    font=("Segoe UI", 16),
                                    activebackground="#924019",
                                    bg="#b2856c",
                                    fg="white")
        self.botonTextoEImagen.place(x=690,y=370,width=180, height=35)

    def update_image_position(self, event=None):
        new_x = self.master.winfo_width() // 2
        self.titulo.place(x=new_x, y=100, anchor="center")

    def margin_left(self, event=None):
        new_y = self.master.winfo_width() // 10
        self.titulo.place(x=100, y=new_y)

root = Tk()
root.wm_title("ProgramArte")
root.configure(bg="#ffebc2")
app = Interfaz(root) 
app.mainloop()


