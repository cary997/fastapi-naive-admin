/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 80300
 Source Host           : localhost:3306
 Source Schema         : fastapi_naive

 Target Server Type    : MySQL
 Target Server Version : 80300
 File Encoding         : 65001

 Date: 10/03/2024 02:44:04
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_menus
-- ----------------------------
DROP TABLE IF EXISTS `auth_menus`;
CREATE TABLE `auth_menus`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `create_at` bigint(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_at` bigint(0) NULL DEFAULT NULL COMMENT '更新时间',
  `path` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'url',
  `name` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '唯一标识或外链链接',
  `redirect` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '重定向url',
  `component` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '组件路径',
  `meta` json NULL COMMENT '菜单元数据',
  `parent` bigint(0) NULL DEFAULT NULL COMMENT '上级菜单',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `path`(`path`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `idx_auth_menus_name_b7e822`(`name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '菜单信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_menus
-- ----------------------------
INSERT INTO `auth_menus` VALUES (1, 1708506083, 1708780924, '/auth/', 'auth', NULL, NULL, '{\"icon\": \"AuthIcon\", \"rank\": 2, \"title\": \"权限管理\", \"en_title\": \"Auth Manage\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 1, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', NULL);
INSERT INTO `auth_menus` VALUES (2, 1708506547, 1708506547, '/auth/users/', 'auth_users', NULL, NULL, '{\"icon\": null, \"rank\": 1, \"title\": \"用户管理\", \"en_title\": \"Users Manage\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": true, \"menu_type\": 2, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 1);
INSERT INTO `auth_menus` VALUES (3, 1708506615, 1708506615, '/auth/roles/', 'auth_roles', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"角色管理\", \"en_title\": \"Roles Manage\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": true, \"menu_type\": 2, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 1);
INSERT INTO `auth_menus` VALUES (4, 1708506653, 1708611990, '/auth/menus/', 'auth_menus', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"菜单管理\", \"en_title\": \"Menus Manage\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": true, \"menu_type\": 2, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 1);
INSERT INTO `auth_menus` VALUES (5, 1708506811, 1708972629, '/extlinks/', 'extlinks', NULL, NULL, '{\"icon\": null, \"rank\": 999, \"title\": \"外部链接\", \"en_title\": \"External Links\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 1, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', NULL);
INSERT INTO `auth_menus` VALUES (6, 1708591816, 1708614313, '/auth/users/add', 'auth_users_add', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"新建用户\", \"en_title\": \"New User\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 3, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 2);
INSERT INTO `auth_menus` VALUES (7, 1708614386, 1708614386, '/auth/users/set/', 'auth_users_set', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"编辑用户\", \"en_title\": \"Edit User\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 3, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 2);
INSERT INTO `auth_menus` VALUES (8, 1708614411, 1708614411, '/auth/users/del/', 'auth_users_del', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"删除用户\", \"en_title\": \"Delete User\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 3, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 2);
INSERT INTO `auth_menus` VALUES (9, 1708614553, 1708614873, '/auth/users/bulkdel/', 'auth_users_bulkdel', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"批量删除用户\", \"en_title\": \"Bulk Delete Users\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 3, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 2);
INSERT INTO `auth_menus` VALUES (10, 1708614673, 1708614888, '/auth/users/bulkset/', 'auth_users_bulkset', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"批量编辑用户\", \"en_title\": \"Bulk Edit Users\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 3, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 2);
INSERT INTO `auth_menus` VALUES (11, 1708614838, 1708614854, '/auth/users/details/', 'auth_users_details', NULL, NULL, '{\"icon\": null, \"rank\": 0, \"title\": \"用户详情\", \"en_title\": \"User Details\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 3, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 2);
INSERT INTO `auth_menus` VALUES (12, 1708615169, 1708615169, '/auth/users/pwdset/', 'auth_users_pwdset', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"重置密码\", \"en_title\": \"Reset Password\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 3, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 2);
INSERT INTO `auth_menus` VALUES (13, 1708623931, 1708623931, '/auth/roles/add/', 'auth_roles_add', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"创建角色\", \"en_title\": \"Create Role\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 3, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 3);
INSERT INTO `auth_menus` VALUES (14, 1708623998, 1708623998, '/auth/roles/del/', 'auth_roles_del', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"删除角色\", \"en_title\": \"Delete Role\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 3, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 3);
INSERT INTO `auth_menus` VALUES (15, 1708624044, 1708624044, '/auth/roles/set/', 'auth_roles_set', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"编辑角色\", \"en_title\": \"Edit Role\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 3, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 3);
INSERT INTO `auth_menus` VALUES (16, 1708624127, 1708624127, '/auth/menus/add/', 'auth_menus_add', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"创建菜单\", \"en_title\": \"Create Menu\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 3, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 4);
INSERT INTO `auth_menus` VALUES (17, 1708624176, 1708624176, '/auth/menus/set/', 'auth_menus_set', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"编辑菜单\", \"en_title\": \"Edit Menu\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 3, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 4);
INSERT INTO `auth_menus` VALUES (18, 1708624219, 1708624219, '/v1/auth/menus/del/', 'auth_menus_del', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"删除菜单\", \"en_title\": \"Delete Menu\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 3, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 4);
INSERT INTO `auth_menus` VALUES (19, 1708707121, 1708707179, '/extlinks/apidocs/', 'http://127.0.0.1:8000/v1/docs', NULL, NULL, '{\"icon\": \"\", \"rank\": null, \"title\": \"Swagger\", \"en_title\": \"Swagger\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 4, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 5);
INSERT INTO `auth_menus` VALUES (20, 1708768118, 1708770288, '/extlinks/apidoc/', 'http://127.0.0.1:8000/v1/redoc', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"API文档\", \"en_title\": \"API Doc\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 4, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 5);
INSERT INTO `auth_menus` VALUES (21, 1708972698, 1708972918, '/system/', 'system', NULL, NULL, '{\"icon\": \"SettingsIcon\", \"rank\": 998, \"title\": \"系统管理\", \"en_title\": \"System Manage\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 1, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', NULL);
INSERT INTO `auth_menus` VALUES (22, 1708972797, 1709217822, '/system/settings/', 'system_settings', NULL, '', '{\"icon\": null, \"rank\": null, \"title\": \"系统设置\", \"en_title\": \"System Settings\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 2, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 21);
INSERT INTO `auth_menus` VALUES (23, 1709090788, 1709090788, '/auth/users/otpreset/', 'auth_users_otpreset', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"重置Totp\", \"en_title\": \"Reset Totp\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 3, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 2);
INSERT INTO `auth_menus` VALUES (24, 1709435070, 1709435086, '/system/info/', 'system_info', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"系统信息\", \"en_title\": \"System Info\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 2, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 21);
INSERT INTO `auth_menus` VALUES (25, 1710005949, 1710005968, '/system/settings/set/', 'system_settings_set', NULL, NULL, '{\"icon\": null, \"rank\": null, \"title\": \"保存\", \"en_title\": \"Save\", \"frameSrc\": null, \"showLink\": true, \"hiddenTag\": false, \"keepAlive\": false, \"menu_type\": 3, \"showParent\": true, \"frameLoading\": true, \"enterTransition\": null, \"leaveTransition\": null}', 22);

-- ----------------------------
-- Table structure for auth_roles
-- ----------------------------
DROP TABLE IF EXISTS `auth_roles`;
CREATE TABLE `auth_roles`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `create_at` bigint(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_at` bigint(0) NULL DEFAULT NULL COMMENT '更新时间',
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色标识',
  `nickname` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色显示名称',
  `desc` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `role_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT 'True:启用 False:禁用',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `idx_auth_roles_name_0d7083`(`name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '角色信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_roles
-- ----------------------------
INSERT INTO `auth_roles` VALUES (1, 1710008987, 1710008987, 'super_admin', '超级管理员', '平台内置角色,默认拥有全部权限', 1);

-- ----------------------------
-- Table structure for auth_roles_menus
-- ----------------------------
DROP TABLE IF EXISTS `auth_roles_menus`;
CREATE TABLE `auth_roles_menus`  (
  `auth_roles_id` bigint(0) NOT NULL,
  `auth_menus_id` bigint(0) NOT NULL,
  INDEX `auth_roles_id`(`auth_roles_id`) USING BTREE,
  INDEX `auth_menus_id`(`auth_menus_id`) USING BTREE,
  CONSTRAINT `auth_roles_menus_ibfk_1` FOREIGN KEY (`auth_roles_id`) REFERENCES `auth_roles` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `auth_roles_menus_ibfk_2` FOREIGN KEY (`auth_menus_id`) REFERENCES `auth_menus` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_roles_menus
-- ----------------------------

-- ----------------------------
-- Table structure for auth_users
-- ----------------------------
DROP TABLE IF EXISTS `auth_users`;
CREATE TABLE `auth_users`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `create_at` bigint(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_at` bigint(0) NULL DEFAULT NULL COMMENT '更新时间',
  `username` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户名',
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '密码',
  `nickname` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '显示名称',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号',
  `email` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮箱',
  `user_type` smallint(0) NOT NULL DEFAULT 1 COMMENT '用户类型(1=local,2=ldap)',
  `user_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT 'True:启用 False:禁用',
  `totp` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'otp Key',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE,
  UNIQUE INDEX `phone`(`phone`) USING BTREE,
  INDEX `idx_auth_users_usernam_f200e3`(`username`, `user_status`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_users
-- ----------------------------
INSERT INTO `auth_users` VALUES (1, 1710008869, 1710008869, 'admin', '$argon2id$v=19$m=65536,t=3,p=4$0xoDwPhfixHiPKd0DmEMgQ$BlUbtCOEZbv4zohU7QV5/vihwPkY8vHdDTMrZJcsm7A', '超管', '', '', 1, 1, NULL);

-- ----------------------------
-- Table structure for auth_users_roles
-- ----------------------------
DROP TABLE IF EXISTS `auth_users_roles`;
CREATE TABLE `auth_users_roles`  (
  `auth_users_id` bigint(0) NOT NULL,
  `auth_roles_id` bigint(0) NOT NULL,
  INDEX `auth_users_id`(`auth_users_id`) USING BTREE,
  INDEX `auth_roles_id`(`auth_roles_id`) USING BTREE,
  CONSTRAINT `auth_users_roles_ibfk_1` FOREIGN KEY (`auth_users_id`) REFERENCES `auth_users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `auth_users_roles_ibfk_2` FOREIGN KEY (`auth_roles_id`) REFERENCES `auth_roles` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_users_roles
-- ----------------------------
INSERT INTO `auth_users_roles` VALUES (1, 1);

-- ----------------------------
-- Table structure for sys_settings
-- ----------------------------
DROP TABLE IF EXISTS `sys_settings`;
CREATE TABLE `sys_settings`  (
  `id` bigint(0) NOT NULL DEFAULT 1,
  `create_at` bigint(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_at` bigint(0) NULL DEFAULT NULL COMMENT '更新时间',
  `general` json NULL COMMENT '常规配置',
  `security` json NULL COMMENT '安全设置',
  `ldap` json NULL COMMENT 'ldap设置',
  `channels` json NULL COMMENT '通知渠道',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '系统设置' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_settings
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
