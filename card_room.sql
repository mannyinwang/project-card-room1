-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema project-card-room1
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `project-card-room1` ;

-- -----------------------------------------------------
-- Schema project-card-room1
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `project-card-room1` DEFAULT CHARACTER SET utf8 ;
USE `project-card-room1` ;

-- -----------------------------------------------------
-- Table `project-card-room1`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project-card-room1`.`users` ;

CREATE TABLE IF NOT EXISTS `project-card-room1`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `balance` INT NULL,
  `photo` BLOB NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `project-card-room1`.`game_types`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project-card-room1`.`game_types` ;

CREATE TABLE IF NOT EXISTS `project-card-room1`.`game_types` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `game_name` VARCHAR(255) NULL,
  `time_limit` INT NULL,
  `min_players` INT NULL,
  `max_players` INT NULL,
  `ante` INT NULL,
  `max_raise` INT NULL,
  `created_at` DATETIME NULL,
  `update_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `project-card-room1`.`games`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project-card-room1`.`games` ;

CREATE TABLE IF NOT EXISTS `project-card-room1`.`games` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `game_type_id` INT NOT NULL,
  `game_status` INT NULL,
  `pot` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_games_game_types1_idx` (`game_type_id` ASC) VISIBLE,
  CONSTRAINT `fk_games_game_types1`
    FOREIGN KEY (`game_type_id`)
    REFERENCES `project-card-room1`.`game_types` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `project-card-room1`.`cards`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project-card-room1`.`cards` ;

CREATE TABLE IF NOT EXISTS `project-card-room1`.`cards` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `number` INT NULL,
  `suit` INT NULL,
  `face_up` TINYINT NULL,
  `game_id` INT NOT NULL,
  `player_id` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_cards_games1_idx` (`game_id` ASC) VISIBLE,
  INDEX `fk_cards_users1_idx` (`player_id` ASC) VISIBLE,
  CONSTRAINT `fk_cards_games1`
    FOREIGN KEY (`game_id`)
    REFERENCES `project-card-room1`.`games` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_cards_users1`
    FOREIGN KEY (`player_id`)
    REFERENCES `project-card-room1`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `project-card-room1`.`plays`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project-card-room1`.`plays` ;

CREATE TABLE IF NOT EXISTS `project-card-room1`.`plays` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `action` VARCHAR(45) NULL,
  `amount` INT NULL,
  `card_id` INT NULL,
  `game_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_plays_games1_idx` (`game_id` ASC) VISIBLE,
  INDEX `fk_plays_cards1_idx` (`card_id` ASC) VISIBLE,
  CONSTRAINT `fk_plays_games1`
    FOREIGN KEY (`game_id`)
    REFERENCES `project-card-room1`.`games` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_plays_cards1`
    FOREIGN KEY (`card_id`)
    REFERENCES `project-card-room1`.`cards` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `project-card-room1`.`games_players`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project-card-room1`.`games_players` ;

CREATE TABLE IF NOT EXISTS `project-card-room1`.`games_players` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `result` INT NULL,
  `game_id` INT NOT NULL,
  `player_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_game_results_games1_idx` (`game_id` ASC) VISIBLE,
  INDEX `fk_game_results_users1_idx` (`player_id` ASC) VISIBLE,
  CONSTRAINT `fk_game_results_games1`
    FOREIGN KEY (`game_id`)
    REFERENCES `project-card-room1`.`games` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_game_results_users1`
    FOREIGN KEY (`player_id`)
    REFERENCES `project-card-room1`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `project-card-room1`.`messages`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project-card-room1`.`messages` ;

CREATE TABLE IF NOT EXISTS `project-card-room1`.`messages` (
  `int` INT NOT NULL,
  `message` VARCHAR(255) NULL,
  `user_id` INT NOT NULL,
  `game_id` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`int`),
  INDEX `fk_messages_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_messages_games1_idx` (`game_id` ASC) VISIBLE,
  CONSTRAINT `fk_messages_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `project-card-room1`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_messages_games1`
    FOREIGN KEY (`game_id`)
    REFERENCES `project-card-room1`.`games` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
