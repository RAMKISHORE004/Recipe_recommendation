CREATE DEFINER=`admin`@`%` FUNCTION `CalculateVectorMagnitude`(
    calorie FLOAT,
    protein FLOAT,
    carbs FLOAT,
    fats FLOAT
) RETURNS float
BEGIN
    DECLARE magnitude FLOAT;

    SET magnitude = SQRT(calorie * calorie + protein * protein + carbs * carbs + fats * fats);

    RETURN magnitude;
END