import time
import random
import json

"""
This script is used by me to practice the import function
-display current time
-display random number
-create a json file "book.json" and display a dictionary of My_Book
"""

Local_Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(f"the time is: {Local_Time}")

Num1 = random.randrange(1, 12)
print(f"the randomized number is: {Num1}")

My_Book = {
    'title':['The Book'],
    'author':['Oran Amar'],
    'year':['2024']
}

with open('book.json', 'w') as outfile:
    json.dump(My_Book, outfile, indent=4)
print("Report generated in book.json")
