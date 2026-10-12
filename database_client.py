
import json
import mysql.connector



def connect_to_database():
    with open("secrets.json", "r") as file:
        config = json.load(file)["mysqlCredentials"]

    return mysql.connector.connect(
        unix_socket="/var/run/mysqld/mysqld.sock",
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )



def display_pokemon(cursor):
    cursor.execute(
        "SELECT pokedexNumber, name, evolutionStage "
        "FROM Pokemon ORDER BY pokedexNumber"
    )

    rows = cursor.fetchall()

    if not rows:
        print("The Pokemon table is empty.")
        return

    print("\n--- Pokemon Table ---")
    print(f"{'Number':<10} {'Name':<20} {'Evolution Stage'}")
    print("-" * 50)

    for number, name, stage in rows:
        print(f"{number:<10} {name:<20} {stage or 'N/A'}")


def insert_pokemon(cursor, connection):
    try:
        number = int(input("Enter Pokedex number: "))
        name = input("Enter Pokemon name: ").strip()
        stage = input("Enter evolution stage (or leave blank): ").strip()

        if not name:
            print("Name cannot be empty.")
            return

        cursor.execute(
            "INSERT INTO Pokemon "
            "(pokedexNumber, name, evolutionStage) "
            "VALUES (%s, %s, %s)",
            (number, name, stage or None)
        )

        connection.commit()
        print("Pokemon added successfully!")

    except ValueError:
        print("Pokedex number must be an integer.")
    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Database error: {err}")


def update_pokemon(cursor, connection):
    try:
        number = int(input("Enter Pokedex number to update: "))

        cursor.execute(
            "SELECT name, evolutionStage FROM Pokemon "
            "WHERE pokedexNumber = %s",
            (number,)
        )
        existing = cursor.fetchone()

        if existing is None:
            print("Pokemon not found.")
            return

        print(f"Current name: {existing[0]}")
        print(f"Current evolution stage: {existing[1] or 'N/A'}")

        name = input("Enter new name: ").strip()
        stage = input("Enter new evolution stage (or leave blank): ").strip()

        if not name:
            print("Name cannot be empty.")
            return

        cursor.execute(
            "UPDATE Pokemon SET name = %s, evolutionStage = %s "
            "WHERE pokedexNumber = %s",
            (name, stage or None, number)
        )

        connection.commit()
        print("Pokemon updated successfully!")

    except ValueError:
        print("Pokedex number must be an integer.")
    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Database error: {err}")


def delete_pokemon(cursor, connection):
    try:
        number = int(input("Enter Pokedex number to delete: "))

        cursor.execute(
            "SELECT name FROM Pokemon WHERE pokedexNumber = %s",
            (number,)
        )
        existing = cursor.fetchone()

        if existing is None:
            print("Pokemon not found.")
            return

        confirm = input(
            f"Delete {existing[0]}? Type y to confirm: "
        ).strip().lower()

        if confirm != "y":
            print("Deletion cancelled.")
            return

        cursor.execute(
            "DELETE FROM Pokemon WHERE pokedexNumber = %s",
            (number,)
        )

        connection.commit()
        print("Pokemon deleted successfully!")

    except ValueError:
        print("Pokedex number must be an integer.")
    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Database error: {err}")


def main():
    connection = None
    cursor = None

    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        print("Connected to database successfully!")

        while True:
            print("\n=== Pokemon Database Menu ===")
            print("1) Display contents of table")
            print("2) Insert new row to table")
            print("3) Update a row of the table")
            print("4) Delete a row of the table")
            print("q) Quit")

            choice = input("Select an option: ").strip().lower()

            if choice == "1":
                display_pokemon(cursor)
            elif choice == "2":
                insert_pokemon(cursor, connection)
            elif choice == "3":
                update_pokemon(cursor, connection)
            elif choice == "4":
                delete_pokemon(cursor, connection)
            elif choice == "q":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Try again.")

    except (mysql.connector.Error, OSError, KeyError, ValueError) as err:
        print(f"Error: {err}")

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
