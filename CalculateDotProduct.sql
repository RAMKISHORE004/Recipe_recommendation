CREATE DEFINER=`admin`@`%` FUNCTION `CalculateDotProduct`(
    cal1 FLOAT, protein1 FLOAT, carb1 FLOAT, fat1 FLOAT,
    cal2 FLOAT, protein2 FLOAT, carb2 FLOAT, fat2 FLOAT
) RETURNS float
BEGIN
    DECLARE dot_product FLOAT;
    
    SET dot_product = (cal1 * cal2) + (protein1 * protein2) + (carb1 * carb2) + (fat1 * fat2);
    
    RETURN dot_product;
END