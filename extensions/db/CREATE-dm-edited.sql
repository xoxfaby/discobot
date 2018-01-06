CREATE TABLE `mysqldb`.`tablename` (
  `id_edited` BIGINT NOT NULL AUTO_INCREMENT,
  `time` VARCHAR(45) NULL,
  `dm_channel-id` VARCHAR(45) NULL,
  `user-id` VARCHAR(45) NULL,
  `user-name` LONGTEXT NULL,
  `message-id` VARCHAR(45) NOT NULL,
  `before-content` LONGTEXT NULL,
  `after-content` LONGTEXT NULL,
  `before-attachmenturl` LONGTEXT NULL,
  `before-attachmentfilename` LONGTEXT NULL,
  `after-attachmenturl` LONGTEXT NULL,
  `after-attachmentfilename` LONGTEXT NULL,
  PRIMARY KEY (`id_edited`))
ROW_FORMAT=COMPRESSED;