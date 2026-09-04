# Databases_Pokemon_Project
This database will model a Pokemon TCG collection! 

***The goal of this database is to track the actual physical Pokemon cards I own physically.
    That way, the collection can be organized and information about it can be extracted
    with ease!***

Entities:
1. Pokemon: represents a pokemon species

   Attributes:
   1. Name
   2. Pokedex Number
   3. Evolution Stage

3. Card: represents the physical printed card
   
   Attrbutes:
   1. Card number
   2. Illustrator
   3. Rarity
   4. Value

5. Set: represents an expanstion/set the cards were released in
   
   Attributes
   1. Set Name
   2. Total Card Count
   3. Series

7. Type: represents the elemental type the pokemon is
   
   Attributes
   1. Type Name
   2. Symbol/Color

Use-cases:
1. What cards am I missing to complete a set?
2. How many cards of this specific pokemon do I have?
3. How many cards of this type of rarity do I have?
4. What is the total net cost of the cards I have come to?
