CREATE DATABASE  IF NOT EXISTS `gaa_analytics`; 
USE `gaa_analytics`;
-- MySQL dump 10.13  Distrib 8.0.14, for Win64 (x86_64)
--
-- Host: localhost    Database: datarepresentation
-- ------------------------------------------------------
-- Server version	8.0.14



--
-- Table structure for table `job`
--

DROP TABLE IF EXISTS `match_info`;
 SET character_set_client = utf8mb4 ;
CREATE TABLE gaa_analytics.match_info 
(game_id int,
	team VARCHAR(2),
	team_name VARCHAR(25),
	venue	VARCHAR(25),
    date datetime,
	competition VARCHAR(50),
	round	VARCHAR(25),
    player int,
	player_name	VARCHAR(25)
 )ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
--

LOCK TABLES `match_info` WRITE;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/match_info.csv' 
INTO TABLE gaa_analytics.match_info 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
UNLOCK TABLES;

