CREATE DEFINER=`admin`@`%` PROCEDURE `RecipeRecommUserdiet`(IN UserID VARCHAR(6))
BEGIN

select * from recipe r 
where r.recipe_id not in (
select r_i.recipe_id from recipe_ingredient r_i
where r_i.ingredient_id not in (
select d_p_i.ingredient_id from dietry_prefer_ingredient d_p_i
where d_p_i.prefer_id in (select u_d_p.prefer_id from user_dietry_prefer u_d_p 
where u_d_p.user_id = UserID))) limit 2;

END