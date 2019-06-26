# Ant Colony Optimization - Find Efficient Path in a Graph

## What is this? 

This is a project to emulate an ant colony. Given a graph containing nodes (cities) and edges (roads) the goal for the ant is to start from the nest city and walk to the food city. 

When the ant reach the food city it drops pheromones on the roads taken to warn the others that is a proper way to reach the food. When the ant reaches the food, it respawn directly at the nest.

Over time, the roads with the most pheromones become the most active. When the food disapear or when the number of ants reaching the food using the roads decrease, the pheromones evaporate and other roads are begining to become more popular.

The ant is parametrized with three variables *alpha*, *beta* and *gamma*. These three parameters decide wether or not the ant is more of an *explorer* or more of a *follower*. We generate the characteristics of the ants randomly.

## Example

Here is an example of how the ant colony behave with a simple graph and two random graphs. The green node is the nest and the orange node is where the food is.

<p align="center">
	<img src="./visualization.gif" />
</p>

## Usage
1. You will need the `tkinter` package for the visualization. Simply install it using `conda install -c anaconda tk` or `pip install tkinter`.

2. Run using `python civilization_sample.py`. You can create your own graphs using the syntax in `civilization_sample.py` or you can generate new random graphs by clicking on the button *new graph*.

Don't hesitate to play with the evaporation rate or the exploration parameter or the number of ants. The efficiency of the path to the food found greatly depends on these parameters.

