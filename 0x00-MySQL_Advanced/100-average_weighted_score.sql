-- Create the procedure ComputeAverageWeightedScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight INT;
    DECLARE weighted_sum FLOAT;

    -- Calculate the total weight (sum of weights of projects the user participated in)
    SELECT SUM(p.weight) INTO total_weight
    FROM projects p
    JOIN corrections c ON p.id = c.project_id
    WHERE c.user_id = user_id;

    -- Calculate the weighted sum of scores for the user
    SELECT SUM(c.score * p.weight) INTO weighted_sum
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- Update the user's average_score in the users table
    UPDATE users
    SET average_score = (weighted_sum / total_weight)
    WHERE id = user_id;
END //

DELIMITER ;
