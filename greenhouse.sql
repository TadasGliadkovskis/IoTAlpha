DROP TABLE IF EXISTS plant_readings,user_plant,user_plants_seq,plants,users,users_seq;
 
 
 CREATE TABLE users_seq
(
  user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
);

 CREATE TABLE users
(user_id varchar(100) NOT NULL DEFAULT '0',
 name varchar(100) NOT NULL,
 username varchar(100) NOT NULL,
 password char(12) NOT NULL,
 PRIMARY KEY (user_id));

 
 DELIMITER $$
CREATE TRIGGER tg_users_insert
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
  INSERT INTO users_seq VALUES (NULL);
  SET NEW.user_id = CONCAT('U', LPAD(LAST_INSERT_ID(), 3, '0'));
END$$
DELIMITER ;

alter table users ADD UNIQUE INDEX(username);
 
  CREATE TABLE plants
(plant_name varchar(100) NOT NULL,
 ideal_lower_temperature decimal(10,2) NOT NULL,
 ideal_higher_temperature decimal(10,2) NOT NULL,
ideal_humidity decimal(10,2) NOT NULL,
ideal_soil_moisture decimal(10,2) NOT NULL,
 PRIMARY KEY (plant_name));
 
 alter table plants ADD UNIQUE INDEX(plant_name);
 
  CREATE TABLE user_plants_seq
(
  plant_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
);
 
 CREATE TABLE user_plant
(plant_id varchar(100) NOT NULL,
 user_id varchar(100) NOT NULL,
plant_name varchar(100) NOT NULL,
 watered datetime DEFAULT CURRENT_TIMESTAMP,
 planted date DEFAULT CURRENT_DATE,
 PRIMARY KEY (plant_id,user_id,plant_name),
 FOREIGN KEY (user_id) REFERENCES users(user_id),
 FOREIGN KEY (plant_name)REFERENCES plants(plant_name));
 
  DELIMITER $$
CREATE TRIGGER tg_user_plants_insert
BEFORE INSERT ON user_plant
FOR EACH ROW
BEGIN
  INSERT INTO user_plants_seq VALUES (NULL);
  SET NEW.plant_id = CONCAT('P', LPAD(LAST_INSERT_ID(), 3, '0'));
END$$
DELIMITER ;

alter table user_plant ADD UNIQUE INDEX(user_id,plant_name);
 
  CREATE TABLE plant_readings
(plant_id varchar(100) NOT NULL,
  raspi_id varchar(100) NOT NULL,
  user_id varchar(100) NOT NULL,
temperature decimal(10,2),
humidity decimal(10,2),
soil_moisture varchar(100),
reading_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES users(user_id),
FOREIGN KEY (plant_id) REFERENCES user_plant(plant_id));


INSERT INTO `users` (`name`, `username`, `password`) VALUES ('Peter', 'peterrocks', 'peter@123'), ('Mike', 'mightymike', 'mike@123'), ('Bryan', 'bryanhere', 'bryan@123');

INSERT INTO `plants` (`plant_name`, `ideal_lower_temperature`, `ideal_higher_temperature`, `ideal_humidity`, `ideal_soil_moisture`) VALUES ('Tomato', '23.8', '32.2', '70', '1.5'), ('Carrot', '12.7', '23.9', '80', '1'), ('Cucumber', '23.9', '29.4', '65', '1.5');

INSERT INTO `user_plant` (`user_id`, `plant_name`) VALUES ('U002', 'Carrot'), ('U003', 'Cucumber'), ('U002', 'Tomato'), ('U001', 'Tomato');

INSERT INTO `plant_readings` (`plant_id`, `raspi_id`, `user_id`, `temperature`, `humidity`, `soil_moisture`) VALUES ('P001', 'R002', 'U002', '9.8', '40', 'dry'), ('P002', 'R003', 'U003', '25.6', '70', 'wet'), ('P002', 'R003', 'U003', '25.6', '70', 'wet'), ('P003', 'R002', 'U002', '15', '75', 'wet'), ('P004', 'R001', 'U001', '23.8', '55', 'dry');

/* Display Queries */

-- For the users table
select name from users where username = 'mightymike';

select name from users where user_id = 'U003';

select user_id from users where username = 'peterrocks';


-- For the plants table
select ideal_humidity from plants where plant_name = 'tomato';


-- For the user_plant table
select plant_id from user_plant where plant_name = 'tomato';

--(to display the names of all the users who have a specific plant. for example, tomato)
select distinct name from users join user_plant using (user_id) where plant_name = 'tomato';

--(to display any ideal condition of a specific user plant)
select distinct ideal_lower_temperature from plants join user_plant using (plant_name) where plant_id = 'P002';


-- For the plant_readings table
select temperature from plant_readings where plant_id = 'P003';

--(to display the name of a user from the raspberry pi id)
select distinct name from users join plant_readings using (user_id) where raspi_id = 'R003';

--(to display the user id and plant name of all the users whose plants are lacking moisture currently)
select distinct user_plant.user_id,user_plant.plant_name from user_plant join plant_readings using (plant_id) where soil_moisture = 'dry';

--(to display the plant_id and planted date of all the plants of a specific user)
select distinct plant_id,planted from user_plant join plant_readings using (plant_id) where plant_readings.user_id = 'U002';


/* Update Queries */

-- For the users table
update users set username = 'bossbryan' where user_id ='U003';


-- For the plants table, there should not be any update queries as the ideal conditions for a soecific plant do not change


-- For the user_plant table
--(if a plant is watered recently, it should be updated in the database)
update user_plant set watered = now() where plant_id ='P002';


-- For the plant_readings table either, there should not be any update queries as it will only be getting new and exact values whenever a plant's conditions are measured


/* Alter Queries */

--if our app reaches a larger scale, we can start storing user location as well
alter table users ADD location varchar(100) NOT NULL;

--later on, if we figure out how to measure the exact soil moisture instead of just 'dry' or 'wet'
alter table plant_readings change soil_moisture soil_moisture decimal(10,2);

