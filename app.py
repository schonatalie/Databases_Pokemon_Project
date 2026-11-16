from flask import Flask, render_template, request, redirect, url_for
from database_client import connect_to_database
import mysql.connector

app = Flask(__name__, template_folder="webpage")


def get_pokemon():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                p.pokedexNumber,
                p.name,
                p.evolutionStage,
                GROUP_CONCAT(
                    pt.typeName ORDER BY pt.typeName SEPARATOR ', '
                ) AS pokemonType
            FROM Pokemon p
            LEFT JOIN PokemonType pt
                ON p.pokedexNumber = pt.pokedexNumber
            GROUP BY
                p.pokedexNumber,
                p.name,
                p.evolutionStage
            ORDER BY p.pokedexNumber
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


@app.route("/", methods=["GET", "POST"])
def pokemon():

    message = request.args.get("message")

    if request.method == "POST":

        number = request.form.get("number", "").strip()
        name = request.form.get("name", "").strip()
        stage = request.form.get("stage", "").strip()

        if not number.isdigit() or not name:
            message = "Please enter a valid Pokedex number and name."

        elif int(number) > 1100 or int(number) < 1:
            message = "Pokedex number must be between 1 and 1100."

        elif len(name) > 50 or len(stage) > 30:
            message = "Name or evolution stage is too long."

        else:
            conn = connect_to_database()
            cursor = conn.cursor()

            try:
                cursor.execute("""
                    INSERT INTO Pokemon
                    (pokedexNumber, name, evolutionStage)
                    VALUES (%s, %s, %s)
                """, (int(number), name, stage or None))

                conn.commit()
                return redirect(url_for("pokemon"))

            except mysql.connector.Error as err:
                conn.rollback()
                message = "Database error: " + str(err)

            finally:
                cursor.close()
                conn.close()

    pokemon_list = get_pokemon()

    return render_template(
        "pokemon.html",
        pokemon=pokemon_list,
        message=message
    )


#UPDATE
@app.route("/edit/<int:number>", methods=["GET", "POST"])
def edit_pokemon(number):

    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM Pokemon WHERE pokedexNumber = %s",
            (number,)
        )
        existing = cursor.fetchone()

        if existing is None:
            return redirect(url_for(
                "pokemon",
                message="Pokemon not found."
            ))

        if request.method == "POST":

            new_number = request.form.get("number", "").strip()
            name = request.form.get("name", "").strip()
            stage = request.form.get("stage", "").strip()

            if not new_number.isdigit() or int(new_number) < 1:
                return render_template(
                    "edit_pokemon.html",
                    pokemon=existing,
                    message="Please enter a valid Pokedex number."
                )

            new_number = int(new_number)

            if not name:
                return render_template(
                    "edit_pokemon.html",
                    pokemon=existing,
                    message="Name cannot be empty."
                )

            if len(name) > 50 or len(stage) > 30:
                return render_template(
                    "edit_pokemon.html",
                    pokemon=existing,
                    message="Name or evolution stage is too long."
                )

            if new_number == number:
                # Only update the name and evolution stage.
                cursor.execute("""
                    UPDATE Pokemon
                    SET name = %s, evolutionStage = %s
                    WHERE pokedexNumber = %s
                """, (name, stage or None, number))

            else:
                # Create the new Pokemon row first so foreign keys
                # can be moved to the new Pokedex number.
                cursor.execute("""
                    INSERT INTO Pokemon
                    (pokedexNumber, name, evolutionStage)
                    VALUES (%s, %s, %s)
                """, (new_number, name, stage or None))

                # Update cards associated with this Pokemon.
                cursor.execute("""
                    UPDATE Card
                    SET pokedexNumber = %s
                    WHERE pokedexNumber = %s
                """, (new_number, number))

                # Update the Pokemon's associated types.
                cursor.execute("""
                    UPDATE PokemonType
                    SET pokedexNumber = %s
                    WHERE pokedexNumber = %s
                """, (new_number, number))

                # Delete the old Pokemon row.
                cursor.execute("""
                    DELETE FROM Pokemon
                    WHERE pokedexNumber = %s
                """, (number,))

            conn.commit()

            return redirect(url_for(
                "pokemon",
                message="Pokemon updated successfully!"
            ))

        return render_template(
            "edit_pokemon.html",
            pokemon=existing
        )

    except mysql.connector.Error as err:
        conn.rollback()

        return render_template(
            "edit_pokemon.html",
            pokemon=existing,
            message="Database error: " + str(err)
        )

    finally:
        cursor.close()
        conn.close() 

