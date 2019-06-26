#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 16:29:42 2017

@author: Valentin Vie
"""

from Ants import *
import tkinter as tk
import random as rand

"""---     Vizualization of the process    ---"""
class Visualization(tk.Tk):
    def __init__(self, C, nb_cities = 20, nb_roads = 30):
        tk.Tk.__init__(self)

        #Initialization of attributes
        self.continue_viz = True
        self.C = C
        self.ran_once = False
        self.nb_iter = 0
        self.nb_cities = nb_cities
        self.nb_roads = nb_roads

        self.title('Vizualization of the colony')
        self.geometry("%dx%d%+d%+d" % (500,650,500,300))
        
        #Canvas zone
        self.canvas = tk.Canvas(self,width = 480,height = 500,bg = 'ivory')
        
        #Top Label
        self.top_label = tk.Label(self, text="My civilization :\nNumber of ants : "+\
                              str(C.nb_ants)+" Exploration : "+\
                              str(C.exploration))
        
        #Bottom lablel
        self.hint_label = tk.Label(self, text="Click on a city to change it to food city or normal city.")
        
        #Buttons area
        self.user_area = tk.Frame(self,width =500,height = 100)
        self.button_go = tk.Button(self.user_area, text = 'Start !',\
                                   command = self.start_vizualization)
        self.button_stop = tk.Button(self.user_area, text = 'Stop !',\
                                   command = self.stop_vizualization, state = tk.DISABLED)
        self.new_simul = tk.Button(self.user_area, text = 'New graph',\
                                   command = self.new_graph)
        self.label_iter = tk.Label(self.user_area,\
                                   text = "Start the vizualization...")
        
        #Mouse clic handling:
        self.canvas.bind('<Button-1>', self.click)
        
        #Initialization of the graph if non already existent
        if len(self.C.city_list) == 0:
            self.new_graph()
        else:
            self.update_viz()
        
        #Pack everything on the window 
        self.canvas.pack(padx = 5,pady = 5, side = tk.BOTTOM)
        self.top_label.pack(padx = 5,pady = 5, side = tk.TOP)
        self.new_simul.pack(side = tk.LEFT)
        self.button_go.pack(side = tk.LEFT)
        self.button_stop.pack(side = tk.LEFT)
        self.label_iter.pack(side = tk.BOTTOM)
        self.hint_label.pack(padx = 5,pady = 5, side = tk.BOTTOM)
        self.user_area.pack()
    
    
    
    def update_viz(self):
        #Update the vizualization

        self.canvas.delete("all")
        
        #Display cities
        self.draw_cities(20)
        #Display roads
        self.draw_roads()
        #Display city labels
        self.draw_labels()
        #Update the label_iter with the good iteration nb
        self.label_iter.config(text = "Nombre d'itérations :"+str(self.nb_iter))
        #Display ants
        self.draw_ants()
    
        
    def draw_labels(self):
        #Display city names
        for city in self.C.city_list:
            self.canvas.create_text(city.x,city.y+20,text = city.name,\
                                    fill = 'red')
    def draw_cities(self, radius):
        #Display cities
        for city in self.C.city_list:
            if city.food:
                self.canvas.create_oval(city.x-radius/2,city.y-radius/2,\
                                    city.x+radius/2,city.y+radius/2,\
                                    fill = 'orange',outline = 'black')
            elif city.nest:
                self.canvas.create_oval(city.x-radius/2,city.y-radius/2,\
                                    city.x+radius/2,city.y+radius/2,\
                                    fill = 'green',outline = 'black')
            else :
                self.canvas.create_oval(city.x-radius/2,city.y-radius/2,\
                                    city.x+radius/2,city.y+radius/2,\
                                    fill = 'white',outline = 'black')

    def draw_roads(self):
        #Display road with different thickness to represent the PL.
        PL_max = 0
        for road in self.C.road_list:
            PL_max = max(road.PL, PL_max)
            #print(PL_max)

        if self.ran_once and PL_max >= 1000:
            for road in self.C.road_list:
                if road.PL > PL_max * 0.65:
                    self.canvas.create_line(road.city_1.x,road.city_1.y,\
                                            road.city_2.x,road.city_2.y,\
                                            fill = 'black', width = 10,arrow = tk.LAST)
                elif road.PL > (PL_max * 0.5):
                    self.canvas.create_line(road.city_1.x,road.city_1.y,\
                                            road.city_2.x,road.city_2.y,\
                                            fill = 'black', width = 7, arrow = tk.LAST)
                
                elif road.PL > (PL_max * 0.4):
                    self.canvas.create_line(road.city_1.x,road.city_1.y,\
                                            road.city_2.x,road.city_2.y,\
                                            fill = 'black', width = 5, arrow = tk.LAST)
                
                elif road.PL > (PL_max * 0.3):
                    self.canvas.create_line(road.city_1.x,road.city_1.y,\
                                            road.city_2.x,road.city_2.y,\
                                            fill = 'black', width = 4, arrow = tk.LAST)
                else :
                    self.canvas.create_line(road.city_1.x,road.city_1.y,\
                                            road.city_2.x,road.city_2.y,\
                                            fill = 'black', width = 1, arrow = tk.LAST)
        else :
            self.ran_once = True
            for road in self.C.road_list:
                self.canvas.create_line(road.city_1.x,road.city_1.y,\
                                            road.city_2.x,road.city_2.y,\
                                            fill = 'black', width = 1, arrow = tk.LAST)
    
    def display_PL(self):
        #Display the pheromone level of the 3 most used roads
        L = sorted(self.C.road_list, key = lambda x: x.PL, reverse=True)
        #print(L)

        for i in range(3):
            road = L[i]
            self.canvas.create_text((road.city_1.x+road.city_2.x)/2-30,\
                                    (road.city_1.y+road.city_2.y)/2-30,\
                                    text = str(int(road.PL)))
    
    def draw_ants(self):
        #Display the ants
        for ant in self.C.ant_list:
            try :
                t = ant.progression/ant.last_road_visited.length
                x1 = ant.last_city_visited.x
                y1 = ant.last_city_visited.y
                x2 = ant.current_city.x
                y2 = ant.current_city.y
                self.canvas.create_oval(t*x1+(1-t)*x2-3, t*y1+(1-t)*y2-3,\
                                        t*x1+(1-t)*x2+3, t*y1+(1-t)*y2+3,\
                                        fill = 'white',outline = 'red')
            except:
                #If the last city is not defined,
                #this happens when the ant is just defined,
                #we choose not to display the ant because it creates an error.
                pass
            
    
    def start_vizualization(self):
        # Start the vizualization and activate the stop button
        if self.continue_viz:
            self.C.iterate()
            self.update_viz()
            self.nb_iter += 1
            self.button_go.configure(state = tk.DISABLED)
            self.button_stop.configure(state = tk.ACTIVE)
            self.after(20, self.start_vizualization)
        else:
            self.continue_viz = True
        
    
    def stop_vizualization(self):
        # Stop the vizualization and switch go button to activated
        self.continue_viz = False
        self.update_viz()
        self.display_PL()
        self.button_go.configure(state = tk.ACTIVE)
        self.button_stop.configure(state = tk.DISABLED)
    
    def new_graph(self):
        #Create a random graph with nb_cities cities and
        #nb_roads roads. We choose to ignore graphs where city_food and 
        #nest_city are directly connected.
        #It is possible that the graphs are impossible to solve.

        self.C.reset()

        if self.nb_roads <= 1:
            print('The number of roads is invalid.')
            return 1
        
        for c in range(self.nb_cities):
            self.C.add_city(str(c),rand.randint(30,450),rand.randint(30,470))

        countRoads = 0
        while countRoads < self.nb_roads:
            name1 = str(rand.randint(0,(self.nb_cities-1)))
            name2 = str(rand.randint(0,(self.nb_cities-1)))

            while name2 == name1 or (name1 == '0' and name2 == '1') or (name2 == '0' and name1 == '1'):
                name2 = str(rand.randint(0,(self.nb_cities-1)))

            #Undirected graph without duplicate edges: 
            if self.C.add_road(name1, name2) and self.C.add_road(name2, name1):
                countRoads += 1
        
        if len(self.C.search_city('0').edges) == 0 or\
        len(self.C.search_city('1').edges) == 0 :
            # If city #1 and city #2 are connected we generate another graph
            self.C.reset()
            self.new_graph()
        
        self.C.nest_city = '0'
        self.C.city_food = '1'
        self.C.initialize()
        self.ran_once = False
        self.nb_iter = 0
        self.update_viz()
    
    def click(self,event):
        click_x = event.x
        click_y = event.y
        for city in self.C.city_list:
            if (click_x-city.x)**2 +(click_y-city.y)**2 <= 10**2:
                city.food = not city.food
                #There can be multiple city_food
        self.ran_once = False
        self.update_viz()
        


"""---     TESTS    ---"""
if __name__ == "__main__":
    nest = '0'
    food = '1'
    explo = 0.3 # 0 means no exploration at all
    evapo = 0.01 # At 0 the pheromones don't eveaporate
    nb_ants = 200 # Number of ants
    nb_cities = 20 # Number of cities
    nb_roads = 30 # Number of roads
    C = Civilization(nest, food, explo, evapo, nb_ants)

    #Will generate a random graph because C is empty:
    window = Visualization(C, nb_cities, nb_roads) 
    window.mainloop()
