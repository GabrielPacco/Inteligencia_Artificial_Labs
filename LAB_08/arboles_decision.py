import math

def P(a ,tam):
    return (a /tam)
SI = 2
NO = 4

def entropia(SI , NO):
    tam = SI + NO
    if SI == 0:
        return - (P(NO , tam) * math.log2(P(NO , tam)))
    elif NO == 0:
        return -(P(SI , tam) * math.log2(P(SI , tam)))
    else:
        return -(P(SI , tam) * math.log2(P(SI , tam))) - (P(NO , tam) * math.log2(P(NO , tam)))
    
eP = entropia(SI , NO)   
print(eP)
def peso(A , B):
    return (A / B)


ganancia = eP - (peso(4 , 10)*entropia(3 , 1) + peso(6 , 10)*entropia(2 , 2) ) 
print(ganancia)