"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from typing import List
from random import random
from projects.pj02 import constants
from math import sin, cos, pi, sqrt





class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)
    
    def distance(self, location1: Point) -> float:
        """This function measure the distance among cells."""
        x_distance = self.x - location1.x
        y_distance = self.y - location1.y
        dis = sqrt((x_distance ** 2) + (y_distance ** 2))
        return dis
    

class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    sickness: int = 0
    
    def __init__(self, location: Point, direction: Point):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction
      
    def is_infected(self) -> bool:
        """A method that will return True when a cell is infected."""
        if self.sickness == constants.INFECTED or self.sickness > constants.INFECTED:
            return True
        else:
            return False

    def contract_disease(self) -> None:
        """Assign a value to sickness attribute."""
        self.sickness = constants.INFECTED
    
    def immunize(self) -> None:
        """Assign a value to sickness attribute."""
        self.sickness = constants.IMMUNE

    def is_immune(self) -> bool:
        """A method that will return True when a cell is immune."""
        if self.sickness == constants.IMMUNE:
            return True
        else:
            return False
    
    def is_vulnerable(self) -> bool:
        """A method that will return True when a cell is vulnerable."""
        if self.sickness == constants.VULNERABLE:
            return True
        else:
            return False

    def tick(self) -> None:
        """The function counts the Recovery periods."""
        self.location = self.location.add(self.direction)
        if self.is_infected():
            self.sickness += 1
        if self.sickness > constants.RECOVERY_PERIOD:
            self.immunize()
        
    def contact_with(self, other: Cell) -> None:
        """Check if one cell is infected and the other not."""
        if self.is_infected() and other.is_vulnerable():
            other.contract_disease()
        
        if other.is_infected() and self.is_vulnerable():
            self.contract_disease()

    def color(self) -> str:
        """Return the color representation of a cell."""
        if self.is_infected() is True:
            return "red"
        if self.is_vulnerable() is True:
            return "gray"
        if self.is_immune() is True:
            return "yellow"
 
   
class Model:
    """The state of the simulation."""

    population: List[Cell]
    time: int = 0
    
    def __init__(self, cells: int, speed: float, infected: int, immuned: int = 0):
        """Initialize the cells with random locations and directions."""
        self.population = []
        for i in range(0, cells - infected):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            self.population.append(Cell(start_loc, start_dir))
        for i in range(0, infected):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            cell_infected = Cell(start_loc, start_dir)
            cell_infected.contract_disease()
            self.population.append(cell_infected)
        if cells == infected or cells < infected:
            print("there is a Value Error")
            raise ValueError
        elif infected == 0 or infected < 0:
            print("there is a Value Error")
            raise ValueError
        elif infected + immuned > cells:
            print("there is an improper number of cells")
            raise ValueError
        
    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        for cell in self.population:
            cell.tick()
            self.enforce_bounds(cell)
        self.check_contacts()

    def random_location(self) -> Point:
        """Generate a random location."""
        start_x = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        random_angle = pi * 2.0 * random()
        dir_x = cos(random_angle) * speed
        dir_y = sin(random_angle) * speed
        return Point(dir_x, dir_y)

    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if cell.location.x > constants.MAX_X:
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1
        if cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1
        if cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1
        if cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1
        
    def check_contacts(self) -> None:
        """This function will check if cells get contacted."""
        for i in range(len(self.population)):
            cell = self.population[i]

            for j in range(i + 1, len(self.population)):
                other_cell = self.population[j]
                if cell.location.distance(other_cell.location) < constants.CELL_RADIUS:
                    cell.contact_with(other_cell)

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        for cell in self.population:
            if cell.is_infected():
                return False
        return True
