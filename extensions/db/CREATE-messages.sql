CREATE TABLE `mysqldb`.`tablename` (
  `id_messages` BIGINT NOT NULL AUTO_INCREMENT,
  `time` VARCHAR(45) NOT NULL,
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
  PRIMARY KEY (`id_messages`));