/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE TABLE IF NOT EXISTS `artists` (
  `record_id` int(11) NOT NULL AUTO_INCREMENT,
  `track_id` text NOT NULL,
  `artist` text DEFAULT NULL,
  PRIMARY KEY (`record_id`)
) ENGINE=InnoDB AUTO_INCREMENT=45693 DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `music` (
  `track_id` text DEFAULT NULL,
  `track` text DEFAULT NULL,
  `time` text DEFAULT NULL,
  `album` text DEFAULT NULL,
  `play_time` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `music_features` (
  `record_id` int(11) NOT NULL AUTO_INCREMENT,
  `track_id` text DEFAULT NULL,
  `acousticness` float DEFAULT NULL,
  `danceability` float DEFAULT NULL,
  `energy` float DEFAULT NULL,
  `instrumentalness` float DEFAULT NULL,
  `key` int(11) DEFAULT NULL,
  `liveness` float DEFAULT NULL,
  `loudness` float DEFAULT NULL,
  `mode` tinyint(4) DEFAULT NULL,
  `speechiness` float DEFAULT NULL,
  `tempo` int(11) DEFAULT NULL,
  `valence` float DEFAULT NULL,
  PRIMARY KEY (`record_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18584 DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `popularity` (
  `record_id` int(11) NOT NULL AUTO_INCREMENT,
  `track_id` text DEFAULT NULL,
  `popularity` int(11) DEFAULT NULL,
  PRIMARY KEY (`record_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18792 DEFAULT CHARSET=utf8mb4;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
