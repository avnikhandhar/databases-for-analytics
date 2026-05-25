import pandas as pd
import numpy as np
import random
import urllib.request
import sqlite3
import json
import re

# Part 1

# Part 1.a

# Generates a list of x random integers between 44 and 100 inclusive.
def generate_random_numbers(x):
    return [random.randint(44, 100) for _ in range(x)]

# Part 1.b

# Generate a list of 90 random numbers
random_numbers = generate_random_numbers(90)

# Convert the list into a pandas Series
numbers_series = pd.Series(random_numbers)

# Filter for numbers below 54 and count them
count_below_54 = (numbers_series < 54).sum()
print(f"Total numbers below 54: {count_below_54}")

# Part 1.c

# Create a numpy array
num_array = np.array(random_numbers)

# Reshape it to a 9x10 matrix
reshaped_array = num_array.reshape(9, 10)

# Replace all numbers greater than or equal to 59 with 100
reshaped_array[reshaped_array >= 59] = 100
print(reshaped_array)

# Part 2

# Define the source URL and the output error file
TWEETS_URL = "https://dbgroup.cdm.depaul.edu/DSC450/Module7.txt"
ERROR_FILE = "Module7_errors.txt"

# Connect to the database
conn = sqlite3.connect('/Users/avnisanghvi/Desktop/courses/quarter-3/databases-for-analytics/'
                       'week-5/hw-5/chauffeurs_database.db')
cursor = conn.cursor()

# Create the NEW SQL table for the user dictionary
cursor.execute('DROP TABLE IF EXISTS Users;')
cursor.execute('''
CREATE TABLE Users (
    id NUMBER(30,0) PRIMARY KEY,
    name VARCHAR(100),
    screen_name VARCHAR(50),
    description TEXT,
    friends_count NUMBER(10,0)
);
''')

# Modify the existing Module 5 "Tweets" table to add the new column
cursor.execute('ALTER TABLE Tweets ADD COLUMN user_id NUMBER(30,0);')

print("Successfully created the 'Users' table and altered the existing 'Tweets' table.")

# 4Stream data from the web and populate both tables
tweets_loaded = 0
errors_encountered = 0

# Open the remote web file and the local error log file
with urllib.request.urlopen(TWEETS_URL) as web_file, open(ERROR_FILE, 'w', encoding='utf-8') as error_file:
    for line in web_file:
        try:
            tweet_data = json.loads(line.decode('utf-8'))

            # Populate the NEW Users Table
            user_data = tweet_data.get('user')
            if user_data:
                u_values = (
                    user_data.get('id'),
                    user_data.get('name'),
                    user_data.get('screen_name'),
                    user_data.get('description'),
                    user_data.get('friends_count')
                )

                # INSERT OR IGNORE skips errors if the same user has written multiple tweets
                cursor.execute('''
                    INSERT OR IGNORE INTO Users (id, name, screen_name, description, friends_count)
                    VALUES (?, ?, ?, ?, ?)
                ''', u_values)

            # Populate the ALTERED Tweets Table
            # Includes 10 parameters now because of the added user_id column
            t_values = (
                tweet_data.get('created_at'),
                tweet_data.get('id_str'),
                tweet_data.get('text'),
                tweet_data.get('source'),
                tweet_data.get('in_reply_to_user_id'),
                tweet_data.get('in_reply_to_screen_name'),
                tweet_data.get('in_reply_to_status_id'),
                tweet_data.get('retweet_count'),
                tweet_data.get('contributors'),
                user_data.get('id') if user_data else None  # References Users(id)
            )

            cursor.execute('''
                INSERT INTO Tweets
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', t_values)

            tweets_loaded += 1

        except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
            # Capture faulty rows and write to error file
            error_file.write(line.decode('utf-8', errors='ignore'))
            errors_encountered += 1

# Commit updates and close connections
conn.commit()

print("\n--- Data Loading Summary ---")
print(f"Successfully loaded tweets into your altered table: {tweets_loaded}")
print(f"Damaged tweets written to '{ERROR_FILE}': {errors_encountered}")

conn.close()


# Part 3.b

# The regex used is: r"^\d{4}(-\d{4}){3}$|^\d{16}$"

# This regex strictly requires EITHER all 3 dashes to be present, OR zero dashes.
#     # ^\d{4}(-\d{4}){3}$  -> matches: 4 digits, followed by (dash + 4 digits) repeated 3 times.
#     # |                   -> OR
#     # ^\d{16}$            -> matches: exactly 16 solid digits.


# function validating the regex
def validate_credit_card(card_number):
    cc_pattern = r"^\d{4}(-\d{4}){3}$|^\d{16}$"

    if re.match(cc_pattern, card_number):
        return True
    return False


# examples to verify the regex
# examples cover the cases of having dashes, may not have dashes, invalid formats
test_cards = { "1234-5678-9012-3456": True, "1111222233334444": True, "1234-56789012-3456": False,
               "1234-5678-9012-345": False, "12345678901234567": False
            }

print("Testing Few Card Numbers")
for card, expected in test_cards.items():
    result = validate_credit_card(card)
    status = "CORRECT" if result == expected else "ERROR"
    print(f"Card: {card:<20} -> Is Valid? {str(result):<5} | Status: {status}")