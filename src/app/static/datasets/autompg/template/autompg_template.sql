-- *************************************************************
-- This script creates a table in the ml_data database for the
-- AutoMPG dataset.
-- *************************************************************

-- Select the ml_data database
use ml_data;

-- Delete AutoMPG table if it already exists
DROP TABLE IF EXISTS autompg;

-- Create the AutoMPG table
CREATE TABLE autompg
(
  autompg_id              INT             PRIMARY KEY     AUTO_INCREMENT,
  mpg                     DOUBLE          NOT NULL,
  cylinders               INT             NOT NULL,
  displacement            DOUBLE          NOT NULL,
  horsepower              DOUBLE          NOT NULL,
  weight                  DOUBLE          NOT NULL,
  acceleration            DOUBLE          NOT NULL,
  model_year              INT             NOT NULL,
  origin                  INT             NOT NULL,
  car_name                VARCHAR(50)     NOT NULL
);

-- Insert rows into the AutoMPG table
INSERT INTO autompg VALUES
