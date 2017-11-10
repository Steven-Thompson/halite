"""
Welcome to your first Halite-II bot!

This bot's name is Settler. It's purpose is simple (don't expect it to win complex games :) ):
1. Initialize game
2. If a ship is not docked and there are unowned planets
2.a. Try to Dock in the planet if close enough
2.b If not, go towards the planet

Note: Please do not place print statements here as they are used to communicate with the Halite engine. If you need
to log anything use the logging module.
"""
# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
# Then let's import the logging module so we can print out information
import logging
from random import *

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("stn")
# Then we print our start message to the logs

ship_target = {}

def get_random_unowned_planet(game_map):
    planets = game_map.all_planets()
    unowned = []

    for planet in planets:
        if not planet.is_owned():
            unowned.append(planet.id)

    if len(unowned) == 0:
        return False

    return unowned[randint(0, len(unowned)-1)]


#register a ships target
def set_ship_target(ship, planet):
    ship_target[ship.id] = planet.id

# Delete a ship from the target array
def delete_ship_target(ship):
    if ship.id in ship_target:
        #logging.info(str(ship.id) + " Has been removed")
        ship_target.pop(ship.id)
        l#ogging.info(ship_target)

# If a ship no longer exists remove its target
def dead_ship_remove_target(ships):
    for ship in ship_target:
        logging.info(ship)
        #if ship.id not in ships:
        #    logging.info("This ship has been destroyed!!!!")



def get_random_enemy_planet(game_map):
    planets = game_map.all_planets()
    owned = []

    for planet in planets:
        if planet.owner != 'stn' and planet.is_owned():
            owned.append(planet.id)

    return owned[randint(0, len(owned)-1)]

# check all planets to see if all are owned.
def are_all_planets_owned():
    planets = game_map.all_planets()
    owner_count = 0

    for planet in planets:
        if planet.is_owned():
            owner_count += 1

    # Check is all planets are owned
    if owner_count == len(planets):
        logging.info("All planets have been taken")
        return True
    else:
        return False






# Get a listing of all planets and check if a ship can dock to it
def ship_docking_check(game_map, ship):
    # Store all planets
    all_planets = game_map.all_planets()

    # Go through each planet to see if the ship can dock to it
    for planet in all_planets:
        # Check there is a dockable planet for the ship
        if ship.can_dock(planet):
            # Check the planet can be docked
            if planet.num_docking_spots > dockable_planet(docked_ships(game_map), planet.id):
                return planet
    return False

def docked_ships(game_map):
    docks = {}

    # Every ship i own
    for ship in game_map.get_me().all_ships():
        if ship.docking_status == ship.DockingStatus.DOCKED:
            docks[ship.id] = ship.planet.id

    # Returns {shipid: planetid}
    return docks

# Returns the number of ships docked at a planet
def dockable_planet(docked_ships, planetid):
    # Return the number of ships docked on the planet
    count = 0
    for shipsdocked in docked_ships.values():
        if shipsdocked == planetid:
            count += 1

    return count










while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()

    # Make a record of the ships that have docked with their status.
    docked_ships(game_map)

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []

    # Look for dead ships and remove them from ship target
    dead_ship_remove_target(game_map.get_me().all_ships())


    shipcount = 0
    # For every ship that I control
    for ship in game_map.get_me().all_ships():
        shipcount += 1

        # Some logic to stop game from crashing. Currently cannot manage too many ships.
        if shipcount > 30:
            #logging.info("ship count over 30")
            continue


        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            # This does not count as a ship i can control
            shipcount -= 1
            continue

        # Check if a ship can dock to a planet
        # Check if the planet is at docking capacity
        # If there is a planet and
        if ship_docking_check(game_map, ship):
            command_queue.append(ship.dock(ship_docking_check(game_map, ship)))
            # Once the ship has docked remove it from the target array
            delete_ship_target(ship)
            continue



        # Get random planet unowned planet
        rand = get_random_unowned_planet(game_map)
        rand_planet = game_map.get_planet(rand)

        # If there is a target the continue
        if ship.id in ship_target:
            navigate_command = ship.navigate(ship.closest_point_to(game_map.get_planet(ship_target[ship.id])), game_map, speed=int(hlt.constants.MAX_SPEED), ignore_ships=False)
        elif are_all_planets_owned() == True:
            logging.info("Sending to enemy planet")
            # If all planets are owned command here
            # Get random enemy planet
            # TODO: If all planets are taken. Make all free ships attack the same planet.
            enemy = get_random_enemy_planet(game_map)
            enemy_planet = game_map.get_planet(enemy)
            set_ship_target(ship, enemy_planet)
            navigate_command = ship.navigate(ship.closest_point_to(enemy_planet), game_map, speed=int(hlt.constants.MAX_SPEED), ignore_ships=False)
        else:
            if rand:
                set_ship_target(ship, rand_planet)
                navigate_command = ship.navigate(
                    ship.closest_point_to(rand_planet), game_map, speed=int(hlt.constants.MAX_SPEED / 2), ignore_ships=False)
            else:
                navigate_command = []



        # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
        # or we are trapped (or we reached our destination!), navigate_command will return null;
        # don't fret though, we can run the command again the next turn)
        if navigate_command:
            command_queue.append(navigate_command)









    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
