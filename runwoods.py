""" CS 5001 -Yijia Zhan - project 10
This module defines a camping simulation application using Pyglet. It includes
classes for configuring the woods, creating a graphical user interface (GUI)
for setting up the simulation parameters, and implementing the main simulation.
"""
# import modules
import random
import datetime

import pyglet
import pyglet_colors
from woodconfig import WoodConfig

import jsonpickle


# CONSTANTS
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_MARGIN = 50
TREE_SIZE_MIN = 100
TREE_SIZE_MAX = 200
ADULT_SIZE = 30
BABY_SIZE = 15
FLYER_SIZE = 1
BABY_DX_MIN = -40
BABY_DX_MAX = 40
BABY_DY_MIN = -30
BABY_DY_MAX = 15
PAPA_DX = 35
PAPA_DY = -20
MOVE_LIMIT = 30
FLY_WAIT_MIN = 2
FLY_WAIT_MAX = 6

# GLOBAL VARIABLES
the_wood = None
scene_paused = False
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)


@window.event
def on_draw():
    """ Draw event for Pyglet - clear the window and draw stuff
    """
    window.clear()
    if the_wood is not None:
        the_wood.draw()


def update(dt):
    """
    Update function called by Pyglet at regular intervals.

    Args:
        dt (float): The time elapsed since the last update.
    """
    if (not scene_paused) and (the_wood is not None):
        the_wood.move()


@window.event
def on_key_press(symbol, modifiers):
    """This is called by Pyglet when a key is pressed
    Args:
        symbol (pyglet.window.key): The key that is pressed
        modifiers (pyglet.window.key): Modifiers but I don't think they work
    """
    global scene_paused
    if symbol == pyglet.window.key.SPACE:
        scene_paused = not scene_paused


class ClickHandler:
    """Handles mouse click events."""
    def __init__(self):
        pass

    def handle_click(self, x, y):
        """Handle the mouse click event."""
        # Print out the x,y coordinate when click the window
        print(f"Mouse clicked at ({x}, {y})")


click_handler = ClickHandler()


@window.event
def on_mouse_press(x, y, button, modifiers):
    """This is called by Pyglet when a mouse button is pressed.

    Args:
        x (int): The x-coordinate of the mouse click.
        y (int): The y-coordinate of the mouse click.
        button (int): The button that was pressed.
        modifiers (int): The modifier keys that were pressed.
    """
    click_handler.handle_click(x, y)


def load_config():
    """ Load the woods configuration from a JSON file

    Returns:
        WoodConfig: The wood configuration object loaded from the file,
        or a default configuration if the file is not found.
    """

    try:
        with open('woodconfig.json', 'r') as config_file:
            config_json = config_file.read()
            wood_config = jsonpickle.decode(config_json)
        return wood_config
    except FileNotFoundError:
        print("Config file not found. Using default configuration.")
        return WoodConfig()


wood_config = load_config()


class Wood:
    """Represent a wood
    """
    def __init__(self):
        """
        Initializes a new instance of the wood class.
        """
        self.tree_list = []
        for _ in range(random.randint(wood_config.tree_min, wood_config.
                                      tree_max)):
            tree = Tree(random.randrange(WINDOW_MARGIN,
                                         WINDOW_WIDTH-WINDOW_MARGIN),
                        random.randrange(WINDOW_MARGIN,
                                         WINDOW_HEIGHT-WINDOW_MARGIN),
                        random.randrange(TREE_SIZE_MIN, TREE_SIZE_MAX))
            self.tree_list.append(tree)

    def populate(self):
        """
        Populate the wood with animal groups.
        """
        self.animal_group_list = []
        family1 = Family(random.randrange(WINDOW_MARGIN,
                                          WINDOW_WIDTH-WINDOW_MARGIN),
                         random.randrange(WINDOW_MARGIN,
                                          WINDOW_HEIGHT-WINDOW_MARGIN),
                         Bear)
        self.animal_group_list.append(family1)
        family2 = Family(random.randrange(WINDOW_MARGIN,
                                          WINDOW_WIDTH-WINDOW_MARGIN),
                         random.randrange(WINDOW_MARGIN,
                                          WINDOW_HEIGHT-WINDOW_MARGIN),
                         Pig)
        self.animal_group_list.append(family2)
        family3 = Flock(Bird)
        self.animal_group_list.append(family3)
        family4 = Family(random.randrange(WINDOW_MARGIN,
                                          WINDOW_WIDTH-WINDOW_MARGIN),
                         random.randrange(WINDOW_MARGIN,
                                          WINDOW_HEIGHT-WINDOW_MARGIN),
                         Mouse)
        self.animal_group_list.append(family4)

    def draw(self):
        """
        Draw the trees and animal groups in the woods.
        """
        for tree in self.tree_list:
            tree.draw()
        for family in self.animal_group_list:
            family.draw()

    def move(self):
        """
        Move the animal groups in the woods.
        """
        for family in self.animal_group_list:
            family.move()

    def random_tree(self):
        """
        Get a random tree from the woods.

        Returns:
            Tree: A randomly selected tree from the woods.
        """
        return random.choice(self.tree_list)


