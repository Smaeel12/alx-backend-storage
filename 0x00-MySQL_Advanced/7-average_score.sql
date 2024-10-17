-- SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student.
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE average_score DECIMAL(5, 2);

    -- Calculate the average score for the user
    SELECT AVG(score) INTO average_score
    FROM corrections
    WHERE user_id = user_id;

    -- Update the average_score in the users table
    UPDATE users
    SET average_score = average_score
    WHERE id = user_id;
END;

//

DELIMITER ;

