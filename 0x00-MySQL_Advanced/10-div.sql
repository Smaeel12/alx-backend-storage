-- Drop the existing function if it exists to avoid duplication
DROP FUNCTION IF EXISTS SafeDiv;

-- Create the SafeDiv function to perform safe division
CREATE FUNCTION SafeDiv(a INT, b INT) 
RETURNS FLOAT
DETERMINISTIC
BEGIN
    -- Return 0 if b is 0, otherwise return the result of a divided by b
    RETURN CASE 
        WHEN b = 0 THEN 0 
        ELSE a / b 
    END;
END;

