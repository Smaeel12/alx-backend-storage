-- Create the procedure ComputeAverageWeightedScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight INT;
    DECLARE weighted_sum FLOAT;

    -- Calculate the total weight (sum of the weights for all projects for this user)
    SELECT SUM(projects.weight) INTO total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Calculate the weighted sum of the scores
    SELECT SUM(corrections.score * projects.weight) INTO weighted_sum
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Update the average_score for the user in the users table
    UPDATE users
    SET average_score = (weighted_sum / total_weight)
    WHERE id = user_id;
END //

DELIMITER ;

