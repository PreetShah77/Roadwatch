-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: roadwatch
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add custom user',6,'add_customuser'),(22,'Can change custom user',6,'change_customuser'),(23,'Can delete custom user',6,'delete_customuser'),(24,'Can view custom user',6,'view_customuser'),(25,'Can add complaint',7,'add_complaint'),(26,'Can change complaint',7,'change_complaint'),(27,'Can delete complaint',7,'delete_complaint'),(28,'Can view complaint',7,'view_complaint'),(29,'Can add system settings',8,'add_systemsettings'),(30,'Can change system settings',8,'change_systemsettings'),(31,'Can delete system settings',8,'delete_systemsettings'),(32,'Can view system settings',8,'view_systemsettings'),(33,'Can add user profile',9,'add_userprofile'),(34,'Can change user profile',9,'change_userprofile'),(35,'Can delete user profile',9,'delete_userprofile'),(36,'Can view user profile',9,'view_userprofile'),(37,'Can add task',10,'add_task'),(38,'Can change task',10,'change_task'),(39,'Can delete task',10,'delete_task'),(40,'Can view task',10,'view_task'),(41,'Can add employee',11,'add_employee'),(42,'Can change employee',11,'change_employee'),(43,'Can delete employee',11,'delete_employee'),(44,'Can view employee',11,'view_employee');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_myapp_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_myapp_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `myapp_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(7,'myapp','complaint'),(6,'myapp','customuser'),(11,'myapp','employee'),(8,'myapp','systemsettings'),(10,'myapp','task'),(9,'myapp','userprofile'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'myapp','0001_initial','2024-11-10 13:38:12.264595'),(2,'contenttypes','0001_initial','2024-11-10 13:38:12.313209'),(3,'admin','0001_initial','2024-11-10 13:38:12.437880'),(4,'admin','0002_logentry_remove_auto_add','2024-11-10 13:38:12.437880'),(5,'admin','0003_logentry_add_action_flag_choices','2024-11-10 13:38:12.455001'),(6,'contenttypes','0002_remove_content_type_name','2024-11-10 13:38:12.531320'),(7,'auth','0001_initial','2024-11-10 13:38:12.798073'),(8,'auth','0002_alter_permission_name_max_length','2024-11-10 13:38:12.856733'),(9,'auth','0003_alter_user_email_max_length','2024-11-10 13:38:12.856733'),(10,'auth','0004_alter_user_username_opts','2024-11-10 13:38:12.869571'),(11,'auth','0005_alter_user_last_login_null','2024-11-10 13:38:12.872786'),(12,'auth','0006_require_contenttypes_0002','2024-11-10 13:38:12.877188'),(13,'auth','0007_alter_validators_add_error_messages','2024-11-10 13:38:12.882681'),(14,'auth','0008_alter_user_username_max_length','2024-11-10 13:38:12.891904'),(15,'auth','0009_alter_user_last_name_max_length','2024-11-10 13:38:12.898716'),(16,'auth','0010_alter_group_name_max_length','2024-11-10 13:38:12.917213'),(17,'auth','0011_update_proxy_permissions','2024-11-10 13:38:12.945283'),(18,'auth','0012_alter_user_first_name_max_length','2024-11-10 13:38:12.958533'),(19,'sessions','0001_initial','2024-11-10 13:38:12.989033'),(20,'myapp','0002_systemsettings_customuser_is_admin_and_more','2024-11-11 02:20:52.284255'),(21,'myapp','0003_employee_task','2024-11-11 04:45:36.955063'),(22,'myapp','0004_rename_phone_no_employee_phone','2024-11-11 04:53:59.454928'),(23,'myapp','0005_employee_password','2024-11-11 06:09:28.328156'),(24,'myapp','0006_employee_last_login','2024-11-11 06:28:12.270203'),(25,'myapp','0007_complaint_resolved_on','2024-11-11 14:53:44.379456'),(26,'myapp','0008_complaint_comment','2024-11-11 15:28:04.630261'),(27,'myapp','0009_alter_complaint_resolved_on','2024-11-11 15:38:21.793798'),(28,'myapp','0010_alter_complaint_resolved_on','2024-11-11 15:51:21.774966'),(29,'myapp','0011_alter_complaint_resolved_on','2024-11-11 15:52:21.857895'),(30,'myapp','0012_alter_complaint_image_alter_complaint_resolved_on_and_more','2024-12-06 05:14:48.308804'),(31,'myapp','0013_alter_complaint_image_alter_complaint_resolved_on_and_more','2024-12-06 05:20:39.142365'),(32,'myapp','0014_alter_systemsettings_options_and_more','2024-12-06 05:31:10.477610'),(33,'myapp','0015_alter_systemsettings_options_and_more','2024-12-06 05:42:01.760922'),(34,'myapp','0016_userprofile_created_at_userprofile_last_login_and_more','2024-12-06 07:10:16.823678');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('ju6g3pwvy09w1pd86k061xp7div88mqf','.eJxVjs0KwjAQhN8lZwndzY_Wo3efIWw2G1OVFJr2JL67LRTR63wzH_NSgZa5hKXJFIakzgrU4TeLxA-pG0h3qrdR81jnaYh6q-idNn0dkzwve_dPUKiVdS0s3h4J-5Nz3AETSE8YsyFnMoNYH9ELRc82I3qynZGc0XQxJUiAq_T7Ed4fvR88ZQ:1tKKKi:C3CmPn3EFkqrAaco7nR2Vq8axDDvOiZbhMhz4fXKBms','2024-12-22 16:40:36.810231'),('p7cmpgq8p7e3p1moard3tci86f95ah60','.eJxVTksOwiAUvAtrQ-CVT3Hp3jOQBzykamhS2pXx7tKkMbqZTOaXeTGP21r81mjxU2JnZtnpVwsYH1R3I92x3mYe57ouU-B7hB9u49c50fNyZP8GCrbS20qgoTAEIyXZDFGMQiAa3SGPVibtcmcIaVAGHAFYBJBKGdJh0Mr10e9H-_4Amno7Vg:1tKK0K:Yyj7f_OY1dsJmz-Sz3Rf2necQcqMi-R2c-C5svYaZn4','2024-12-22 16:19:32.591496');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;

