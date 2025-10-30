
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2021-08-17  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
#    return [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def taboo_cells(warehouse):
    '''
    Identify taboo cells of a warehouse.
    
    A "taboo cell" is a cell where if a box is pushed, the puzzle becomes unsolvable.
    Cells outside the playable area (i.e. unreachable from the worker) should not be marked.
    
    The rules are:
      Rule 1: If a cell is a corner (two perpendicular adjacent walls) and is not a target, it is taboo.
      Rule 2: (Not implemented here) All cells between two corners along a wall are taboo if none
              of those cells is a target.
    
    This version uses a flood-fill algorithm to compute the reachable area from the worker’s
    starting position, ensuring that only cells “inside” the warehouse are considered.
    
    @param warehouse: a Warehouse object with at least the following attributes:
                      - walls: a set of (x, y) wall coordinates
                      - targets: a set of (x, y) target coordinates
                      - worker: a tuple (x, y) indicating the worker's starting position
    @return: A string representation of the warehouse grid where walls are '#' and taboo cells are 'X'
             (only the reachable area is marked).
    '''
    
    taboo = taboo_cells_map(warehouse)
    walls = warehouse.walls

    all_coords = walls
    min_x = min(x for x, y in all_coords)
    max_x = max(x for x, y in all_coords)
    min_y = min(y for x, y in all_coords)
    max_y = max(y for x, y in all_coords)

    grid = []
    for y in range(min_y, max_y + 1):
        row = ''
        for x in range(min_x, max_x + 1):
            if (x, y) in walls:
                row += '#'
            elif (x, y) in taboo:
                row += 'X'
            else:
                row += ' '
        grid.append(row)
    return '\n'.join(grid)

def flood_fill(grid, start):
    stack = [start]
    reachable = set()

    while stack:
        x, y = stack.pop()
        if (x, y) in reachable:
            continue
        reachable.add((x, y))
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in grid and (nx, ny) not in reachable:
                stack.append((nx, ny))
    return reachable

def is_corner(grid, x, y):
    wall_up = (x, y - 1) in grid
    wall_down = (x, y + 1) in grid
    wall_left = (x - 1, y) in grid
    wall_right = (x + 1, y) in grid

    return (wall_up and wall_left) or (wall_up and wall_right) or \
           (wall_down and wall_left) or (wall_down and wall_right)
    

# find the taboo coords, NOT STRING 
def taboo_cells_map(warehouse):
    walls = warehouse.walls
    targets = warehouse.targets
    worker = warehouse.worker

    # Create a grid dictionary to mark walls
    grid = {}
    for (x, y) in walls:
        grid[(x, y)] = '#'

    # Use flood fill to get reachable positions from the worker
    reachable = flood_fill(grid, worker)

    taboo = set()

    # Rule 1: Add corner taboo cells
    for (x, y) in reachable:
        if (x, y) in targets or (x, y) in walls:
            continue
        wall_up = (x, y - 1) in walls
        wall_down = (x, y + 1) in walls
        wall_left = (x - 1, y) in walls
        wall_right = (x + 1, y) in walls

        if (wall_up and wall_left) or (wall_up and wall_right) or \
           (wall_down and wall_left) or (wall_down and wall_right):
            taboo.add((x, y))

    # Rule 2: Mark straight lines between two corners along a wall (no targets allowed)
    min_x = min(x for x, y in reachable)
    max_x = max(x for x, y in reachable)
    min_y = min(y for x, y in reachable)
    max_y = max(y for x, y in reachable)

    # Horizontal scan
    for y in range(min_y, max_y + 1):
        x = min_x
        while x <= max_x:
            segment = []
            while (x, y) in reachable and not ((x,y) in targets) and not ((x,y) in walls):
                segment.append((x, y))
                x += 1
            if len(segment) >= 2:
                left_wall = (segment[0][0] - 1, y) in walls
                right_wall = (segment[-1][0] + 1, y) in walls
                wall_above = all((x, y - 1) in walls for (x, y) in segment)
                wall_below = all((x, y + 1) in walls for (x, y) in segment)
                if left_wall and right_wall and (wall_above or wall_below):
                    taboo.update(segment)
            x += 1

    # Vertical scan
    for x in range(min_x, max_x + 1):
        y = min_y
        while y <= max_y:
            segment = []
            while (x, y) in reachable and not ((x,y) in targets) and not ((x,y) in walls):
                segment.append((x, y))
                y += 1
            if len(segment) >= 2:
                top_wall = (x, segment[0][1] - 1) in walls
                bottom_wall = (x, segment[-1][1] + 1) in walls
                wall_left = all((x - 1, y) in walls for (x, y) in segment)
                wall_right = all((x + 1, y) in walls for (x, y) in segment)
                if top_wall and bottom_wall and (wall_left or wall_right):
                    taboo.update(segment)
            y += 1

    return taboo


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from scipy.optimize import linear_sum_assignment
import numpy as np

