CREATE DEFINER=`admin`@`%` PROCEDURE `calculateCosineSimilarity`(
    IN cals1 FLOAT,
    IN protein1 FLOAT,
    IN carbs1 FLOAT,
    IN fats1 FLOAT,
    IN cals2 FLOAT,
    IN protein2 FLOAT,
    IN carbs2 FLOAT,
    IN fats2 FLOAT,
    OUT cosineSimilarity FLOAT
)
BEGIN
    DECLARE dotProduct FLOAT;
    DECLARE magnitude1 FLOAT;
    DECLARE magnitude2 FLOAT;

    -- Calculate dot product
    CALL calculateDotProduct(cals1, protein1, carbs1, fats1, cals2, protein2, carbs2, fats2, dotProduct);

    -- Calculate magnitude of each vector
    CALL calculateMagnitude(cals1, protein1, carbs1, fats1, magnitude1);
    CALL calculateMagnitude(cals2, protein2, carbs2, fats2, magnitude2);

    IF magnitude1 = 0 OR magnitude2 = 0 THEN
        SET cosineSimilarity = NULL; -- Handle division by zero case
    ELSE
        SET cosineSimilarity = dotProduct / (magnitude1 * magnitude2);
    END IF;
END