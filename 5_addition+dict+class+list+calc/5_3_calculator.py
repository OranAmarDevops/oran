"""
This script is used by me to practice a error handling basic using a calculator
return error if not on the list
"""


def my_func(num1, num2, operation):
    allowed_operations= ['add', 'subtract', 'multiply']
    if operation not in allowed_operations:
        return 'invalid operation'
    
    
    if operation =='add':
        return num1+num2
    elif operation =='subtract':
        return num1-num2
    elif operation =='multiply':
        return num1*num2
    
    
result = my_func(1, 2, 'add')
print(result)