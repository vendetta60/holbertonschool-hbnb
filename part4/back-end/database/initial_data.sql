-- HBnB Initial Data Insertion Script
-- This script inserts the administrator user and initial amenities

-- Insert Administrator User
-- Password: admin1234 (hashed using bcrypt)
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

-- Verify the inserted data
SELECT 'Admin User Created:' as message;
SELECT id, first_name, last_name, email, is_admin FROM User WHERE email = 'admin@hbnb.io';

SELECT 'Amenities Created:' as message;
SELECT id, name FROM Amenity;
