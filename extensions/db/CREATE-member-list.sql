CREATE TABLE `mysqldb`.`tablename` (
  `id_member-list` BIGINT NOT NULL AUTO_INCREMENT,
  `user-id` VARCHAR(45) NOT NULL,
  `user-name` LONGTEXT NOT NULL,
  PRIMARY KEY (`id_member-list`))
ROW_FORMAT=COMPRESSED;