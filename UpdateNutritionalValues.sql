CREATE DEFINER=`admin`@`%` PROCEDURE `UpdateNutritionalValues`(IN recipeID VARCHAR(8))
BEGIN
    DECLARE totalCalories DECIMAL(10, 2);
    DECLARE totalFats DECIMAL(10, 2);
    DECLARE totalCarbs DECIMAL(10, 2);
    DECLARE totalProtein DECIMAL(10, 2);

    -- Calculate total nutritional values per serving
    WITH nutries_per_quantity as(
		select r.recipe_id as recipe_id,
		r.servings as servings,
		i.calories_100_g*(r_i.quantity_in_g/100) as calories_per_quantity,
		i.fats_100_g*(r_i.quantity_in_g/100) as fats_per_quantity,
		i.carbs_100_g*(r_i.quantity_in_g/100) as carbs_per_quantity,
		i.protein_100_g*(r_i.quantity_in_g/100) as protein_per_quantity
		from ingredient i
		JOIN
		recipe_ingredient r_i
		on i.ingredient_id = r_i.ingredient_id
		JOIN
		recipe r
		on r.recipe_id = r_i.recipe_id
		where r_i.recipe_id = recipeID
	)
	select 
		SUM(npq.calories_per_quantity)/npq.servings as calories_per_serving,
		SUM(npq.fats_per_quantity)/npq.servings as fats_per_serving,
		SUM(npq.carbs_per_quantity)/npq.servings as carbs_per_serving,
		SUM(npq.protein_per_quantity)/npq.servings as protein_per_serving
		INTO totalCalories, totalFats, totalCarbs, totalProtein 
		from nutries_per_quantity npq
		group by recipe_id ;

    -- Update recipe table with calculated values
    UPDATE recipe
    SET
        calories_per_serving = totalCalories,
        fats_per_serving = totalFats,
        carbs_per_serving = totalCarbs,
        protein_per_serving = totalProtein
    WHERE
        recipe_id = recipeID;
END