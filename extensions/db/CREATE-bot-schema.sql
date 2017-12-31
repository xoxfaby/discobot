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
  PRIMARY KEY (`id_guildlog`),
  UNIQUE INDEX `guildid_UNIQUE` (`guildid` ASC));

CREATE TABLE `mysqldb`.`_errorlog` (
  `id_errorlog` INT NOT NULL AUTO_INCREMENT,
  `time` VARCHAR(45) NOT NULL,
  `guild-id` VARCHAR(45) NOT NULL,
  `user-id` VARCHAR(45) NOT NULL,
  `user-name` LONGTEXT NOT NULL,
  `message-id` VARCHAR(45) NOT NULL,
  `errormessage` LONGTEXT NOT NULL,
  `content` LONGTEXT NOT NULL,
  PRIMARY KEY (`id_errorlog`));

CREATE TABLE `mysqldb`.`_weathertable` (
  `id_weathertable` INT NOT NULL AUTO_INCREMENT,
  `user-id` VARCHAR(45) NOT NULL,
  `zipcode` INT NOT NULL,
  PRIMARY KEY (`id_weathertable`),
  UNIQUE INDEX `user-id_UNIQUE` (`user-id` ASC))
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;

CREATE TABLE `mysqldb`.`_encountered-users` (
  `id_encountered-users` INT NOT NULL AUTO_INCREMENT,
  `firstseen` VARCHAR(45) NOT NULL,
  `user-id` VARCHAR(45) NOT NULL,
  `user-name` LONGTEXT NOT NULL,
  PRIMARY KEY (`id_encountered-users`),
  UNIQUE INDEX `user-id_UNIQUE` (`user-id` ASC));

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
  `content` LONGTEXT NOT NULL,
  PRIMARY KEY (`id_commandtable`));