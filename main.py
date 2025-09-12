from kivy.uix.gridlayout import accumulate
from kivy.uix.screenmanager import Scale
"""
Develop a program that simulates a Finite Automaton (DFA or NFA) and accepts or rejects strings
based on a given Regular Expression (RE). The RE should be converted to an automaton 
before string recognition. 
 
1. Convert the regular expression into an NFA or DFA. 
 
2. Simulate the automaton and check if the input string is accepted by the automaton. 

3. Implement basic regular expression features like union, concatenation, and Kleene star. 

4.Provide examples of strings that should be accepted or rejected based on the regular expression. 

5.Python/Java program that simulates an FA and checks string acceptance based on a regular expression. 

6.Documentation describing the automaton simulation and how the regular expression is processed. 

7.Video showing how the program simulates the FA and tests a variety of input strings. 
"""
#Concatenation means ab or a.b
#Union means a|b / a + b / a or BoxLayout:
#Kleene star means a* or a^0 or a^n where n>=0

#make a simple FA simulator that can take a regex and an input string and tell if the string is accepted or rejected by the FA

#Starting with concatenation, convert a.b into nfa using by representing into a transition table
class State:
    def __init__(self, name, isAcceptState=False):
        self.name = name
        self.transitions = {}
        self.isAcceptState = isAcceptState

class NFA:
    def __init__(self):
        self.graph = {}

    def add_state(self, state):
        if state not in self.graph:
            self.graph[state] = {}

    def add_transition(self, from_state, to_state, symbol):
        if from_state not in self.graph:
            self.add_state(from_state)
        
        if to_state not in self.graph:
            self.add_state(to_state)

        if symbol in self.graph[from_state]:
            self.graph[from_state][symbol].append(to_state)
        else:
            self.graph[from_state][symbol] = [to_state]
        
            
    
    def display(self):
        print("NFA Transition Table:")
        for state in self.graph:
            print(f"State {state}:")
            for symbol, destinations in self.graph[state].items():
                print(f"'{symbol}' -> {destinations}")
               
                    


class regex_to_nfa:
    def __init__(self, inputString, alphabet):
        #check for reg ex operators such as * . +
        self.inputString = inputString # ab* or a+b or a.b
        self.operators = set(['*', '.', '+'])
        self.alphabet = set(alphabet) # {a,b}
        self.states = 0
        self.nfa = NFA()
    
        for i in range(len(inputString)):
            NFA.add_state(f"q{i}")
            self.states += 1
            
            currentChar = i < len(self.inputString) - 1
            afterChar = self.inputString[i+1]

            if currentChar not in self.operators and afterChar not in self.operators: # if the current char and next char is not an operator then add a transition of current state to next state
                NFA.add_transition(f"q{i}", f"q{i+1}", self.inputString[i]) # add transition from current state to next state with current char as symbol
            elif afterChar in self.operators:
                if afterChar == '*': # if the next char is a kleene star then add a transition from current state to next state with current char as symbol and also add a transition from next state to current state with epsilon as symbol
                    NFA.add_transition(f"q{i}", f"q{i+1}", self.inputString[i]) # add transition from current state to next state with current char as symbol
                    NFA.add_transition(f"q{i+1}", f"q{i}", 'ε') # add transition from next state to current state with epsilon as symbol
                    NFA.add_transition(f"q{i}", f"q{i}", 'ε') # add transition from current state to itself with epsilon as symbol
                elif afterChar == '.': # if the next char is a concatenation then add a transition from current state to next state with current char as symbol
                    NFA.add_transition(f"q{i}", f"q{i+1}", self.inputString[i]) # add transition from current state to next state with current char as symbol
                elif afterChar == '+': # if the next char is a union then add a transition from current state to next state with current char as symbol and also add a transition from current state to next state with epsilon as symbol
                    NFA.add_transition(f"q{i}", f"q{i+1}", self.inputString[i]) # add transition from current state to next state with current char as symbol
                    NFA.add_transition(f"q{i}", f"q{i+1}", 'ε') # add transition from current state to next state with epsilon as symbol



        

        

def main():
    g = NFA()
    
    

if __name__ == "__main__":
    main()