#DELETE
@app.route("/delete/<int:number>", methods=["POST"])
def delete_pokemon(number):

    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        #check whether any cards reference this Pokemon
        cursor.execute(
            "SELECT COUNT(*) FROM Card WHERE pokedexNumber = %s",
            (number,)
        )

        card_count = cursor.fetchone()[0]

        if card_count > 0:
            return redirect(url_for(
                "pokemon",
                message="Cannot delete this Pokemon because cards reference it."
            ))

        #delete associated PokemonType entries first
        cursor.execute(
            "DELETE FROM PokemonType WHERE pokedexNumber = %s",
            (number,)
        )

        #delete the Pokemon
        cursor.execute(
            "DELETE FROM Pokemon WHERE pokedexNumber = %s",
            (number,)
        )

        if cursor.rowcount == 0:
            conn.rollback()
            message = "Pokemon not found."
        else:
            conn.commit()
            message = "Pokemon deleted successfully!"

    except mysql.connector.Error as err:
        conn.rollback()
        message = "Database error: " + str(err)

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("pokemon", message=message))


#MANY-TO-MANY CODE -- Pokemon to Type

def run_query(sql, params=()):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(sql, params)
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def add_pokemon_type(dex, type_name):
    if not dex or not type_name:
        return False, "Please make a choice from the list."

    already = run_query(
        "SELECT 1 FROM PokemonType WHERE pokedexNumber = %s AND typeName = %s",
        (dex, type_name)
    )

    if already:
        return False, "That Pokemon already has that type."

    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO PokemonType (pokedexNumber, typeName) VALUES (%s, %s)",
            (dex, type_name)
        )
        conn.commit()
        return True, "Added " + type_name + " to Pokemon #" + str(dex) + "."

    except mysql.connector.Error as err:
        conn.rollback()
        return False, "Database error: " + str(err)

    finally:
        cursor.close()
        conn.close()


#SELECT: list every type & clicking type shows its Pokemon!
@app.route("/types")
def types():
    type_list = run_query("""
        SELECT t.typeName, t.color, COUNT(pt.pokedexNumber) AS pokemonCount
        FROM `Type` t
        LEFT JOIN PokemonType pt ON t.typeName = pt.typeName
        GROUP BY t.typeName, t.color
        ORDER BY t.typeName
    """)

    return render_template(
        "types.html", types=type_list, message=request.args.get("message")
    )


#SELECT & INSERT -- pokemon w/ one type, and adding another pokemon
@app.route("/types/<type_name>", methods=["GET", "POST"])
def type_pokemon(type_name):
    message = request.args.get("message")

    found = run_query(
        "SELECT typeName, color FROM `Type` WHERE typeName = %s", (type_name,)
    )

    if not found:
        return redirect(url_for("types", message="Type not found."))

    type_row = found[0]

    if request.method == "POST":
        success, message = add_pokemon_type(
            request.form.get("pokedexNumber", type=int), type_row["typeName"]
        )

        if success:
            return redirect(url_for(
                "type_pokemon", type_name=type_row["typeName"], message=message
            ))

    pokemon_with_type = run_query("""
        SELECT p.pokedexNumber, p.name, p.evolutionStage
        FROM Pokemon p
        JOIN PokemonType pt ON p.pokedexNumber = pt.pokedexNumber
        WHERE pt.typeName = %s
        ORDER BY p.pokedexNumber
    """, (type_row["typeName"],))

    available = run_query("""
        SELECT pokedexNumber, name
        FROM Pokemon
        WHERE pokedexNumber NOT IN (
            SELECT pokedexNumber FROM PokemonType WHERE typeName = %s
        )
        ORDER BY pokedexNumber
    """, (type_row["typeName"],))

    return render_template(
        "type_pokemon.html",
        type=type_row,
        pokemon=pokemon_with_type,
        available=available,
        message=message
    )


#SELECT & INSERT (continued) -- types of one pokemon, and adding another type
@app.route("/pokemon/<int:number>/types", methods=["GET", "POST"])
def pokemon_types(number):
    message = request.args.get("message")

    found = run_query(
        "SELECT pokedexNumber, name FROM Pokemon WHERE pokedexNumber = %s",
        (number,)
    )

    if not found:
        return redirect(url_for("pokemon", message="Pokemon not found."))

    pokemon_row = found[0]

    if request.method == "POST":
        success, message = add_pokemon_type(
            number, request.form.get("typeName", "").strip()
        )

        if success:
            return redirect(url_for(
                "pokemon_types", number=number, message=message
            ))

    current_types = run_query("""
        SELECT t.typeName, t.color
        FROM `Type` t
        JOIN PokemonType pt ON t.typeName = pt.typeName
        WHERE pt.pokedexNumber = %s
        ORDER BY t.typeName
    """, (number,))

    available = run_query("""
        SELECT typeName
        FROM `Type`
        WHERE typeName NOT IN (
            SELECT typeName FROM PokemonType WHERE pokedexNumber = %s
        )
        ORDER BY typeName
    """, (number,))

    return render_template(
        "pokemon_types.html",
        pokemon=pokemon_row,
        types=current_types,
        available=available,
        message=message
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True, host="0.0.0.0")