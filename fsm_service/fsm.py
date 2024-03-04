from typing import Any, List, Optional
from abc import abstractmethod
from datetime import datetime
import pickle

class State:
    def __init__(self, id: str, val: Optional[Any]=None) -> None:
        self.id = id
        self.value = val
    @property
    def value(self):
        return self._val
    
    @value.setter
    def value(self, val: Any):
        self._val = val
    
    @abstractmethod
    def reset_state(self): #to reset the value
        pass
    @abstractmethod
    def update_state(self): #to update the value
        pass

    def __str__(self):
        return f"State: {self.id}, val: {self.value}"

class FSM:
    def __init__(self, 
                 states: List[State], #Q
                 start_state: State, #q0
                 end_state: State, #F
                 symbols: List[str], #Sigma
                 current_state: Optional[State]=None, #for persistence
                 persist_on_failure: Optional[bool]=False
                 ) -> None:
        self.states = states
        self.state_lookup = {state.id: state for state in self.states}
        self.start_state = start_state
        self.end_state = end_state
        self.symbols = symbols
        self._persist_on_failure = persist_on_failure
        self.current_state = self.start_state if not current_state else current_state

    def _process_symbol(self, inp_symbol: str) -> State:
        next_state = self.transition_fn(self.current_state, inp_symbol)
        return next_state
    
    def process_symbols(self, seq: List[str]) -> State:
        try:
            for symbol in seq:
                print(f"({self.current_state.id}) --\'{symbol}\'--> ", end="")
                self.current_state = self._process_symbol(symbol)
                if self.current_state==self.end_state:
                    print(f"({self.current_state.id})")
                    return self.current_state
        except Exception as e:
            print("Encountered a failure!")
            print("Details:-", e)
            if self._persist_on_failure:
                self.persist_state()
            exit(-1) 
        print(f"({self.current_state.id})")
        return self.current_state

    def persist_state(self):
        print("Persisting FSM state..")
        file_name = f"fsm_{datetime.now().strftime('%Y_%m_%d')}.pkl"
        print(f"States persisted in file: {file_name}")
        pickle.dump(self, open(file_name, "wb"))
    
    #tried to store just the values, it got complicated, considering the challenge to resolve state object types
    def restore_machine(self, pkl_file: str):
        self = pickle.load(open(pkl_file, 'rb'))
        return self

    @abstractmethod
    def transition_fn(self, inp: State, symbol: str) -> State:
        return
    
    def __str__(self):
        return f"""Possible States: {[str(c) for c in self.states]}\nCurrent State: {str(self.current_state)}"""
