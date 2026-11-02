
from flask import Flask, render_template, request, redirect, url_for
from database_client import connect_to_database
import mysql.connector

app = Flask(__name__, template_folder="webpage")


@app.route("/", methods=["GET", "POST"])
def pokemon():

    message = None

    if request.method == "POST":

        number = request.form.get("number", "").strip()
        name = request.form.get("name", "").strip()
        stage = request.form.get("stage", "").strip()

        if not number.isdigit() or not name:
            message = "Please enter a valid Pokedex number and name."

        elif int(number) > 1100:
            message = "Pokedex number is too large."

        elif len(name) > 50 or len(stage) > 30:
            message = "Name or evolution stage is too long."

        else:
            conn = connect_to_database()
            cursor = conn.cursor()

            try:
                #inserting new pokemon
                query = """
                    INSERT INTO Pokemon
                    (pokedexNumber, name, evolutionStage)
                    VALUES (%s, %s, %s)
                """

                cursor.execute(query, (int(number), name, stage or None))
                conn.commit()

                return redirect(url_for("pokemon"))

            except mysql.connector.IntegrityError:
                conn.rollback()
                message = "That Pokedex number already exists or violates a database constraint."

            except mysql.connector.Error as err:
                conn.rollback()
                message = "Database error: " + str(err)

            finally:
                cursor.close()
                conn.close()

    #retrieving pokemon
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

        pokemon_list = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    return render_template(
        "pokemon.html",
        pokemon=pokemon_list,
        message=message
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True, host="0.0.0.0")
