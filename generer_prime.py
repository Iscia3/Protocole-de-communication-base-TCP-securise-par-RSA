import random
import premier 

def gen_prime(length):
    random.seed()
    first_digit="123456789"
    digit="0"+first_digit
    last_digit="1379"
    nb=""
    nb_premier=""
    for i in range(length):
        if i==0:
            nb=nb+random.choice(first_digit)
        elif i==length-1:
            nb=nb+random.choice(last_digit)
        else:
            nb=nb+random.choice(digit)
    #print(nb)

    if premier.is_prime(nb)==True:
        nb_premier=nb
    else:
        return gen_prime(length)
    
    return nb_premier


#print(gen_prime(2000))