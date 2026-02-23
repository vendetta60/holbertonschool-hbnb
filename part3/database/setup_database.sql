-- Create database and select it
CREATE DATABASE IF NOT EXISTS hbnb_dev;
USE hbnb_dev;

-- Drop tables if they exist
DROP TABLE IF EXISTS Place_Amenity;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Place;
DROP TABLE IF EXISTS Amenity;
DROP TABLE IF EXISTS User;

-- Create User Table
CREATE TABLE User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Amenity Table
CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Place Table
CREATE TABLE Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE
);

-- Create Review Table
CREATE TABLE Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_place_review (user_id, place_id)
);

-- Create Place_Amenity Junction Table
CREATE TABLE Place_Amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_place_owner ON Place(owner_id);
CREATE INDEX idx_review_user ON Review(user_id);
CREATE INDEX idx_review_place ON Review(place_id);
CREATE INDEX idx_user_email ON User(email);

-- Insert Administrator User
-- Password: admin1234
INSERT INTO User (id, first_name, last_name, email, password, is_admin, created_at, updated_at) 
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewuBhBz3/4LZ8zHm',
    TRUE,
    NOW(),
    NOW()
);

-- Insert Initial Amenities
INSERT INTO Amenity (id, name, created_at, updated_at) VALUES
('5dd4aec2-6f89-4716-ad9e-e91ab793ae49', 'WiFi', NOW(), NOW()),
('4eef95bb-f888-47c4-98e9-d82df2521970', 'Swimming Pool', NOW(), NOW()),
('e289c879-02cc-465f-999d-90cf5513c8e8', 'Air Conditioning', NOW(), NOW());

-- Verify the setup
SELECT 'Database setup completed successfully!' as message;
SELECT 'Admin user created:' as info;
SELECT id, first_name, last_name, email, is_admin FROM User WHERE email = 'admin@hbnb.io';
SELECT 'Amenities created:' as info;
SELECT id, name FROM Amenity;
