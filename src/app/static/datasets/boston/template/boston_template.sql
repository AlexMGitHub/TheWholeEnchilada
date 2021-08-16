-- *************************************************************
-- This script creates a table in the ml_data database for the
-- Boston dataset.
-- *************************************************************

-- Select the ml_data database
use ml_data;

-- Delete Boston table if it already exists
DROP TABLE IF EXISTS boston;

-- Create the Boston table
CREATE TABLE boston
(
  boston_id               INT             PRIMARY KEY     AUTO_INCREMENT,
  CRIM                    DOUBLE          NOT NULL,
  ZN                      DOUBLE          NOT NULL,
  INDUS                   DOUBLE          NOT NULL,
  CHAS                    INT             NOT NULL,
  NOX                     DOUBLE          NOT NULL,
  RM                      DOUBLE          NOT NULL,
  AGE                     DOUBLE          NOT NULL,
  DIS                     DOUBLE          NOT NULL,
  RAD                     INT             NOT NULL,
  TAX                     DOUBLE          NOT NULL,
  PTRATIO                 DOUBLE          NOT NULL,
  B                       DOUBLE          NOT NULL,
  LSTAT                   DOUBLE          NOT NULL,
  MEDV                    DOUBLE          NOT NULL
);

-- Insert rows into the Boston table
INSERT INTO boston VALUES
