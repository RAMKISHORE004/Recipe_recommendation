CREATE TABLE users (
	user_id    VARCHAR(6) PRIMARY KEY, 
	first_name VARCHAR(20), 
	last_name  VARCHAR(20),
    email      VARCHAR(30),
	username   VARCHAR(20) NOT NULL, 
	password   VARCHAR(40) NOT NULL
);
select * from users;
select count(*) from users;

CREATE TABLE user_recipe_log (
	user_id    VARCHAR(6),
    recipe_id  VARCHAR(8),
    date_time  DATETIME,
    money_saved numeric(5,2),
    primary key (user_id, recipe_id),
	foreign key (user_id) references users (user_id)
	on delete cascade,
	foreign key (recipe_id) references recipe (recipe_id)
);
select * from user_recipe_log;

CREATE TABLE dietry_prefer (
    prefer_id VARCHAR(6) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(255)
);
select * from dietry_prefer;

CREATE TABLE user_dietry_prefer(
	user_id    VARCHAR(6),
	prefer_id VARCHAR(6),
	description VARCHAR(255),
    primary key (user_id, prefer_id),
	foreign key (user_id) references users (user_id)
	on delete cascade,
	foreign key (prefer_id) references dietry_prefer (prefer_id)
);
select * from user_dietry_prefer;

CREATE TABLE dietry_prefer_ingredient(
	prefer_id VARCHAR(6),
    ingredient_id    VARCHAR(6),
	description VARCHAR(255),
    primary key (prefer_id, ingredient_id),
    foreign key (prefer_id) references dietry_prefer (prefer_id)
	on delete cascade,
    foreign key (ingredient_id) references ingredient (ingredient_id)
);
select * from dietry_prefer_ingredient;

CREATE TABLE allergy (
    allergy_id VARCHAR(6) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(255)
);
select * from allergy;
select count(*) from allergy;

CREATE TABLE user_allergy(
	user_id    VARCHAR(6),
	allergy_id VARCHAR(6),
	description VARCHAR(255),
    primary key (user_id, allergy_id),
	foreign key (user_id) references users (user_id)
	on delete cascade,
	foreign key (allergy_id) references allergy (allergy_id)
);
select * from user_allergy;

CREATE TABLE ingredient (
    ingredient_id    VARCHAR(6) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    calories_100_g   numeric(5,2),
    fats_100_g       numeric(5,2),
    carbs_100_g      numeric(5,2),
    protein_100_g    numeric(5,2),
    allergy_id       VARCHAR(6),
    description      VARCHAR(255),
    foreign key (allergy_id) references allergy (allergy_id)
		on delete set null
);
select * from ingredient;
TRUNCATE TABLE ingredient;
select count(*) from ingredient;
INSERT INTO ingredient(ingredient_id, name, calories_100_g, fats_100_g, carbs_100_g, protein_100_g, allergy_id) 
         VALUES ('65635', 'Zucchini', 15, 0.4, 2.7, 1.1, '54360');

CREATE TABLE ingredient_type (
    ingredient_type_id    VARCHAR(6) PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL,
    group_name VARCHAR(50),
    class_name VARCHAR(50),
    description      VARCHAR(255),
    foreign key (allergy_id) references allergy (allergy_id)
		on delete set null
);


CREATE TABLE recipe (
    recipe_id    VARCHAR(8) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    steps      VARCHAR(7000),
    serving_size   VARCHAR(10),
    servings      numeric(5),
    description      VARCHAR(2000)
);
select * from recipe;
drop table recipe;

CREATE TABLE user_recipe(
	user_id    VARCHAR(6),
	recipe_id VARCHAR(8),
    review VARCHAR(255),
    rating numeric(2),
	description VARCHAR(255),
    primary key (user_id, recipe_id),
	foreign key (user_id) references users (user_id)
	on delete cascade,
	foreign key (recipe_id) references recipe (recipe_id)
);
select * from user_recipe;

drop table user_recipe;

CREATE TABLE recipe_ingredient (
    recipe_id      VARCHAR(8),
    ingredient_id  VARCHAR(6),
    quantity       numeric(5,3),
    unit           VARCHAR(20),
    description    VARCHAR(255),
    primary key (recipe_id, ingredient_id),
	foreign key (recipe_id) references recipe (recipe_id)
		on delete cascade,
	foreign key (ingredient_id) references ingredient (ingredient_id)
);
select * from recipe_ingredient;

CREATE TABLE online_store (
    store_id VARCHAR(6) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    web_link VARCHAR(255),
    description VARCHAR(255)
);
select * from online_store;

CREATE TABLE online_store_ingredient(
	store_id VARCHAR(6),
    ingredient_id    VARCHAR(6),
    price numeric(5,2),
    per_quantity numeric(5,2),
	description VARCHAR(255),
    primary key (store_id, ingredient_id),
    foreign key (store_id) references online_store (store_id)
	on delete cascade,
    foreign key (ingredient_id) references ingredient (ingredient_id)
);
select * from online_store_ingredient;







