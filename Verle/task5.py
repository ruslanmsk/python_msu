import tkinter as tk
import numpy as np
#import matplotlib
import random
from math import sqrt
from math import fabs
from scipy import constants
from scipy import integrate
#import threading
import _thread
import time
from multiprocessing import Process, Queue, current_process, Pool
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
#import verleCython

M=9**9



def isFactor(x):
    result = Python_Verle([x],1)
    return [result[0].x,result[0].y,result[0].u,result[0].v, result[0].m, result[0].color, result[0].lifeTime]
    

class Point:
    def __init__(self, x, y, u, v, m, color = 'red', lifetime = 2):
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.m = m
        self.color = color
        self.lifeTime = lifetime


        
def CalculateAcceleration(bodies):
    acceleration = np.zeros((len(bodies),2))
    for i in range(len(bodies)):
        for j in range(len(bodies)):
            if i != j:
                vector_radius_i = sqrt(bodies[i].x**2 + bodies[i].y**2)
                vector_radius_j = sqrt(bodies[j].x**2 + bodies[j].y**2)
                r = fabs(vector_radius_j-vector_radius_i)
                r = sqrt((bodies[i].x-bodies[j].x)**2+(bodies[i].y-bodies[j].y)**2)
                if r >= 16: 
                    acceleration[i][0] += constants.G*100000000*bodies[j].m*(bodies[j].x-bodies[i].x)/(r**3)
                    acceleration[i][1] += constants.G*100000000*bodies[j].m*(bodies[j].y-bodies[i].y)/(r**3)
    return acceleration # может быть copy надо 
        
def Python_Verle(bodies,dt):
    acceleration = CalculateAcceleration(bodies)
    print(acceleration)
    for i in range(len(bodies)):
        bodies[i].x = bodies[i].x + bodies[i].u*dt+ 0.5*acceleration[i][0]*dt
        bodies[i].y = bodies[i].y + bodies[i].v*dt+ 0.5*acceleration[i][1]*dt
    acceleration_2 = CalculateAcceleration(bodies)
    for i in range(len(bodies)):
        bodies[i].u = bodies[i].u + 0.5*(acceleration[i][0]+acceleration_2[i][0])*dt
        bodies[i].v = bodies[i].v + 0.5*(acceleration[i][1]+acceleration_2[i][1])*dt
    for item in bodies:
        # возможно надо подругому
        if item.lifeTime - dt < 0:
            bodies.remove(item)
        else:
            item.lifeTime -= dt
    return bodies

               
def OdeInt_Verle(bodies, t_max, count_step):
    count = len(bodies)
    def OdeInt_Helper(y,t):
        result = np.zeros(4*count)
        for i in range(count):
            result[2*i] = y[2*count+2*i]
            result[2*i+1] = y[2*count+2*i+1]
            for j in range(count):
                if j != i:
                    vector_radius = sqrt((y[2*j]-y[2*i])**2+(y[2*j+1]-y[2*i+1])**2)
                    if vector_radius >= 16:
                        result[2*count+2*i]+=constants.G*100000000*bodies[j].m*(y[2*j]-y[2*i])/(vector_radius**3)
                        result[2*count+2*i+1]+=constants.G*100000000*bodies[j].m*(y[2*j+1]-y[2*i+1])/(vector_radius**3)
        return result
    initialСonditions = np.zeros(4*count)
    for i in range(count):
        initialСonditions[2*i] = bodies[i].x
        initialСonditions[2*i+1] = bodies[i].y
        initialСonditions[2*count + 2*i] = bodies[i].u
        initialСonditions[2*count + 2*i+1] = bodies[i].v
    t = np.linspace(0, t_max, count_step)
    return integrate.odeint(OdeInt_Helper, initialСonditions, t)
    
    
    
