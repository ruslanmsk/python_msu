import tkinter as tk
import numpy as np
import matplotlib
import random
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

M=10**10

class Point:
    def __init__(self, x, y, u, v, m, color = 'red', lifetime = 2):
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.m = m
        self.color = color
        self.lifeTime = lifetime


class AlphaAndOmegaCreator:
    def __init__(self, x, y, u, v, m, color):
         newPoint = Point().__init__(x, y, u, v, m, color)
         return newPoint

    def play(self):
        Application.canvas


class Application(tk.Frame):
    BallList = []
    #_fig =  Figure(figsize=(5, 4), dpi=100, facecolor='white')
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.create_canvas()
        self.create_user_panel()

    def create_canvas(self) -> object:
        self.f = Figure(figsize=(5, 4), dpi=100)
        self.plt = self.f.add_subplot(111)
        #a = f.add_subplot(111)
        #t = arange(0.0, 3.0, 0.01)
        #s = sin(2 * pi * t)

        #a.plot(t, s)

        self.canvas = FigureCanvasTkAgg(self.f, master=root)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=6, column=1, columnspan=6)
        '''self.canvas = tk.Canvas(bg="blue", height=400, width=800)
        self.canvas.grid(row=5, column=1, columnspan=6)'''

    def create_user_panel(self)->object:
        self.x_label = tk.Label(text="X")
        self.x_label.grid(row=1, column=1)
        self.x_value = tk.DoubleVar()
        self.x_coor = tk.Entry(bd=5, textvariable=self.x_value)
        self.x_coor.grid(row=1, column=2)

        self.y_label = tk.Label(text="Y")
        self.y_label.grid(row=2, column=1)
        self.y_value = tk.DoubleVar()
        self.y_coor = tk.Entry(bd=5, textvariable=self.y_value)
        self.y_coor.grid(row=2, column=2)

        self.u_label = tk.Label(text="U")
        self.u_label.grid(row=1, column=3)
        self.u_value = tk.DoubleVar()
        self.u_coor = tk.Entry(bd=5, textvariable=self.u_value)
        self.u_coor.grid(row=1, column=4)

        self.v_label = tk.Label(text="V")
        self.v_label.grid(row=2, column=3)
        self.v_value = tk.DoubleVar()
        self.v_coor = tk.Entry(bd=5, textvariable=self.v_value)
        self.v_coor.grid(row=2, column=4)

        self.m_label = tk.Label(text="M")
        self.m_label.grid(row=3, column=1)
        self.m = tk.Scale(variable="weight", activebackground="red", orient="horizontal")
        self.m.grid(row=3, column=2)

        self.create_point = tk.Button(text="generate", command=self.CreateRandom)
        self.create_point.grid(row=3, column=3, columnspan=2)

        self.Verle1 = tk.Radiobutton(text="Верле(Python)", variable="verle", value=1)
        self.Verle1.grid(row=4, column=1)

        self.Verle2 = tk.Radiobutton(text="Верле(odeint)", variable="verle", value=2)
        self.Verle2.grid(row=4, column=2)

        self.Verle3 = tk.Radiobutton(text="Верле(cython)", variable="verle", value=3)
        self.Verle3.grid(row=4, column=3)

        self.Verle4 = tk.Radiobutton(text="Верле(parallel)", variable="verle", value=4)
        self.Verle4.grid(row=4, column=4)
        
        self.x_label = tk.Label(text="emitter_X")
        self.x_label.grid(row=5, column=1)
        self.x_coor = tk.Entry(bd=5)
        self.x_coor.grid(row=5, column=2)

        self.emitter_y_label = tk.Label(text="emitter_Y")
        self.emitter_y_label.grid(row=5, column=3)
        self.emitter_y_coor = tk.Entry(bd=5)
        self.emitter_y_coor.grid(row=5, column=4)
        
        self.verle_step = tk.Button(text="verle step", command=self.NextStep)
        self.verle_srep.grid(row=7,column=1)

        self.Verle1.select()

    def CreatePoint(self):
        self.BallList.append(Point(self.x_value.get(), self.y_value.get(), self.u_value.get(), self.v_value.get(), self.m.get(), 'blue', 333))
        self.Draw()
        
                
    def CreateRandom(self):
        self.BallList.append(Point(random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), random.randint(1, 20), "red", 3223))
        self.Draw()
        
        
    def NextStep(self):
        Verl(self.BallList, 1)
        self.Draw()
        
        
    def Draw(self):
        self.plt.clear()
        colors = []
        area = []
        x = []
        y = []
        for i in self.BallList:
            x.append(i.x)
            y.append(i.y)
            area.append(int(i.m/M)+20)
            colors.append(i.color)
        self.plt.scatter(x, y, s=area,c=colors,alpha=0.5)
        self.plt.axis([-10, 10, -10, 10])
        self.canvas.draw()


root = tk.Tk(className="MovingBalls")
app = Application(master=root)
app.mainloop()

