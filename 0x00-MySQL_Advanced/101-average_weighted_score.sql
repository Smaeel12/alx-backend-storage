-- Drop the existing procedure if it exists to avoid duplication
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

-- Create the stored procedure to compute the average weighted score for all users
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Declare variables to store total weighted score and total weight for each user
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight INT;

    -- Declare a cursor to iterate over all users
    DECLARE user_cursor CURSOR FOR 
        SELECT id FROM users;

    -- Declare a continue handler to set done to TRUE when there are no more rows
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN user_cursor;

    -- Loop through each user
    read_loop: LOOP
        -- Fetch the next user_id
        FETCH user_cursor INTO user_id;

        -- Exit the loop if no more users are found
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Calculate the total weighted score and total weight for the current user
        SELECT SUM(c.score * p.weight) INTO total_weighted_score,
               SUM(p.weight) INTO total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Update the user's average score
        IF total_weight > 0 THEN
            UPDATE users
            SET average_score = total_weighted_score / total_weight
            WHERE id = user_id;
        ELSE
            UPDATE users
            SET average_score = 0
            WHERE id = user_id; -- Set average_score to 0 if no projects found
        END IF;
    END LOOP;

    -- Close the cursor
    CLOSE user_cursor;
END;

