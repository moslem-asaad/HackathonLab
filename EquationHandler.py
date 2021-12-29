import random

def generate_equation():
    sign = random.randint(0,1)
    if sign == 0: 
        num1 = random.randint(0,9)
        num2 = random.randint(0,9-num1)
        return [0,num1,num2]
    else:
        num1 = random.randint(0,9)
        num2 = random.randint(0,9)
        if num1 > num2 : 
            return [1,num1,num2]
        else:
            return [1,num2,num1]
            
def equation_to_str(equation):
    if (equation[0] == 0):
        return str(equation[1]) + "+" + str(equation[2])
    else:
        return str(equation[1]) + "-" + str(equation[2])

def equation_result (equation):
    if (equation[0] == 0):
        return equation[1] +  equation[2]
    else:
        return equation[1] - equation[2]  
