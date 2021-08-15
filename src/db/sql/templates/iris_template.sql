-- *************************************************************
-- This script creates a table in the ml_data database for the
-- Iris dataset.
-- *************************************************************

-- Select the ml_data database
use ml_data;

-- Delete Iris table if it already exists
DROP TABLE IF EXISTS iris;

-- Create the Iris table
CREATE TABLE iris
(
  iris_id               INT             PRIMARY KEY     AUTO_INCREMENT,
  sepal_length          DOUBLE          NOT NULL,
  sepal_width           DOUBLE          NOT NULL,
  petal_length          DOUBLE          NOT NULL,
  petal_width           DOUBLE          NOT NULL,
  class                 VARCHAR(30)     NOT NULL
);

-- Insert rows into the Iris table
INSERT INTO iris VALUES
