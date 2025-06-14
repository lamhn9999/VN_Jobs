CREATE DATABASE IF NOT EXISTS job_desc_db;

USE job_desc_db;
CREATE TABLE location (
    location_id INT PRIMARY KEY AUTO_INCREMENT,
    province VARCHAR(30),
    city VARCHAR(30),
    district VARCHAR(30)
);

CREATE TABLE company (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(200),
    location_id INT,
    FOREIGN KEY (location_id) REFERENCES location(location_id)
);

CREATE TABLE job (
    job_id INT PRIMARY KEY AUTO_INCREMENT,
    field VARCHAR(50),
    -- specialty VARCHAR(100),
    -- role VARCHAR(50),
    experience VARCHAR(50)
);

CREATE TABLE job_desc (
	job_desc_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    -- location_id INT,
    description TEXT,
    job_id INT,
    min_salary INT,
    max_salary INT,
    currency VARCHAR(10),
    created_at DATE,
    expired_at DATE,
    isactive TINYINT(1),
    -- link varchar(255),
    FOREIGN KEY (job_id) REFERENCES job(job_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id)
    -- FOREIGN KEY (location_id) REFERENCES location(location_id)
);
