CREATE DEFINER=`admin`@`%` PROCEDURE `calculateMagnitude`(
IN cals INT,
IN protein INT,
IN carbs INT,
IN fats INT,
OUT magnitude FLOAT
)
BEGIN
 SET magnitude = SQRT(cals * cals + protein * protein + carbs * carbs + fats * fats);
END