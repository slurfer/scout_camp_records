-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: localhost    Database: scoutCamp
-- ------------------------------------------------------
-- Server version	8.0.32-0ubuntu0.22.04.2

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
-- Table structure for table `age_categories`
--

DROP TABLE IF EXISTS `age_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `age_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `age_categories`
--

LOCK TABLES `age_categories` WRITE;
/*!40000 ALTER TABLE `age_categories` DISABLE KEYS */;
INSERT INTO `age_categories` VALUES (1,'vlčata'),(2,'svetlusky');
/*!40000 ALTER TABLE `age_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `camps`
--

DROP TABLE IF EXISTS `camps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `camps` (
  `id` int NOT NULL AUTO_INCREMENT,
  `starts_on` date DEFAULT NULL,
  `ends_on` date DEFAULT NULL,
  `leader_id` int DEFAULT NULL,
  `leader_deputy_id` int DEFAULT NULL,
  `medic_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  CONSTRAINT `fk_camps_leader_deputy_id` FOREIGN KEY (`id`) REFERENCES `members` (`id`),
  CONSTRAINT `fk_camps_leader_id` FOREIGN KEY (`id`) REFERENCES `members` (`id`),
  CONSTRAINT `fk_camps_medic_id` FOREIGN KEY (`id`) REFERENCES `members` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camps`
--

LOCK TABLES `camps` WRITE;
/*!40000 ALTER TABLE `camps` DISABLE KEYS */;
INSERT INTO `camps` VALUES (1,'2023-06-02','2023-06-17',1,2,3),(2,'2023-06-02','2023-06-17',1,2,6),(3,'2023-06-02','2023-06-17',1,2,6),(4,'2023-06-02','2023-06-17',1,2,NULL);
/*!40000 ALTER TABLE `camps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `members`
--

DROP TABLE IF EXISTS `members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `members` (
  `id` int NOT NULL AUTO_INCREMENT,
  `time_created` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `time_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(45) NOT NULL,
  `surname` varchar(45) NOT NULL,
  `birth_date` date NOT NULL,
  `age_category_id` int DEFAULT NULL,
  `gender` varchar(45) DEFAULT NULL,
  `mother_id` int DEFAULT NULL,
  `father_id` int DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `mother_id_idx` (`mother_id`),
  KEY `father_id_idx` (`father_id`),
  KEY `age_category_id_idx` (`age_category_id`),
  CONSTRAINT `father_id` FOREIGN KEY (`father_id`) REFERENCES `parents` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `member_age_category_id` FOREIGN KEY (`age_category_id`) REFERENCES `age_categories` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `mother_id` FOREIGN KEY (`mother_id`) REFERENCES `parents` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members`
--

LOCK TABLES `members` WRITE;
/*!40000 ALTER TABLE `members` DISABLE KEYS */;
INSERT INTO `members` VALUES (1,'2023-01-17 22:02:37','2023-01-17 22:02:37','Martin','Doušek','2004-05-25',NULL,NULL,NULL,NULL,NULL),(2,'2023-01-17 22:02:37','2023-01-17 22:02:37','Lubomír','Janda','2004-09-17',NULL,NULL,NULL,NULL,'So this is good.'),(3,'2023-01-17 22:02:37','2023-01-17 22:02:37','Lubomír','Janda','2004-09-17',NULL,NULL,NULL,NULL,'So this is good.'),(4,'2023-01-17 22:02:37','2023-01-17 22:02:37','Lubomír','Janda','2004-09-17',NULL,NULL,NULL,NULL,'So this is good.'),(5,'2023-01-17 22:02:37','2023-01-17 22:02:37','Lubomír','Janda','2004-09-17',NULL,NULL,NULL,NULL,'Description can be updated'),(7,'2023-01-17 22:02:37','2023-01-17 22:02:37','Martin','Doušek','2004-09-17',NULL,NULL,1,2,'So this is good.'),(11,'2023-01-17 22:02:37','2023-01-17 22:02:37','Alfons','Mucha','2004-07-12',1,'muž',1,2,'Ahoj'),(12,'2023-01-17 22:02:37','2023-01-17 22:02:37','Alfons','Mucha','2004-07-12',1,NULL,1,2,'Ahoj'),(13,'2023-01-17 22:02:37','2023-01-17 22:02:37','Alfons','Mucha','2004-07-12',1,'muž',NULL,2,'Ahoj'),(14,'2023-01-17 22:02:37','2023-01-17 22:02:37','Alfons','Mucha','2004-07-12',1,'muž',1,2,NULL),(15,'2023-01-17 22:05:49','2023-01-17 22:05:49','Alfons','Mucha','2004-07-12',1,'muž',1,2,'Ahoj'),(16,'2023-01-18 21:44:38','2023-01-18 21:44:38','Martin','Doušek','2004-09-17',NULL,NULL,1,2,'So this is good.'),(17,'2023-01-18 21:45:12','2023-01-18 21:45:12','Martin','Doušek','2004-09-17',NULL,NULL,1,2,'So this is good.'),(18,'2023-01-18 21:58:53','2023-01-18 21:58:53','Martin','Doušek','2004-09-17',1,NULL,1,2,'So this is good.'),(20,'2023-01-18 22:35:38','2023-01-18 22:35:38','Martin','Doušek','2004-09-17',1,NULL,1,2,'So this is good.'),(22,'2023-01-18 22:36:25','2023-01-18 22:36:25','Martin','Doušek','2004-09-17',1,NULL,1,2,'So this is good.'),(23,'2023-01-18 22:37:22','2023-01-18 22:37:22','Martin','Doušek','2004-09-17',1,NULL,1,2,'So this is good.'),(24,'2023-01-18 22:45:35','2023-01-18 22:45:35','Martin','Doušek','2004-09-17',1,NULL,1,2,'So this is good.'),(25,'2023-01-19 15:03:48','2023-01-19 15:03:48','Martin','Doušek','2004-09-17',1,NULL,1,2,'Description can be updated'),(26,'2023-01-19 20:14:57','2023-01-19 20:14:57','Martin','Doušek','2004-09-17',1,NULL,NULL,2,'Description can be updated'),(27,'2023-01-23 16:18:41','2023-01-23 16:18:41','Martin','Doušek','2004-09-17',1,NULL,1,2,'So this is good.'),(28,'2023-01-23 16:18:51','2023-01-23 16:18:51','Martin','Doušek','2004-09-17',1,NULL,1,2,'So this is good.'),(29,'2023-01-23 16:19:29','2023-01-23 16:19:29','Martin','Doušek','2004-09-17',1,NULL,1,2,'So this is good.'),(30,'2023-01-23 16:20:29','2023-01-23 16:20:29','Martin','Doušek','2004-09-17',1,NULL,1,2,'So this is good.'),(31,'2023-01-23 16:20:38','2023-01-23 16:20:38','Martin','Doušek','2004-09-17',1,NULL,1,2,'So this is good.'),(32,'2023-01-26 22:32:58','2023-01-26 22:32:58','Martin','Doušek','2004-09-17',1,NULL,1,2,'So this is good.'),(33,'2023-01-26 22:55:06','2023-01-26 22:55:06','Martin','Doušek','2004-09-17',1,NULL,1,2,'So this is good.'),(34,'2023-01-26 22:55:13','2023-01-26 22:55:13','Martin','Doušek','2004-09-17',1,NULL,1,2,'So this is good.'),(35,'2023-01-31 12:24:42','2023-01-31 12:24:42','Václav','Zvěřina','2004-09-17',1,NULL,1,2,'So this is good.');
/*!40000 ALTER TABLE `members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parents`
--

DROP TABLE IF EXISTS `parents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `surname` varchar(45) DEFAULT NULL,
  `relationship_with_child` varchar(45) DEFAULT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parents`
--

LOCK TABLES `parents` WRITE;
/*!40000 ALTER TABLE `parents` DISABLE KEYS */;
INSERT INTO `parents` VALUES (1,'Miloslava','Doušková','matka',NULL,NULL),(2,'Jiří','Doušek','otec',NULL,NULL),(5,'Martin','Doušek','matka',NULL,NULL);
/*!40000 ALTER TABLE `parents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `participants`
--

DROP TABLE IF EXISTS `participants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `participants` (
  `id` int NOT NULL AUTO_INCREMENT,
  `member_id` int NOT NULL,
  `camp_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `member_id_idx` (`member_id`),
  KEY `camp_id_idx` (`camp_id`),
  CONSTRAINT `camp_id` FOREIGN KEY (`camp_id`) REFERENCES `camps` (`id`),
  CONSTRAINT `member_id` FOREIGN KEY (`member_id`) REFERENCES `members` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `participants`
--

LOCK TABLES `participants` WRITE;
/*!40000 ALTER TABLE `participants` DISABLE KEYS */;
INSERT INTO `participants` VALUES (16,3,1),(17,3,2),(19,1,1),(20,1,3),(21,1,2),(22,29,1),(23,30,1),(29,31,1),(30,31,2),(31,31,3),(51,32,1),(52,32,2),(53,34,1),(54,35,1);
/*!40000 ALTER TABLE `participants` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-28 20:50:53