--
-- Table structure for table `myapp_complaint`
--

DROP TABLE IF EXISTS `myapp_complaint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `myapp_complaint` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `complaint_id` varchar(8) NOT NULL,
  `issue_type` varchar(50) NOT NULL,
  `severity` varchar(10) NOT NULL,
  `description` longtext NOT NULL,
  `location` varchar(100) NOT NULL,
  `coordinates` varchar(100) NOT NULL,
  `image` varchar(100) NOT NULL,
  `google_drive_url` varchar(200) DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `status` varchar(50) NOT NULL,
  `resolved_on` longtext NOT NULL,
  `comment` longtext NOT NULL DEFAULT (_utf8mb3''),
  PRIMARY KEY (`id`),
  UNIQUE KEY `complaint_id` (`complaint_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myapp_complaint`
--

/*!40000 ALTER TABLE `myapp_complaint` DISABLE KEYS */;
INSERT INTO `myapp_complaint` VALUES (1,'2EYIEB20','crack','low','','Nagalpur Char Rasta, Mehsana','23.585516494595982, 72.37413614819336','2EYIEB20.jpg',NULL,'2024-11-17 14:56:42.755779','user@user.com','resolved','17-11-2024',''),(2,'XU07XXDX','pothole','medium','','Modhera Char Rasta, Mehsana','23.594267208759906, 72.37896412442016','XU07XXDX.jpg',NULL,'2024-11-17 14:57:13.054236','user@user.com','resolved','03-12-2024',''),(3,'7JVRB5VR','crack','high','','Radhanpur Char Rasta, Mehsana','23.606123986675495, 72.38130301068115','7JVRB5VR.jpg',NULL,'2024-11-17 14:57:41.980661','user@user.com','in-progress',' ',''),(4,'B3EAFW8C','pothole','medium','','Kherva','23.540829599348363, 72.43833750317383','B3EAFW8C.jpg',NULL,'2024-11-17 14:59:05.290359','user2@user.com','resolved','17-11-2024',''),(5,'58APTZON','crack','medium','','Kherva','23.531139536465506, 72.4565009814453','58APTZON.jpg',NULL,'2024-11-18 07:31:41.252545','user@user.com','pending',' ',''),(7,'X3UKL78T','crack','medium','','Kherva','23.528542632430003, 72.4619941455078','X3UKL78T.jpg',NULL,'2024-12-03 06:04:20.562159','admin@admin.com','pending',' ',''),(8,'9CV7L59S','pothole','high','','Kherva','23.5219321, 72.4613075','9CV7L59S.jpg',NULL,'2024-12-03 06:04:47.914053','admin@admin.com','pending',' ',''),(9,'ETT8VSHX','crack','medium','','Kherva','23.5219321, 72.4613075','ETT8VSHX.jpg',NULL,'2024-12-03 06:05:00.035269','admin@admin.com','pending',' ',''),(10,'09M8NDAU','pothole','high','','Kherva','23.5219321, 72.4613075','09M8NDAU.png',NULL,'2024-12-03 06:06:49.829248','admin@admin.com','pending',' ',''),(13,'7SWHJZXX','pothole','high','','Mehsana-Becharaji Road','23.5831296, 72.368128','7SWHJZXX.jpg',NULL,'2024-12-08 16:20:17.713942','tempuser1@gmail.com','pending',' ',''),(14,'1CFC69MC','pothole','high','A large pothole in the middle of the busy road','Mehsana-Becharaji Road','23.5831296, 72.368128','1CFC69MC.jpg',NULL,'2024-12-08 16:38:30.082904','temp12@gmail.com','pending',' ','');
/*!40000 ALTER TABLE `myapp_complaint` ENABLE KEYS */;

--
-- Table structure for table `myapp_customuser`
--

DROP TABLE IF EXISTS `myapp_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `myapp_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `last_login` datetime(6) DEFAULT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `full_name` varchar(60) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(128) NOT NULL,
  `joining_date` date NOT NULL,
  `joining_time` time(6) NOT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `is_government_official` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myapp_customuser`
