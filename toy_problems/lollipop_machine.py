from typing import Optional

from fsm_service.fsm import FSM
from fsm_service.fsm import State

class LollipopCounter(State):
    def __init__(self, id: str) -> None:
        super().__init__(id=id, val=0)

    def reset_state(self):
        self.value = 0
    
    def update_state(self):
        self.value +=1
    
class LollipopMachine(FSM):
    def __init__(self, persist_on_failure: Optional[bool]=False) -> None:
        #initialze states
        lemon_counter = LollipopCounter(id='Q_l')
        strawberry_couter = LollipopCounter(id='Q_s')
        start = State(id='Q0')
        error = State(id='Q_e')
        end = State(id='Q_f')
        super().__init__(states=[start, 
                                 lemon_counter, 
                                 strawberry_couter, 
                                 error, 
                                 end],
                         symbols=['s', 'l', 'c'],
                         start_state=start, 
                         end_state=end,
                         current_state=start,
                         persist_on_failure=persist_on_failure)
    
    def transition_fn(self, curr_state: State, symbol: str) -> State:
        if symbol not in self.symbols:
            raise Exception("Invalid Symbol")
        if symbol=='c':
            next_state = self.state_lookup["Q_f"]
            return next_state
        if symbol=='l':
            next_state = self.state_lookup["Q_l"]
        elif symbol=='s':
            next_state = self.state_lookup["Q_s"]
        if curr_state.id!=next_state.id:#eg: if l is given to sls
            next_state.reset_state()
        next_state.update_state()
        if next_state.value!=0 and next_state.value%3==0:
            next_state.reset_state()
            next_state = self.state_lookup["Q_e"]
        return next_state
        
