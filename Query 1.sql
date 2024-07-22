create DATABASE book_store;
USE book_store;

CREATE TABLE books (
  isbn CHAR(10) PRIMARY KEY,
  author VARCHAR(100) NOT NULL,
  title VARCHAR(128) NOT NULL,
  price FLOAT NOT NULL,
  subject VARCHAR(30) NOT NULL
);
CREATE TABLE members (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  fname VARCHAR(20) NOT NULL,
  lname VARCHAR(20) NOT NULL,
  address VARCHAR(50) NOT NULL,
  city VARCHAR(30) NOT NULL,
  state VARCHAR(20) NOT NULL,
  zip INT NOT NULL,
  phone VARCHAR(12) NULL,
  email VARCHAR(40) NULL,
  password VARCHAR(20) NULL,
  creditcardtype VARCHAR(10) NULL,
  creditcardnumber CHAR(16) NULL
);

CREATE TABLE orders (
  user_id INT NOT NULL,
  ono INT PRIMARY KEY NOT NULL,
  recieved DATE NULL,
  shipped DATE NULL,
  shipCity VARCHAR(30) NULL,
  shipState VARCHAR(20) NULL,
  shipZip INT NULL,
  FOREIGN KEY (user_id) REFERENCES members(user_id)
);

CREATE TABLE odetails (
  ono INT NOT NULL,
  isbn CHAR(10) NOT NULL,
  quantity INT NOT NULL,
  price FLOAT NOT NULL,
  PRIMARY KEY (ono, isbn),
  FOREIGN KEY (ono) REFERENCES orders(ono),
  FOREIGN KEY (isbn) REFERENCES books(isbn)
);

CREATE TABLE cart (
  user_id INT NOT NULL,
  isbn CHAR(10) NOT NULL,
  quantity INT NOT NULL,
  PRIMARY KEY (user_id, isbn),
  FOREIGN KEY (user_id) REFERENCES members(user_id),
  FOREIGN KEY (isbn) REFERENCES books(isbn)
);