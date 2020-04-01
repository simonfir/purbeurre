SET NAMES utf8;

DROP TABLE IF EXISTS ProductCategory;
DROP TABLE IF EXISTS SavedSubstitute;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Category;

CREATE TABLE Product (
	id SMALLINT UNSIGNED AUTO_INCREMENT,
	product_name VARCHAR(100) NOT NULL,
	generic_name VARCHAR(300),
	brands VARCHAR(100),
	stores VARCHAR(100),
	url VARCHAR(200),
	nutrition_grade_fr CHAR(1),
	PRIMARY KEY (id)
);

CREATE TABLE Category (
	id SMALLINT UNSIGNED AUTO_INCREMENT,
	tag VARCHAR(100) NOT NULL UNIQUE,
	name VARCHAR(100),
	PRIMARY KEY (id)
);

CREATE TABLE ProductCategory (
	product_id SMALLINT UNSIGNED,
	category_id SMALLINT UNSIGNED,
	PRIMARY KEY (product_id, category_id),
	CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES Product(id),
	CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES Category (id)
);

CREATE TABLE SavedSubstitute (
	original_product_id SMALLINT UNSIGNED,
	substitute_product_id SMALLINT UNSIGNED,
	PRIMARY KEY (original_product_id, substitute_product_id),
	CONSTRAINT fk_original_product_id FOREIGN KEY (original_product_id) REFERENCES Product(id),
	CONSTRAINT fk_substitute_product_id FOREIGN KEY (substitute_product_id) REFERENCES Product(id)
);
