import Tkinter,tkFileDialog
from PIL import Image, ImageTk
from Imagehandler import Imagehandler
import cv2
import os

class Window:
    def choose_file(self):
        filename = tkFileDialog.askopenfile()
        if filename is not None:
            image=Image.open(filename.name)
            image=image.resize((300,300),Image.ANTIALIAS)
            photo=ImageTk.PhotoImage(image)

            self.label1.configure(image=photo)
            self.label1.image=photo
            self.process(filename.name)

    def restart(self):
        self.win.destroy()
        Window()

    def process(self, name):
        obj= Imagehandler(name)
        newImg = obj.QRCodeInImage()
        if newImg is not None:
            image = cv2.cvtColor(newImg,cv2.COLOR_BGR2RGB)
            #print (type(image))
            cv2.imwrite(str(os.getcwd())+"/Results/a.png",image)

            img = Image.open(str(os.getcwd())+"/Results/a.png")
            #print (type(img))

            img = img.resize((300,300),Image.ANTIALIAS)
            photo= ImageTk.PhotoImage(img)
            self.label2.configure(image=photo)
            self.label2.image=photo

    def __init__(self):
        root= Tkinter.Tk()
        root.geometry('700x500')
        self.win=root
        browse=Tkinter.Button(root,text="browse",command=self.choose_file)
        browse.place(x=10,y=10)

        restart=Tkinter.Button(root,text="restart",command=self.restart)
        restart.place(x=100,y=10)

        image1=Image.open("res/No_Input.png")
        image1=image1.resize((300,300),Image.ANTIALIAS)
        photo1=ImageTk.PhotoImage(image1)

        self.label1 = Tkinter.Label(image=photo1)
        self.label1.image=photo1

        self.label1.place(x=10,y=100)


        image2=Image.open("res/No_Output.png")
        #print (type(image2),"jefbkkbbef")
        image2=image2.resize((300,300),Image.ANTIALIAS)
        photo2=ImageTk.PhotoImage(image2)

        self.label2=Tkinter.Label(image=photo2)
        self.label2.image=photo2
        self.label2.place(x=350,y=100)
        root.mainloop()

Window()



