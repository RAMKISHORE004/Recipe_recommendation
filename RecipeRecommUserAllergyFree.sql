CREATE DEFINER=`admin`@`%` PROCEDURE `RecipeRecommUserAllergyFree`(IN UserID VARCHAR(6))
BEGIN
    select distinct * from recipe r
where not exists (select * from recipe_ingredient r_i
where r.recipe_id = r_i.recipe_id and
r_i.ingredient_id in (select i.ingredient_id from
user_allergy u_a,
ingredient i
where
u_a.allergy_id = i.allergy_id and
u_a.user_id = UserID)) limit 5;
END