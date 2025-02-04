<?php
$servername = ""
$username = ""
$password = ""
$dbname = ""

$conn = new msql($servername,$username,$password,$dbname)

if ($conn->connection_error){
    die("Connection Failure:" .$conn->connection_error)
}

$fullname = $_POST['fullname'];
$pass = password_hash($_POST['password'], PASSWORD_DEFAULT);
$email = $_POST['email']
$date_of_birth = $_POST['date_of_birth']

# send info to sql
$sql = "INSERT INTO Users (PasswordHash, Email, FullName, DateOfBirth) VALUES (?, ?, ?, ?, ?)",
$stmt = $conn->prepare($sql);
$stmt->bind_param("sssss", $pass, $email, $fullname, $date_of_birth);

if ($stmt->execute()) {
    echo "New patient info inserted successfully!";
} else {
    echo "Error: " . $stmt->error;
}

$stmt->close();
$conn->close();#/












?>