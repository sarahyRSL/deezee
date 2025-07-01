DROP TABLE IF EXISTS employee;
CREATE TABLE employee (
	id	int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name	varchar(255) NOT NULL,
	email	varchar(255) NOT NULL,
	phone	varchar(255) NOT NULL,
	created_at	varchar(255),
	last_changed	varchar(255),
	remote_addr	varchar(255),
	is_locked	int
);
DROP TABLE IF EXISTS locations;
CREATE TABLE locations (
	id	int NOT NULL PRIMARY KEY AUTO_INCREMENT,
	label	varchar(255)
);
DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id	int NOT NULL PRIMARY KEY AUTO_INCREMENT,
	username	varchar(255) NOT NULL UNIQUE,
	password	varchar(255) NOT NULL,
	permission_level	varchar(255)
);
DROP TABLE IF EXISTS vendors;
CREATE TABLE vendors (
	id	int NOT NULL PRIMARY KEY AUTO_INCREMENT,
	created_at	int,
	changed_at	int,
	remote_addr	varchar(255),
	locked	int,
	name	varchar(255),
	company	varchar(255),
	email	varchar(255),
	phone	varchar(255),
	address	varchar(255),
	address2	varchar(255),
	city	varchar(255),
	state	varchar(255),
	zip	varchar(255),
	country	varchar(255)
);
CREATE TABLE vendor_locations (
    vendor_id INT,
    location_id INT,
    PRIMARY KEY (vendor_id, location_id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);