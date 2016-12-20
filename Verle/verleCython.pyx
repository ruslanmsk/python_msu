from scipy import constants
import numpy as np
from math import sqrt
from math import fabs

def CalculateAcceleration(bodies):
    acceleration = np.zeros((len(bodies),2))
    for i in range(len(bodies)):
        for j in range(len(bodies)):
            if i != j:
                vector_radius_i = sqrt(bodies[i].x**2 + bodies[i].y**2)
                vector_radius_j = sqrt(bodies[j].x**2 + bodies[j].y**2)
                acceleration[i][0] += constants.G*bodies[j].m*(bodies[j].x-bodies[i].x)/(fabs(vector_radius_j-vector_radius_i)**3)
                acceleration[i][1] += constants.G*bodies[j].m*(bodies[j].y-bodies[i].y)/(fabs(vector_radius_j-vector_radius_i)**3)
    return acceleration

def Python_Verle(bodies,dt):
    acceleration = CalculateAcceleration(bodies)
    for i in range(len(bodies)):
        bodies[i].x = bodies[i].x + bodies[i].u*dt+ 0.5*acceleration[i][0]*dt
        bodies[i].y = bodies[i].y + bodies[i].v*dt+ 0.5*acceleration[i][1]*dt
    acceleration_2 = CalculateAcceleration(bodies)
    for i in range(len(bodies)):
        bodies[i].u = bodies[i].u + 0.5*(acceleration[i][0]+acceleration_2[i][0])*dt
        bodies[i].v = bodies[i].v + 0.5*(acceleration[i][1]+acceleration_2[i][1])*dt
    for item in bodies:
        if item.lifeTime - dt < 0:
            bodies.remove(item)
        else:
            item.lifeTime -= dt
    return bodies