class Tree:
    """ One tree in the woods
    """
    def __init__(self, x, y, size):
        """ create one tree
        Args:
            x (int): The x-coordinate of the tree.
            y (int): The y-coordinate of the tree.
            size (int): The size of the tree.
        """
        self.x = x
        self.y = y
        self.size = size
        self.shape_list = []
        self.batch = pyglet.shapes.Batch()
        trunk1 = pyglet.shapes.Rectangle(x-(size//40), y, size*0.05, size*0.2,
                                         pyglet_colors.BROWN, batch=self.batch)
        self.shape_list.append(trunk1)
        bottom_branches = pyglet.shapes.Triangle(x, y+(size*0.7),
                                                 x-(size*0.25), y+(size*0.2),
                                                 x+(size*0.25), y+(size*0.2),
                                                 color=pyglet_colors.GREEN,
                                                 batch=self.batch)
        self.shape_list.append(bottom_branches)
        middle_branches = pyglet.shapes.Triangle(x, y+(size*0.8),
                                                 x-(size*0.2), y+(size*0.4),
                                                 x+(size*0.2), y+(size*0.4),
                                                 color=pyglet_colors.GREEN,
                                                 batch=self.batch)
        self.shape_list.append(middle_branches)
        top_branches = pyglet.shapes.Triangle(x, y+size,
                                              x-(size*0.15), y+(size*0.6),
                                              x+(size*0.15), y+(size*0.6),
                                              color=pyglet_colors.GREEN,
                                              batch=self.batch)
        self.shape_list.append(top_branches)

    def draw(self):
        """Draw the tree using Pyglet's batch drawing."""

        self.batch.draw()

    def perch_x(self):
        """Get a random x-coordinate for an animal to perch on the tree.

        Returns:
            int: A random x-coordinate within the permissible range
        """
        return random.randrange(int(self.x-(self.size*0.15)),
                                int(self.x+(self.size*0.15)))

    def perch_y(self):
        """Get a random y-coordinate for an animal to perch on the tree.

        Returns:
            int: A random y-coordinate within the permissible range
        """
        return random.randrange(int(self.y+(self.size*0.25)),
                                int(self.y+(self.size*0.8)))


class AnimalGroup:
    """ This is an interface for Family and Flock to show
    the methods they have in common
    """
    def move(self):
        """move the entire animal group
        """
        pass

    def draw(self):
        """draw the entire animal group"""
        pass


class Family(AnimalGroup):
    """Represents a family of animals in the woods

    Args:
        AnimalGroup (superclass): Family inherits from AnimalGroup
    """
    def __init__(self, x, y, animal_class):
        """Initialize a family with a mama, papa, and baby animals.


        Args:
            x (int): X-coordinate of the family.
            y (int): Y-coordinate of the family.
            animal_class (class): The type of animal in the family.
        """
        self.x = x
        self.y = y
        self.dx = random.randrange(-MOVE_LIMIT, MOVE_LIMIT)
        self.dy = random.randrange(-MOVE_LIMIT, MOVE_LIMIT)
        self.animal_list = []
        self.mama = animal_class(x, y, ADULT_SIZE)
        self.animal_list.append(self.mama)
        self.baby_list = []
        for _ in range(random.randint(wood_config.baby_min,
                                      wood_config.baby_max)):
            baby = animal_class(x+random.randrange(BABY_DX_MIN, BABY_DX_MAX),
                                y+random.randrange(BABY_DY_MIN, BABY_DY_MAX),
                                BABY_SIZE)
            self.animal_list.append(baby)
            self.baby_list.append(baby)
        self.papa = animal_class(x+PAPA_DX, y+PAPA_DY, ADULT_SIZE)
        self.animal_list.append(self.papa)

    def draw(self):
        """Draw the entire family."""
        for animal in self.animal_list:
            animal.draw()

    def move(self):
        """Move the entire family."""
        self.x += self.dx
        self.y += self.dy
        if self.x < 0:
            self.x = -self.x
            self.dx = random.randrange(10, MOVE_LIMIT)
        elif self.x > window.width:
            self.x = (2 * window.width) - self.x
            self.dx = random.randrange(-MOVE_LIMIT, -10)
        if self.y < 0:
            self.y = -self.y
            self.dy = random.randrange(10, MOVE_LIMIT)
        elif self.y > window.height:
            self.y = (2 * window.height) - self.y
            self.dy = random.randrange(-MOVE_LIMIT, -10)
        self.mama.move(self.x, self.y)
        for baby in self.baby_list:
            baby.move(self.x+random.randrange(BABY_DX_MIN, BABY_DX_MAX),
                      self.y+random.randrange(BABY_DY_MIN, BABY_DY_MAX))
        self.papa.move(self.x+PAPA_DX, self.y+PAPA_DY)


class Animal:
    """Represent an animal in the woods
    """
    def __init__(self, x, y):
        """Initiate an animal in the woods

        Args:
        x (int): X-coordinate of the animal
        y (int): Y-coordinate of the animal
        """
        self.x = x
        self.y = y
        self.batch = pyglet.shapes.Batch()
        self.shape_list = []

    def draw(self):
        """Draw the animal."""
        self.batch.draw()

    def move(self, x, y):
        """Move the animal to the specified coordinates.

        Args:
            x (int): x-coordinate to move to
            y (int): y-coordinate to move to
        """
        dx = x - self.x
        dy = y - self.y
        for shape in self.shape_list:
            shape.x += dx
            shape.y += dy
        self.x = x
        self.y = y


class Mouse(Animal):
    """Represnt a mouse
    Args:
        Animal (class): Superclass from which mouse inherits
    """
    def __init__(self, x, y, size):
        """Initialize a mouse.

        Args:
            x (int): X-coordinate of the mouse.
            y (int): Y-coordinate of the mouse.
            size (int): Size of the mouse.
        """
        super().__init__(x, y)

        ear_radius = 0.5 * size
        face = pyglet.shapes.Circle(x, y, size,
                                    color=pyglet_colors.PINK,
                                    batch=self.batch)
        self.shape_list.append(face)
        ear1 = pyglet.shapes.Circle(x + size, y + size, ear_radius,
                                    color=pyglet_colors.PINK,
                                    batch=self.batch)
        self.shape_list.append(ear1)
        ear2 = pyglet.shapes.Circle(x - size, y + size,
                                    ear_radius, color=pyglet_colors.PINK,
                                    batch=self.batch)
        self.shape_list.append(ear2)

        eye1 = pyglet.shapes.Circle(x+(0.4*size), y, 0.16*size,
                                    color=pyglet_colors.BLACK,
                                    batch=self.batch)
        self.shape_list.append(eye1)

        eye2 = pyglet.shapes.Circle(x-(0.4*size), y, 0.16*size,
                                    color=pyglet_colors.BLACK,
                                    batch=self.batch)
        self.shape_list.append(eye2)


class Bear(Animal):
    """Represnt a bear
    Args:
        Animal (class): Superclass from which Bear inherits
    """
    def __init__(self, x, y, size):
        """Initialize a bear.

        Args:
            x (int): X-coordinate of the bear.
            y (int): Y-coordinate of the bear.
            size (int): Size of the bear.
        """
        super().__init__(x, y)

        face = pyglet.shapes.Circle(x, y, size, color=pyglet_colors.BROWN,
                                    batch=self.batch)
        self.shape_list.append(face)

        ear1 = pyglet.shapes.Circle(x+(0.6*size), y+size, 0.4*size,
                                    color=pyglet_colors.BROWN,
                                    batch=self.batch)
        self.shape_list.append(ear1)
        ear2 = pyglet.shapes.Circle(x-(0.6*size), y+size, 0.4*size,
                                    color=pyglet_colors.BROWN,
                                    batch=self.batch)
        self.shape_list.append(ear2)

        eye1 = pyglet.shapes.Circle(x+(0.4*size), y, 0.16*size,
                                    color=pyglet_colors.BLACK,
                                    batch=self.batch)
        self.shape_list.append(eye1)

        eye2 = pyglet.shapes.Circle(x-(0.4*size), y, 0.16*size,
                                    color=pyglet_colors.BLACK,
                                    batch=self.batch)
        self.shape_list.append(eye2)


class Pig(Animal):
    """Represent a pig.

    Args:
        Animal (class): Superclass from which Pig inherits.
    """
    def __init__(self, x, y, size):
        """Initialize a pig.

        Args:
            x (int): X-coordinate of the pig.
            y (int): Y-coordinate of the pig.
            size (int): Size of the pig.
        """
        super().__init__(x, y)
        face = pyglet.shapes.Circle(x, y, size,
                                    color=pyglet_colors.CHOCOLATE1,
                                    batch=self.batch)
        self.shape_list.append(face)
        ear1 = pyglet.shapes.Ellipse(x+(0.6*size), y+size, 0.4*size,
                                     0.5*size, color=pyglet_colors.CHOCOLATE1,
                                     batch=self.batch)
        self.shape_list.append(ear1)
        ear2 = pyglet.shapes.Ellipse(x-(0.6*size), y+size, 0.4*size,
                                     0.5*size, color=pyglet_colors.CHOCOLATE1,
                                     batch=self.batch)
        self.shape_list.append(ear2)
        eye1 = pyglet.shapes.Circle(x+(0.40*size), y, 0.16*size,
                                    color=pyglet_colors.BLACK,
                                    batch=self.batch)
        self.shape_list.append(eye1)
        eye2 = pyglet.shapes.Circle(x-(0.40*size), y, 0.16*size,
                                    color=pyglet_colors.BLACK,
                                    batch=self.batch)
        self.shape_list.append(eye2)


class Flock(AnimalGroup):
    """Represents a flock of birds in the woods.

    Args:
        AnimalGroup (class): An interface for common methods.
    """
    def __init__(self, flyer_class):
        """Initialize a flock with a list of bird flyers.

        Args:
            flyer_class (class): The type of bird in the flock.
        """
        self.flyer_list = []
        for _ in range(random.randint(wood_config.bird_min,
                                      wood_config.bird_max)):
            tree = the_wood.random_tree()
            flyer = flyer_class(tree.perch_x(), tree.perch_y(), FLYER_SIZE)
            self.flyer_list.append(flyer)

    def draw(self):
        """Draw the entire flock of birds."""
        for flyer in self.flyer_list:
            flyer.draw()

    def move(self):
        """Move the entire flock of birds to random tree perches."""
        for flyer in self.flyer_list:
            tree = the_wood.random_tree()
            flyer.move(tree.perch_x(), tree.perch_y())


class Bird(Animal):
    """Represent a bird

    Args:
        Animal (class): Superclass from which Bird inherits
    """
    def __init__(self, x, y, size):
        """Initialize a bird.

        Args:
            x (int): X-coordinate of the bird.
            y (int): Y-coordinate of the bird.
            size (int): Size of the bird.
        """
        super().__init__(x, y)
        self.last_moved = datetime.datetime.now()

        body = pyglet.shapes.Circle(x, y, 18 * size,
                                    color=pyglet_colors.WHITE,
                                    batch=self.batch)
        self.shape_list.append(body)
        beak = pyglet.shapes.Triangle(x, y - (8 * size), x + (12 * size), y,
                                      x, y + (8 * size),
                                      color=pyglet_colors.ORANGE,
                                      batch=self.batch)
        self.shape_list.append(beak)
        eye1 = pyglet.shapes.Circle(x - (4 * size), y + (4 * size),
                                    4 * size, color=pyglet_colors.BLACK,
                                    batch=self.batch)
        self.shape_list.append(eye1)
        eye2 = pyglet.shapes.Circle(x + (4 * size), y + (4 * size),
                                    4 * size, color=pyglet_colors.BLACK,
                                    batch=self.batch)
        self.shape_list.append(eye2)

    def move(self, x, y):
        """Move the bird to the specified coordinates.

        Args:
            x (int): X-coordinate to move to.
            y (int): Y-coordinate to move to.
        """
        if (datetime.datetime.now() - self.last_moved).seconds >= \
                random.randrange(FLY_WAIT_MIN, FLY_WAIT_MAX):
            super().move(x, y)
            self.last_moved = datetime.datetime.now()


class App:
    """ Application class
    """
    def __init__(self):
        """ Initiate the application
        """
        self.paused = False
        self.click_handler = ClickHandler()

    def toggle_pause(self):
        """ Toggle the pause state of the application"""
        self.paused = not self.paused

    def run(self):
        """ Run the application
        """
        global the_wood
        the_wood = Wood()
        the_wood.populate()
        pyglet.clock.schedule_interval(update, 1 / wood_config.move_interval)
        pyglet.app.run()


if __name__ == "__main__":
    app = App()
    app.run()