def Multiprocessing_Verle(bodies, index, dt):
    acceleration = [0,0]
    for j in range(len(bodies)):
            if index != j:
                vector_radius_i = sqrt(bodies[index].x**2 + bodies[index].y**2)
                vector_radius_j = sqrt(bodies[j].x**2 + bodies[j].y**2)
                r = fabs(vector_radius_j-vector_radius_i)
                r = sqrt((bodies[index].x-bodies[j].x)**2+(bodies[index].y-bodies[j].y)**2)
                if r >= 16: 
                    acceleration[0] += constants.G*100000000*bodies[j].m*(bodies[j].x-bodies[index].x)/(r**3)
                    acceleration[1] += constants.G*100000000*bodies[j].m*(bodies[j].y-bodies[index].y)/(r**3)
    
    
    bodies[index].x = bodies[index].x + bodies[index].u*dt+ 0.5*acceleration[0]*dt
    bodies[index].y = bodies[index].y + bodies[index].v*dt+ 0.5*acceleration[1]*dt
    acceleration_2 = [0,0]
    for j in range(len(bodies)):
            if index != j:
                vector_radius_i = sqrt(bodies[index].x**2 + bodies[index].y**2)
                vector_radius_j = sqrt(bodies[j].x**2 + bodies[j].y**2)
                r = fabs(vector_radius_j-vector_radius_i)
                r = sqrt((bodies[index].x-bodies[j].x)**2+(bodies[index].y-bodies[j].y)**2)
                if r >= 16: 
                    acceleration[0] += constants.G*100000000*bodies[j].m*(bodies[j].x-bodies[index].x)/(r**3)
                    acceleration[1] += constants.G*100000000*bodies[j].m*(bodies[j].y-bodies[index].y)/(r**3)
                    
    bodies[index].u = bodies[index].u + 0.5*(acceleration[0]+acceleration_2[0])*dt
    bodies[index].v = bodies[index].v + 0.5*(acceleration[1]+acceleration_2[1])*dt
    if bodies[index].lifeTime - dt < 0:
        bodies.remove(bodies[index])
    else:
        bodies[index].lifeTime -= dt
    return bodies
    
    
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
        self.create_point.grid(row=3, column=3, columnspan=1)
        
        self.create_point = tk.Button(text="create", command=self.CreatePoint)
        self.create_point.grid(row=3, column=4, columnspan=1)

        #self.Verle_value = tk.IntVar()
        
#        self.Verle1 = tk.Radiobutton(text="Верле(Python)", variable=self.Verle_value, value=1, indicatoron=0)
#        self.Verle1.grid(row=4, column=1)
#
#        self.Verle2 = tk.Radiobutton(text="Верле(odeint)", variable=self.Verle_value, value=2, indicatoron=0)
#        self.Verle2.grid(row=4, column=2)
#
#        self.Verle3 = tk.Radiobutton(text="Верле(cython)",variable=self.Verle_value, value=3, indicatoron=0)
#        self.Verle3.grid(row=4, column=3)
#
#        self.Verle4 = tk.Radiobutton(text="Верле(parallel)", variable=self.Verle_value, value=4, indicatoron=0)
#        self.Verle4.grid(row=4, column=4)
        
#        self.x_label = tk.Label(text="emitter_X")
#        self.x_label.grid(row=5, column=1)
#        self.x_coor = tk.Entry(bd=5)
#        self.x_coor.grid(row=5, column=2)

#        self.emitter_y_label = tk.Label(text="emitter_Y")
#        self.emitter_y_label.grid(row=5, column=3)
#        self.emitter_y_coor = tk.Entry(bd=5)
#        self.emitter_y_coor.grid(row=5, column=4)
        self.options = ["Верле(Python)", "Odeint", "Верле(cython)", "Верле(parallel)"]
        
        self.Verle_value = tk.StringVar()
        self.Verle_value.set("Верле(Python)")
        self.Verle = tk.OptionMenu(root, self.Verle_value, *self.options)
        self.Verle.grid(row=5, column=1)
        self.Verle.config(font=('calibri',(10)),bg='white',width=12)
        self.Verle['menu'].config(font=('calibri',(10)),bg='white')
        
        self.verle_step = tk.Button(text="play", command=self.Play)
        self.verle_step.grid(row=5, column=2)
        
        self.verle_step = tk.Button(text="verle step", command=self.NextStep)
        self.verle_step.grid(row=7, column=1)
        
        self.verle_step = tk.Button(text="calculate time", command=self.CalculateTime)
        self.verle_step.grid(row=7, column=2)
        


        #self.Verle1.select()

        
    def CalculateTime(self):
        count_step = 10
        start = time.time()
        for i in range(count_step):
            Python_Verle(self.BallList, 1)
        end = time.time()
        print("Python_Verle, time = " + str((end-start)) + ", кол-во шагов = " + str(count_step) + ", кол-во шаров = " + str(len(self.BallList)))
        
        start = time.time()
        OdeInt_Verle(self.BallList, 10, 10)
        end = time.time()
        print("OdeInt_Verle, time = " + str((end-start)) + ", кол-во шагов = " + str(count_step) + ", кол-во шаров = " + str(len(self.BallList)))
        
        start = time.time()
        for i in range(10):
             self.Verle_Parallel(1)
        end = time.time()
        print("Multiprocessing_Verle, time = " + str((end-start)) + ", кол-во шагов = " + str(count_step) + ", кол-во шаров = " + str(len(self.BallList)))
        
