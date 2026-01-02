import itertools
from functools import reduce
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
counter = itertools.count()

def new_state():
    return f"q{next(counter)}"


class NFA:
    def __init__(self):
        self.states = set()
        self.start = None
        self.accepts = set()
        self.transitions = {} 
 
    def add_state(self, name, is_start= False, is_accept =False):
        self.states.add(name)
        if is_start:
            self.start = name
        if is_accept:
            self.accepts.add(name)
        if name not in self.transitions:
            self.transitions[name] = {}
        return name
    
    def add_transition(self, from_state, symbol, to_state):
        self.transitions[from_state].setdefault(symbol, set()).add(to_state)
            
    
    def display(self):
        print("NFA Transition Table:")
    
        # collect all symbols across transitions
        symbols = sorted({sym for trans in self.transitions.values() for sym in trans})
        
        # header row
        header = "State\t" + "\t".join(symbols)
        print(header)
        
        # each state row
        for state in sorted(self.states):   # sort for consistent order
            row = [state]
            for sym in symbols:
                dests = self.transitions[state].get(sym, set())
                if dests:
                    row.append(",".join(sorted(dests)))  # show multiple destinations
                else:
                    row.append("Φ")
            print("\t".join(row))
            
    def simulate(self, string):
        current_states = {self.start}
        for ch in string:
            next_states = set()
            for state in current_states:
                if ch in self.transitions[state]:
                    next_states |= self.transitions[state][ch]
            current_states = next_states
            if not current_states:  # dead end
                return False
        # accept if any current state is in accepts
        return any(s in self.accepts for s in current_states)
    
def reconstruct(nfa):
    new_nfa = NFA()
    new_nfa.add_state(nfa.start, is_start=True)
    stack = [new_nfa.start]
    visited = set()
    
    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        for symbol, destinations in nfa.transitions[state].items():
            for dest in destinations:
                is_accept = False
                if dest in nfa.accepts:
                    is_accept = True
                new_nfa.add_state(dest, is_accept=is_accept)
                new_nfa.add_transition(state, symbol, dest)
                stack.append(dest)
            
    return new_nfa        
    
                    

def regex_to_nfa(postfix):
    stack = []
    #ab.
    for token in postfix:
        if str(token).isalnum():
            nfa = NFA()
            start = nfa.add_state(new_state(), is_start=True)
            finish = nfa.add_state(new_state(), is_accept=True)
            
            nfa.add_transition(start, token, finish)
            stack.append(nfa)
        elif str(token) == ".":
            #get the last 2 recent nfa fragments
            nfa2 = stack.pop() 
            nfa1 = stack.pop()
            
            #connect both nfa fragments 
            
            for accept_states in list(nfa1.accepts): #get accept state of left nfa
                for symbol, destinations in nfa2.transitions[nfa2.start].items(): #get the transition table for start state of 2nd nfa
                    for destination in destinations: #get the destinations of symbols of the start state of nfa2
                        nfa1.add_transition(accept_states, symbol, destination) #swap the transition table of nfa2's start state and place it inside the accept state of nfa1
            nfa1.accepts = set(nfa2.accepts) #Nfa 1 will be the bigger NFA so we  set the accept state to the 2nd nfa
            nfa1.states.update(nfa2.states) #merge the nfa states
            nfa1.transitions.update(nfa2.transitions)
            stack.append(nfa1)
                    
        elif token == '+':  # union
            n2 = stack.pop()
            n1 = stack.pop()
            nfa = NFA()
            s = nfa.add_state(new_state(), is_start=True)
            # copy n1
            nfa.states |= n1.states
            nfa.transitions.update(n1.transitions)
            nfa.accepts |= n1.accepts
            # copy n2
            nfa.states |= n2.states
            nfa.transitions.update(n2.transitions)
            nfa.accepts |= n2.accepts
            # connect new start to both n1 and n2 starts
            for sym, dests in n1.transitions[n1.start].items():
                for d in dests:
                    nfa.add_transition(s, sym, d)
            for sym, dests in n2.transitions[n2.start].items():
                for d in dests:
                    nfa.add_transition(s, sym, d)
            stack.append(nfa)

        elif token == '*':  # kleene star
            n = stack.pop()
            # Make start state accepting
            n.accepts.add(n.start)
            # Add loops on transitions from accept states
            for a in list(n.accepts):
                for sym, dests in list(n.transitions[n.start].items()):
                    for d in dests:
                        n.add_transition(a, sym, d)
            stack.append(n)

    return stack.pop()

        
def standardize(regex): 
    result = [] 
    operators = set(['*', '.', '+'])
    prev = None 
    for c in regex: 
        if prev is not None: # in between 2 symbols we add a dot, if its closing parentheses then an opening, then we add a dot
            if (prev not in operators and prev != '(') or prev == "*" or prev == ")": 
                if c not in operators and c != ')' or c == "(": 
                    result.append('.') 
        result.append(c) 
        prev = c 
    return ''.join(result)

def postfix(regex):
    
    operators = {"*":3, ".":2, "+":1}
    result= []
    stack = []
    
    for c in regex:
        if str(c).isalnum():
            result.append(c)
        elif c == "(":
            stack.append(c)
        elif c == ")":
            while stack and stack[-1] != "(":
                result.append(stack.pop())
            stack.pop()
        else: #finds an operator
            while stack and stack[-1] != "(" and operators[stack[-1]] >= operators[c]:
                result.append(stack.pop())
            stack.append(c)
            
    while stack:
        result.append(stack.pop())
    return "".join(result)


def main():
    regex = "ab+(ba)*"
    print(f"Regex: {regex}")
    postfix1 = postfix(standardize(regex))
    print(f"Postfix: {postfix1}")
    nfa = regex_to_nfa(postfix1)
    nfa = reconstruct(nfa)
    nfa.display()
    
    test_strings = ["", "ab","ba","baba","abab"]
    for s in test_strings:
        print(f"{s}: {'ACCEPTED' if nfa.simulate(s) else 'REJECTED'}")
    
    print("\nAccept States:")
    print("\n".join(i for i in nfa.accepts))
    
    print("\nStart States:")
    print(nfa.start)
    

if __name__ == "__main__":
    main()

