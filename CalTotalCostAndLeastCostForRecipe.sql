CREATE DEFINER=`admin`@`%` PROCEDURE `CalculateTotalCostAndLeastCostForRecipe`(
IN recipeId VARCHAR(6)
)
BEGIN
    DROP TEMPORARY TABLE IF EXISTS TempTotalCostPerStore;
    DROP TEMPORARY TABLE IF EXISTS TempLeastCostPerIngredient;
    DROP TEMPORARY TABLE IF EXISTS TempLeastCostStorePerIngredient;
    -- Create a temporary table to store the total cost for each store for the given recipe
    CREATE TEMPORARY TABLE TempTotalCostPerStore AS
    SELECT ri.recipe_id, osi.store_id, SUM(osi.price_per_unit) AS total_cost
    FROM recipe_ingredient ri
    JOIN online_store_ingredient osi ON ri.ingredient_id = osi.ingredient_id AND ri.recipe_id = recipeID AND osi.price_per_unit > 0
    GROUP BY ri.recipe_id, osi.store_id;

    -- Create a temporary table to find the least cost for each ingredient for the given recipe
    CREATE TEMPORARY TABLE TempLeastCostPerIngredient AS
    SELECT ingredient_id, MIN(price_per_unit) AS min_price
    FROM online_store_ingredient
    WHERE price_per_unit > 0 AND ingredient_id IN (SELECT ingredient_id FROM recipe_ingredient WHERE recipe_id = recipeID)
    GROUP BY ingredient_id;

    -- Find the store with the least cost for each ingredient for the given recipe
    CREATE TEMPORARY TABLE TempLeastCostStorePerIngredient AS
    SELECT osi.ingredient_id, osi.store_id
    FROM online_store_ingredient osi
    JOIN TempLeastCostPerIngredient lci ON osi.ingredient_id = lci.ingredient_id AND osi.price_per_unit = lci.min_price;

    -- Calculate the total least cost across all ingredients for the given recipe
    SELECT SUM(osi.price_per_unit) AS least_total_cost
    INTO @leastTotalCost
    FROM TempLeastCostStorePerIngredient lcsi
    JOIN online_store_ingredient osi ON lcsi.ingredient_id = osi.ingredient_id AND lcsi.store_id = osi.store_id;

    -- Display the total cost for each store for the given recipe
    SELECT store_id, total_cost
    FROM TempTotalCostPerStore;
	-- HERE    
    -- Find the ingredient_id and the store with the least cost for that ingredient for the given recipe
    SELECT MIN_store_with_least_cost.ingredient_id, MIN_store_with_least_cost.store_id AS store_id_with_least_cost
    FROM (
        SELECT osi.ingredient_id, osi.store_id, MIN(osi.price_per_unit) AS min_price
        FROM online_store_ingredient osi
        JOIN recipe_ingredient ri ON osi.ingredient_id = ri.ingredient_id 
            AND ri.recipe_id = recipeID
            AND osi.price_per_unit > 0
        GROUP BY osi.ingredient_id, osi.store_id
    ) AS MIN_store_with_least_cost
    WHERE (MIN_store_with_least_cost.ingredient_id, MIN_store_with_least_cost.min_price) IN (
        SELECT osi.ingredient_id, MIN(osi.price_per_unit) AS min_price
        FROM online_store_ingredient osi
        JOIN recipe_ingredient ri ON osi.ingredient_id = ri.ingredient_id 
            AND ri.recipe_id = recipeID
            AND osi.price_per_unit > 0
        GROUP BY osi.ingredient_id
    );
    
    
    -- Display the actual least cost for making the given recipe
    SELECT @leastTotalCost AS actual_least_cost;

    -- Drop temporary tables
    DROP TEMPORARY TABLE IF EXISTS TempTotalCostPerStore;
    DROP TEMPORARY TABLE IF EXISTS TempLeastCostPerIngredient;
    DROP TEMPORARY TABLE IF EXISTS TempLeastCostStorePerIngredient;
END