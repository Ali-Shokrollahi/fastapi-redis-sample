This project is a **FastAPI-based job listings system** that leverages **Redis caching** to optimize performance and reduce database queries. 

##  Redis Caching Logic  

### 🔹 1. Caching Frequently Accessed Jobs  
- When a job is retrieved, its **popularity score** is increased in a Redis **Sorted Set (`jobs:popular`)**.  
- If a job is accessed frequently (score ≥ 3), it gets **stored in Redis** for faster retrieval.  

### 🔹 2. Popular Jobs Tracking  
- The system keeps track of **most viewed jobs** using Redis.  
- Popular jobs are retrieved efficiently from Redis instead of querying the database.  

### 🔹 3. Expiring Cached Jobs  
- Cached jobs automatically **expire after 1 hour** to ensure data freshness.  
- When a job is updated or deleted, its cached version is **removed from Redis**.  

This caching strategy improves response times and reduces database load, making the system **more scalable and efficient**.