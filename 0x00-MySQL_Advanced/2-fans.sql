-- script that ranks country origins of bands, ordered by the number of (non-unique) fans

-- index on the 'origin' column to speed up grouping and ordering
CREATE INDEX idx_origin ON metal_bands (origin);

-- Sum the number of fans per country (grouped by origin)
SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
