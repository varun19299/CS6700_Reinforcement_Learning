'''
RL Assignment - 2

Bellman operator class.

Used by q2.py
'''

# Library imports
import numpy as np 
import matplotlib.pyplot as plt

class Bellman(object):
    '''
    Implement bellman equations.
    Implements solving them (VI, PI, API etc)

    '''
    def __init__(self,terminal_state,states,actions,n_stages=-1,minimise=True):
        '''
        Args:

        * states: Doesnot include terminal state, list of states (in order)
        * actions: List of actions possible at each stage. If an action is not possible at each stage, set the prob likewise.

        '''
        self.states=np.array(states)
        self.actions=np.array(actions)
        self.n_states=len(states)
        self.n_actions=len(actions)
        self.n_stages=n_stages
        self._J=np.zeros(self.n_states)
        self._r=np.zeros((self.n_states,self.n_states,self.n_actions))
        self._P=np.zeros((self.n_states,self.n_states,self.n_actions))
        self.minimise=minimise

    @property
    def J(self):
        '''
        Reward or cost function. Defined at a stage.
        '''
        return self._J

    @J.setter
    def J(self,vec):
        if len(vec)==self.n_states:
            self._J=vec

    @property
    def r(self):
        '''
        Reward/ Cost mapping for a particular action-state set.
        '''
        return self._r
    
    @r.setter
    def r(self,mat):
        if mat.shape==(self.n_states,self.n_states,self.n_actions):
            self._r=mat

    @property
    def P(self):
        '''
        Transition probabilities for a particular action from a particular state to another.
        '''
        return self._P
    
    @P.setter
    def P(self,mat):
        if mat.shape==(self.n_states,self.n_states,self.n_actions):
            self._P=mat

    def T(self):
        '''
        Bellman Operator T.
        '''
        if self.minimise:
            self._J=np.min(np.sum(self.r*self.P+self.P*self.J[np.newaxis,:,np.newaxis],axis=1),axis=1)
        else:
            self._J=np.max(np.sum(self.r*self.P+self.P*self.J[np.newaxis,:,np.newaxis],axis=1),axis=1)
        
    def T_pi(self,pi):
        '''
        Pi maps states to actions
        pi[state]=action
        '''
        actions=pi[self.states]
        i=list(range(self.n_states))
        self._J=np.sum(self.r[i,:,pi[i]]*self.P[i,:,pi[i]] + self.P[i,:,pi[i]]*self.J[np.newaxis,:,np.newaxis],axis=1)
    
    def stationary_policy(self,pi,epsilon=0.01):
        '''
        Find the stationary policy for a given J

        Args:
        * pi: a mapping from states to actions.
        * epsilon: threshold for maximal difference comparison.
        '''
        J_prev=self.J
        self.T_pi(pi)
        J_af=self.J
        while np.max(np.abs(J_prev-J_af))>epsilon:
            J_prev=J_af
            self.T_pi(pi)
            J_af=self.J
            if self.minimise:
                print(f"Cost to go is {self.J}")
            else:
                print(f"Reward to go is {self.J}")

    def optimal_policy(self,epsilon=0.01,verbose=False):
        '''
        Find the optimal policy starting at a given J.

        Agrs:
        * epsilon: threshold for maximal difference comparison.
        * verbose: whether to print policies at each stage.

        Returns:
        * J_array,actions_array: indexed from N to 1. (imp)
        '''
        count=0
        J_prev=self.J
        self.T()
        J_af=self.J
        J_array=[J_af]
        actions_array=[]

        while (np.max(np.abs(J_prev-J_af))>epsilon and self.n_stages<0) or (count<self.n_stages):
            J_prev=J_af
            self.T()
            J_af=self.J
            J_array.append(J_af)
            if self.minimise:
                print(f"Cost to go is {self.J} at count {count}")
            else:
                print(f"Reward to go is {self.J} at count {count}")

            if verbose:
                # Record actions
                actions=self.read_optimal_policy()
                actions_array.append(actions)
            count+=1

        return J_array,actions_array

    def read_optimal_policy(self):
        '''
        Prints optimal policy at each {stage}.
        '''
        if self.minimise:
            actions= np.argmin(np.sum(self.r*self.P+self.P*self.J[np.newaxis,:,np.newaxis],axis=1),axis=1)
        else:
            actions= np.argmax(np.sum(self.r*self.P+self.P*self.J[np.newaxis,:,np.newaxis],axis=1),axis=1)
        print({f"state {state}":f"action {action}" for state,action in zip(range(self.n_states),actions)})
        return actions

def main():
    '''
    Test fixture with Q1.
    '''
    bel=Bellman(1,[0,1,2],[0,1,2],10,False)
    bel.J=np.zeros(3)
    
    P=np.zeros((3,3,3))
    P[:,:,0]=np.array([[1/2,1/4,1/4],[1/16,3/4,3/16],[1/4,1/8,5/8]])
    P[:,:,1]=np.array([[1/2,0,1/2],[1/16,7/8,1/16],[0,0,0]])
    P[:,:,2]=np.array([[1/4,1/4,1/2],[1/8,3/4,1/8],[3/4,1/16,3/16]])

    bel.P=P

    r=np.zeros((3,3,3))
    r[:,:,0]=np.array([[10,4,8],[8,2,4],[4,6,4]])
    r[:,:,1]=np.array([[14,0,18],[8,16,8],[0,0,0]])
    r[:,:,2]=np.array([[10,2,8],[6,4,2],[4,0,8]])

    bel.r=r

    bel.optimal_policy()

    bel.read_optimal_policy()

if __name__=='__main__':
    main()
