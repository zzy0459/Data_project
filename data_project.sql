/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50744 (5.7.44)
 Source Host           : localhost:3306
 Source Schema         : data_project

 Target Server Type    : MySQL
 Target Server Version : 50744 (5.7.44)
 File Encoding         : 65001

 Date: 17/11/2024 07:42:51
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for conversation
-- ----------------------------
DROP TABLE IF EXISTS `conversation`;
CREATE TABLE `conversation`  (
  `AutoID` int(11) NOT NULL AUTO_INCREMENT,
  `ConversationID` int(11) NULL DEFAULT NULL,
  `Title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `Satisfaction` int(11) NULL DEFAULT NULL,
  `Evaluate_Content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Persona` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Accuracy` int(11) NULL DEFAULT NULL,
  `adaptability` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`AutoID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of conversation
-- ----------------------------
INSERT INTO `conversation` VALUES (1, 1, '打招呼', 8, '很好', NULL, NULL, NULL);
INSERT INTO `conversation` VALUES (2, 2, '杜甫', NULL, NULL, '你是杜甫', NULL, NULL);

-- ----------------------------
-- Table structure for message
-- ----------------------------
DROP TABLE IF EXISTS `message`;
CREATE TABLE `message`  (
  `AutoID` int(11) NOT NULL AUTO_INCREMENT,
  `MessageID` int(11) NULL DEFAULT NULL,
  `Content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `ConversationID` int(11) NULL DEFAULT NULL,
  `User` int(11) NULL DEFAULT NULL,
  `Number` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`AutoID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of message
-- ----------------------------
INSERT INTO `message` VALUES (1, 1, '你好', 1, 1, 1);
INSERT INTO `message` VALUES (2, 2, '有什么可以帮你的吗？', 1, 0, 2);
INSERT INTO `message` VALUES (3, 3, '请问8.9和8.11谁比较大？', 1, 1, 3);
INSERT INTO `message` VALUES (4, 4, '8.9比8.11小。', 1, 0, 4);
INSERT INTO `message` VALUES (5, NULL, '12.11和12.9哪个大？', 1, 1, 5);
INSERT INTO `message` VALUES (6, NULL, '$12.9$比$12.11$大。', 1, 0, 6);
INSERT INTO `message` VALUES (7, NULL, '12.141和12.89哪个大？', 1, 1, 7);
INSERT INTO `message` VALUES (8, NULL, '要比较 $12.141$ 和 $12.89$，我们可以从左到右逐位进行比较。\n\n首先，整数部分都是 $12$，所以我们比较小数部分：\n\n- $12.141$ 的小数部分是 $0.141$\n- $12.89$ 的小数部分是 $0.89$\n\n接下来比较小数部分的第一位：\n\n- $0.141$ 的第一位是 $1$\n- $0.89$ 的第一位是 $8$\n\n显然，$8 > 1$，所以 $0.89 > 0.141$。\n\n因此，$12.89 > 12.141$。', 1, 0, 8);

SET FOREIGN_KEY_CHECKS = 1;
