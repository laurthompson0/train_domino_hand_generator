import random

def generate_dominos():
    dominos = []
    for i in range(13):
        for j in range(i,13):
            dominos.append(set([i, j]))
    return dominos


def generate_hand(size: int):
    dominos = generate_dominos()
    hand_size = 0
    hand = []
    while hand_size < size:
        selected_domino = dominos[random.randint(0, len(dominos)-1)]
        if selected_domino not in hand:
            hand.append(selected_domino)
            hand_size += 1
    return hand

def get_next_domino(current_train: list[list], current_hand: list[set], desired_val: int):
        new_train = current_train.copy()
        new_hand = current_hand.copy()
        idxs = []
        for idx, domino in enumerate(new_hand):
            if desired_val in domino:
                idxs.append(idx)
        if not idxs:
            return new_train, new_hand
        next_domino_idx = idxs[random.randint(0, len(idxs)-1)]
        next_domino = new_hand[next_domino_idx].copy()
        del new_hand[next_domino_idx]
        
        next_domino.remove(desired_val)
        if len(next_domino) == 0:
            other_val = desired_val
        else: other_val = next_domino.pop()
        new_train.append([desired_val, other_val])

        return new_train, new_hand

def generate_train(hand: list[set], start: int):
    current_hand = hand.copy()
    current_train = []
    desired_val = start
    
    while current_hand:
        #print(current_train)
        new_train, new_hand = get_next_domino(current_train, current_hand, desired_val)
        #print(current_train)
        if (new_train == current_train):
            #print(current_train)
            break

        current_train = new_train.copy()
        current_hand = new_hand.copy()
        desired_val = current_train[-1][-1]

    
    return (current_train, current_hand)
    
def generate_best_train(hand: list[set], start: int, num_trails: int):
    best_train = []
    best_hand = []
    for i in range(num_trails):
        current_train, current_hand = generate_train(hand, start)
        if len(current_train) > len(best_train):
            best_train = current_train.copy()
            best_hand = current_hand.copy()
        elif len(current_train) == len(best_train):
            sum_current_hand = sum(sum(domino) for domino in current_hand)
            sum_best_hand = sum(sum(domino) for domino in best_hand)
            if sum_current_hand < sum_best_hand:
                best_train = current_train.copy()
                best_hand = current_hand.copy()
        
        if len(best_hand) == 0:
            print(i)
            break

    return best_train, best_hand


def hand_from_user_input():
    hand = []
    inp = ""
    print("Enter comma separated pairs. Hit enter after each pair")
    while True:
        inp = input()
        if "done" in inp:
            break
        vals = inp.split(",")
        hand.append(set((int(vals[0]), int(vals[1]))))
    return hand

                

if __name__ == "__main__":
    #print(generate_dominos())
    hand = generate_hand(25)
    #hand = hand_from_user_input()
    print(hand)
    print(generate_best_train(hand, 12, 100000))
