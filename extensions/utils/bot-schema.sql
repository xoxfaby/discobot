CREATE SCHEMA `mysqldb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;

CREATE TABLE `mysqldb`.`_guildlog` (
  `id_guildlog` INT NOT NULL AUTO_INCREMENT,
  `firstseen` VARCHAR(45) NOT NULL,
  `guildid` VARCHAR(45) NOT NULL,
  `guildname` LONGTEXT NOT NULL,
  `largeguild` TINYINT NOT NULL,
  `leavetime` VARCHAR(45) NULL,
  `guild-owner-name` LONGTEXT NOT NULL,
  `guild-owner-id` VARCHAR(45) NOT NULL,
  `number-users-on-join` INT NOT NULL,
  `guild-created-date-UTC` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`guildid`),
  KEY `idx_id_guildlog` (`id_guildlog`),
  UNIQUE INDEX `guildid_UNIQUE` (`guildid` ASC))
ROW_FORMAT=COMPRESSED;

CREATE TABLE `mysqldb`.`_errorlog` (
  `id_errorlog` INT NOT NULL AUTO_INCREMENT,
  `time` VARCHAR(45) NOT NULL,
  `guild-id` VARCHAR(45) NOT NULL,
  `user-id` VARCHAR(45) NOT NULL,
  `user-name` LONGTEXT NOT NULL,
  `message-id` VARCHAR(45) NOT NULL,
  `errormessage` LONGTEXT NOT NULL,
  `content` LONGTEXT NOT NULL,
  PRIMARY KEY (`id_errorlog`),
  KEY `idx_id_errorlog` (`id_errorlog`))
ROW_FORMAT=COMPRESSED;

CREATE TABLE `mysqldb`.`_weathertable` (
  `id_weathertable` INT NOT NULL AUTO_INCREMENT,
  `user-id` VARCHAR(45) NOT NULL,
  `zipcode` INT NOT NULL,
  PRIMARY KEY (`user-id`),
  KEY `idx_id_weathertable` (`id_weathertable`),
  UNIQUE INDEX `user-id_UNIQUE` (`user-id` ASC))
ROW_FORMAT=COMPRESSED;

CREATE TABLE `mysqldb`.`_encountered-users` (
  `id_encountered-users` INT NOT NULL AUTO_INCREMENT,
  `firstseen` VARCHAR(45) NOT NULL,
  `user-id` VARCHAR(45) NOT NULL,
  `user-name` LONGTEXT NOT NULL,
  PRIMARY KEY (`user-id`),
  KEY `idx_id_encountered-users` (`id_encountered-users`),
  UNIQUE INDEX `user-id_UNIQUE` (`user-id` ASC))
ROW_FORMAT=COMPRESSED;

CREATE TABLE `mysqldb`.`_commandtable` (
  `id_commandtable` INT NOT NULL AUTO_INCREMENT,
  `time` VARCHAR(45) NOT NULL,
  `guild-id` VARCHAR(45) NOT NULL,
  `guild-name` VARCHAR(45) NOT NULL,
  `channel-id` VARCHAR(45) NOT NULL,
  `channel-name` VARCHAR(45) NOT NULL,
  `user-id` VARCHAR(45) NOT NULL,
  `user-name` LONGTEXT NOT NULL,
  `message-id` VARCHAR(45) NOT NULL,
  `command` VARCHAR(45) NOT NULL,
  `content` LONGTEXT NOT NULL,
  PRIMARY KEY (`id_commandtable`))
ROW_FORMAT=COMPRESSED;

CREATE TABLE `mysqldb`.`_serverconfig` (
  `id_serverconfig` INT NOT NULL AUTO_INCREMENT,
  `guild-id` VARCHAR(45) NOT NULL,
  `whoconfiged` VARCHAR(45) NOT NULL,
  `lastconfiged` VARCHAR(45) NOT NULL,
  `initialchannel` VARCHAR(45) NOT NULL,
  `enablelogging` TINYINT(4) NOT NULL DEFAULT '1',
  `enableusewelcome` TINYINT(4) NOT NULL,
  `enableadminlogs` TINYINT(4) NOT NULL,
  `enablevoicelogs` TINYINT(4) NOT NULL,
  `enableawoo` VARCHAR(45) NOT NULL,
  `welcomechannel` VARCHAR(45) DEFAULT NULL,
  `adminchannel` VARCHAR(45) DEFAULT NULL,
  `voicelogchannel` VARCHAR(45) DEFAULT NULL,
  `awoochannel` varchar(45) DEFAULT NULL,
  `partmessage` varchar(2000) NOT NULL DEFAULT 'ok bye {0}',
  `welcomemessage` varchar(2000) NOT NULL DEFAULT 'welcome to {1}, {0}~',
  PRIMARY KEY (`guild-id`),
  KEY `idx_id_serverconfig` (`id_serverconfig`),
  UNIQUE KEY `guild-id_UNIQUE` (`guild-id`))
ROW_FORMAT=COMPRESSED;

CREATE TABLE `mysqldb`.`_guild_links` (
  `id_guild_links` INT NOT NULL,
  `guild-id` VARCHAR(45) NOT NULL,
  `links` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`guild-id`),
  KEY `idx_id_guild_links`(`id_guild_links`))
ROW_FORMAT=COMPRESSED;

CREATE TABLE `mysqldb`.`_messages` (
  `id_messages` BIGINT NOT NULL AUTO_INCREMENT,
  `create-time` VARCHAR(45) NOT NULL,
  `guild-id` VARCHAR(45) NOT NULL,
  `guild-name` LONGTEXT NOT NULL,
  `channel-id` VARCHAR(45) NOT NULL,
  `channel-name` LONGTEXT NOT NULL,
  `user-id` VARCHAR(45) NOT NULL,
  `user-name` LONGTEXT NOT NULL,
  `message-id` VARCHAR(45) NOT NULL,
  `content` LONGTEXT NULL,
  `attachmenturl` LONGTEXT NULL,
  `attachmentfilename` LONGTEXT NULL,
  `isedited` TINYINT NOT NULL,
  `isdeleted` TINYINT NOT NULL,
  `edit-time` VARCHAR(45) NULL,
  `delete-time` VARCHAR(45) NULL,
  `edit-before-content` LONGTEXT NULL,
  `edit-after-content` LONGTEXT NULL,
  `edit-before-attachmenturl` LONGTEXT NULL,
  `edit-before-attachmentfilename` LONGTEXT NULL,
  `edit-after-attachmenturl` LONGTEXT NULL,
  `edit-after-attachmentfilename` LONGTEXT NULL,
  PRIMARY KEY (`message-id`),
  KEY `idx_messages_guild-id` (`guild-id`),
  KEY `idx_messages_user-id` (`user-id`),
  KEY `idx_messages_channel-id` (`channel-id`),
  KEY `idx_messages_id` (`id_messages`))
ROW_FORMAT=COMPRESSED;

CREATE TABLE `mysqldb`.`_voice` (
  `id_voice` BIGINT NOT NULL AUTO_INCREMENT,
  `time` VARCHAR(45) NOT NULL,
  `guild-id` VARCHAR(45) NOT NULL,
  `guild-name` LONGTEXT NOT NULL,
  `user-id` VARCHAR(45) NOT NULL,
  `user-name` LONGTEXT NOT NULL,
  `voicechannel-id` VARCHAR(45) NOT NULL,
  `voicechannel-name` LONGTEXT NOT NULL,
  `selfdeaf` TINYINT NOT NULL,
  `selfmute` TINYINT NOT NULL,
  `serverdeaf` TINYINT NOT NULL,
  `servermute` TINYINT NOT NULL,
  PRIMARY KEY (`id_voice`))
ROW_FORMAT=COMPRESSED;

CREATE TABLE `mysqldb`.`_memberlog` (
  `id_member-list` BIGINT NOT NULL AUTO_INCREMENT,
  `time` VARCHAR(45) NOT NULL,
  `guild-id` VARCHAR(45) NOT NULL,
  `guild-name` LONGTEXT NOT NULL,
  `user-id` VARCHAR(45) NOT NULL,
  `user-name` LONGTEXT NOT NULL,
  `action` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_member-list`))
