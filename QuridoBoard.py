MAX_BOARD_SIZE = 16
START_WALL_COUNT = 8
BOARD_AIR = 0
BOARD_PLAYER1 = 1
BOARD_PLAYER2 = 2
BOARD_WALL = 3


class QuridoBoard:
    def __init__(self):
        self.board = [[BOARD_AIR] * (MAX_BOARD_SIZE + 1) for i in range(MAX_BOARD_SIZE + 1)]
        self.left_wall = [-1, START_WALL_COUNT, START_WALL_COUNT]
        self.board[int(MAX_BOARD_SIZE/2)][2] = BOARD_PLAYER1
        self.board[int(MAX_BOARD_SIZE/2)][MAX_BOARD_SIZE-2] = BOARD_PLAYER2
        self.player_pos = [[-1, -1], [int(MAX_BOARD_SIZE/2), 2], [int(MAX_BOARD_SIZE/2), MAX_BOARD_SIZE - 2]]

    def move_player(self, player_num, direction):
        if self.can_move(player_num, self.player_pos[player_num][0], self.player_pos[player_num][1], direction) == "walk":
            if self.move_player_pos(player_num, direction):
                return True
        return False

    def jump_player(self, player_num, direction, jump_way):
        if self.can_move(player_num, self.player_pos[player_num][0], self.player_pos[player_num][1], direction) == jump_way:
            if self.jump_player_pos(player_num, direction, jump_way):
                return True
        return False

    def use_wall(self, player_num, x2, y2, dir):
        if dir == "vertical":
            x1 = x2
            x3 = x2
            y1 = y2 - 1
            y3 = y2 + 1
        elif dir == "horizon":
            x1 = x2 - 1
            x3 = x2 + 1
            y1 = y2
            y3 = y2
        else:
            return False
        if self.can_use_wall(player_num, x2, y2, dir):
            self.board[x1][y1] = BOARD_AIR
            self.board[x2][y2] = BOARD_AIR
            self.board[x3][y3] = BOARD_AIR
            return True
        else:
            return False

    def get_possible_moves(self, player_num):
        possible_moves = []
        x = self.player_pos[player_num][0]
        y = self.player_pos[player_num][1]
        if self.can_move(player_num, x, y, "up") != "none":
            possible_moves.append(self.can_move(player_num, x, y, "up") + "/up")
        if self.can_move(player_num, x, y, "down") != "none":
            possible_moves.append(self.can_move(player_num, x, y, "down") + "/down")
        if self.can_move(player_num, x, y, "left") != "none":
            possible_moves.append(self.can_move(player_num, x, y, "left") + "/left")
        if self.can_move(player_num, x, y, "right") != "none":
            possible_moves.append(self.can_move(player_num, x, y, "right") + "/right")
        for i in range(8):
            for j in range(8):
                if self.can_use_wall(player_num, 2*i+1, 2*j+1, "horizon"):
                    possible_moves.append("use-wall/" + str(2*i+1) + "/" + str(2*j+1) + "/horizon")
                if self.can_use_wall(player_num, 2*i+1, 2*j+1, "vertical"):
                    possible_moves.append("use-wall/" + str(2*i+1) + "/" + str(2*j+1) + "/vertical")
        return possible_moves

    def is_win(self, player_num):
        if player_num == BOARD_PLAYER1:
            end_line = MAX_BOARD_SIZE - 2
        else:
            end_line = 2
        for i in range(MAX_BOARD_SIZE):
            if self.board[i][end_line] == player_num:
                return True
        return False

    def print_board(self):
        for low in self.board:
            for block in low:
                if block == BOARD_AIR:
                    print("□", end='')
                elif block == BOARD_WALL:
                    print("■", end='')
                elif block == BOARD_PLAYER1:
                    print("◎", end='')
                elif block == BOARD_PLAYER2:
                    print("●", end='')
            print()

    def can_move(self, player_num, x, y, direction):
        opp_player_num = self.get_opponent_player(player_num)
        if direction == "up":
            # if not overBoard
            if y + 2 <= MAX_BOARD_SIZE:
                # if wall
                if self.board[x][y + 1] == BOARD_WALL:
                    return False
                # if not wall
                elif self.board[x][y + 1] == BOARD_AIR:
                    # if not wall and nothing
                    if self.board[x][y + 2] == BOARD_AIR:
                        return "walk"
                    # if not wall but opponent player
                    elif self.board[x][y + 2] == opp_player_num:
                        # if not over board (jump)
                        if y + 3 <= MAX_BOARD_SIZE:
                            if self.board[x][y + 3] == BOARD_AIR:
                                return "jump-forward"
                            elif self.board[x + 1][y + 2] == BOARD_AIR and self.board[x - 1][y + 2] == BOARD_AIR:
                                return "jump-both"
                            elif self.board[x + 1][y + 2] == opp_player_num:
                                return "jump-left"
                            elif self.board[x - 1][y + 2] == opp_player_num:
                                return "jump-right"
            return "none"
        elif direction == "down":
            if y - 2 >= 0:
                if self.board[x][y - 1] == BOARD_AIR:
                    if self.board[x][y - 2] == BOARD_AIR:
                        return "walk"
                    elif self.board[x][y - 2] == opp_player_num:
                        if y - 3 >= 0:
                            if self.board[x][y - 3] == BOARD_AIR:
                                return "jump-forward"
                            elif self.board[x + 1][y - 2] == BOARD_AIR and self.board[x - 1][y - 2] == BOARD_AIR:
                                return "jump-both"
                            elif self.board[x - 1][y - 2] == opp_player_num:
                                return "jump-left"
                            elif self.board[x + 1][y - 2] == opp_player_num:
                                return "jump-right"
            return "none"
        elif direction == "right":
            if x + 2 <= MAX_BOARD_SIZE:
                if self.board[x + 1][y] == BOARD_AIR:
                    if self.board[x + 2][y] == BOARD_AIR:
                        return "walk"
                    elif self.board[x + 2][y] == opp_player_num:
                        if x + 3 <= MAX_BOARD_SIZE:
                            if self.board[x + 3][y] == BOARD_AIR:
                                return "jump-forward"
                            elif self.board[x + 2][y + 1] == BOARD_AIR\
                                and self.board[x + 2][y - 1] == BOARD_AIR:
                                return "jump-both"
                            elif self.board[x + 2][y + 1] == opp_player_num:
                                return "jump-left"
                            elif self.board[x + 2][y - 1] == opp_player_num:
                                return "jump-right"
            return "none"
        elif direction == "left":
            if x - 2 >= 0:
                if self.board[x - 1][y] == BOARD_AIR:
                    if self.board[x - 2][y] == BOARD_AIR:
                        return "walk"
                    elif self.board[x - 2][y] == opp_player_num:
                        if x - 3 >= 0:
                            if self.board[x - 3][y] == BOARD_AIR:
                                return "jump-forward"
                            elif self.board[x - 2][y + 1] == BOARD_AIR and self.board[x - 2][y - 1] == BOARD_AIR:
                                return "jump-both"
                            elif self.board[x - 2][y - 1] == opp_player_num:
                                return "jump-left"
                            elif self.board[x - 2][y + 1] == opp_player_num:
                                return "jump-right"
            return "none"
        return "none"

    def can_use_wall(self, player_num, x2, y2, dir):
        if dir == "vertical":
            x1 = x2
            x3 = x2
            y1 = y2 - 1
            y3 = y2 + 1
        elif dir == "horizon":
            x1 = x2 - 1
            x3 = x2 + 1
            y1 = y2
            y3 = y2
        else:
            return False
        # if player's wall remain and valid wall
        if self.board[x1][y1] != BOARD_AIR or self.board[x2][y2] != BOARD_AIR or self.board[x3][y3] and x2 * y2 % 2 == 1\
                and self.left_wall[player_num] > 0:
            self.board[x2][y1] = BOARD_WALL
            self.board[x2][y2] = BOARD_WALL
            if self.calculate_need_turn(player_num) != -1:
                self.board[x1][y1] = BOARD_AIR
                self.board[x2][y2] = BOARD_AIR
                self.board[x3][y3] = BOARD_AIR
                return True
            else:
                self.board[x1][y1] = BOARD_AIR
                self.board[x2][y2] = BOARD_AIR
                self.board[x3][y3] = BOARD_AIR
                return False
        else:
            return False


    def move_player_pos(self, player_num, direction):
        self.board[self.player_pos[player_num][0]][self.player_pos[player_num][1]] = BOARD_AIR
        if direction == "up":
            self.player_pos[player_num][1] += 2
        elif direction == "down":
            self.player_pos[player_num][1] -= 2
        elif direction == "right":
            self.player_pos[player_num][0] += 2
        elif direction == "left":
            self.player_pos[player_num][0] -= 2
        else:
            return False
        self.board[self.player_pos[player_num][0]][self.player_pos[player_num][1]] = player_num
        return True

    def jump_player_pos(self, player_num, direction, jump_way):
        self.board[self.player_pos[player_num][0]][self.player_pos[player_num][1]] = BOARD_AIR
        if direction == "up":
            if jump_way == "jump-forward":
                self.player_pos[player_num][1] += 4
            elif jump_way == "jump-left":
                self.player_pos[player_num][0] -= 2
                self.player_pos[player_num][1] += 2
            elif jump_way == "jump-right":
                self.player_pos[player_num][0] += 2
                self.player_pos[player_num][1] += 2
            else:
                return False
        elif direction == "down":
            if jump_way == "jump-forward":
                self.player_pos[player_num][1] -= 4
            elif jump_way == "jump-left":
                self.player_pos[player_num][0] += 2
                self.player_pos[player_num][1] -= 2
            elif jump_way == "jump-right":
                self.player_pos[player_num][0] -= 2
                self.player_pos[player_num][1] -= 2
            else:
                return False
        elif direction == "right":
            if jump_way == "jump-forward":
                self.player_pos[player_num][0] += 4
            elif jump_way == "jump-left":
                self.player_pos[player_num][0] += 2
                self.player_pos[player_num][1] += 2
            elif jump_way == "jump-right":
                self.player_pos[player_num][0] += 2
                self.player_pos[player_num][1] -= 2
            else:
                return False
        elif direction == "left":
            if jump_way == "jump-forward":
                self.player_pos[player_num][0] -= 4
            elif jump_way == "jump-left":
                self.player_pos[player_num][0] -= 2
                self.player_pos[player_num][1] -= 2
            elif jump_way == "jump-right":
                self.player_pos[player_num][0] -= 2
                self.player_pos[player_num][1] += 2
            else:
                return False
        else:
            return False
        self.board[self.player_pos[player_num][0]][self.player_pos[player_num][1]] = player_num

    def calculate_need_turn(self, player_num:int):
        if player_num == 1:
            end_line = MAX_BOARD_SIZE - 2
        elif player_num == 2:
            end_line = 2
        # 2차원 보드랑 똑같은 크기
        score_board = [[-1] * (MAX_BOARD_SIZE + 1) for i in range(MAX_BOARD_SIZE + 1)]
        count = 0
        # 2차원좌표 배열
        root_stack = [[self.player_pos[player_num][0], self.player_pos[player_num][1]]]
        score_board[self.player_pos[player_num][0]][self.player_pos[player_num][1]] = 0

        def set_root(pos, x, y, count):
            if score_board[pos[0] + x][pos[1] + y] == -1:
                score_board[pos[0] + x][pos[1] + y] = count
                root_stack.append([pos[0] + x, pos[1] + y])

        while True:
            count += 1
            tmp_stack = []
            tmp_stack.extend(root_stack)
            # root_stack 의 각 좌표마다 실행
            for pos in tmp_stack:
                # 위
                can_move_up = self.can_move(player_num, pos[0], pos[1], "up")
                if can_move_up == "walk":
                    # 방문하지 않은곳이면
                    set_root(pos, 0, 2, count)
                elif can_move_up == "jump-forward":
                    set_root(pos, 0, 4, count)
                elif can_move_up == "jump-both":
                    set_root(pos, 2, 2, count)
                    set_root(pos, -2, 2, count)
                elif can_move_up == "jump-right":
                    set_root(pos, 2, 2, count)
                elif can_move_up == "jump-left":
                    set_root(pos, -2, 2, count)
                # 아래
                can_move_down = self.can_move(player_num, pos[0], pos[1], "down")
                if can_move_down == "walk":
                    set_root(pos, 0, -2, count)
                elif can_move_down == "jump-forward":
                    set_root(pos, 0, -4, count)
                elif can_move_down == "jump-both":
                    set_root(pos, 2, -2, count)
                    set_root(pos, -2, 2, count)
                elif can_move_down == "jump-right":
                    set_root(pos, -2, -2, count)
                elif can_move_down == "jump-left":
                    set_root(pos, 2, -2, count)
                # 오른쪽
                can_move_right = self.can_move(player_num, pos[0], pos[1], "right")
                if can_move_right == "walk":
                    set_root(pos, 2, 0, count)
                elif can_move_right == "jump-forward":
                    set_root(pos, 4, 0, count)
                elif can_move_right == "jump-both":
                    set_root(pos, 2, -2, count)
                    set_root(pos, 2, 2, count)
                elif can_move_right == "jump-right":
                    set_root(pos, 2, -2, count)
                elif can_move_right == "jump-left":
                    set_root(pos, 2, 2, count)
                # 왼쪽
                can_move_left = self.can_move(player_num, pos[0], pos[1], "left")
                if can_move_left == "walk":
                    set_root(pos, -2, 0, count)
                elif can_move_left == "jump-forward":
                    set_root(pos, -4, 0, count)
                elif can_move_left == "jump-both":
                    set_root(pos, -2, -2, count)
                    set_root(pos, -2, 2, count)
                elif can_move_left == "jump-right":
                    set_root(pos, -2, 2, count)
                elif can_move_left == "jump-left":
                    set_root(pos, -2, -2, count)
                root_stack.remove(pos)
            if not root_stack:
                for i in score_board:
                    for j in i:
                        print(str(j) + "\t", end='')
                    print()
                return -1
            for i in range(MAX_BOARD_SIZE):
                if score_board[i][end_line] != -1:
                    return score_board[i][end_line]

    def get_opponent_player(self, player_num):
        if player_num == BOARD_PLAYER1:
            return BOARD_PLAYER2
        elif player_num == BOARD_PLAYER2:
            return BOARD_PLAYER1
        else:
            return -1



