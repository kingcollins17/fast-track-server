use fast_track_db;

DROP TABLE IF EXISTS `tasks`;
CREATE TABLE `tasks` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `status` ENUM ('pending', 'todo', 'review', 'done') DEFAULT 'pending',
  `deadline` datetime NOT NULL,
  `completed_at` DATETIME,
  `created_at` datetime not null DEFAULT NOW(),
  `updated_at` datetime not null DEFAULT NOW() ON UPDATE NOW(),
  `feature_id` INT UNSIGNED NOT NULL,
  `parent_task_id` INT UNSIGNED,
  `assigned_team_id` INT UNSIGNED,
  `assigned_account_id` INT UNSIGNED,
    FOREIGN KEY (`feature_id`)
    REFERENCES `features` (`id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
    FOREIGN KEY (`parent_task_id`)
    REFERENCES `tasks` (`id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,FOREIGN KEY (`assigned_team_id`)
    REFERENCES `teams` (`id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,FOREIGN KEY (`assigned_account_id`)
    REFERENCES `accounts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,

  PRIMARY KEY `pk_id`(`id`)
) ENGINE = InnoDB;


DROP TABLE IF EXISTS `task_dependencies`;
CREATE TABLE `task_dependencies` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `depender_id` INT UNSIGNED NOT NULL,
  `depended_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY `pk_id`(`id`),
  FOREIGN KEY (`depender_id`)
    REFERENCES `tasks` (`id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  FOREIGN KEY (`depended_id`)
    REFERENCES `tasks` (`id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
) ENGINE = InnoDB;