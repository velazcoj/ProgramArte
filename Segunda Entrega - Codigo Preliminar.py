from tkinter import Tk,Label,Button,Entry,Frame, Text

from abc import ABC, abstractmethod

class Generador:
    def __init__(self, contenido_inicial):
        self.contenidoInicial = contenido_inicial
        

    @abstractmethod
    def generar(self, apartir_de):
        pass



# class GeneradorTexto(Generador): #objeto de la clase generador
#     def __init__ (self):
#         pass
#     def generar(self, apartir_de):
        
#         texto_generado = "Hola, esto es un texto generado"
#         return texto_generado


class GeneradorTexto(Generador): #objeto de la clase generador
    def __init__(self, contenido_inicial=""): 
        super().__init__(contenido_inicial)

    
    def generar(self, apartir_de):
        texto_generado = "Hola, esto es un texto generado"
        return texto_generado



    
class FrameMenuPrincipal(Frame):

    def __init__(self, master=None):
        super().__init__(master,width=720, height=570)
        self.master = master
        self.pack()
        self.create_widgets()
        self.generador = GeneradorTexto()
        

    # def fEnviar(self):
         
    #     n1 = self.txtNum1.get("1.0", "end-1c")
    #     self.txtNum1.delete("1.0", "end")
    #     self.txtNum3.delete("1.0", "end")  
    #     self.txtNum3.insert("1.0", f" aando descalza, por las calles soleadas de mi música\n soltando pájaros blancos de mis manos\n besando las pupilas negras de soles amarillos\n ando descalza, sobre pasto tierno y acordes azulados")
 
    def solicitarTexto(self):
        textoingresado = self.txtNum1.get("1.0", "end-1c")  # Obtiene el texto del input
        self.txtNum1.delete("1.0", "end")
        self.txtNum3.delete("1.0", "end")  
        resultado = self.generador.generar(textoingresado)  # Genera texto basado en el input
        self.txtNum3.insert("1.0", resultado)  # Inserta el resultado en la caja de texto de respuesta




    def create_widgets(self):
        #Creacion de menu, posiciones, colores...
        
        self.lblTitle = Label(self,text="ProgramArte", fg="black",font= "consolas 20 bold", bd=2,padx=10, pady=10)
        self.lblTitle.pack( padx=10, pady=10)
        
        self.lblNum1 = Label(self,text="Escribe Algo: ",bg="white")
        self.txtNum1=Text(self,bg="white", height=1)
        
        self.btn1=Button(self,text="Enviar", command=self.solicitarTexto)

        self.lblNum3 = Label(self,text="IA dice:",bg="yellow")
        self.txtNum3=Text(self,bg="cyan")

        
        
        self.lblTitle.place(x=10,y=10,width=700, height=100)
        
        
        self.lblNum1.place(x=20,y=200,width=100, height=10)
        self.txtNum1.place(x=120,y=200,width=200, height=30)
        
        self.btn1.place(x=340,y=200,width=80, height=20)
        
        self.lblNum3.place(x=20,y=300,width=100, height=10)
        self.txtNum3.place(x=220,y=300,width=440, height=200)



root = Tk()
root.wm_title("ProgramArte")
app = FrameMenuPrincipal(root) 
app.mainloop()
