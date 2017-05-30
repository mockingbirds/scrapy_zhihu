/*
Navicat MySQL Data Transfer

Source Server         : scrapystudy
Source Server Version : 50718
Source Host           : localhost:3306
Source Database       : lagoudatabase

Target Server Type    : MYSQL
Target Server Version : 50718
File Encoding         : 65001

Date: 2017-05-30 21:04:55
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for lagou_table
-- ----------------------------
DROP TABLE IF EXISTS `lagou_table`;
CREATE TABLE `lagou_table` (
  `url` varchar(300) NOT NULL,
  `url_obj_id` varchar(50) NOT NULL,
  `title` varchar(100) NOT NULL,
  `salary` varchar(20) DEFAULT NULL,
  `job_city` varchar(10) DEFAULT NULL,
  `work_years` varchar(100) DEFAULT NULL,
  `degree_need` varchar(30) DEFAULT NULL,
  `job_type` varchar(20) DEFAULT NULL,
  `publish_time` varchar(20) DEFAULT NULL,
  `tags` varchar(100) DEFAULT NULL,
  `job_advantage` varchar(1000) DEFAULT NULL,
  `job_desc` longtext,
  `job_addr` varchar(50) DEFAULT NULL,
  `company_url` varchar(300) DEFAULT NULL,
  `company_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`url_obj_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;
