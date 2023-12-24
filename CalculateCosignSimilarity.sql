CREATE DEFINER=`admin`@`%` FUNCTION `CalculateCosignSimilarity`(
    cal1 FLOAT, protein1 FLOAT, carb1 FLOAT, fat1 FLOAT,
    cal2 FLOAT, protein2 FLOAT, carb2 FLOAT, fat2 FLOAT
) RETURNS float
BEGIN
    DECLARE dot_product FLOAT;
    DECLARE magnitude1 FLOAT;
    DECLARE magnitude2 FLOAT;
    DECLARE similarity FLOAT;

    SET dot_product = CalculateDotProduct(cal1, protein1, carb1, fat1, cal2, protein2, carb2, fat2);
    SET magnitude1 = CalculateVectorMagnitude(cal1, protein1, carb1, fat1);
    SET magnitude2 = CalculateVectorMagnitude(cal2, protein2, carb2, fat2);

    IF magnitude1 = 0 OR magnitude2 = 0 THEN
        SET similarity = 0; -- To handle division by zero
    ELSE
        SET similarity = dot_product / (magnitude1 * magnitude2);
    END IF;

    RETURN similarity;
END