--

/*!40000 ALTER TABLE `myapp_customuser` DISABLE KEYS */;
INSERT INTO `myapp_customuser` VALUES (1,'2024-12-08 16:40:36.802058','admin','admin','admin admin','admin@admin.com','pbkdf2_sha256$600000$yw30A0kh4WwS69d48tDui5$xSRJCREFlXge9ILOwK8QaN+Qf3Bha8rdMAC9uVa6+dY=','2024-11-17','14:41:34.455929','1234567890',1,1),(2,'2024-12-08 14:12:20.687991','user','user','user user','user@user.com','pbkdf2_sha256$600000$P23Fg6JhU8Mfa7aVjZwpuV$Dp6KCv0dqmu5QOke+8YXsjUWCLKpqFw3/gJggef4RxI=','2024-11-17','14:55:19.305454',NULL,0,0),(3,'2024-11-17 14:58:36.911361','user2','user','user2 user','user2@user.com','pbkdf2_sha256$600000$nKwZicPmdK6Aucs59stqei$1WvPyUMcBrAz4oxKry8vOwrt1NbRi6olFHqNwI7izQ8=','2024-11-17','14:58:26.014903',NULL,0,0),(5,'2024-12-08 16:37:32.215662','temp','temp','temp temp','temp12@gmail.com','pbkdf2_sha256$600000$ky8jR2OXMbBc6yUToBiw5b$rQ9709U9O2KBGk2kiGHjhdfOOstkPv7uIY/Rui9jttc=','2024-12-07','05:23:30.477274','4645454245',0,0),(6,NULL,'temp','user','temp user','tempuser@gmail.com','pbkdf2_sha256$600000$eDTNqjn4BlaP0Xfq3fD5kg$oVFIGbvsYYBo+RI6QrXdnk8rH7LaEcku4PS/OhDhTcc=','2024-12-08','16:18:02.555526',NULL,0,0),(7,'2024-12-08 16:19:32.584908','temp','user','temp user','tempuser1@gmail.com','pbkdf2_sha256$600000$piaK9sZBE5mgl01LThIz2e$/TAoXzCKABb+4N6+wsdfqHlbn823K9Q0DlbTg8bG6JI=','2024-12-08','16:19:09.811926',NULL,0,0);
/*!40000 ALTER TABLE `myapp_customuser` ENABLE KEYS */;

