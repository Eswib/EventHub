-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: events
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `arrangement`
--

DROP TABLE IF EXISTS `arrangement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `arrangement` (
  `id` int NOT NULL AUTO_INCREMENT,
  `navn` varchar(45) NOT NULL,
  `beskrivelse` varchar(200) NOT NULL,
  `dato` datetime NOT NULL,
  `sted` varchar(100) NOT NULL,
  `bruker_id` int NOT NULL,
  `bilde` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_Arrangementer_Brukere1_idx` (`bruker_id`),
  CONSTRAINT `fk_arrangement_bruker` FOREIGN KEY (`bruker_id`) REFERENCES `bruker` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arrangement`
--

LOCK TABLES `arrangement` WRITE;
/*!40000 ALTER TABLE `arrangement` DISABLE KEYS */;
INSERT INTO `arrangement` VALUES (1,'Sommerfest 2025','Årets store sommerfest med grilling og musikk!','2025-06-15 18:00:00','Parken ved fjorden',1,NULL),(2,'Konsert med Lokalt Band','Intimkonsert med det lokale bandet \"Nordlys\".','2025-07-20 20:00:00','Kulturhuset',2,NULL),(3,'Fagseminar om Bærekraft','Et dagsseminar om bærekraftige løsninger for fremtiden.','2025-09-05 09:00:00','Universitetet i Bodø',1,NULL),(4,'Julemarked i Sentrum','Tradisjonelt julemarked med salg av håndverk og lokale produkter.','2025-12-10 11:00:00','Torget',3,NULL),(5,'Champagnefrokost hos Preben','Preben inviterer i år igjen på champagnefrokost på Bodøs beste vestkant. Ingen inngang med Cava, Prosecco eller annet skvip ','2025-05-17 06:30:00','Prebens kåk',5,'download.png'),(8,'Sankthansaften i fjæra','Bodø Bokbrenneklubb arranger sin årlige Sankthansfeiring 24. juni. Kom og brenn din favorittbok!','2025-06-24 18:00:00','Fjæra',6,'bok.png'),(9,'Julekveld i stua','Når nettene blir lange og kulda setter inn, da er det tid for julekalas hos Preben','2025-12-27 20:00:00','Prebens kåk',6,'jul.png');
/*!40000 ALTER TABLE `arrangement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bruker`
--

DROP TABLE IF EXISTS `bruker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bruker` (
  `id` int NOT NULL AUTO_INCREMENT,
  `epost` varchar(45) NOT NULL,
  `passord` varchar(200) NOT NULL,
  `navn` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bruker`
--

LOCK TABLES `bruker` WRITE;
/*!40000 ALTER TABLE `bruker` DISABLE KEYS */;
INSERT INTO `bruker` VALUES (1,'ola.nordmann@example.com','scrypt:32768:8:1$KCxqX9G4Jw6U8v4T$9e6b6c6ba265f3a99b7356d58aa186bf65999adba857582c27a011e24fb567194990ec7a19ef02cd045d58753c3df88a7e21e920b586e26b3af7add23f503cf6','Ola Nordmann'),(2,'kari.hansen@example.com','scrypt:32768:8:1$xCqf0R5Qa5D91a9V$f698820681004b75bdc05b413e34a9287c20d6803cd7a160d012d5adceca3955b8dcb4d1e260e257cee9c1921f3098bba7c693d08b4920c4e754c1e3b2d4fbed','Kari Hansen'),(3,'lars.olsen@example.com','scrypt:32768:8:1$OUpHVP7ACFpSKMCt$2591aa701803fe60b549bbc074c5e441676c095a3e78cd558b3bec886aaf4e2dcee3e901a42f23308f2c3bc6bc2c065e02f64412b604f8586b12bdfce244d51b','Lars Olsen'),(4,'anne.jensen@example.com','scrypt:32768:8:1$BXKzqkjlOdlqKHxy$8cee688e1f9978098163b656296c3a130836ffe6751da1aba2913cc45efe740cda6f9f478edc8cba6bc849bf5cded85f80412be020a79941f9384e2db90eb431','Anne Jensen'),(5,'eswibe@gmail.com','scrypt:32768:8:1$hQWYB7NtLXH3ZOC7$cb4eca735106e20b7f8b2a67cab71f123081814a824e1554a35529ec4b1191067327a84b10a7a96c5daf76e16b644c6277480363f354d3f8e9181a0ff0a0d6d3','Espen Wibe'),(6,'test@test.no','scrypt:32768:8:1$dpSrIGIeR60iapi3$71ed0f17b646b02e30909015cb07a5c7d8a96888b4322834a10f1267d35fbebab89352add36503228c5b41d04df7527a57e8092f6171d66954a840ff81bb383a','Test Testesen');
/*!40000 ALTER TABLE `bruker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `påmelding`
--

DROP TABLE IF EXISTS `påmelding`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `påmelding` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bruker_id` int NOT NULL,
  `arrangement_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_Påmeldinger_Brukere_idx` (`bruker_id`),
  KEY `fk_Påmeldinger_Arrangementer1_idx` (`arrangement_id`),
  CONSTRAINT `fk_påmelding_arrangement` FOREIGN KEY (`arrangement_id`) REFERENCES `arrangement` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_påmelding_bruker` FOREIGN KEY (`bruker_id`) REFERENCES `bruker` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `påmelding`
--

LOCK TABLES `påmelding` WRITE;
/*!40000 ALTER TABLE `påmelding` DISABLE KEYS */;
INSERT INTO `påmelding` VALUES (1,1,1),(2,2,1),(3,3,2),(4,4,2),(5,1,3),(6,2,3),(7,3,4),(9,5,5),(11,6,8),(13,6,5),(15,5,1);
/*!40000 ALTER TABLE `påmelding` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-20 11:54:48
