import PyGoL
import random

conway = PyGoL.PyRule([3],[2,3])
board = PyGoL.PyGoLEngine(32,32, conway)

random.seed(5)

for i in range(32):
    for j in range(32):
        board.set(i,j,random.randint(0,1))
        
with open("output.txt","w") as file:
    for i in range(1000000):
        out = ""
        board.run()
        for y in range(32):
            for x in range(32):
                out += str(int(board.get(x,y)))
            out += '\n'
        out+= "\n\n"
        file.write(out)

