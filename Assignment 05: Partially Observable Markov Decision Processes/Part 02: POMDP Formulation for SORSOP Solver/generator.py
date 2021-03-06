# Initializing basic parameters for POMDP
actions = ['stay', 'up', 'down', 'left', 'right']
observations = ['o1', 'o2', 'o3', 'o4', 'o5', 'o6']
cells = []
states = []
transitions = []
initial_belief = []
observation_fn = []
rewards = []

# For determining the probability for the given transition
def find_prob(action, i, j):  
    px = 0.79
    pox = 0.21

    a1x = i[0][0]
    a1y = i[0][1]
    a2x = j[0][0]
    a2y = j[0][1]  

    t1x = i[1][0]
    t1y = i[1][1]
    t2x = j[1][0]
    t2y = j[1][1]

    p = 0.0

    # Target's movement
    if t1x == t2x:
        if abs(t2y - t1y) == 1:
            p = 0.15
    if t1y == t2y:
        if abs(t2x - t1x) == 1:
            p = 0.15
    if t1x == t2x and t1y == t2y:
        if t1x == 1 and t1y == 1:
            p = 0.55
        else:
            p = 0.40

    # Call status
    if i[2] == 0:
        if j[2] == 0:
            p *= 0.60
        elif j[2] == 1:
            p *= 0.40
    elif i[2] == 1:
        if j[2] == 0:
            p *= 0.20
        elif j[2] == 1:
            p *= 0.80 

    # Agent's movement
    if action == 'stay':
        if a1x == a2x and a1y == a2y:
            p *= 1.0
        else:
            p *= 0.0
    elif action == 'up':
        if a1x == a2x:
            if a1x == 2 and a1y == a2y:
                p *= px
            elif a2y - a1y == 1:
                p *= px
            elif a1y - a2y == 1:
                p *= pox
        else:
            p *= 0.0
    elif action == "down":
        if a1x == a2x:
            if a1x == 0 and a1y == a2y:
                p *= px
            elif a1y - a2y == 1:
                p *= px
            elif a2y - a1y == 1:
                p *= pox
        else:
            p *= 0.0
    elif action == "left":
        if a1y == a2y:
            if a1y == 0 and a1x == a2x:
                p *= px
            elif a1x - a2x == 1:
                p *= px
            elif a2x - a1x == 1:
                p *= pox
        else:
            p *= 0.0
    elif action == "right":
        if a1y == a2y:
            if a1x == 2 and a1y == a2y:
                p *= px
            elif a2x - a1x == 1:
                p *= px
            elif a1x - a2x == 1:
                p *= pox
        else:
            p *= 0.0

    return p    

# For determining the observational probabilities
def find_observation(action, state, obs):
    if state[0] == state[1] and obs == 'o1':
        return 1.0
    elif state[0][1] == state[1][1] and state[1][0] - state[0][0] == 1 and obs == 'o2':
        return 1.0
    elif state[0][0] == state[1][0] and state[0][1] - state[1][1] == 1 and obs == 'o3':
        return 1.0
    elif state[0][1] == state[1][1] and state[0][0] - state[1][0] == 1 and obs == 'o4':
        return 1.0
    elif state[0][0] == state[1][0] and state[1][1] - state[0][1] == 1 and obs == 'o5':
        return 1.0
    elif obs == 'o6':
        return 1.0

    return 0.0

# For determining the rewards
def find_reward(action, si, sj, obs):
    if find_prob(action, si, sj) != 0.0:
        if action == 'stay' and si[1] == sj[1]:
            return 0
        elif action  == 'stay' and sj[0] == sj[1] and sj[2] ==1:
            return 30
        elif sj[0] == sj[1] and sj[2] == 1:
            return -1  + 30
        else:
            return -1
    else:
        return 0

# For generating all the cells of the matrix
for i in range(0,3):
    for j in range(0, 3):
        cells.append((i, j))

# For generating all the states of the POMDP
for i in cells:
    for j in cells:
        for call in range(0,2):
            states.append((i, j, call))

# # For generating different types of  transistions
for i in states:
    for j in states:
        for action in actions:
                transitions.append("T: " + action + " : " + str(i).replace(' ', '') + " : " + str(j).replace(' ', '') + " " + str(find_prob(action, i, j)))

# For generating the initial belief state
for state in states:
    if state[1] == '(1,1)':
        if state[0] == '(0,0)' or state[0] == '(0,2)' or state[0] == '(2,2)' or state[0] =='(2,0)':
            initial_belief.append("0.125")
        else:
            initial_belief.append("0.0")
    else:
        initial_belief.append("0.0")

# For generating the observation probabilities
for action in actions:
    for state in states:
        for observation in observations:
                observation_fn.append("O: " + action + " : " + str(state).replace(' ', '') + " : " + observation + " " + str(find_observation(action, state, observation)))

# Generating the rewards
for action in actions:
    for si in states:
        for sj in states:
            for obs in observations:
                rewards.append("R: " + action + " : " + str(si).replace(' ', '') + " : " +  str(sj).replace(' ', '') +  " : " + obs + " " + str(find_reward(action, si, sj, obs)))

# Generate the parameters by changing the X.append to print and execute the following commands for getting each paramters in separate files.
# python3 generator.py > states.txt
# python3 generator.py > transition.txt
# python3 generator.py > observations.txt
# python3 generator.py > rewards.txt