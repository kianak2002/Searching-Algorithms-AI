'''
class for nodes
we save the butter and robot for each node
and also parent and th action from parent for path
'''


class node():
    def __init__(self, parent, robot, butter, action_from_par):
        self.parent = parent
        self.robot = robot
        self.butter = butter
        self.action_from_par = action_from_par


'''
class for map and finding robot and butters and plates and obstacles position
and check the available actions for both normal and reversed movements
'''


class environment():
    def __init__(self, map_file):
        self.rows, self.cols = map(int, map_file.readline().split())
        self.table = [map_file.readline().split() for j in range(self.rows)]
        self.find_people()
        self.find_butter()

    '''
    to have the plates and butters position
    '''

    def map(self):
        return self.people_list, self.butter_list

    '''
    to find plates(people) position
    '''

    def find_people(self):
        self.people_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                if 'p' in self.table[i][j]:
                    self.people_list.append((i, j))

    '''
    to find robot position
    '''

    def find_robot(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if 'r' in self.table[i][j]:
                    return i, j

    '''
    to find the butters position
    '''

    def find_butter(self):
        self.butter_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                if 'b' in self.table[i][j]:
                    self.butter_list.append((i, j))

    '''
    to find the obstacles position
    '''

    def find_obstacles(self):
        self.obstacle_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                if 'x' in self.table[i][j]:
                    self.obstacle_list.append((i, j))

    '''
    check all the available actions for robot and return them
    '''

    def available_actions(self, robot, butter):
        actions = []
        if robot[0] - 1 >= 0 and self.table[robot[0] - 1][robot[1]] != "x":
            if butter == (robot[0] - 1, robot[1]):
                if robot[0] - 2 >= 0 and self.table[robot[0] - 2][robot[1]] != "x":
                    actions.append("U")
            else:
                actions.append("U")

        if robot[0] + 1 < self.rows and self.table[robot[0] + 1][robot[1]] != "x":
            if butter == (robot[0] + 1, robot[1]):
                if robot[0] + 2 < self.rows and self.table[robot[0] + 2][robot[1]] != "x":
                    actions.append("D")
            else:
                actions.append("D")

        if robot[1] - 1 >= 0 and self.table[robot[0]][robot[1] - 1] != "x":
            if butter == (robot[0], robot[1] - 1):
                if robot[1] - 2 >= 0 and self.table[robot[0]][robot[1] - 2] != "x":
                    actions.append("L")
            else:
                actions.append("L")

        if robot[1] + 1 < self.cols and self.table[robot[0]][robot[1] + 1] != "x":
            if butter == (robot[0], robot[1] + 1):
                if robot[1] + 2 < self.cols and self.table[robot[0]][robot[1] + 2] != "x":
                    actions.append("R")
            else:
                actions.append("R")
        return actions

    '''
    check the action given with all available actions
    if allowed then it moves the robot and if needed the butter
    '''

    def step(self, robot, butter, action):
        # action : "U", "D", "R", "L"
        # robot: tuple (x, y)
        if action not in self.available_actions(robot, butter):
            raise ValueError("action is not available")

        if action == "U":
            next_robot = robot[0] - 1, robot[1]
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            if next_robot == butter:
                butter = butter[0] - 1, butter[1]
            return next_robot, butter, int(cost)

        elif action == "D":
            next_robot = robot[0] + 1, robot[1]
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            if next_robot == butter:
                butter = butter[0] + 1, butter[1]
            return next_robot, butter, int(cost)

        elif action == "L":
            next_robot = robot[0], robot[1] - 1
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            if next_robot == butter:
                butter = butter[0], butter[1] - 1
            return next_robot, butter, int(cost)

        elif action == "R":
            next_robot = robot[0], robot[1] + 1
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            if next_robot == butter:
                butter = butter[0], butter[1] + 1
            return next_robot, butter, int(cost)

        else:
            raise ValueError("action is wrong")

    '''
    check all the available actions for robot in reversed state and return them
    '''

    def available_actions_reverse(self, robot, butter):
        actions = []
        if robot[0] - 1 >= 0 and self.table[robot[0] - 1][robot[1]] != "x":
            if butter != (robot[0] - 1, robot[1]):
                actions.append("U")

        if robot[0] + 1 < self.rows and self.table[robot[0] + 1][robot[1]] != "x":
            if butter != (robot[0] + 1, robot[1]):
                actions.append("D")

        if robot[1] - 1 >= 0 and self.table[robot[0]][robot[1] - 1] != "x":
            if butter != (robot[0], robot[1] - 1):
                actions.append("L")

        if robot[1] + 1 < self.cols and self.table[robot[0]][robot[1] + 1] != "x":
            if butter != (robot[0], robot[1] + 1):
                actions.append("R")

        return actions

    '''
    check the action given with all available actions for the reversed state
    if allowed then it moves the robot and if needed the butter
    '''

    def step_inverse(self, robot, butter, action):
        # action : "U", "D", "R", "L"
        # robot: tuple (x, y)
        if action not in self.available_actions_reverse(robot, butter):
            raise ValueError("action is not available")

        if action == "U":
            next_robot = robot[0] - 1, robot[1]
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            robot_D = robot[0] + 1, robot[1]
            if butter == robot_D:
                butter = robot
            return next_robot, butter, int(cost)

        elif action == "D":
            next_robot = robot[0] + 1, robot[1]
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            robot_U = robot[0] - 1, robot[1]
            if butter == robot_U:
                butter = robot
            return next_robot, butter, int(cost)

        elif action == "L":
            next_robot = robot[0], robot[1] - 1
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            robot_R = robot[0], robot[1] + 1
            if butter == robot_R:
                butter = robot
            return next_robot, butter, int(cost)

        elif action == "R":
            next_robot = robot[0], robot[1] + 1
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            robot_L = robot[0], robot[1] - 1
            if butter == robot_L:
                butter = robot
            return next_robot, butter, int(cost)

        else:
            raise ValueError("action is wrong")


'''
class for bidirectional method and returning the path and actions
'''


class agent():
    def __init__(self, env):
        self.env = env
        self.butter = env.find_butter()
        self.robot = env.find_robot()
        self.people = env.find_people()

    '''
    The Main Method!!!
    for the normal walking from the start node its as same as bfs
    for the reversed walking the goal is butter in plate and robot next to them
    so for reversed we start from all the states that robot is next to the plates(people)
    returns the robot position for the other movements
    returns the path and actions
    '''

    def bidirectional_bfs(self, people_list, butter, robot):
        queue_r = []
        queue_p = []
        is_visited_r = {}
        is_visited_p = {}
        root_r = node(None, robot, butter, None)
        queue_r.append(root_r)

        for i in range(len(people_list)):
            actions = env.available_actions(people_list[i], people_list[i])
            for a in actions:
                next_robot, next_butter, _ = env.step(people_list[i], people_list[i], a)
                child = node(None, robot=next_robot, butter=people_list[i], action_from_par=None)
                queue_p.append(child)

        while len(queue_p) > 0 and len(queue_r) > 0:
            node_r = queue_r.pop(0)
            node_p = queue_p.pop(0)
            is_visited_r[node_r.robot + node_r.butter] = node_r
            is_visited_p[node_p.robot + node_p.butter] = node_p
            #  the robots see each other:)) and the butters are in the same position
            if node_r.robot + node_r.butter in is_visited_p.keys():
                action_path, path = self.show_bidirectional_path(node_r, is_visited_p[node_r.robot + node_r.butter])
                n = is_visited_p[node_r.robot + node_r.butter]
                while n.parent != None:
                    n = n.parent
                return n.robot, action_path, path
            if node_p.robot + node_p.butter in is_visited_r.keys():
                action_path, path = self.show_bidirectional_path(is_visited_r[node_p.robot + node_p.butter], node_p)
                n = node_p
                while n.parent != None:
                    n = n.parent
                return n.robot, action_path, path
            actions = env.available_actions(node_r.robot, node_r.butter)
            for a in actions:
                next_robot, next_butter, _ = env.step(node_r.robot, node_r.butter, a)
                if next_robot + next_butter not in is_visited_r.keys():
                    child = node(node_r, next_robot, next_butter, a)
                    queue_r.append(child)

            actions = env.available_actions_reverse(robot=node_p.robot, butter=node_p.butter)
            for a in actions:
                next_robot, next_butter, _ = env.step_inverse(robot=node_p.robot, butter=node_p.butter, action=a)
                if next_robot + next_butter not in is_visited_p.keys():
                    child = node(node_p, next_robot, next_butter, a)
                    queue_p.append(child)
        return [], [], []

    '''
    building the path correctly and returns it
    also returns the actions the same way
    '''

    def show_bidirectional_path(self, final_node_r, final_node_p):
        path = []
        action_path = []
        n = final_node_r
        print("****")
        while n.parent != None:
            path.append(n.robot)
            action_path.append(n.action_from_par)
            n = n.parent
        path.append(n.robot)
        path.reverse()
        action_path.reverse()
        n = final_node_p
        while n.parent != None:
            action_path.append(self.inverse(n.action_from_par))
            n = n.parent
            path.append(n.robot)
        return action_path, path

    '''
    just for inversing the actions for the reversed state
    '''

    def inverse(self, action):
        if action == "U":
            return "D"
        if action == "D":
            return "U"
        if action == "R":
            return "L"
        if action == "L":
            return "R"


def beauty(table, cols):
    for i in range(len(table)):
        print(*table[i], sep='\t\t')


'''
to draw a map step by step
'''


def terminal(table, cols, path, action, butter):
    print()
    beauty(table, cols)
    print('------------------------------------------')
    xButter, yButter = butter[0], butter[1]
    check = False
    for i in range(1, len(action) + 1):
        print(table[path[i][0]][path[i][1]])
        table[path[i][0]][path[i][1]] += 'r'
        if path[i][0] == xButter and path[i][1] == yButter:
            check = True
            table[path[i][0]][path[i][1]] = table[path[i][0]][path[i][1]].replace('b', '')
        if action[i - 1] == 'U':
            table[path[i][0] + 1][path[i][1]] = table[path[i][0] + 1][path[i][1]].replace('r', '')
            if check:
                table[path[i][0] - 1][path[i][1]] += 'b'
                xButter -= 1
        if action[i - 1] == 'D':
            table[path[i][0] - 1][path[i][1]] = table[path[i][0] - 1][path[i][1]].replace('r', '')
            if check:
                table[path[i][0] + 1][path[i][1]] += 'b'
                xButter += 1
        if action[i - 1] == 'R':
            table[path[i][0]][path[i][1] - 1] = table[path[i][0]][path[i][1] - 1].replace('r', '')
            if check:
                table[path[i][0]][path[i][1] + 1] += 'b'
                yButter += 1
        if action[i - 1] == 'L':
            table[path[i][0]][path[i][1] + 1] = table[path[i][0]][path[i][1] + 1].replace('r', '')
            if check:
                table[path[i][0]][path[i][1] - 1] += 'b'
                yButter -= 1
        check = False
        beauty(table, cols)
        print('--------------------------------------')


'''
prints the path and actions and cost and goal depth
'''
if __name__ == "__main__":
    with open("test1.txt", "r") as file:
        env = environment(file)
    people_list, butter_list = env.map()
    beauty(env.table, env.cols)
    robot = env.find_robot()
    test_agent = agent(env)
    for i in range(len(butter_list)):
        robot, action_path, path = test_agent.bidirectional_bfs(people_list, butter_list[i], robot)
        if path == []:
            print("Impossible")
        print("path:", path)
        print("actions:", action_path)
        print("cost:", len(action_path))
        print("goal depth:", len(action_path))

        terminal(env.table, env.cols, path, action_path, butter_list[i])
