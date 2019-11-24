-- MySQL dump 10.16  Distrib 10.1.34-MariaDB, for Win32 (AMD64)
--
-- Host: localhost    Database: ihome
-- ------------------------------------------------------
-- Server version	10.1.34-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('857c87d9ba50');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_area_info`
--

DROP TABLE IF EXISTS `ih_area_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_area_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_area_info`
--

LOCK TABLES `ih_area_info` WRITE;
/*!40000 ALTER TABLE `ih_area_info` DISABLE KEYS */;
INSERT INTO `ih_area_info` VALUES (NULL,NULL,1,'东城区'),(NULL,NULL,2,'西城区'),(NULL,NULL,3,'朝阳区'),(NULL,NULL,4,'海淀区'),(NULL,NULL,5,'昌平区'),(NULL,NULL,6,'丰台区'),(NULL,NULL,7,'房山区'),(NULL,NULL,8,'通州区'),(NULL,NULL,9,'顺义区'),(NULL,NULL,10,'大兴区'),(NULL,NULL,11,'怀柔区'),(NULL,NULL,12,'平谷区'),(NULL,NULL,13,'密云区'),(NULL,NULL,14,'延庆区'),(NULL,NULL,15,'石景山区');
/*!40000 ALTER TABLE `ih_area_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_facility_info`
--

DROP TABLE IF EXISTS `ih_facility_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_facility_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_facility_info`
--

LOCK TABLES `ih_facility_info` WRITE;
/*!40000 ALTER TABLE `ih_facility_info` DISABLE KEYS */;
INSERT INTO `ih_facility_info` VALUES (NULL,NULL,1,'无线网络'),(NULL,NULL,2,'热水淋浴'),(NULL,NULL,3,'空调'),(NULL,NULL,4,'暖气'),(NULL,NULL,5,'允许吸烟'),(NULL,NULL,6,'饮水设备'),(NULL,NULL,7,'牙具'),(NULL,NULL,8,'香皂'),(NULL,NULL,9,'拖鞋'),(NULL,NULL,10,'手纸'),(NULL,NULL,11,'毛巾'),(NULL,NULL,12,'沐浴露、洗发露'),(NULL,NULL,13,'冰箱'),(NULL,NULL,14,'洗衣机'),(NULL,NULL,15,'电梯'),(NULL,NULL,16,'允许做饭'),(NULL,NULL,17,'允许带宠物'),(NULL,NULL,18,'允许聚会'),(NULL,NULL,19,'门禁系统'),(NULL,NULL,20,'停车位'),(NULL,NULL,21,'有线网络'),(NULL,NULL,22,'电视'),(NULL,NULL,23,'浴缸');
/*!40000 ALTER TABLE `ih_facility_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_house_facility`
--

DROP TABLE IF EXISTS `ih_house_facility`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_house_facility` (
  `house_id` int(11) NOT NULL,
  `facility_id` int(11) NOT NULL,
  PRIMARY KEY (`house_id`,`facility_id`),
  KEY `facility_id` (`facility_id`),
  CONSTRAINT `ih_house_facility_ibfk_1` FOREIGN KEY (`facility_id`) REFERENCES `ih_facility_info` (`id`),
  CONSTRAINT `ih_house_facility_ibfk_2` FOREIGN KEY (`house_id`) REFERENCES `ih_house_info` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_house_facility`
--

LOCK TABLES `ih_house_facility` WRITE;
/*!40000 ALTER TABLE `ih_house_facility` DISABLE KEYS */;
INSERT INTO `ih_house_facility` VALUES (1,1),(1,3),(1,5),(1,7),(1,12),(2,1),(2,9),(3,1),(3,3),(3,7),(3,9),(3,19);
/*!40000 ALTER TABLE `ih_house_facility` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_house_image`
--

DROP TABLE IF EXISTS `ih_house_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_house_image` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` int(11) NOT NULL,
  `url` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `house_id` (`house_id`),
  CONSTRAINT `ih_house_image_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `ih_house_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_house_image`
--

LOCK TABLES `ih_house_image` WRITE;
/*!40000 ALTER TABLE `ih_house_image` DISABLE KEYS */;
INSERT INTO `ih_house_image` VALUES ('2019-11-19 17:48:35','2019-11-19 17:48:35',1,1,'FsxYqPJ-fJtVZZH2LEshL7o9Ivxn'),('2019-11-19 17:49:12','2019-11-19 17:49:12',2,1,'FsHyv4WUHKUCpuIRftvwSO_FJWOG'),('2019-11-22 16:02:11','2019-11-22 16:02:11',3,3,'FsHyv4WUHKUCpuIRftvwSO_FJWOG'),('2019-11-23 18:11:39','2019-11-23 18:11:41',5,2,'FsHyv4WUHKUCpuIRftvwSO_FJWOG');
/*!40000 ALTER TABLE `ih_house_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_house_info`
--

DROP TABLE IF EXISTS `ih_house_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_house_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `area_id` int(11) NOT NULL,
  `title` varchar(64) NOT NULL,
  `price` int(11) DEFAULT NULL,
  `address` varchar(512) DEFAULT NULL,
  `room_count` int(11) DEFAULT NULL,
  `acreage` int(11) DEFAULT NULL,
  `unit` varchar(32) DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  `beds` varchar(64) DEFAULT NULL,
  `deposit` int(11) DEFAULT NULL,
  `min_days` int(11) DEFAULT NULL,
  `max_days` int(11) DEFAULT NULL,
  `order_count` int(11) DEFAULT NULL,
  `index_image_url` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `area_id` (`area_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `ih_house_info_ibfk_1` FOREIGN KEY (`area_id`) REFERENCES `ih_area_info` (`id`),
  CONSTRAINT `ih_house_info_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `ih_user_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_house_info`
--

LOCK TABLES `ih_house_info` WRITE;
/*!40000 ALTER TABLE `ih_house_info` DISABLE KEYS */;
INSERT INTO `ih_house_info` VALUES ('2019-11-19 17:46:02','2019-11-24 21:19:38',1,8,1,'测试1',39900,'测试地址1',7,199,'复式',7,'双人床7张',100000,1,0,1,'FsxYqPJ-fJtVZZH2LEshL7o9Ivxn'),('2019-11-19 20:13:49','2019-11-19 20:13:49',2,8,1,'测试2',12200,'测试2',5,120,'三室两厅',7,'双人床7张',20000,1,0,0,'FsHyv4WUHKUCpuIRftvwSO_FJWOG'),('2019-11-22 16:01:50','2019-11-22 16:02:11',3,8,1,'测试3',14400,'东城区',4,121,'三室两厅',4,'双人床7张',44400,1,0,0,'FsHyv4WUHKUCpuIRftvwSO_FJWOG');
/*!40000 ALTER TABLE `ih_house_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_order_info`
--

DROP TABLE IF EXISTS `ih_order_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_order_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `begin_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `days` int(11) NOT NULL,
  `house_price` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `status` enum('WAIT_ACCEPT','WAIT_PAYMENT','PAID','WAIT_COMMENT','COMPLETE','CANCELED','REJECTED') DEFAULT NULL,
  `comment` text,
  `trade_no` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `house_id` (`house_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_ih_order_info_status` (`status`),
  CONSTRAINT `ih_order_info_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `ih_house_info` (`id`),
  CONSTRAINT `ih_order_info_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `ih_user_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_order_info`
--

LOCK TABLES `ih_order_info` WRITE;
/*!40000 ALTER TABLE `ih_order_info` DISABLE KEYS */;
INSERT INTO `ih_order_info` VALUES ('2019-11-24 14:17:07','2019-11-24 21:19:38',1,10,1,'2019-11-24 00:00:00','2019-11-25 00:00:00',2,39900,79800,'COMPLETE','真不错啊','2019112422001427641000099895'),('2019-11-24 14:22:45','2019-11-24 14:24:20',2,10,2,'2019-11-24 00:00:00','2019-11-24 00:00:00',1,12200,12200,'REJECTED','任性',NULL),('2019-11-24 14:33:05','2019-11-24 14:34:52',3,10,2,'2019-11-26 00:00:00','2019-11-26 00:00:00',1,12200,12200,'REJECTED','还是任性',NULL);
/*!40000 ALTER TABLE `ih_order_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_user_profile`
--

DROP TABLE IF EXISTS `ih_user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_user_profile` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `mobile` varchar(11) NOT NULL,
  `real_name` varchar(32) DEFAULT NULL,
  `id_card` varchar(20) DEFAULT NULL,
  `avatar_url` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_user_profile`
--

LOCK TABLES `ih_user_profile` WRITE;
/*!40000 ALTER TABLE `ih_user_profile` DISABLE KEYS */;
INSERT INTO `ih_user_profile` VALUES ('2019-11-13 14:24:39','2019-11-18 20:32:56',4,'caiyun','pbkdf2:sha256:150000$ygWb0wY2$04afdc353d4426f2177faae95d1290c7a98d80e7073a0f4b9faf21bd997f5d6e','13676977767','彩云','411524199709285135','Fos7KrDJ_rTR_Lqjjg_R8M5aX2Sw'),('2019-11-13 15:05:58','2019-11-13 15:05:58',5,'18111111111','pbkdf2:sha256:150000$VOCMAKHK$6e41c0ad4c934eb4bfccfd592bcd071cde4888a9914d0df63a50c425dddd5222','18111111111',NULL,NULL,NULL),('2019-11-13 15:45:11','2019-11-13 15:45:11',6,'18111111112','pbkdf2:sha256:150000$XOj9htVZ$a04ceabe3a4257c314dcdd0953fb3f40f8e58078ceda3a411f4de27b166f2302','18111111112',NULL,NULL,NULL),('2019-11-16 00:36:37','2019-11-18 20:03:31',8,'rusi','pbkdf2:sha256:150000$WHcmInON$1055c203bd01f2b2fff5e6a67e6283fe75a52dc2e6448a21b7bbb23b68672d6d','18538383342','罗拉','411524199709285135','Fos7KrDJ_rTR_Lqjjg_R8M5aX2Sw'),('2019-11-20 18:52:30','2019-11-24 21:09:04',10,'彩云','pbkdf2:sha256:150000$rEgRa6xX$8ab5cf27d035315f50bc6461242f0e038772f91e7ec88fe7521e0d86053c2f44','13178901928',NULL,NULL,'FpnMpF6KP-DoSfTX3ifxioLJ9tF7');
/*!40000 ALTER TABLE `ih_user_profile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-24 22:55:51
