CREATE TABLE results(
    id INT PRIMARY KEY ,
    patient_id INT,
    test_name VARCHAR(100),
    result_value VARCHAR(100),
    FOREIGN KEY (patient_id) REFERENCES patients(id)
)