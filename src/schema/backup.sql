drop database fast_track_db;
create database fast_track_db;
use fast_track_db;
-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: fast_track_db
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `fullname` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `email_verified` tinyint(1) NOT NULL DEFAULT '1',
  `fcm_reg_token` varchar(1024) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (8,'techie99','techie99@gmail.com','Collins Nnanna','$2b$12$D4dquC5Z9j5OY.WYMwKDgeEopLYxhuCB3Kor0j13NkvhqJVVrjYxi',1,1,NULL,'2024-12-07 17:14:30','2024-12-07 17:14:30'),(9,'jondoe','jondoe@gmail.com','Jon Doe','$2b$12$B5PryhyYxHh3TZtzL/.iLu0XEu3t2th3nQndIqiSqS9txcPXwxCnK',1,1,NULL,'2024-12-07 17:43:34','2024-12-07 17:43:34'),(10,'janedoe','janedoe@gmail.com','Jane Doe','$2b$12$27qwkmb217nkG.ub/3gXM.afVHhWhxgwX0MjG0g7o/Kx7B/xisNg2',1,1,NULL,'2024-12-07 17:43:46','2024-12-07 17:45:01');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `features`
--

DROP TABLE IF EXISTS `features`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `features` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` text,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deadline` datetime DEFAULT NULL,
  `project_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `features_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `features`
--

