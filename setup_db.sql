-- Drop tables if they exist to ensure clean setup (optional, comment out if not needed)
DROP TABLE IF EXISTS interviews CASCADE;
DROP TABLE IF EXISTS trainer_batches CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS trainers CASCADE;

-- Create tables
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    enrollment_date DATE,
    batch_id INTEGER,
    status VARCHAR(20) CHECK (status IN ('active', 'completed', 'dropped')),
    total_fee NUMERIC,
    fee_paid NUMERIC DEFAULT 0,
    last_payment_date DATE,
    remarks TEXT
);

CREATE TABLE trainers (
    trainer_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    specialization TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    availability_json JSONB,
    notes TEXT
);

CREATE TABLE trainer_batches (
    id SERIAL PRIMARY KEY,
    trainer_id INTEGER REFERENCES trainers(trainer_id) ON DELETE CASCADE,
    batch_id INTEGER NOT NULL,
    course_name VARCHAR(100),
    days TEXT[],
    start_time TIME,
    end_time TIME
);

CREATE TABLE interviews (
    interview_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id) ON DELETE CASCADE,
    trainer_id INTEGER REFERENCES trainers(trainer_id) ON DELETE CASCADE,
    company_name VARCHAR(100),
    job_role VARCHAR(100),
    interview_date DATE,
    interview_stage VARCHAR(50),
    status VARCHAR(50),
    offered BOOLEAN DEFAULT FALSE,
    salary_offered NUMERIC,
    trainer_feedback TEXT,
    trainer_recommendation TEXT
);

-- Insert sample data
INSERT INTO students (full_name, email, phone, enrollment_date, batch_id, status, total_fee, fee_paid, last_payment_date, remarks) VALUES
('Aryan Sharma', 'aryan.sharma@example.com', '9000000001', '2024-06-10', 101, 'active', 50000, 30000, '2024-07-01', 'Paid in 2 installments'),
('Meera Jain', 'meera.jain@example.com', '9000000002', '2024-06-12', 102, 'active', 55000, 55000, '2024-07-05', 'Paid in full'),
('Ravi Verma', 'ravi.verma@example.com', '9000000003', '2024-06-15', 101, 'active', 50000, 25000, '2024-07-03', 'Partial payment'),
('Simran Kaur', 'simran.kaur@example.com', '9000000004', '2024-06-18', 103, 'dropped', 60000, 20000, '2024-06-25', 'Dropped after 2 weeks'),
('Aditya Roy', 'aditya.roy@example.com', '9000000005', '2024-06-20', 104, 'active', 60000, 60000, '2024-07-08', 'Cleared dues'),
('Sneha Iyer', 'sneha.iyer@example.com', '9000000006', '2024-06-22', 105, 'active', 45000, 20000, '2024-07-04', 'On payment plan'),
('Nikhil Bansal', 'nikhil.bansal@example.com', '9000000007', '2024-06-25', 103, 'active', 48000, 48000, '2024-07-07', 'Paid via UPI'),
('Pooja Mehta', 'pooja.mehta@example.com', '9000000008', '2024-06-26', 102, 'completed', 50000, 50000, '2024-06-30', 'Course completed'),
('Zaid Sheikh', 'zaid.sheikh@example.com', '9000000009', '2024-06-28', 104, 'active', 55000, 30000, '2024-07-06', 'Pending balance'),
('Kriti Nanda', 'kriti.nanda@example.com', '9000000010', '2024-07-01', 105, 'active', 48000, 10000, '2024-07-09', 'New joiner');


