
DROP TABLE PurchaseItem;
CREATE TABLE PurchaseItem(
RestaurantID NUMBER(4) CHECK (RestaurantID > 0),
MenuItem     VARCHAR2(50),
CustEmail    VARCHAR2(100),

PRIMARY KEY(RestaurantID, MenuItem, CustEmail),

FOREIGN KEY(CustEmail) 
    REFERENCES RestCustomer(CustEmail),
    
FOREIGN key(RestaurantID)
    REFERENCES Restaurant(RestaurantID),
    
CONSTRAINT MenuConstraint
    FOREIGN KEY(RestaurantID, MenuItem)
         REFERENCES Menu(RestaurantID, MenuItem)
);

-- (CustEmail, CustName, CustAddr)
CREATE TABLE RestCustomer(
CustEmail VARCHAR2(100),
CustName  VARCHAR2(100),
CustAddr  VARCHAR2(200),

PRIMARY KEY (CustEmail)
);

-- (RestaurantID, RestName, RestAddr)

CREATE TABLE Restaurant(
RestaurantID NUMBER(4) CHECK (RestaurantID > 0) PRIMARY KEY,
RestName VARCHAR2(80),
RestAddress VARCHAR2(200));

-- (RestaurantID, MenuItem, Price)

CREATE TABLE Menu(
RestaurantID NUMBER(4) CHECK (RestaurantID > 0),
MenuItem    VARCHAR2(50),
Price       NUMBER(6,2),  -- Up to 9999.99

PRIMARY KEY(RestaurantID, MenuItem));

--(1, Wings, 4.99)
--(2, Wings, 4.99)
---(3, Wings, 5.99)
INSERT INTO Menu VALUES(1, 'Wings', 4.99);
INSERT INTO Menu VALUES(2, 'Wings', 4.99);
INSERT INTO Menu VALUES(3, 'Wings', 5.99);
INSERT INTO Menu VALUES(3, 'Bagel', 2.99);

INSERT INTO Menu VALUES(2, 'Bagel', -1.99);


--(1, Ben’s, 123 F)
--(2, Denny’s, 222 7th)
--(3, Kuzu, 111 7th)
INSERT INTO Restaurant VALUES(1, 'Ben''s', '123 Fake Street');
INSERT INTO Restaurant VALUES(2, 'Denny''s', '222 7th Avenue');
INSERT INTO Restaurant VALUES(3, 'Kuzu', '111 7th Avenue');

-- (a@b.c, Abe, 37 Jackson.)
-- (j@b.c, Jane, 1 Main.)
INSERT INTO RestCustomer VALUES('a@b.c', 'Abe', '37 Jackson St.');
INSERT INTO RestCustomer VALUES('j@b.c', 'Jane', '1 Main St.');


--(1, Wings, a@b.c)
--(2, Wings, a@b.c)
--(3, Wings, a@b.c)
--(1, Wings, j@b.c)
INSERT INTO PurchaseItem VALUES(1, 'Wings', 'a@b.c');
INSERT INTO PurchaseItem VALUES(2, 'Wings', 'a@b.c');
INSERT INTO PurchaseItem VALUES(3, 'Wings', 'a@b.c');
INSERT INTO PurchaseItem VALUES(1, 'Wings', 'j@b.c');

SELECT * FROM Restaurant;

SELECT * FROM PurchaseItem;

SELECT * FROM Menu;