class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes

    # ------------ CLASS VARS ---------------
    DIR_DELTA = {
        'Left':  (-1, 0),
        'Right': (1, 0),
        'Up':    (0, -1),
        'Down':  (0, 1)
    }

    
    # ---------- CODE --------------
    def __init__(self, warehouse):
        self.worker = warehouse.worker
        self.walls = warehouse.walls
        self.targets = warehouse.targets
        self.boxes = warehouse.boxes
        self.size = (warehouse.ncols, warehouse.nrows)
        self.boxes_with_weights = set(zip(warehouse.boxes, warehouse.weights)) # zip weights and coords into frozenset
        self.initial = (self.worker, frozenset(self.boxes_with_weights)) # set for efficiency
        self.taboo = taboo_cells_map(warehouse)
        assert self.worker not in self.walls
        assert self.boxes not in self.walls
        assert self.targets not in self.walls
        assert len(self.boxes) != 0




    
    def actions(self, state):
        """
        Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        """
        worker = state[0]
        box_pos = {pos for (pos, _) in state[1]} # extract positions

        L = [] # list of legal actions

        for direction, (dx, dy) in self.DIR_DELTA.items():
            # test positions around worker
            new_pos = (worker[0] + dx, worker[1] + dy)
            
            # if new pos is a box, check if it can be pushed
            if new_pos in box_pos:
                box_push = (new_pos[0] + dx, new_pos[1] + dy)
                # taboo avoided unless theyre targets
                if box_push not in box_pos and box_push not in self.walls and (box_push not in self.taboo or box_push in self.targets):
                    L.append(direction)
            # check if a new position is not a wall
            elif new_pos not in self.walls:
                L.append(direction)

        # print(f"State: {state}")
        # print(f"Legal actions: {L}")
        return L # return legal actions
    
    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        """
        assert action in self.actions(state)

        worker, boxes = state
        dx, dy = self.DIR_DELTA[action]
        new_worker = (worker[0] + dx, worker[1] + dy)

        new_boxes_pos = {pos for (pos, _) in boxes}
        new_boxes = set(boxes)

        # if new worker position is a box, update box position
        if new_worker in new_boxes_pos:
            # Grab matching (coords, weight) box
            old_box = next((coords, weight) for (coords, weight) in boxes if coords == new_worker)
            weight = old_box[1]
            new_box_pos = (new_worker[0] + dx, new_worker[1] + dy) # update position to one way from worker, same directtion
            new_box = (new_box_pos, weight) # make new box

            new_boxes.remove(old_box)
            new_boxes.add(new_box)

        # print(f"Action: {action}, Worker: {worker} -> {new_worker}")
        # print(f"Boxes: {boxes} -> {new_boxes}")

        return (new_worker, frozenset(new_boxes))
    

    # def value(self, state):
    #     """
    #     For optimization problems, each state has a value.  Hill-climbing
    #     and related algorithms try to maximize this value.
    #     """
    #     raise NotImplementedError
    
    # def goal_test(state):
    #     """Return True if the state is a goal. The default method compares the
    #     state to self.goal, as specified in the constructor. Override this
    #     method if checking against a single self.goal is not enough."""
    #     return state == self.targets
    
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        worker1, boxes1 = state1
        worker2, boxes2 = state2

        # If a box was moved, find the one that changed
        box_diff = boxes2 - boxes1
        if box_diff:
            # Get the (new_pos, weight) of the moved box
            (new_pos, weight) = next(iter(box_diff))
            return c + weight + 1
        else:
            return c + 1


    def h(self, node):
        # worker, boxes = node.state
        # total_dist = 0
        # for box_pos, weight in boxes:
        #     # Manhattan distance from this box to the closest target
        #     closest_target_dist = min( abs(box_pos[0] - tx) + abs(box_pos[1] - ty) for (tx, ty) in self.targets )
        #     total_dist += closest_target_dist * weight
        # return total_dist
        # hungarian
        boxes = list(node.state[1])
        targets = list(self.targets)

        cost_matrix = np.zeros((len(boxes), len(targets)))
        for i, (box_pos, weight) in enumerate(boxes):
            for j, target in enumerate(targets):
                dist = abs(box_pos[0] - target[0]) + abs(box_pos[1] - target[1])
                if (weight):
                    cost_matrix[i][j] = dist * weight
                else:
                    cost_matrix[i][j] = dist

        # hungarian algorithm
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        return int(sum(cost_matrix[row][col] for row, col in zip(row_ind, col_ind)))

    def goal_test(self, state):
        box_positions = {pos for (pos, _) in state[1]}
        return box_positions == set(self.targets)
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    worker = warehouse.worker
    boxes = warehouse.boxes
    walls = warehouse.walls
    DIR_DELTA = {
        'Left':  (-1, 0),
        'Right': (1, 0),
        'Up':    (0, -1),
        'Down':  (0, 1)
    }
    
    for action in action_seq:
        dx, dy = DIR_DELTA[action]
        new_worker = (worker[0] + dx, worker[1] + dy)
         # if new pos is in a wall, return
        if new_worker in walls:
            return "Impossible"
        # if new position is a box, and the following position is a box or a wall, return
        if (new_worker in boxes) and ((new_worker[0] + dx, new_worker[1] + dy) in walls or boxes):
            return "Impossible"
        # if new pos is a box, move box
        if new_worker in boxes:
            newbox = (new_worker[0] + dx, new_worker[1] + dy)
            boxes.remove(new_worker)
            boxes.add(newbox)
        # move worker if all passes
        worker = new_worker

    # Return the grid as a string.
    warehouse.worker = worker
    warehouse.boxes = boxes
    return warehouse.__str__()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    
    problem = SokobanPuzzle(warehouse)
    node = search.astar_graph_search(problem, problem.h)
    if not node:
        return "Impossible", None
    return node.solution(), node.path_cost



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

