#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 15:09:14 2017

@author: Valentin Vie
"""
import random as rand
import math as m

"""---     CLASS ANT (Workers / Explorers)    ---"""

class Ant:    
    def __init__(self, start_city, exploration):
        self.porte_nouriture = False
        self.alpha = rand.random()*10-5 # Number in [-5, 5] parameter #1 of the ant
        self.beta = rand.random()*10-5 # Number in [-5, 5] parameter #2 of the ant
        self.gamma = rand.random() # Number between 0 and 1 the exploration parameter q
        self.exploration = exploration # Exploration factor given by the civilization: 0 = no exploration
        
        self.city_visited = [] # List of cities already visited
        self.road_visited = [] # List of roads already visited
        self.last_road_visited = 0
        self.last_city_visited = start_city
        self.current_city = start_city # Next city to be reached
        self.progression = 0 # Remaining length to reach the current_city
        self.length_traveled = 0 # Total length the ant traveled
        
        self.success = 0 # Number of time the ant reached the end: success
        self.nest_city = start_city
    
    def __str__(self):
        #Display the ant's attributes
        return "Ants : ({}, {}, {}), Ville {}".\
        format(round(self.alpha,3),round(self.beta,3),\
               round(self.gamma,3),self.last_city_visited)
    
    def release_pheromone(self):
        #Drop pheromones on the roads visited when we reach the end
        self.road_visited= list(set(self.road_visited)) #Remove duplicates elements

        for road in self.road_visited: 
            road.PL += 1/m.sqrt(self.length_traveled)*5000
            # Parameter fixed empirically

    def avail_roads(self, city):
        # Return the roads we can take without taking the same one the ant was on
        Roads = city.edges
        R_available = []
        for r in Roads:
            if r.city_2.name != self.last_city_visited.name:
                R_available.append(r)
        return Roads
        
    def no_exploration_choice(self, R_dispo):
        R0 = 0
        criterion = -1
        petit_PL = True
        for r in R_dispo :
            if r.PL >= 100 :
                petit_PL = False

        if petit_PL: 
        # If the pheromone level is lower than 100 (hard coded),
        # we choose the next city in a random way.
        # The ants can't smell anything.
            return R_dispo[rand.randint(0,len(R_dispo)-1)]
        else:
            # Otherwise we choose according to another formula 
            # depending on the pheromone level & beta.
            for r in R_dispo:
                if r.PL*(1/r.length)**self.beta > criterion:
                    R0 = r
                    criterion = r.PL*(1/r.length)**self.beta 
            return R0
    
    def with_exploration_choice(self,R_dispo):
        proba_list = [] # Probablity to go to each city next
        # We go to the city if we draw a number between proba_list[i-1] and proba_list[i]
        S = self.sum_probability(R_dispo)
        for r in R_dispo:

            numerator = (r.PL)**self.alpha * (1/r.length)**self.beta
            
            try :
                proba_list.append(proba_list[-1]+numerator/S)
            except : 
                # if it is the first element of proba_list
                proba_list.append(numerator/S)
        
        choice = rand.random()
        index = 0
        for p in proba_list:
            if p <= choice:
                index += 1
        return R_dispo[index]

    
    def sum_probability(self,R_dispo):
        #sum the probabilities over the reachable cities
        S = 0
        for r in R_dispo:
            S += (r.PL)**self.alpha * (1/r.length)**self.beta
        return S
    
    def choose_new_route(self):
        roads_avail = self.avail_roads(self.current_city) 
        # All the available roads

        if self.gamma > self.exploration: # witout exploration...
            return self.no_exploration_choice(roads_avail)
        else : # with exploration...
            return self.with_exploration_choice(roads_avail)
        

    def move_on(self):
        if self.progression > 0:
            self.progression -= 10 # We move by 1 step
        else: # We reached the end of the road
            if self.current_city.food:
                self.success += 1
                self.release_pheromone()
                # We release the pheromones on all taken roads.
                self.city_visited = []
                self.road_visited = []
                self.last_road_visited = 0
                self.last_city_visited = self.nest_city
                self.current_city = self.nest_city # We start to look for food again
                self.progression = 0 
                self.length_traveled = 0
            else: # We are not to the food city yet yet...
                # We choose another road
                new_r = self.choose_new_route()
                self.road_visited.append(new_r)
                self.last_road_visited = new_r
                # We switch current_city and the new one
                self.last_city_visited = self.current_city
                self.current_city = new_r.city_2
                # We add to the traveled length
                self.length_traveled += new_r.length
                self.progression = new_r.length
                self.city_visited.append(new_r.city_2)
            
    

        
"""---     CLASSE ROADS (Edges)    ---"""

class Road:
    def __init__(self, city_1, city_2, L):
        self.city_1 = city_1 # City object
        self.city_2 = city_2
        self.length = L # Integer
        self.PL = 0 # Pheromone Level

    def __repr__(self):
        return "Road : From {} to {}, {}km, {}PL".\
        format(self.city_1.name,self.city_2.name,round(self.length,2),\
               round(self.PL,3))

    
    def get_PL(self):
        return self._PL
    def set_PL(self, new_PL):
        self._PL = new_PL
    PL = property(get_PL,set_PL)
    # Calls get_PL and set_PL when accessing the attribute of a Route 
    #(https://www.programiz.com/python-programming/property) 
    
    
"""---     CLASS CITY (Nodes)    ---"""

class City:
    def __init__(self, name, x, y, edges = None):
        self.name = name
        if edges is None:
            self.edges = [] # List of roads departing from it
        else:
            self.edges = edges

        self.x = x # Position on the Canvas
        self.y = y
        self.food = False # Not the food city by default
        self.nest = False # Not the nest city by default
    
    def __repr__(self):
        return "City : name({}), edges({}), x({}), y({})".\
        format(self.name, self.edges, self.x, self.y)
    
    def __str__(self):
        return "City : name({}), edges({}), x({}), y({})".\
        format(self.name, self.edges, self.x, self.y)
    
    def get_x(self):
        return self._x
    def set_x(self,x_new):
        self._x = x_new
    x = property(get_x,set_x)

    def get_y(self):
        return self._y
    def set_y(self,y_new):
        self._y = y_new
    y = property(get_y,set_y)
    
    def get_name(self):
        return self.name


"""---     CLASS CIVILIZATION (Cities + Roads + Ants)    ---"""

class Civilization:
    def __init__(self, nest_city, city_food, explo, evapo, nb_ants):
        self.nb_ants = nb_ants
        self.city_list = []
        self.city_name_list = []
        self.ant_list = []
        self.road_list = []
        self.exploration = explo # Exploration parameter q0 in the slides
        self.evapo = evapo # Evaporation parameter (between 0 and 1)
        self.nest_city = nest_city #String name of a City
        self.city_food = city_food #String name of a City
    
    def __repr__(self):
        return str(self.city_list) + str(self.road_list)
    
    def __str__(self):
        out = []
        out.append("Villes :\n")
        for c in self.city_list:
            out.append(str(c))
            out.append('\n')
        
        out.append("\nRoutes :\n")
        for r in self.road_list:
            out.append(str(r))
            out.append('\n')

        return ''.join(out)
            
        
    def search_city(self, city_name): 
        # Return the city with name city_name
        L = self.city_name_list
        if city_name in L:
            return self.city_list[L.index(city_name)]
        else:
            return None
    

    def init_pheromones(self):
        #Initialize all roads by adding 1000PL on all roads
        PL_init = 1000
        for r in self.road_list:
            r.PL = PL_init

    
    def evaporate(self):
        # Evaporate the PL level on the roads
        for r in self.road_list:
            r.PL = (1-self.evapo)*r.PL
    
    def add_city(self, name, x, y):
        # The cities must be added first...
        self.city_list.append(City(name, x, y))
        self.city_name_list.append(name)
    
    def add_road(self,city_1,city_2): # From city_1 to city_2
        # Return True if road added False otherwise.
        # Avoid duplicates.

        C1 = self.search_city(city_1)# We get object city_1
        C2 = self.search_city(city_2)# We get object city_2

        if C1 is not None and C2 is not None:
            #Check if road already exists
            for road in C1.edges:
                if road.city_2.name == city_2:
                    return False

            length = m.sqrt((C1.x-C2.x)**2+(C1.y-C2.y)**2)
            R = Road(C1,C2,length)
            self.road_list.append(R)
            C1.edges.append(R)
            return True
        else:
            print("""The cities at the egdes of the road don't exist.
                Please create them first.""")
            return False

    
    def initialize(self):
        self.init_pheromones()
        try:
            self.nest_city = self.search_city(self.nest_city)
            # We replace the string in nest_city with the object nest_city
            self.city_food = self.search_city(self.city_food)
            self.nest_city.nest = True
            self.city_food.food = True
        except:
            print("The nest and/or food city don't exists.")
            return 0
        self.ant_list = [Ant(self.nest_city,self.exploration) for i \
                           in range(self.nb_ants)]
        # We create the ans
    
    def iterate(self):
        # We make all the ants move and we eveaporate the pheromones
        for ant in self.ant_list:
                ant.move_on()
        self.evaporate()
    
    def reset(self):
        # To reset the civilization
        self.city_list = []
        self.city_name_list = []
        self.ant_list = []
        self.road_list = []
        