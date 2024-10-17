-- Drop the existing index if it exists to avoid duplication
DROP INDEX IF EXISTS idx_name_first_score ON names;

-- Create a new index on the first letter of name and score for optimized search
CREATE INDEX idx_name_first_score ON names (name(1), score);

