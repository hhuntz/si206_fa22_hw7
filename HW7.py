
# Your name:
# Your student id:
# Your email:
# List who you have worked with on this project:

import unittest
import sqlite3
import json
import os

def read_data(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def make_types_table(data, cur, conn):
    type_list = []
    for pokemon in data:
        pokemon_type = pokemon['type'][0]
        if pokemon_type not in type_list:
            type_list.append(pokemon_type)
    cur.execute("CREATE TABLE IF NOT EXISTS Types (id INTEGER PRIMARY KEY, type TEXT UNIQUE)")
    for i in range(len(type_list)):
        cur.execute("INSERT OR IGNORE INTO Types (id,type) VALUES (?,?)",(i,type_list[i]))
    conn.commit()

## [TASK 1]: 25 points
# Finish the function make_pokemon_table

    # This function takes 3 arguments: JSON data,
        # the database cursor, and the database connection object

    # It iterates through the JSON data to get a list of pokemon
    # and loads all of the pokemon into a database table called 'Pokemon', 
    # with the following columns:
        # name (datatype: text; Primary key)
        # type_id (datatype: integer)
        # HP (datatype: integer)
        # attack (datatype: integer)
        # defense (datatype: integer)
        # speed (datatype: integer)
    # To find the type_id for each pokemon, you will have to look up 
    # the first type of each pokemon in the types table we 
    # create for you -- see make_types_table above for details.

def make_pokemon_table(data, cur, conn):
    pass

## [TASK 2]: 10 points
# Finish the function hp_search

    # This function takes 3 arguments as input: an HP integer
    # the database cursor, and database connection object. 
 
    # It selects all the pokemon of a particular HP 
    # and returns a list of tuples. Each tuple contains:
        # the pokemon name, its type_id, and its HP.

def hp_search(hp, cur, conn):
    pass

## [TASK 3]: 10 points
# finish the function hp_speed_attack_search

    # This function takes 5 arguments as input: an HP integer,
    # a speed integer, an attack integer, the database cursor, 
    # and the database connection object.

    # It selects all the pokemon at the HP passed to the function 
    # that have a speed greater than the speed rating passed to the function
    # and at an attack greater than the attack rating passed to the function. 
    # This function returns a list of tuples each containing 
    # the pokemon’s name, speed, attack, and defense.


def hp_speed_attack_search(hp, speed, attack, cur, conn):
    pass

## [TASK 4]: 15 points
# finish the function type_speed_defense_search

    # This function takes 5 arguments as input: a type string, 
    # a defense integer, a speed integer, the database cursor,
    # and the database connection object. 

    # It selects all pokemon of the passed type 
    # that have speed greater than the passed speed
    # and defense greater than the passed defense.
    # It returns a list of tuples, each containing the
    # pokemon name, type, speed, and defense.
    # HINT: You'll have to use JOIN for this task.

def type_speed_defense_search(type, speed, defense, cur, conn):
    pass


# [EXTRA CREDIT]
# You’ll make 2 new functions, make_bilingual_table() and bilingual_type_search(), 
# and then write at least 2 meaningful test cases for each of them. 

    # The first function takes 3 arguments: JSON data, 
    # the database cursor, and the database connection object. 
    # It iterates through the JSON data to get a list of pokemon 
    # and loads all of the pokemon into a database table 
    # called ‘Bilingual_Pokemon' with the following columns:
        # english_name (datatype: text; Primary key)
        # french_name (datatype: text)
        # type_id (datatype: integer)
        # hp (datatype: integer)

    # To find the type_id for each pokemon, you will have to 
    # look up the first type of each pokemon in the types table 
    # we create for you -- see make_types_table above for details. 
    
    # The second function takes in a type string, the database cursor, 
    # and the database connection object. It selects all the pokemon 
    # of the given type that have the same name in French and English. 
    # It returns a list of tuples, each with a pokemon’s name, type, and hp. 

def make_bilingual_table(json, cur, conn):
    pass

def bilingual_type_search(type, cur, conn):
    pass


class TestAllMethods(unittest.TestCase):
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(path+'/'+'pokemon.db')
        self.cur = self.conn.cursor()
        self.data = read_data('pokemon.txt')
        self.conn2 = sqlite3.connect(path+'/'+'bilingual_pokemon.db')
        self.cur2 = self.conn2.cursor()

    def test_pokemon_table(self):
        self.cur.execute('SELECT * from Pokemon')
        pokemon_list = self.cur.fetchall()

        self.assertEqual(len(pokemon_list), 106)
        self.assertEqual(len(pokemon_list[0]),6)
        self.assertIs(type(pokemon_list[0][0]), str)
        self.assertIs(type(pokemon_list[0][1]), int)
        self.assertIs(type(pokemon_list[0][2]), int)
        self.assertIs(type(pokemon_list[0][3]), int)
        self.assertIs(type(pokemon_list[0][4]), int)
        self.assertIs(type(pokemon_list[0][5]), int)

    def test_hp_search(self):
        x = sorted(hp_search(50, self.cur, self.conn))
        self.assertEqual(len(x), 8)
        self.assertEqual(len(x[0]), 3)
        self.assertEqual(x[0][0], "Cloyster")

        y = sorted(hp_search(30, self.cur, self.conn))
        self.assertEqual(len(y), 6)
        self.assertEqual(y[2],('Krabby', 2, 30))
        self.assertEqual(y[4][2], 30)
        self.assertEqual(y[5][1], 2)

        z = sorted(hp_search(105, self.cur, self.conn))
        self.assertEqual(len(z) ,3)
        self.assertEqual(z[0][0], "Kangaskhan")
        self.assertEqual(z[2][2], 105)
        self.assertEqual(len(hp_search(20, self.cur, self.conn)), 0)

    def test_hp_speed_attack_search(self):

        a = hp_speed_attack_search(60, 30, 85, self.cur, self.conn)
        self.assertEqual(len(a), 4)
        self.assertEqual(a[0][1], 80)
        self.assertEqual(a[3][2], 105)
        self.assertEqual(len(a[1]), 4)

        self.assertEqual(len(hp_speed_attack_search(70, 40, 85, self.cur, self.conn)), 0)

    def test_type_speed_defense_search(self):
 
        b = sorted(type_speed_defense_search("Fire", 60, 60, self.cur, self.conn))
        self.assertEqual(len(b), 2)
        self.assertEqual(type(b[0][0]), str)
        self.assertEqual(type(b[1][1]), str)
        self.assertEqual(len(b[1]), 4) 
        self.assertEqual(b[1], ('Ninetales', 'Fire', 100, 75)) 

        c = sorted(type_speed_defense_search("Grass", 60, 70, self.cur, self.conn))
        self.assertEqual(len(c), 1)
        self.assertEqual(c, [('Venusaur', 'Grass', 80, 83)])
    
    # test extra credit
    def test_make_bilingual_table(self):
        pass

    def test_bilingual_type_search(self):
        pass


def main():
    json_data = read_data('pokemon.txt')
    cur, conn = open_database('pokemon.db')
    make_types_table(json_data, cur, conn)

    make_pokemon_table(json_data, cur, conn)

    #### FEEL FREE TO USE THIS SPACE TO TEST OUT YOUR FUNCTIONS

    conn.close()


if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
