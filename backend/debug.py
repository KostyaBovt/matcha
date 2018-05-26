import time
from random import randint

def vdf(variable, name="no_name"):
    curTime = time.time()
    rand = randint(10000, 99999)
    fileName = "vdf | " + str(curTime) + " | " + name + " | " + str(rand) + ".py"
    f = open(fileName, 'w')
    f.write(str(variable))
    f.close()
