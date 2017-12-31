CREATE TABLE `mysqldb`.`tablename` (
  `id_DM` BIGINT NOT NULL AUTO_INCREMENT,
  `time` VARCHAR(45) NULL,
  `dm_channel-id` VARCHAR(45) NULL,
  `user-id` VARCHAR(45) NULL,
  `user-name` LONGTEXT NULL,
  `message-id` VARCHAR(45) NOT NULL,
  `content` LONGTEXT NULL,
  `attachmenturl` LONGTEXT NULL,
  `attachmentfilename` LONGTEXT NULL,
  PRIMARY KEY (`id_DM`));