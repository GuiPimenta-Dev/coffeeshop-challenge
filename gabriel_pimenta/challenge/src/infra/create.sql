CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,            
    name VARCHAR(100) NOT NULL,          
    type VARCHAR(50) NOT NULL  
);

CREATE TABLE public.orders (
    id SERIAL PRIMARY KEY,            
    product VARCHAR(100) NOT NULL,     
    variation VARCHAR(100) NOT NULL,   
    price DECIMAL(10, 2) NOT NULL,   
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   
    status VARCHAR(50) NOT NULL,  
    customer_id INT NOT NULL,          
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES public.users(id) ON DELETE CASCADE 
);