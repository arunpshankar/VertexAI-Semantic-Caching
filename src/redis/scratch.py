import redis
import json
import hashlib

# Connection information for Redis
redis_host = 'localhost'
redis_port = 6379
redis_password = ""

def generate_md5_hash(input_string):
    """ Generate a 32-character MD5 hash for a given input string. """
    return hashlib.md5(input_string.encode()).hexdigest()

def write_to_redis(data):
    """ Write data to Redis database. """
    try:
        # Create the Redis Connection object with decode_responses to convert Redis responses to Python strings
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        
        # Loop through the data and store each item in Redis
        for elem in data:
            json_data = json.dumps(elem)  # Convert dictionary to JSON string
            r.set(elem["id"], json_data)  # Set the data in Redis using the 'id' as key
            print(f"Entry {elem['id']} stored successfully.")
    except Exception as e:
        print("Error in connecting to Redis:", e)

def read_from_redis(keys):
    """ Retrieve and display data from Redis database using a list of keys. """
    try:
        # Reuse the Redis connection object
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        
        # Loop through the list of keys and fetch the data from Redis
        for key in keys:
            data = r.get(key)
            if data is not None:
                print(f"Data retrieved for {key}: {data}")
            else:
                print(f"No data found for {key}")
    except Exception as e:
        print("Error in retrieving data from Redis:", e)

if __name__ == '__main__':
    # Questions related to financial services documents
    questions = [
        "What are the requirements for a KYC document?",
        "How to validate a financial statement?",
        "What information is needed for credit risk assessment?",
        "Are there standard formats for auditing reports?"
    ]

    # Prepare data with MD5 hash IDs
    input_data = [
        {"id": generate_md5_hash(question), "Name": f"Question about {question}"}
        for question in questions
    ]
    
    # Write data to Redis
    write_to_redis(input_data)
    
    # Read data from Redis using generated IDs
    read_from_redis([data['id'] for data in input_data])
