# Databases_Pokemon_Project
This database will model a Pokemon TCG collection! 

***The goal of this database is to track the actual physical Pokemon cards I own physically.
    That way, the collection can be organized and information about it can be extracted
    with ease!***

Entities:
1. Pokemon: represents a pokemon species
   Attributes:
   *Name
   *Pokedex Number
   *Evolution Stage

2. Card: represents the physical printed card
   Attrbutes:
   *Card number
   *Illustrator
   *Rarity
   *Value

4. Set: represents an expanstion/set the cards were released in
   Attributes
   *Set Name
   *Total Card Count
   *Series

5. Type: represents the elemental type the pokemon is
   Attributes
   *Type Name
   *Symbol/Color

Use-cases:
1. What cards am I missing to complete a set?
2. How many cards of this specific pokemon do I have?
3. How many cards of this type of rarity do I have?
4. What is the total net cost of the cards I have come to?
