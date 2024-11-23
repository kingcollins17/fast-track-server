DROP DATABASE fast_track_db;

CREATE DATABASE fast_track_db;

use fast_track_db;

DROP TABLE IF EXISTS `accounts`;

CREATE TABLE `accounts` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) UNIQUE NOT NULL,
  `email` VARCHAR(255) UNIQUE NOT NULL,
  `fullname` VARCHAR(255),
  `password` VARCHAR(255),
  `active` BOOLEAN NOT NULL DEFAULT TRUE,
  `email_verified` BOOLEAN NOT NULL DEFAULT TRUE,
  `fcm_reg_token` VARCHAR(1024),
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY `pk_id`(`id`)
) ENGINE = InnoDB;


DROP TABLE IF EXISTS `organizations`;

CREATE TABLE `organizations` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `organization_name` VARCHAR(255),
  `type` ENUM ('default', 'standard', 'enterprise') NOT NULL DEFAULT 'default',
  `member_capacity` INT UNSIGNED NOT NULL DEFAULT 100,
  `max_teams_per_project` INT UNSIGNED NOT NULL DEFAULT 4,
  `owner_id` INT UNSIGNED NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(), 
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY `pk_id`(`id`),
  FOREIGN KEY (`owner_id`)
    REFERENCES `accounts` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
) ENGINE = InnoDB;


DROP TABLE IF EXISTS `projects`;
CREATE TABLE `projects` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `project_name` VARCHAR(255),
  `max_issue_per_feature` INT UNSIGNED NOT NULL DEFAULT 100,
  `max_teams` INT UNSIGNED NOT NULL DEFAULT 4,
  `max_team_members` INT UNSIGNED NOT NULL DEFAULT 4,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `organization_id` INT UNSIGNED NOT NULL, 
  PRIMARY KEY `pk_id`(`id`),
  FOREIGN KEY (`organization_id`)
    REFERENCES `organizations` (`id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
) ENGINE = InnoDB;

DROP TABLE IF EXISTS `organization_roles`;
CREATE TABLE `organization_roles` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `role` VARCHAR(100) NOT NULL DEFAULT 'default',
  `can_create_issue` BOOLEAN NOT NULL DEFAULT FALSE,
  `can_assign_tasks` BOOLEAN NOT NULL DEFAULT FALSE,
  `can_review_tasks` BOOLEAN NOT NULL DEFAULT FALSE,
  `can_create_feature` BOOLEAN NOT NULL DEFAULT FALSE,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `project_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY `pk_id`(`id`)
) ENGINE = InnoDB;


DROP TABLE IF EXISTS `organization_members`;
CREATE TABLE `organization_members` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `role_id` INT UNSIGNED NOT NULL, 
  `member_id` INT UNSIGNED NOT NULL,
  `organization_id` INT UNSIGNED NOT NULL,
  `joined_at` DATETIME NOT NULL DEFAULT NOW(),
  UNIQUE (`member_id`, `organization_id`),
    FOREIGN KEY (`organization_id`)
    REFERENCES `organizations` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
      FOREIGN KEY (`member_id`)
      REFERENCES `accounts` (`id`)
      ON DELETE NO ACTION
      ON UPDATE CASCADE,
      FOREIGN KEY (`role_id`)
       REFERENCES `organization_roles` (`id`)
       ON DELETE NO ACTION
       ON UPDATE CASCADE,
  PRIMARY KEY `pk_id`(`id`)
) ENGINE = InnoDB;


DROP TABLE IF EXISTS `teams`;
CREATE TABLE `teams` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `team_name` VARCHAR(255) NOT NULL,
  `type` ENUM ('default', 'standard') DEFAULT 'default',
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `project_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY `pk_id`(`id`),
  CONSTRAINT `fk_teams_projects`
    FOREIGN KEY (`project_id`)
    REFERENCES `projects` (`id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
) ENGINE = InnoDB;

DROP TABLE IF EXISTS `team_members`;
CREATE TABLE `team_members` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `team_id` INT UNSIGNED NOT NULL,
  `account_id` INT UNSIGNED NOT NULL,
  `joined_at` DATETIME NOT NULL DEFAULT NOW(),
  FOREIGN KEY (`team_id`)
    REFERENCES `teams` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (`account_id`)
     REFERENCES `accounts` (`id`)
     ON DELETE CASCADE
     ON UPDATE CASCADE,
  PRIMARY KEY `pk_id`(`id`),
  UNIQUE (`team_id`, `account_id`)
) ENGINE = InnoDB;

DROP TABLE IF EXISTS `features`;
CREATE TABLE `features` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255),
  `description` TEXT,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `deadline` DATETIME,
  `project_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY `pk_id`(`id`),
  FOREIGN KEY (`project_id`)
    REFERENCES `projects` (`id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
) ENGINE = InnoDB;


DROP TABLE IF EXISTS `issues`;
CREATE TABLE `issues` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255),
  `description` TEXT,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `deadline` DATETIME,
  `assigned_team_id` INT UNSIGNED NOT NULL,
  `feature_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY `pk_id`(`id`),
  FOREIGN KEY (`assigned_team_id`)
    REFERENCES `teams` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (`feature_id`)
     REFERENCES `features` (`id`)
     ON DELETE CASCADE
     ON UPDATE CASCADE
) ENGINE = InnoDB;

DROP TABLE IF EXISTS `tasks`;
CREATE TABLE `tasks` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255),
  `status` ENUM ('pending', 'todo', 'in_progress', 'to_be_reviewed', 'in_review', 'done'),
  `description` TEXT,
  `deadline` DATETIME,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `assignee_id` INT UNSIGNED NOT NULL,
  `issue_id` INT UNSIGNED NOT NULL,
   FOREIGN KEY (`assignee_id`)
    REFERENCES `accounts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
   FOREIGN KEY (`issue_id`)
    REFERENCES `issues` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  PRIMARY KEY `pk_id`(`id`)
) ENGINE = InnoDB;

DROP TABLE IF EXISTS `task_requirements`;
CREATE TABLE `task_requirements` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `requirement` VARCHAR(255),
  `status` ENUM ('pending', 'submitted', 'passed', 'failed'),
  `resources` JSON,
  `task_id` INT UNSIGNED NOT NULL,
  `assignee_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY `pk_id`(`id`),
  FOREIGN KEY (`task_id`)
    REFERENCES `tasks` (`id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  FOREIGN KEY (`assignee_id`)
   REFERENCES `accounts` (`id`)
   ON DELETE NO ACTION
   ON UPDATE CASCADE
) ENGINE = InnoDB;


DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `comment` TEXT,
  `commenter_id` INT UNSIGNED NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `feature_id` INT UNSIGNED,
  `issue_id` INT UNSIGNED,
  `task_id` INT UNSIGNED,  
    FOREIGN KEY (`feature_id`)
    REFERENCES `features` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,  
    FOREIGN KEY (`issue_id`)
    REFERENCES `issues` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,  
    FOREIGN KEY (`task_id`)
    REFERENCES `tasks` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,  
    FOREIGN KEY (`commenter_id`)
    REFERENCES `accounts` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  PRIMARY KEY `pk_id`(`id`)
) ENGINE = InnoDB;


DROP TABLE IF EXISTS `comment_tags`;
CREATE TABLE `comment_tags` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `account_id` INT UNSIGNED NOT NULL,
  `comment_id` INT UNSIGNED NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
   FOREIGN KEY (`account_id`)
    REFERENCES `accounts` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,  
   FOREIGN KEY (`comment_id`)
    REFERENCES `comments` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  PRIMARY KEY `pk_id`(`id`)
) ENGINE = InnoDB;