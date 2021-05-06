#TuringMachine.py
#Dan Moran
#CS 72400
'''
Write a one tape, one track, two-way infinite tape, deterministic Turing Machine simulator.
Once running, your program should ask for a file name, which contains the “code” of the TM
as input. It should then ask for an input word and output the sequence of IDs that the TM goes
through on that input. When it gets to a final state it should clearly indicate that the string was
accepted. If it gets to any other state, symbol pair with no transition it should stop computing
and indicate the string was not accepted. If looping, the TM should be stoppable by your choice of
input. This should not crash the simulator. In any of these cases the user should be prompted to
run the TM on another input string.
'''
import time

class TuringMachine:
   def __init__(self, program, input, state=0):
      self.length = len(input)
      self.delta = {}
      self.state = str(state)
      self.tape = ''.join(['B']*self.length)
      self.head = self.length // 2
      self.start = self.head
      self.end = self.head + self.length
      self.tape = self.tape[:self.head] + input + self.tape[self.head:]
      for line in program.splitlines():
         if(len(line)!= 0 and line[0] != "/"):
            line = line.replace(" ","")
            current_state = line[0]
            current_tape_symbol = line[1]
            new_state = line[2]
            new_tape_symbol = line[3]
            direction = line[4]
            self.delta[current_state, current_tape_symbol] = (new_tape_symbol, direction, new_state)   
   
   def step(self):
      if self.state != 'f':
         current_tape_symbol = self.tape[self.head]
         action = self.delta.get((self.state, current_tape_symbol))
         if action:
            new_tape_symbol, direction, new_state = action
            self.tape = self.tape[:self.head] + new_tape_symbol + self.tape[self.head+1:]
            if direction != '*':
               if direction == 'R':
                  self.head += 1
                  if current_tape_symbol == "B":
                     self.tape += "B" #pad tape with blanks to simulate infinite tape in context.  I know this will add an unnecessary amount, but better safe than sorry.  After all, it's supposed to be infinite!
               else:
                  self.head -= 1
                  if current_tape_symbol == "B":
                     self.tape = "B" + self.tape #pad tape with blanks to simulate infinite tape in context.  I know this will add an unnecessary amount, but better safe than sorry.  After all, it's supposed to be infinite!
               if(self.state != new_state):
                  self.fail = 0
               self.state = new_state
               

   def run(self):
      self.fail = 0
      while self.state != 'f' and self.fail<1000 : # prevent infinite loop
         print(self.tape[self.start-1:self.head]+"-"+self.state+"-"+self.tape[self.head:self.end+1])
         self.step()
         self.fail+=1
      if self.state == "f":
         print("HUZZAH!\nThis string has been accepted by Mr. Turing and his Machine. Well done.")
      else:
         print("WRONG!\nMr. Turing and his Machine find this input COMPLETELY unacceptable.  Please try again.")
 

go_var = "Y"
print("Welcome to the TuringSim 5000")
time.sleep(1)
print('This program will run any turing machine can come up with on any input your heart desires, assuming you use roughly the same format as Eric Schweitzer.  While the TuringSim 5000 has a built-in fail-safe, if at any point you feel unsafe, you can stop by simply typing "ctrl + c" on your keyboard.')
time.sleep(3)
while(go_var == "Y" or go_var == "y"):
   program_file = input('Please enter program as a text file: ')
   TMinput = input('Please enter an input word for the Turing Machine: ')
   print("Please keep all arms and legs inside the vehicle... or chair... or whereever they were before you started messing around with this.")
   program = open(program_file).read()
   TM = TuringMachine(program, TMinput)
   try:
      TM.run()
   except KeyboardInterrupt:
      print("TuringSim 5000 has been killed (x_x)")
   time.sleep(2)
   go_var = input('Restart? Type Y for yes.')
