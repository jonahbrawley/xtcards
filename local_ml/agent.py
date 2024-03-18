import numpy as np
import random

class Agent:
    weights = np.array([
            [ 0.03819951, -1.03355934, -0.09588605,  0.13251864, -0.09245909, 0.07737056, -1.04014128],
            [ 0.10645625, -0.27743013,  0.09613875,  0.11725271,  0.23562889, 0.09762969, -1.02672867],
            [ 2.02177145,  0.19779792, -0.05365719, -0.1985246 , -0.30240015, -4.9486393 ,  2.55148784]])

    @staticmethod
    def predict(ai_state):
        # process ai_state
        p_s = Agent.process_state(ai_state)
        
        # should fold?
        fold_class = p_s @ Agent.weights[0][:-1]
        pass_fold = Agent.sigmoid(Agent.weights[0][-1]) > random.random()
        if fold_class > 0 and not pass_fold:
            return 'fold', 0
        
        # # should call or raise?
        call_class = p_s @ Agent.weights[1][:-1]
        pass_call = Agent.sigmoid(Agent.weights[1][-1]) > random.random()
        if call_class > 0 and not pass_call:
            return 'call', 0
        
        # # how much raise?
        raise_out = (p_s @ Agent.weights[2][:-1])
        raise_activated = Agent.sigmoid(raise_out)
        raise_chips = int(round(raise_activated * (ai_state['ai_chips'] - ai_state['min_req_bet'])))
        
        if raise_chips <= 0:
            return "call", 0
            
        return 'raise', raise_chips
    
    @staticmethod
    def process_state(ai_state):
        p_s = np.ndarray(6,)
        
        # river state
        if ai_state['river_state'] == 'PREFLOP':
            p_s[0] = 0.0
        elif ai_state['river_state'] == 'FLOP':
            p_s[0] = 0.3333333
        elif ai_state['river_state'] == 'TURN':
            p_s[0] = 0.6666666
        elif ai_state['river_state'] == 'RIVER':
            p_s[0] = 1.0
    
        # hand strength
        p_s[1] = np.log10((float(ai_state["ai_hand_strength"]) / 0.8e13)-0.03) + 1.0
    
        # rough % estimate of chips the ai has already bet
        curr_chips = float(ai_state['ai_chips'])
        starting_chips = curr_chips + ai_state['ai_total_bets']
        total_bets_ratio =  1 - (curr_chips / starting_chips)
        p_s[2] = total_bets_ratio
    
        # % of current chip count for min_req_bet
        p_s[3] = ai_state['min_req_bet'] / (curr_chips + 1e-5)


        # remember if raised
        p_s[4] = 1.0 if (ai_state['ai_last_action'] == 'raise') else 0
        
        # bias
        p_s[5] = 1.0
    
        return p_s

    
    @staticmethod
    def sigmoid(x):
        # print(x)
        return 1.0 / (1.0 + np.exp(-x))