 DROP TABLE IF EXISTS plant_readings,user_plant,plants,users;
 
 CREATE TABLE users
(user_id varchar(100) NOT NULL,
 name varchar(100) NOT NULL,
 location varchar(100) NOT NULL,
 username varchar(100) NOT NULL,
 password char(12) NOT NULL,
 PRIMARY KEY (user_id));
 
  CREATE TABLE plants
(plant_name varchar(100) NOT NULL,
 ideal_lower_temperature decimal(10,2) NOT NULL,
 ideal_higher_temperature decimal(10,2) NOT NULL,
ideal_humidity decimal(10,2) NOT NULL,
ideal_soil_moisture decimal(10,2) NOT NULL,
 PRIMARY KEY (plant_name));
 
 CREATE TABLE user_plant
(plant_id varchar(100) NOT NULL,
 user_id varchar(100) NOT NULL,
plant_name varchar(100) NOT NULL,
 watered date,
 planted date,
 PRIMARY KEY (plant_id,user_id,plant_name),
 FOREIGN KEY (user_id) REFERENCES users(user_id),
 FOREIGN KEY (plant_name)REFERENCES plants(plant_name));
 
  CREATE TABLE plant_readings
(plant_id varchar(100) NOT NULL,
  raspi_id varchar(100) NOT NULL,
  user_id varchar(100) NOT NULL,
temperature decimal(10,2),
humidity decimal(10,2),
soil_moisture decimal(10,2),
reading_time TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES users(user_id),
FOREIGN KEY (plant_id) REFERENCES user_plant(plant_id));


INSERT INTO `users` (`user_id`, `name`, `location`, `username`, `password`) VALUES ('U001', 'Peter', 'Dundalk', 'peterrocks', 'peter@123'), ('U002', 'Mike', 'Drogheda', 'mightymike', 'mike@123'), ('U003', 'Bryan', 'Dublin', 'bryanhere', 'bryan@123');

INSERT INTO `plants` (`plant_name`, `ideal_lower_temperature`, `ideal_higher_temperature`, `ideal_humidity`, `ideal_soil_moisture`) VALUES ('Tomato', '23.8', '32.2', '70', '1.5'), ('Carrot', '12.7', '23.9', '80', '1'), ('Cucumber', '23.9', '29.4', '65', '1.5');

INSERT INTO `user_plant` (`plant_id`, `user_id`, `plant_name`, `watered`, `planted`) VALUES ('P001', 'U002', 'Carrot', '2021-11-03', '2021-11-01'), ('P002', 'U003', 'Cucumber', '2021-11-02', '2021-11-02'), ('P003', 'U002', 'Tomato', '2021-11-02', '2021-11-01'), ('P004', 'U001', 'Tomato', '2021-11-04', '2021-11-02');

INSERT INTO `plant_readings` (`plant_id`, `raspi_id`, `user_id`, `temperature`, `humidity`, `soil_moisture`) VALUES ('P001', 'R002', 'U002', '9.8', '40', '0.5'), ('P002', 'R003', 'U003', '25.6', '70', '3.2'), ('P002', 'R003', 'U003', '25.6', '70', '3.2'), ('P003', 'R002', 'U002', '15', '75', '2.6'), ('P004', 'R001', 'U001', '23.8', '55', '1.6');