#        start = time.time()
#        for i in range(10):
#             verleCython.Python_Verle(self.BallList, 1)
#        end = time.time()
#        print("Cython_Verle, time = " + str((end-start)) + ", кол-во шагов = " + str(count_step) + ", кол-во шаров = " + str(len(self.BallList)))
        
        
        
    def CreatePoint(self):
        self.BallList.append(Point(self.x_value.get(), self.y_value.get(), self.u_value.get(), self.v_value.get(), self.m.get(), np.random.rand(3,1), 100000))
        self.Draw()
        
                
    def CreateRandom(self):
        self.BallList.append(Point(random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), random.randint(100, 20000), np.random.rand(3,1), 100000))
        self.Draw()
        
        
    def Play(self):
        for i in range(100):
            self.NextStep()
            
        
    def NextStep(self):
        verle_flag = self.Verle_value.get()
        if verle_flag == self.options[0]:
            Python_Verle(self.BallList, 1)
        if verle_flag == self.options[1]:
            self.VerleOdeint()
        if verle_flag == self.options[2]:
            verleCython.Python_Verle(self.BallList, 1)
        if verle_flag == self.options[3]:
            self.Verle_Parallel(1)
        self.Draw()
        
        
        
    def Verle_Parallel(self, time):
        try:
            for i in range(len(self.BallList)):
                _thread.start_new_thread(Multiprocessing_Verle, (self.BallList, i, time) )
        except:
            print ("Error: unable to start thread")
#        if __name__ == '__main__':
#            pool = Pool(processes=18)
#            possibleFactors = self.BallList
#            print ('Checking ', 2222)
#            result = pool.map(isFactor, possibleFactors)
#            #cleaned = [x for x in result if not x is None]
#            print ('Factors are', result)
#            self.BallList = []
#            for i in range(len(result)):
#                self.BallList.append(Point(result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],result[i][5],result[i][6]))

        
    def VerleOdeint(self):
        TMax = 1 # область [0,Tmax] 
        TN = 2 # количество шагов
        res = OdeInt_Verle(self.BallList, TMax, TN)
        y = [None]*len(self.BallList)
        x = [None]*len(self.BallList)
        clr = [None]*len(self.BallList)
        area = [None]*len(self.BallList)
        j = 0
        while j < TN:
            #self.plt.clear()
            i = 0
            while i < len(self.BallList):
                x[i] = res[j][2*i]
                y[i] = res[j][2*i+1]
                clr[i] = self.BallList[i].color
                area[i] = int(self.BallList[i].m/M)+20
                i += 1
            #self.plt.scatter(x, y, s=area, c=clr, alpha=0.5)
            #self.plt.axis([-10, 10, -10, 10])
            #self.canvas.draw()
            j += 1
        i = 0
        while i < len(self.BallList):
            self.BallList[i].x = res[TN-1][2*i]
            self.BallList[i].y = res[TN-1][2*i+1]
            self.BallList[i].u = res[TN-1][2*len(self.BallList)+2*i]
            self.BallList[i].v = res[TN-1][2*len(self.BallList)+2*i+1]
            i += 1
        
        
    def Draw(self):
        x_max = 150
        y_max = 150
        self.plt.clear()
        colors = []
        area = []
        x = []
        y = []
        for i in self.BallList:
            x.append(i.x)
            y.append(i.y)
            if fabs(i.x) > x_max - 10:
                x_max = x_max + min(50, i.y + 20)
            if fabs(i.y) > y_max - 10:
                y_max = y_max + min(50, i.x + 20)
            area.append(int(i.m*1000000)/M)
            colors.append(i.color)
        self.plt.scatter(x, y, s=area,c=colors,alpha=0.9, edgecolors="m", marker='o')
        self.plt.axis([-x_max, x_max, -y_max, y_max])
        self.plt.legend()
        self.canvas.draw()

if __name__ == '__main__':
    root = tk.Tk(className="MovingBalls")
    app = Application(master=root)
    app.mainloop()

