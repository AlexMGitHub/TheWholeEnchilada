-- *************************************************************
-- This script creates a table in the ml_data database for the
-- Wine dataset.
-- *************************************************************

-- Select the ml_data database
use ml_data;

-- Delete wine table if it already exists
DROP TABLE IF EXISTS wine;

-- Create the wine table
CREATE TABLE wine
(
  wine_id                 INT             PRIMARY KEY     AUTO_INCREMENT,
  fixed_acidity           DOUBLE          NOT NULL,
  volatile_acidity        DOUBLE          NOT NULL,
  citric_acid             DOUBLE          NOT NULL,
  residual_sugar          DOUBLE          NOT NULL,
  chlorides               DOUBLE          NOT NULL,
  free_sulfur_dioxide     DOUBLE          NOT NULL,
  total_sulfur_dioxide    DOUBLE          NOT NULL,
  density                 DOUBLE          NOT NULL,
  ph                      DOUBLE          NOT NULL,
  sulphates               DOUBLE          NOT NULL,
  alcohol                 DOUBLE          NOT NULL,
  quality                 VARCHAR(2)      NOT NULL
);

-- Insert rows into the wine table
INSERT INTO wine VALUES
