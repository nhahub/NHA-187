-- 1. Create the Database if it doesn't exist
CREATE DATABASE IF NOT EXISTS smart_complaints;

-- 2. Switch to that database
USE smart_complaints;

-- 3. Create the table for processed complaints
CREATE TABLE IF NOT EXISTS complaints_analyzed (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- Auto-generated ID for database management
    complaint_id VARCHAR(255),                -- The ID from the Source/Streamlit
    name VARCHAR(255),                        -- Customer Name
    national_id VARCHAR(255),                 -- Customer ID
    complaint TEXT,                           -- The full text of the complaint
    submitted_at VARCHAR(50),                 -- When the user sent it
    category_prediction VARCHAR(100),         -- AI Output 1
    sentiment_prediction VARCHAR(50),         -- AI Output 2
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- When Spark finished processing it
);