--
-- Table structure for table `myapp_employee`
--

DROP TABLE IF EXISTS `myapp_employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `myapp_employee` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `emp_id` varchar(10) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `emp_id` (`emp_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myapp_employee`
--

/*!40000 ALTER TABLE `myapp_employee` DISABLE KEYS */;
INSERT INTO `myapp_employee` VALUES (1,'1001','admin','admin','admin@admin.com','1234567890','admin','pbkdf2_sha256$600000$yw30A0kh4WwS69d48tDui5$xSRJCREFlXge9ILOwK8QaN+Qf3Bha8rdMAC9uVa6+dY=',NULL);
/*!40000 ALTER TABLE `myapp_employee` ENABLE KEYS */;

--
-- Table structure for table `myapp_systemsettings`
--

DROP TABLE IF EXISTS `myapp_systemsettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `myapp_systemsettings` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `setting_name` varchar(50) NOT NULL,
  `setting_value` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myapp_systemsettings`
--

/*!40000 ALTER TABLE `myapp_systemsettings` DISABLE KEYS */;
/*!40000 ALTER TABLE `myapp_systemsettings` ENABLE KEYS */;

--
-- Table structure for table `myapp_task`
--

DROP TABLE IF EXISTS `myapp_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `myapp_task` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `task_type` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `is_completed` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `assigned_employee_id` bigint NOT NULL,
  `complaint_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `myapp_task_assigned_employee_id_6a9ad789_fk_myapp_employee_id` (`assigned_employee_id`),
  KEY `myapp_task_complaint_id_53c82ea3_fk_myapp_complaint_id` (`complaint_id`),
  CONSTRAINT `myapp_task_assigned_employee_id_6a9ad789_fk_myapp_employee_id` FOREIGN KEY (`assigned_employee_id`) REFERENCES `myapp_employee` (`id`),
  CONSTRAINT `myapp_task_complaint_id_53c82ea3_fk_myapp_complaint_id` FOREIGN KEY (`complaint_id`) REFERENCES `myapp_complaint` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myapp_task`
--

/*!40000 ALTER TABLE `myapp_task` DISABLE KEYS */;
/*!40000 ALTER TABLE `myapp_task` ENABLE KEYS */;

--
-- Table structure for table `myapp_userprofile`
--

DROP TABLE IF EXISTS `myapp_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `myapp_userprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `myapp_userprofile_user_id_8f877d36_fk_myapp_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `myapp_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myapp_userprofile`
--

/*!40000 ALTER TABLE `myapp_userprofile` DISABLE KEYS */;
INSERT INTO `myapp_userprofile` VALUES (1,1,1,'2024-12-06 17:52:52.459967',NULL,'2024-12-06 17:52:52.459967'),(3,1,2,'2024-12-07 05:15:27.393351',NULL,'2024-12-07 05:15:27.393351'),(4,1,5,'2024-12-07 05:23:30.754833','2024-12-07 05:23:30.771446','2024-12-07 05:23:30.771446'),(5,1,6,'2024-12-08 16:18:03.158567','2024-12-08 16:18:03.224335','2024-12-08 16:18:03.225328'),(6,1,7,'2024-12-08 16:19:10.390472','2024-12-08 16:19:10.393888','2024-12-08 16:19:10.394903');
/*!40000 ALTER TABLE `myapp_userprofile` ENABLE KEYS */;

--
-- Dumping routines for database 'roadwatch'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-10 21:36:27