INSERT INTO trainers (full_name, email, phone, specialization, is_active, availability_json, notes) VALUES
('Amit Rathi', 'amit@debugshala.com', '9011111111', 'Java Full Stack', true, '{"Monday":["10:00-12:00"], "Wednesday":["14:00-16:00"]}', '10+ yrs exp'),
('Divya Gupta', 'divya@debugshala.com', '9011111112', 'Data Science', true, '{"Tuesday":["11:00-13:00"], "Thursday":["10:00-12:00"]}', 'Ex-IBM'),
('Manish Tiwari', 'manish@debugshala.com', '9011111113', 'MERN Stack', true, '{"Monday":["09:00-11:00"], "Friday":["15:00-17:00"]}', 'Strong frontend'),
('Surbhi Yadav', 'surbhi@debugshala.com', '9011111114', 'Data Analysis', true, '{"Tuesday":["14:00-16:00"]}', 'Excel + Python'),
('Vikram Chauhan', 'vikram@debugshala.com', '9011111115', 'Java Full Stack', true, '{"Monday":["08:00-10:00"], "Wednesday":["12:00-14:00"]}', 'Backend expert'),
('Neha Khatri', 'neha@debugshala.com', '9011111116', 'Data Science', true, '{"Wednesday":["10:00-12:00"], "Friday":["10:00-12:00"]}', 'ML specialist'),
('Rahul Sinha', 'rahul@debugshala.com', '9011111117', 'MERN Stack', true, '{"Thursday":["11:00-13:00"], "Saturday":["10:00-12:00"]}', 'Node.js heavy'),
('Ishita Basu', 'ishita@debugshala.com', '9011111118', 'Data Analysis', true, '{"Tuesday":["09:00-11:00"]}', 'Power BI focus'),
('Karan Malhotra', 'karan@debugshala.com', '9011111119', 'Java Full Stack', false, '{"Monday":["10:00-12:00"]}', 'On break'),
('Preeti Deshmukh', 'preeti@debugshala.com', '9011111120', 'Data Science', true, '{"Wednesday":["14:00-16:00"]}', 'DL/NLP focus');


INSERT INTO trainer_batches (trainer_id, batch_id, course_name, days, start_time, end_time) VALUES
(1, 101, 'Java Full Stack', ARRAY['Monday', 'Wednesday'], '10:00', '12:00'),
(2, 102, 'Data Science', ARRAY['Tuesday', 'Thursday'], '10:00', '12:00'),
(3, 103, 'MERN Stack', ARRAY['Monday', 'Friday'], '09:00', '11:00'),
(4, 104, 'Data Analysis', ARRAY['Tuesday', 'Thursday'], '14:00', '16:00'),
(5, 101, 'Java Full Stack', ARRAY['Wednesday'], '12:00', '14:00'),
(6, 102, 'Data Science', ARRAY['Wednesday', 'Friday'], '10:00', '12:00'),
(7, 103, 'MERN Stack', ARRAY['Thursday', 'Saturday'], '11:00', '13:00'),
(8, 104, 'Data Analysis', ARRAY['Tuesday'], '09:00', '11:00'),
(2, 105, 'Data Science', ARRAY['Wednesday'], '14:00', '16:00'),
(1, 105, 'Java Full Stack', ARRAY['Monday'], '08:00', '10:00');

INSERT INTO interviews (student_id, company_name, job_role, interview_date, interview_stage, status, offered, salary_offered, trainer_feedback, trainer_recommendation) VALUES
(1, 'TCS', 'Java Developer', '2024-07-08', 'Technical', 'cleared', true, 450000, 'Good logic and confidence.', 'Recommended'),
(2, 'Infosys', 'Data Analyst', '2024-07-05', 'HR', 'pending', false, NULL, 'Needs more confidence.', 'Recommended with conditions'),
(3, 'Wipro', 'Backend Intern', '2024-07-06', 'Screening', 'rejected', false, NULL, 'Struggled with SQL.', 'Not ready yet'),
(4, 'HCL', 'MERN Developer', '2024-07-07', 'Technical', 'pending', false, NULL, 'Frontend okay, backend weak.', 'Partial recommendation'),
(5, 'Capgemini', 'Java Dev', '2024-07-09', 'Final', 'cleared', true, 480000, 'Very good communication.', 'Highly Recommended'),
(6, 'Genpact', 'Data Analyst', '2024-07-08', 'HR', 'cleared', true, 400000, 'Average logic but good DAX skills.', 'Recommended'),
(7, 'Cognizant', 'Node.js Dev', '2024-07-07', 'Screening', 'rejected', false, NULL, 'Did not understand async.', 'Not recommended'),
(8, 'LTI', 'ML Engineer', '2024-07-06', 'Technical', 'pending', false, NULL, 'Knows basics, needs depth.', 'Train more'),
(9, 'Accenture', 'Java Intern', '2024-07-08', 'Screening', 'cleared', true, 350000, 'Impressive under pressure.', 'Recommended'),
(10, 'Tata Elxsi', 'BI Developer', '2024-07-09', 'Technical', 'pending', false, NULL, 'Missed questions on joins.', 'Review SQL module');