ROW_FORMAT=COMPRESSED;

CREATE TABLE `mysqldb`.`_dm_messages` (
  `id_DM` BIGINT NOT NULL AUTO_INCREMENT,
  `create-time` VARCHAR(45) NOT NULL,
  `dm_channel-id` VARCHAR(45) NOT NULL,
  `user-id` VARCHAR(45) NOT NULL,
  `user-name` LONGTEXT NOT NULL,
  `message-id` VARCHAR(45) NOT NULL,
  `content` LONGTEXT NULL,
  `attachmenturl` LONGTEXT NULL,
  `attachmentfilename` LONGTEXT NULL,
  `isedited` TINYINT NULL DEFAULT '0',
  `isdeleted` TINYINT NULL DEFAULT '0',
  `edit-time` VARCHAR(45) NULL,
  `delete-time` VARCHAR(45) NULL,
  `edit-before-content` LONGTEXT NULL,
  `edit-after-content` LONGTEXT NULL,
  `edit-before-attachmenturl` LONGTEXT NULL,
  `edit-before-attachmentfilename` LONGTEXT NULL,
  `edit-after-attachmenturl` LONGTEXT NULL,
  `edit-after-attachmentfilename` LONGTEXT NULL,
  PRIMARY KEY (`message-id`),
  KEY `idx_dm_messages_user-id` (`user-id`),
  KEY `idx_dm_messages_channel-id` (`dm_channel-id`),
  KEY `idx_dm_messages_message-id` (`id_DM`))
ROW_FORMAT=COMPRESSED;

CREATE TABLE `mysqldb`.`prefixes` (
  `idprefixes` INT NOT NULL AUTO_INCREMENT,
  `guildid` VARCHAR(45) NOT NULL,
  `prefix` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`guildid`),
  UNIQUE INDEX `guildid_UNIQUE` (`guildid` ASC),
  UNIQUE INDEX `idprefixes_UNIQUE` (`idprefixes` ASC))
ROW_FORMAT=COMPRESSED;
