#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 16:29:42 2017

@author: Valentin Vie
"""

from Ants import *
from Visualization import *

"""---     Non random example    ---"""
nest = 'Paris'
food = 'Lyon'
explo = 0.3 # 0 means no exploration at all
evapo = 0.01 # At 0 the pheromones don't eveaporate
nb_ants = 200

C = Civilization(nest, food, explo, evapo, nb_ants)

#Adding cities...
C.add_city('Paris',250,40)
C.add_city('Lyon',250,470)
C.add_city('Amiens',370,300)
C.add_city('Lille',370,100)
C.add_city('Nantes',250,320)
C.add_city('Tour',50,320)
C.add_city('Aix',450,400)

#Adding roads...
C.add_road('Lyon','Nantes')
C.add_road('Lyon','Aix')

C.add_road('Aix','Amiens')
C.add_road('Aix','Nantes')
C.add_road('Aix','Lyon')

C.add_road('Amiens','Aix')
C.add_road('Amiens','Lille')
C.add_road('Amiens','Nantes')

C.add_road('Lille','Amiens')
C.add_road('Lille','Paris')

C.add_road('Tour','Nantes')

C.add_road('Nantes','Paris')
C.add_road('Nantes','Tour')
C.add_road('Nantes','Lyon')
C.add_road('Nantes','Aix')
C.add_road('Nantes','Amiens')

C.add_road('Paris','Lille')
C.add_road('Paris','Nantes')

C.initialize()
#print(C)

window = Visualization(C)
window.mainloop()

