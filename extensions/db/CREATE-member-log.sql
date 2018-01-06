CREATE TABLE `mysqldb`.`tablename` (
  `id_member-list` BIGINT NOT NULL AUTO_INCREMENT,
  `time` VARCHAR(45) NOT NULL,
  `guild-id` VARCHAR(45) NOT NULL,
  `guild-name` LONGTEXT NOT NULL,
  `user-id` VARCHAR(45) NOT NULL,
  `user-name` LONGTEXT NOT NULL,
  `action` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_member-list`))
ROW_FORMAT=COMPRESSED;