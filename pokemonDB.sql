-- MySQL dump 10.13  Distrib 8.4.10, for Linux (x86_64)
--
-- Host: localhost    Database: pokemonDB
-- ------------------------------------------------------
-- Server version	8.4.10-0ubuntu0.26.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Card`
--

DROP TABLE IF EXISTS `Card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Card` (
  `pokedexNumber` int NOT NULL,
  `cardNumber` varchar(20) NOT NULL,
  `value` decimal(10,2) DEFAULT NULL,
  `illustrator` varchar(80) DEFAULT NULL,
  `rarity` varchar(50) DEFAULT NULL,
  `setName` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`pokedexNumber`,`cardNumber`),
  KEY `setName` (`setName`),
  CONSTRAINT `Card_ibfk_1` FOREIGN KEY (`pokedexNumber`) REFERENCES `Pokemon` (`pokedexNumber`),
  CONSTRAINT `Card_ibfk_2` FOREIGN KEY (`setName`) REFERENCES `PokemonSet` (`setName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Card`
--

LOCK TABLES `Card` WRITE;
/*!40000 ALTER TABLE `Card` DISABLE KEYS */;
INSERT INTO `Card` VALUES (906,'061',4.98,'Saboteri','Promo','Mega Evolution Promos'),(924,'167',0.18,'Sekio','Common','Paldea Evolved');
/*!40000 ALTER TABLE `Card` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pokemon`
--

DROP TABLE IF EXISTS `Pokemon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Pokemon` (
  `pokedexNumber` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `evolutionStage` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`pokedexNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pokemon`
--

LOCK TABLES `Pokemon` WRITE;
/*!40000 ALTER TABLE `Pokemon` DISABLE KEYS */;
INSERT INTO `Pokemon` VALUES (906,'Sprigatito','Basic'),(924,'Tandemaus','Basic');
/*!40000 ALTER TABLE `Pokemon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PokemonSet`
--

DROP TABLE IF EXISTS `PokemonSet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PokemonSet` (
  `setName` varchar(100) NOT NULL,
  `cardCount` int DEFAULT NULL,
  `series` varchar(80) DEFAULT NULL,
  `releaseDate` date DEFAULT NULL,
  PRIMARY KEY (`setName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PokemonSet`
--

LOCK TABLES `PokemonSet` WRITE;
/*!40000 ALTER TABLE `PokemonSet` DISABLE KEYS */;
INSERT INTO `PokemonSet` VALUES ('Mega Evolution Promos',105,'Mega Evolution','2025-09-13'),('Paldea Evolved',193,'Scarlet & Violet','2023-06-09');
/*!40000 ALTER TABLE `PokemonSet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PokemonType`
--

DROP TABLE IF EXISTS `PokemonType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PokemonType` (
  `pokedexNumber` int NOT NULL,
  `typeName` varchar(30) NOT NULL,
  PRIMARY KEY (`pokedexNumber`,`typeName`),
  KEY `typeName` (`typeName`),
  CONSTRAINT `PokemonType_ibfk_1` FOREIGN KEY (`pokedexNumber`) REFERENCES `Pokemon` (`pokedexNumber`),
  CONSTRAINT `PokemonType_ibfk_2` FOREIGN KEY (`typeName`) REFERENCES `Type` (`typeName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PokemonType`
--

LOCK TABLES `PokemonType` WRITE;
/*!40000 ALTER TABLE `PokemonType` DISABLE KEYS */;
INSERT INTO `PokemonType` VALUES (924,'Colorless'),(906,'Grass');
/*!40000 ALTER TABLE `PokemonType` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Type`
--

DROP TABLE IF EXISTS `Type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Type` (
  `typeName` varchar(30) NOT NULL,
  `effect` varchar(100) DEFAULT NULL,
  `color` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`typeName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Type`
--

LOCK TABLES `Type` WRITE;
/*!40000 ALTER TABLE `Type` DISABLE KEYS */;
INSERT INTO `Type` VALUES ('Colorless','Neutral vs all types','Gray'),('Grass','Strong vs Water','Green');
/*!40000 ALTER TABLE `Type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-27 19:11:44
