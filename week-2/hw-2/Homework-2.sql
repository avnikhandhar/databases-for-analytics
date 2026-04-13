-- Solution 1-1

-- 'Customer' table creation
CREATE TABLE Customer(
    customer_id NUMBER(*,0),
    name VARCHAR2(50),
    email VARCHAR2(20),
    
    CONSTRAINT Customer_PK
        PRIMARY KEY(customer_id)
);

-- 'Restaurant' table creation
CREATE TABLE Restaurant(
    restaurant_id NUMBER(*,0),
    name VARCHAR2(50),
    isopen CHAR(1),
    
    CONSTRAINT Restaurant_PK
        PRIMARY KEY(restaurant_id)
);

-- 'Order' table creation
CREATE TABLE OrderDetails(
    order_id NUMBER(*,0),
    customer_id NUMBER(*,0),
    restaurant_id NUMBER(*,0),
    total_price NUMBER(*,2),
    status VARCHAR2(10),
    
    CONSTRAINT Order_PK
        PRIMARY KEY(order_id),
    
    CONSTRAINT Order_FK1
        FOREIGN KEY(customer_id)
            REFERENCES Customer(customer_id),
            
    CONSTRAINT Order_FK2
        FOREIGN KEY(restaurant_id)
            REFERENCES Restaurant(restaurant_id)
);


-- 'Order Item' table creation
CREATE TABLE OrderItem(
    order_id NUMBER(*,0),
    item_name VARCHAR2(15),
    quantity NUMBER(*,0),
    price NUMBER(*,2),
    
    CONSTRAINT OrderItem_PK
        PRIMARY KEY(order_id, item_name),
    
    CONSTRAINT OrderItem_FK
        FOREIGN KEY(order_id)
            REFERENCES OrderDetails(order_id)
);

--Solution 1-2

-- Inserting data into customer table
INSERT INTO customer VALUES (101, 'Avni Sanghvi', 'asanghvi@gmail.com');
INSERT INTO customer VALUES (102, 'Tanvi Sanghvi', 'tsanghvi@gmail.com');
INSERT INTO customer VALUES (103, 'Chirag Khandhar', 'ckhandhar@gmail.com');

SELECT * FROM customer;

-- Inserting data into restaurant table
INSERT INTO restaurant VALUES(1, 'Restaurant1', 'Y');
INSERT INTO restaurant VALUES(2, 'Restaurant2', 'Y');

SELECT * FROM restaurant;

-- Inserting data into OrderDetails table
INSERT INTO orderdetails VALUES (100, 102, 1, 50, 'Delivered');
INSERT INTO orderdetails VALUES (104, 101, 2, 35, 'Preparing');
INSERT INTO orderdetails VALUES (105, 103, 2, 48, 'Received');
INSERT INTO orderdetails VALUES (103, 101, 1, 80, 'Delivered');
INSERT INTO orderdetails VALUES (101, 102, 1, 16, 'Preparing');
INSERT INTO orderdetails VALUES (106, 103, 2, 25, 'Delivered');

SELECT * FROM orderdetails;

-- Inserting data into OrderItems table - order_id, item name,qty, price
INSERT INTO orderitem VALUES (100, 'Item A', 2, 25);
INSERT INTO orderitem VALUES (104, 'Item B', 5, 7);
INSERT INTO orderitem VALUES (105, 'Item C', 4, 12);
INSERT INTO orderitem VALUES (103, 'Item D', 4, 20);
INSERT INTO orderitem VALUES (101, 'Item E', 2, 8);
INSERT INTO orderitem VALUES (106, 'Item F', 2, 12.5);

SELECT * FROM orderitem;

-- Solution 1-3

-- Create table for Department
CREATE TABLE Departments(
    dept_name VARCHAR2(20),
    chair VARCHAR2(50),
    cllg VARCHAR2(100),
    
    CONSTRAINT Department_PK
        PRIMARY KEY(dept_name)
);

-- Create table for Advisors
CREATE TABLE Advisors(
    adv_id VARCHAR2(3),
    adv_name VARCHAR2(50),
    address VARCHAR2(100),
    research_area VARCHAR2(50),
    dept_name VARCHAR2(20),
    
    CONSTRAINT Advisor_PK
        PRIMARY KEY(adv_id),
    
    CONSTRAINT Advisor_FK
        FOREIGN KEY(dept_name)
            REFERENCES Departments(dept_name)
);

-- Create table for Students
CREATE TABLE Students(
    student_id VARCHAR2(3),
    firstName VARCHAR2(15),
    lastName VARCHAR2(15),
    DOB DATE,
    telephone NUMBER(*,0),
    adv_id VARCHAR2(3),
    
    CONSTRAINT Student_PK
        PRIMARY KEY(student_id),
    
    CONSTRAINT Student_FK
        FOREIGN KEY(adv_id)
            REFERENCES Advisors(adv_id)
);