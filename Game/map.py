import pygame

from box import Box

class Map:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        BROWN = (102, 51, 0)

        wall_width = 30
        wall_height = 30

        obstacle_1_x = 293
        obstacle_1_y = 0
        obstacle_1_w = int(wall_width)
        obstacle_1_h = int(screen_height*3/4)

        obstacle_2_x = 555
        obstacle_2_y = int(screen_height/4)
        obstacle_2_w = int(wall_width)
        obstacle_2_h = int(screen_height*3/4)

        obstacle_3_x = 817
        obstacle_3_y = 0
        obstacle_3_w = int(wall_width)
        obstacle_3_h = int(screen_height*3/4)

        obstacle_4_x = 934
        obstacle_4_y = int(screen_height/2)
        obstacle_4_w = 10
        obstacle_4_h = 10

        self.left_wall = Box(0, 0, wall_width, screen_height, BROWN)
        self.right_wall = Box(screen_width-wall_width, 0, wall_width, screen_height, BROWN)
        self.top_wall = Box(0, 0, screen_width, wall_height, BROWN)
        self.bottom_wall = Box(0, screen_height-wall_height, screen_width, wall_height, BROWN)

        self.obstacle_1 = Box(obstacle_1_x - int(obstacle_1_w/2),
                              obstacle_1_y,
                              obstacle_1_w,
                              obstacle_1_h,
                              BROWN)
        
        self.obstacle_2 = Box(obstacle_2_x - int(obstacle_2_w/2),
                              obstacle_2_y,
                              obstacle_2_w,
                              obstacle_2_h,
                              BROWN)
        
        self.obstacle_3 = Box(obstacle_3_x - int(obstacle_3_w/2),
                              obstacle_3_y,
                              obstacle_3_w,
                              obstacle_3_h,
                              BROWN)
        
        self.obstacle_4 = Box(obstacle_4_x - int(obstacle_4_w/2),
                              obstacle_4_y - int(obstacle_4_h/2),
                              obstacle_4_w,
                              obstacle_4_h,
                              BROWN)


    def box_list(self):
        return [self.left_wall, 
                self.right_wall,
                self.top_wall,
                self.bottom_wall,
                self.obstacle_1,
                self.obstacle_2,
                self.obstacle_3,
                self.obstacle_4]