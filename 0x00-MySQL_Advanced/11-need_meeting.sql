-- Drop the existing view if it exists to avoid duplication
DROP VIEW IF EXISTS need_meeting;

-- Create the view need_meeting to list students needing a meeting
CREATE VIEW need_meeting AS
SELECT name
FROM students
WHERE score < 80 -- Students with a score strictly less than 80
AND (last_meeting IS NULL OR last_meeting < DATE_SUB(CURDATE(), INTERVAL 1 MONTH)); -- No last_meeting or more than 1 month ago

