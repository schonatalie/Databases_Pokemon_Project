"""
Pokemon DB - many-to-many menu program: Pokemon <-> Type (junction: pokemon_type)

"""

import json
import mysql.connector

# ---------------------------------------------------------------------------
# Pokemon table  (PK = pokedexNumber)
P_TABLE = "Pokemon"
P_ID = "pokedexNumber"
P_NAME = "name"
P_STAGE = "evolutionStage"

# Type table  (PK = typeName)
T_TABLE = "Type"
T_NAME = "typeName"
T_COLOR = "color"

# Junction table for "Has Type"
J_TABLE = "PokemonType"
J_P = "pokedexNumber"
J_T = "typeName"
# ---------------------------------------------------------------------------


def get_connection():
    with open("secrets.json", "r") as file:
        config = json.load(file)["mysqlCredentials"]

    return mysql.connector.connect(
        unix_socket="/var/run/mysqld/mysqld.sock",
        user=config["user"],
        password=config["password"],
        database=config["database"],
    )


# ------------------------------ helpers ------------------------------------
def ask_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter a number.")


def pokemon_name(cur, dex):
    cur.execute(f"SELECT {P_NAME} FROM {P_TABLE} WHERE {P_ID} = %s", (dex,))
    row = cur.fetchone()
    return row[0] if row else None


def type_exists(cur, type_name):
    cur.execute(f"SELECT {T_NAME} FROM {T_TABLE} WHERE {T_NAME} = %s", (type_name,))
    row = cur.fetchone()
    return row[0] if row else None  # returns canonical spelling


# ------------------------------ menu actions -------------------------------
# 1) Print Pokemon
def print_pokemon(cur):
    cur.execute(f"SELECT {P_ID}, {P_NAME}, {P_STAGE} FROM {P_TABLE} ORDER BY {P_ID}")
    rows = cur.fetchall()
    print(f"\n{'DEX#':>5}  {'NAME':<20} STAGE")
    print("-" * 40)
    if not rows:
        print("(no results)")
    for dex, name, stage in rows:
        print(f"{dex:>5}  {name:<20} {stage}")
    print()


# 2) Print Types
def print_types(cur):
    cur.execute(f"SELECT {T_NAME}, {T_COLOR} FROM {T_TABLE} ORDER BY {T_NAME}")
    rows = cur.fetchall()
    print(f"\n{'TYPE':<15} COLOR")
    print("-" * 30)
    if not rows:
        print("(no results)")
    for name, color in rows:
        print(f"{name:<15} {color}")
    print()


# 3) Print the types a Pokemon has
def print_types_for_pokemon(cur):
    dex = ask_int("Enter Pokedex number: ")
    name = pokemon_name(cur, dex)
    if name is None:
        print("No Pokemon with that Pokedex number.\n")
        return
    cur.execute(
        f"""
        SELECT t.{T_NAME}, t.{T_COLOR}
        FROM {T_TABLE} t
        JOIN {J_TABLE} j ON j.{J_T} = t.{T_NAME}
        WHERE j.{J_P} = %s
        ORDER BY t.{T_NAME}
        """,
        (dex,),
    )
    rows = cur.fetchall()
    print(f"\nTypes of #{dex} {name}")
    print("-" * 30)
    if not rows:
        print("(no types)")
    for tname, color in rows:
        print(f"{tname:<15} {color}")
    print()


# 4) Print the Pokemon of a type
def print_pokemon_of_type(cur):
    tname = type_exists(cur, input("Enter type name: ").strip())
    if tname is None:
        print("No such type.\n")
        return
    cur.execute(
        f"""
        SELECT p.{P_ID}, p.{P_NAME}
        FROM {P_TABLE} p
        JOIN {J_TABLE} j ON j.{J_P} = p.{P_ID}
        WHERE j.{J_T} = %s
        ORDER BY p.{P_ID}
        """,
        (tname,),
    )
    rows = cur.fetchall()
    print(f"\nPokemon with type {tname}")
    print("-" * 30)
    if not rows:
        print("(no results)")
    for dex, name in rows:
        print(f"{dex:>5}  {name}")
    print()


# 5) Add a type to a Pokemon
def add_type_to_pokemon(conn, cur):
    dex = ask_int("Enter Pokedex number: ")
    name = pokemon_name(cur, dex)
    if name is None:
        print("No Pokemon with that Pokedex number.\n")
        return
    tname = type_exists(cur, input("Enter type name to add: ").strip())
    if tname is None:
        print("No such type.\n")
        return
    cur.execute(
        f"SELECT 1 FROM {J_TABLE} WHERE {J_P} = %s AND {J_T} = %s", (dex, tname)
    )
    if cur.fetchone():
        print(f"{name} already has type {tname}.\n")
        return
    cur.execute(
        f"INSERT INTO {J_TABLE} ({J_P}, {J_T}) VALUES (%s, %s)", (dex, tname)
    )
    conn.commit()
    print(f"Added type {tname} to {name}.\n")


# 6) Remove a type from a Pokemon
def remove_type_from_pokemon(conn, cur):
    dex = ask_int("Enter Pokedex number: ")
    name = pokemon_name(cur, dex)
    if name is None:
        print("No Pokemon with that Pokedex number.\n")
        return
    tname = input("Enter type name to remove: ").strip()
    cur.execute(
        f"DELETE FROM {J_TABLE} WHERE {J_P} = %s AND {J_T} = %s", (dex, tname)
    )
    conn.commit()
    if cur.rowcount:
        print(f"Removed type {tname} from {name}.\n")
    else:
        print(f"{name} doesn't have type '{tname}' - nothing removed.\n")


MENU = """\
===== Pokemon / Type Menu =====
1) Print Pokemon
2) Print Types
3) Print Types a Pokemon has
4) Print Pokemon of a Type
5) Add a Type to a Pokemon
6) Remove a Type from a Pokemon
q) Quit
"""


def main():
    conn = get_connection()
    cur = conn.cursor()
    try:
        while True:
            print(MENU)
            choice = input("Choice: ").strip().lower()
            if choice == "1":
                print_pokemon(cur)
            elif choice == "2":
                print_types(cur)
            elif choice == "3":
                print_types_for_pokemon(cur)
            elif choice == "4":
                print_pokemon_of_type(cur)
            elif choice == "5":
                add_type_to_pokemon(conn, cur)
            elif choice == "6":
                remove_type_from_pokemon(conn, cur)
            elif choice == "q":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.\n")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
