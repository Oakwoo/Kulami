import pygame
import random
def find_root(belong, block):
    while(belong[block] != block):
        block = belong[block]
    return block
class Board():
    def __init__(self, screen, width, height, boardcolor, hole_size, tile_edge_color):
        self.screen = screen
        self.width = width
        self.height = height
        self.image = pygame.image.load('image/hole.png')
        self.image = pygame.transform.scale(self.image, (hole_size, hole_size))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.boardcolor = boardcolor
        self.tile_edge_color = tile_edge_color
        self.board_feature = [[0 for t in range(self.height * 2)] for i in range(self.width * 2)]
        self.tiles = []

    def init_board_feature(self):
        for tile in self.tiles:
            for i in range(tile[0] * 2, (tile[0] + tile[2]) * 2):
                self.board_feature[i][2 * (tile[1] + tile[3]) - 1] = -10
            for i in range(tile[1] * 2, (tile[1] + tile[3]) * 2):
                self.board_feature[2 * (tile[0] + tile[2]) - 1][i] = -10

    def blitme(self):
        self.screen.fill(self.boardcolor)
        pygame.draw.rect(self.screen, self.tile_edge_color, (0, 0, self.screen.get_width(), self.screen.get_height()), 6)
        for i in range(self.height):
            self.rect.top = i*self.image.get_height()
            for t in range(self.width):
                self.rect.left = t*self.image.get_width()
                self.screen.blit(self.image, self.rect)
        # cut into tile
        #tiles = [(0,0,5,2),(0,2,2,4),(2,2,3,4),(5,0,1,4),(5,4,1,2)]
        vertical_cut = int(self.width/2)
        horizontal_cut = int(self.height/2)
        # book which edge has been delete
        del_column = [[0 for i in range(horizontal_cut+1)] for t in range(vertical_cut)]
        del_raw = [[0 for i in range(vertical_cut+1)] for t in range(horizontal_cut)]
        # book merge situation
        belong = {}
        for i in range((vertical_cut+1)*(horizontal_cut+1)):
            belong[i] = i
        # random generate location for edges
        candidate_postion_column = [i for i in range(1, self.width)]
        candidate_postion_row = [i for i in range(1, self.height)]
        position_column = [0]+sorted(random.sample(candidate_postion_column, vertical_cut))+[self.width]
        position_row = [0]+sorted(random.sample(candidate_postion_row, horizontal_cut))+[self.height]
        #print(position_column)
        #print(position_row)
        info = {}
        for i in range(horizontal_cut+1):
            for t in range(vertical_cut+1):
                info[i*(vertical_cut+1)+t] = (position_column[t], position_row[i],position_column[t+1]-position_column[t],position_row[i+1]-position_row[i])
        # random delete some edges
        for i in range(int(0.2*(2 * vertical_cut * vertical_cut))):
            while(True):
                is_column = random.choice((True,False))
                if is_column:
                    first_index = random.randint(0, vertical_cut-1)
                    second_index = random.randint(0, horizontal_cut)
                    # check it can be delete or not
                    if del_column[first_index][second_index] == 1:
                        continue
                    if second_index-1 >=0 and (del_raw[second_index-1][first_index] == 1 or del_raw[second_index-1][first_index+1] == 1):
                        continue
                    if second_index < horizontal_cut and (del_raw[second_index][first_index] == 1 or del_raw[second_index][first_index+1] == 1):
                        continue
                    # delete the edge
                    del_column[first_index][second_index] = 1
                    #print("column ",(first_index,second_index))
                    left_block = second_index*(vertical_cut+1)+first_index
                    right_block = second_index*(vertical_cut+1)+first_index+1
                    left_root = find_root(belong, left_block)
                    right_root = find_root(belong, right_block)
                    belong[right_root] =  belong[left_root]
                    info[left_root] = (info[left_root][0], info[left_root][1], info[left_root][2]+info[right_root][2], info[left_root][3])
                    break
                else:
                    first_index = random.randint(0,horizontal_cut-1)
                    second_index = random.randint(0,vertical_cut)
                    # check it can be delete or not
                    if del_raw[first_index][second_index] == 1:
                        continue
                    if second_index-1 >=0 and (del_column[second_index-1][first_index] == 1 or del_column[second_index-1][first_index+1] == 1 ):
                        continue
                    if second_index < vertical_cut and (del_column[second_index][first_index] == 1 or del_column[second_index][first_index+1] == 1 ):
                        continue
                    # delete the edge
                    del_raw[first_index][second_index] = 1
                    #print("raw ",(first_index,second_index))
                    up_block = first_index*(vertical_cut+1)+second_index
                    down_block = (first_index+1)*(vertical_cut+1)+second_index
                    up_root = find_root(belong, up_block)
                    down_root = find_root(belong, down_block)
                    belong[down_root] = belong[up_root]
                    info[up_root] = (info[up_root][0], info[up_root][1], info[up_root][2], info[up_root][3]+info[down_root][3])
                    break

        tiles = []
        for k,v in belong.items():
            if k == v:
                tiles.append(info[k])
        print(tiles)
        self.tiles = tiles
        # draw the tile
        for t in tiles:
            pygame.draw.rect(self.screen, (150, 127, 103), (t[0]*self.image.get_width(), t[1]*self.image.get_height(), t[2]*self.image.get_width(), t[3]*self.image.get_height()), 6)