LOCK TABLES `features` WRITE;
/*!40000 ALTER TABLE `features` DISABLE KEYS */;
INSERT INTO `features` VALUES (4,'Accounts Managment and Authentication','User Should be able to Login end to end','2024-12-07 19:12:57','2024-12-07 19:12:57','2025-11-07 18:11:58',4),(5,'Authentication','Login and Register','2024-12-07 19:47:22','2024-12-07 19:47:22','2024-12-07 18:46:58',5),(6,'Applications and Inventory','Login and Register','2024-12-07 19:47:59','2024-12-07 19:47:59','2024-12-07 18:46:58',5);
/*!40000 ALTER TABLE `features` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member_roles`
--

DROP TABLE IF EXISTS `member_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_roles` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int unsigned NOT NULL,
  `role_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `member_id` (`member_id`,`role_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `member_roles_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `organization_members` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `member_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `organization_roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member_roles`
--

LOCK TABLES `member_roles` WRITE;
/*!40000 ALTER TABLE `member_roles` DISABLE KEYS */;
INSERT INTO `member_roles` VALUES (15,17,18),(16,18,19),(17,19,19);
/*!40000 ALTER TABLE `member_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organization_members`
--

DROP TABLE IF EXISTS `organization_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organization_members` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `account_id` int unsigned NOT NULL,
  `organization_id` int unsigned NOT NULL,
  `joined_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `acct_idx_org_idx` (`account_id`,`organization_id`),
  KEY `organization_id` (`organization_id`),
  CONSTRAINT `organization_members_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `organization_members_ibfk_2` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organization_members`
--

LOCK TABLES `organization_members` WRITE;
/*!40000 ALTER TABLE `organization_members` DISABLE KEYS */;
INSERT INTO `organization_members` VALUES (17,8,14,'2024-12-07 17:15:17'),(18,10,14,'2024-12-07 17:47:49'),(19,9,14,'2024-12-07 17:48:13');
/*!40000 ALTER TABLE `organization_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organization_roles`
--

DROP TABLE IF EXISTS `organization_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organization_roles` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `role` varchar(100) NOT NULL DEFAULT 'default',
  `can_manage_teams` tinyint(1) NOT NULL DEFAULT '0',
  `can_manage_projects` tinyint(1) NOT NULL DEFAULT '0',
  `can_manage_tasks` tinyint(1) NOT NULL DEFAULT '0',
  `can_manage_roles` tinyint(1) NOT NULL DEFAULT '0',
  `can_send_invites` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `organization_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `organization_id` (`organization_id`),
  CONSTRAINT `organization_roles_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organization_roles`
--

LOCK TABLES `organization_roles` WRITE;
/*!40000 ALTER TABLE `organization_roles` DISABLE KEYS */;
INSERT INTO `organization_roles` VALUES (18,'admin',1,1,1,1,1,'2024-12-07 17:15:17','2024-12-07 17:15:17',14),(19,'Junior',0,0,0,0,0,'2024-12-07 17:16:05','2024-12-07 17:16:05',14);
/*!40000 ALTER TABLE `organization_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organizations`
--

DROP TABLE IF EXISTS `organizations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organizations` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `organization_name` varchar(255) DEFAULT NULL,
  `type` enum('default','standard','enterprise') NOT NULL DEFAULT 'default',
  `member_capacity` int unsigned NOT NULL DEFAULT '100',
  `max_teams_per_project` int unsigned NOT NULL DEFAULT '4',
  `owner_id` int unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `owner_id` (`owner_id`),
  CONSTRAINT `organizations_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `accounts` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organizations`
--

LOCK TABLES `organizations` WRITE;
/*!40000 ALTER TABLE `organizations` DISABLE KEYS */;
INSERT INTO `organizations` VALUES (14,'Zidepeople','enterprise',100,4,8,'2024-12-07 17:15:17','2024-12-07 17:15:17');
/*!40000 ALTER TABLE `organizations` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE TRIGGER `CreateAdminRole` AFTER INSERT ON `organizations` FOR EACH ROW BEGIN
     DECLARE role_id INT;
     DECLARE member_id INT;
     INSERT INTO 
          organization_roles (role, can_manage_teams, can_manage_projects, can_manage_tasks, can_manage_roles, can_send_invites, organization_id )
         VALUES ('admin', TRUE,TRUE,TRUE,TRUE,TRUE, NEW.id);
     SET role_id = LAST_INSERT_ID();
     INSERT INTO organization_members (account_id, organization_id) VALUES (NEW.owner_id, NEW.id);
     SET member_id = LAST_INSERT_ID();

     INSERT INTO member_roles (`member_id`, `role_id`) VALUES (member_id, role_id);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `project_name` varchar(255) DEFAULT NULL,
  `deadline` datetime NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `organization_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `organization_id` (`organization_id`),
  CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (4,'Mobile App','2025-12-07 16:18:00','2024-12-07 17:18:28','2024-12-07 17:18:28',14),(5,'Website','2024-12-07 18:46:24','2024-12-07 19:46:37','2024-12-07 19:46:37',14);
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_dependencies`
--

DROP TABLE IF EXISTS `task_dependencies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_dependencies` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `depender_id` int unsigned NOT NULL,
  `depended_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `depender_id` (`depender_id`),
  KEY `depended_id` (`depended_id`),
  CONSTRAINT `task_dependencies_ibfk_1` FOREIGN KEY (`depender_id`) REFERENCES `tasks` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `task_dependencies_ibfk_2` FOREIGN KEY (`depended_id`) REFERENCES `tasks` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_dependencies`
--

LOCK TABLES `task_dependencies` WRITE;
/*!40000 ALTER TABLE `task_dependencies` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_dependencies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text,
  `status` enum('pending','todo','review','done') DEFAULT 'pending',
  `requirements` json DEFAULT NULL,
  `deadline` datetime NOT NULL,
  `completed_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `feature_id` int unsigned NOT NULL,
  `parent_task_id` int unsigned DEFAULT NULL,
  `assigned_team_id` int unsigned DEFAULT NULL,
  `assigned_account_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `feature_id` (`feature_id`),
  KEY `parent_task_id` (`parent_task_id`),
  KEY `assigned_team_id` (`assigned_team_id`),
  KEY `assigned_account_id` (`assigned_account_id`),
  CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`feature_id`) REFERENCES `features` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `tasks_ibfk_2` FOREIGN KEY (`parent_task_id`) REFERENCES `tasks` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `tasks_ibfk_3` FOREIGN KEY (`assigned_team_id`) REFERENCES `teams` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `tasks_ibfk_4` FOREIGN KEY (`assigned_account_id`) REFERENCES `accounts` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (3,'Sign-in and Sign-up',NULL,'pending','{}','2025-10-08 16:41:33',NULL,'2024-12-08 17:48:42','2024-12-08 17:48:42',4,NULL,5,NULL),(4,'Sign In UI Implementation',NULL,'pending','{}','2025-12-08 16:53:25',NULL,'2024-12-08 17:56:32','2024-12-08 17:56:32',4,3,NULL,10);
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team_members`
--

DROP TABLE IF EXISTS `team_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `team_members` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `team_id` int unsigned NOT NULL,
  `account_id` int unsigned NOT NULL,
  `joined_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `team_id` (`team_id`,`account_id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `team_members_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `team_members_ibfk_2` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_members`
--

LOCK TABLES `team_members` WRITE;
/*!40000 ALTER TABLE `team_members` DISABLE KEYS */;
INSERT INTO `team_members` VALUES (3,5,10,'2024-12-07 18:02:02'),(5,5,9,'2024-12-07 18:55:23'),(6,6,9,'2024-12-07 18:59:28'),(7,6,10,'2024-12-07 18:59:39');
/*!40000 ALTER TABLE `team_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teams` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `team_name` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `organization_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_teams_projects` (`organization_id`),
  CONSTRAINT `fk_teams_organizations` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams`
--

LOCK TABLES `teams` WRITE;
/*!40000 ALTER TABLE `teams` DISABLE KEYS */;
INSERT INTO `teams` VALUES (5,'POD 1','2024-12-07 17:19:16','2024-12-07 17:19:16',14),(6,'POD 4','2024-12-07 18:59:12','2024-12-07 18:59:12',14);
/*!40000 ALTER TABLE `teams` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-08 18:28:48
