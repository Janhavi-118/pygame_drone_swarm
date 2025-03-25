#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import math
from door_detector import door_detector
import numpy as np
import cv2
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import MultiArrayDimension
import pygame
import time
import sys

grid = np.zeros((35,55))


WIDTH, HEIGHT = 55, 35
CELL_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (128, 128, 128)
RED = (0,255, 0)
BLUE = (0, 128, 128)


obstacles = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0),
                (16, 0), (17, 0), (18, 0), (19, 0), (20, 0), (21, 0), (22, 0), (23, 0), (24, 0), (25, 0), (26, 0), (27, 0), (28, 0), (29, 0),
                (30, 0), (31, 0), (32, 0), (33, 0), (34, 0), (35, 0), (36, 0), (37, 0), (38, 0), (39, 0), (40, 0), (41, 0), (42, 0), (43, 0), (44, 0), (45, 0),
                (46, 0), (47, 0), (48, 0), (49, 0), (50, 0), (51, 0), (52, 0), (53, 0), (54, 0), 
                (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15),
                (0, 16), (0, 17), (0, 18), (0, 19), (0, 20), (0, 21), (0, 22), (0, 23), (0, 24), (0, 25), (0, 26), (0, 27), (0, 28), (0, 29),
                (54, 0), (54, 1), (54, 2), (54, 3), (54, 4), (54, 5), (54, 6), (54, 7), (54, 8), (54, 9), (54, 10), (54, 11), (54, 12), (54, 13), (54, 14), (54, 15),
                (54, 16), (54, 17), (54, 18), (54, 19), (54, 20), (54, 21), (54, 22), (54, 23), (54, 24), (54, 25), (54, 26), (54, 27), (54, 28), (54, 29),
                (0, 25), (1, 25), (2, 25), (3, 25), (4, 25), (5, 25), (6, 25), (7, 25), (8, 25), (9, 25), (10, 25), (11, 25), (12, 25), (13, 25), 
                (14, 25), (15, 25), (16, 25), (17, 25), (18, 25), (19, 25), (20, 25), (21, 25), (22, 25), (23, 25), (24, 25),
                (30, 25), (31, 25), (32, 25), (33, 25), (34, 25), (35, 25), (36, 25), (37, 25), (38, 25), (39, 25), (40, 25), (41, 25), (42, 25), (43, 25), 
                (44, 25), (45, 25), (46, 25), (47, 25), (48, 25), (49, 25), (50, 25), (51, 25), (52, 25), (53, 25), (54, 25),
                
                (2,22),(2,22),(3,23),(4,24),(17,23),(18,23),(10,24),
                (7,14),(7,13),(19,16),(20,15),(11,16),
                (5,5),(19,5),(11,16),
                (52,22),(52,22),(51,23),(50,24),(37,23),(36,23),(44,24),
                (47,14),(47,13),(35,16),(34,15),(43,16),
                (49,5),(47,6),(35,5),
                (0, 0), (1, 0), (2, 0),(3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0),
                (16, 0), (17, 0), (18, 0), (19, 0), (20, 0), (21, 0), (22, 0), (23, 0), (24, 0), (25, 0), (26, 0), (27, 0), (28, 0), (25, 0),
                (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15),
                (0, 16), (0, 17), (0, 18), (0, 19), (0, 20), (0, 21), (0, 22), (0, 23), (0, 24), (0, 25), (0, 26), (0, 27), (0, 28), (0, 29),
                (0, 25), (1, 25), (2, 25), (3, 25), (4, 25), (5, 25), (6, 25), (7, 25), (8, 25), (9, 25), (10, 25), (11, 25), (12, 25), (13, 25), 
                (14, 25), (15, 25), (16, 25), (17, 25), (18, 25), (19, 25), (20, 25), (21, 25), (22, 25), (23, 25), (24, 25),
                (1,1),(1,2),(1,3),(1,4), (2,1),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(3,4),(4, 1), (4, 2), (4, 3),(4, 4), (5, 1), (5, 2), (5, 3), (5, 4), (6, 1), (6, 2), (6, 3), 
                (6, 4), (7, 1), (7, 2), (7, 3), (7, 4), (8, 1), (8, 2), (8, 3),(8, 4), (9, 1), (9, 2), (9, 3), (9, 4), (10, 1), (10, 2), (10, 3), 
                (10, 4), (11, 1), (11, 2), (11, 3), (11, 4), (12, 1), (12, 2), (12, 3), (12, 4), (13, 1), (13, 2), (13, 3), (13, 4), (14, 1), (14, 2),
                (14, 3), (14, 4), (15, 1), (15, 2), (15, 3), (15, 4), (16, 1), (16, 2), (16, 3), (16, 4), (17, 1), (17, 2), (17, 3), (17, 4),
                (18, 1), (18, 2), (18, 3), (18, 4), (19, 1), (19, 2), (19, 3), (19, 4), (20, 1), (20, 2), (20, 3), (20, 4), (21, 1), (21, 2), 
                (21, 3), (21, 4),
                (33,1),(33,2),(33,3),(33,4), (34,1),(34,2),(34,3),(34,4),(35,1),(35,2),(35,3),(35,4),(36, 1), (36, 2), (36, 3),(36, 4), (37, 1), (37, 2), (37, 3), (37, 4), (38, 1), (38, 2), (38, 3), 
                (38, 4), (39, 1), (39, 2), (39, 3), (39, 4), (40, 1), (40, 2), (40, 3),(40, 4), (41, 1), (41, 2), (41, 3), (41, 4), (42, 1), (42, 2), (42, 3), 
                (42, 4), (43, 1), (43, 2), (43, 3), (43, 4), (44, 1), (44, 2), (44, 3), (44, 4), (45, 1), (45, 2), (45, 3), (45, 4), (46, 1), (46, 2),
                (46, 3), (46, 4), (47, 1), (47, 2), (47, 3), (47, 4), (48, 1), (48, 2), (48, 3), (48, 4), (49, 1), (49, 2), (49, 3), (49, 4),
                (50, 1), (50, 2), (50, 3), (50, 4), (51, 1), (51, 2), (51, 3), (51, 4), (52, 1), (52, 2), (52, 3), (52, 4), (53, 1), (53, 2), 
                (53, 3), (53, 4),
                (1,9),(1,10),(1,11),(1,12),(2,9),(2,10),(2,11),(2,12),(3,9),(3,10),(3,11),(3,12), (4, 9), (4, 10), (4, 11), 
                (4, 12),(5, 9), (5, 10), (5, 11), (5, 12), (6, 9), (6, 10),(6, 11), (6, 12), (7, 9), (7, 10), (7, 11), (7, 12), (8, 9), 
                (8, 10),(8, 11), (8, 12), (9, 9), (9, 10), (9, 11), (9, 12), (10, 9), (10, 10), (10, 11), (10, 12), (11, 9), (11, 10), (11, 11),
                (11, 12), (12, 9), (12, 10), (12, 11), (12, 12), (13, 9), (13, 10), (13, 11), (13, 12), (14, 9), (14, 10), (14, 11), 
                (14, 12), (15, 9), (15, 10), (15, 11), (15, 12), (16, 9), (16, 10), (16, 11), (16, 12), (17, 9), (17, 10), (17, 11), 
                (17, 12), (18, 9), (18, 10), (18, 11), (18, 12), (19, 9), (19, 10), (19, 11), (19, 12), (20, 9), (20, 10), (20, 11),
                (20, 12), (21, 9), (21, 10), (21, 11), (21, 12),
                (33,9),(33,10),(33,11),(33,12),(34,9),(34,10),(34,11),(34,12),(35,9),(35,10),(35,11),(35,12), (36, 9), (36, 10), (36, 11), 
                (36, 12),(37, 9), (37, 10), (37, 11), (37, 12), (38, 9), (38, 10),(38, 11), (38, 12), (39, 9), (39, 10), (39, 11), (39, 12), (40, 9), 
                (40, 10),(40, 11), (40, 12), (41, 9), (41, 10), (41, 11), (41, 12), (42, 9), (42, 10), (42, 11), (42, 12), (43, 9), (43, 10), (43, 11),
                (43, 12), (44, 9), (44, 10), (44, 11), (44, 12), (45, 9), (45, 10), (45, 11), (45, 12), (46, 9), (46, 10), (46, 11), 
                (46, 12), (47, 9), (47, 10), (47, 11), (47, 12), (48, 9), (48, 10), (48, 11), (48, 12), (49, 9), (49, 10), (49, 11), 
                (49, 12), (50, 9), (50, 10), (50, 11), (50, 12), (51, 9), (51, 10), (51, 11), (51, 12), (52, 9), (52, 10), (52, 11),
                (52, 12), (53, 9), (53, 10), (53, 11), (53, 12),
                (1,17),(1,18),(1,19),(1,20),(2,17),(2,18),(2,19),(2,20),(3,17),(3,18),(3,19),(3,20),
                (4, 17), (4, 18), (4, 19), (4, 20), (5, 17), (5, 18), (5, 19), (5, 20),
                (6, 17), (6, 18), (6, 19), (6, 20), (7, 17), (7, 18), (7, 19), (7, 20), (8, 17), (8, 18), (8, 19), (8, 20), (9, 17),
                (9, 18), (9, 19), (9, 20), (10, 17), (10, 18), (10, 19), (10, 20), (11, 17), (11, 18), (11, 19), (11, 20), (12, 17), 
                (12, 18), (12, 19), (12, 20), (13, 17), (13, 18), (13, 19), (13, 20), (14, 17), (14, 18), (14, 19), (14, 20), (15, 17),
                (15, 18), (15, 19), (15, 20), (16, 17), (16, 18), (16, 19), (16, 20), (17, 17), (17, 18), (17, 19), (17, 20), 
                (18, 17), (18, 18), (18, 19), (18, 20), (19, 17), (19, 18), (19, 19), (19, 20), (20, 17), (20, 18), (20, 19), 
                (20, 20), (21, 17), (21, 18), (21, 19), (21, 20),
                (33,17),(33,18),(33,19),(33,20),(34,17),(34,18),(34,19),(34,20),(35,17),(35,18),(35,19),(35,20),
                (36, 17), (36, 18), (36, 19), (36, 20), (37, 17), (37, 18), (37, 19), (37, 20),
                (38, 17), (38, 18), (38, 19), (38, 20), (39, 17), (39, 18), (39, 19), (39, 20), (40, 17), (40, 18), (40, 19), (40, 20), (41, 17),
                (41, 18), (41, 19), (41, 20), (42, 17), (42, 18), (42, 19), (42, 20), (43, 17), (43, 18), (43, 19), (43, 20), (44, 17), 
                (44, 18), (44, 19), (44, 20), (45, 17), (45, 18), (45, 19), (45, 20), (46, 17), (46, 18), (46, 19), (46, 20), (47, 17),
                (47, 18), (47, 19), (47, 20), (48, 17), (48, 18), (48, 19), (48, 20), (49, 17), (49, 18), (49, 19), (49, 20), 
                (50, 17), (50, 18), (50, 19), (50, 20), (51, 17), (51, 18), (51, 19), (51, 20), (52, 17), (52, 18), (52, 19), 
                (52, 20), (53, 17), (53, 18), (53, 19), (53, 20),
                (1,21),(1,22),(1,23),(1,24), (2,21),(2,22),(2,23),(2,24),(3,21),(3,22),(3,23),(3,24),(4, 21), (4, 22), (4, 23),(4, 24), (5, 21), (5, 22), (5, 23), (5, 24), (6, 21), (6, 22), (6, 23), 
                (6, 24), (7, 21), (7, 22), (7, 23), (7, 24), (8, 21), (8, 22), (8, 23),(8, 24), (9, 21), (9, 22), (9, 23), (9, 24), (10, 21), (10, 22), (10, 23), 
                (10, 24), (11, 21), (11, 22), (11, 23), (11, 24), (12, 21), (12, 22), (12, 23), (12, 24), (13, 21), (13, 22), (13, 23), (13, 24), (14, 21), (14, 22),
                (14, 23), (14, 24), (15, 21), (15, 22), (15, 23), (15, 24), (16, 21), (16, 22), (16, 23), (16, 24), (17, 21), (17, 22), (17, 23), (17, 24),
                (18, 21), (18, 22), (18, 23), (18, 24), (19, 21), (19, 22), (19, 23), (19, 24), (20, 21), (20, 22), (20, 23), (20, 24), (21, 21), (21, 22), 
                (21, 23), (21, 24),
                (33, 21),(33, 22),(33, 23),(33, 24),(34, 21),(34, 22),(34, 23),(34, 24),(35, 21),(35, 22),(35, 23),(35, 24),(36, 21), (36, 22), (36, 23),(36, 24), (37, 21), (37, 22), (37, 23), (37, 24), (38, 21), (38, 22), (38, 23), 
                (38, 24),(39, 21),(39, 22),(39, 23),(39, 24), (40, 21), (40, 22), (40, 23),(40, 24), (41, 21), (41, 22), (41, 23), (41, 24), (42, 21), (42, 22), (42, 23), 
                (42, 24),(43, 21),(43, 22),(43, 23),(43, 24), (44, 21), (44, 22), (44, 23), (44, 24), (45, 21), (45, 22), (45, 23), (45, 24), (46, 21), (46, 22),
                (46, 23),(46, 24),(47, 21),(47, 22), (47, 23), (47, 24), (48, 21), (48, 22), (48, 23), (48, 24), (49, 21), (49, 22), (49, 23), (49, 24),
                (50, 21),(50, 22),(50, 23),(50, 24), (51, 21), (51, 22), (51, 23), (51, 24), (52, 21), (52, 22), (52, 23), (52, 24), (53, 21), (53, 22), 
                (53, 23),(53, 24)]
    

for i in range(55):
    for j in range(35):
        if (i,j) in obstacles:
            grid[j][i] = 1
        else:
            grid[j][i] = 2
print("ive made the grid for obstacles")
    
class Swarm(Node):
    def __init__(self, init_pos, screen):
        super().__init__('swarm_node')  # Initialize ROS2 Node
        self.init_pos = init_pos
        self.vel_x = 0
        self.vel_y = 0
        self.current_pose_x = self.init_pos[0]
        self.current_pose_y = self.init_pos[1]
        self.drone_count = 5
        self.drone_list = ["left", "right", "master", "front", "back"]
        self.curr_drone_list = ["left", "right", "master", "front", "back"]
        self.Path_Data = []
        self.detatch_data = [0, 0, 0, 0, 0]
        self.screen = screen
        self.motion_pub = self.create_publisher(Int32MultiArray, 'Motion_Data', 1)
        self.det_pub_l = self.create_publisher(Int32MultiArray, 'Left_Detatch_Data', 10)
        self.det_pub_r = self.create_publisher(Int32MultiArray, 'Right_Detatch_Data', 10)
        self.det_pub_f = self.create_publisher(Int32MultiArray, 'Front_Detatch_Data', 10)
        self.det_pub_b = self.create_publisher(Int32MultiArray, 'Back_Detatch_Data', 10)
        self.Motion_Data = Int32MultiArray()
        self.Motion_Data.data = self.Path_Data
        self.Detatch_Poses = Int32MultiArray()
        self.Detatch_Poses.layout.dim.append(MultiArrayDimension())
        self.Detatch_Poses.layout.dim[0].label = 'point_x'
        self.Detatch_Poses.layout.dim[0].size = 5
        self.Detatch_Poses.layout.dim[0].stride = 5
        self.Detatch_Poses.data = self.detatch_data
        self.timer = self.create_timer(1.0, self.navigate)

    def detatch(self,drone_name):
        self.curr_drone_list.remove(drone_name)
        self.drone_count-=2
        self.Detatch_Poses.data = self.detatch_data
        if drone_name == "left":
            i=0
            while i < 3:
                print("publishing: ",self.detatch_data, " for left")
                self.det_pub_l.publish(self.Detatch_Poses)
                i+=1
        elif drone_name == "right":
            i=0
            while i < 3:
                print("publishing: ",self.detatch_data, " for right")
                self.det_pub_r.publish(self.Detatch_Poses)
                i+=1
        elif drone_name == "front":
            i=0
            while i < 3:
                print("publishing: ",self.detatch_data, " for front")
                self.det_pub_f.publish(self.Detatch_Poses)
                i+=1
        elif drone_name == "back":
            i=0
            while i < 3:
                print("publishing: ",self.detatch_data, " for back")
                self.det_pub_b.publish(self.Detatch_Poses)
                i+=1
        return


    def navigate(self):
        d = door_detector("Master")
        self.current_pose_x = self.init_pos[0]
        self.current_pose_y = self.init_pos[1]
        door_detected = 0
        self.motion_pub.publish(self.Motion_Data)

        while self.drone_count != 1:    
            self.vel_y = 1    
            while door_detected == 0 and self.current_pose_x >0 and self.current_pose_y > 0:
                cam_scan = d.get_cam_scan(grid,self.current_pose_x,self.current_pose_y)
                new_pose_x = self.current_pose_x - self.vel_x
                new_pose_y = self.current_pose_y - self.vel_y
                print(self.current_pose_x,self.current_pose_y)
                print(self.drone_count)
                source_col = 0
                for i in cam_scan:
                    if 20 in i:
                        source_col= list(i).index(20)
                print(cam_scan)        
                pat = d.detect_pattern(cam_scan,[self.current_pose_x,self.current_pose_y])
                print(pat)
                pygame.draw.rect(self.screen, RED, (new_pose_x * CELL_SIZE, new_pose_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)) 
                if self.drone_count == 5:
                    for i, j in [(-1,0),(0, -1), (1, 0), (0, 1)]:  # Coordinates for 4 surrounding robots
                        pygame.draw.rect(self.screen, RED, ((self.current_pose_x + i) * CELL_SIZE, (self.current_pose_y + j) * CELL_SIZE, CELL_SIZE, CELL_SIZE)) 
                        pygame.display.flip()
                if self.drone_count == 4:
                    for i, j in [(0, -1), (1, 0), (0, 1)]:  # Coordinates for 4 surrounding robots
                        pygame.draw.rect(self.screen, RED, (new_pose_x * CELL_SIZE, new_pose_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Single cell robot
                        pygame.draw.rect(self.screen, BLUE, ((self.current_pose_x + i) * CELL_SIZE, (self.current_pose_y + j) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        pygame.display.flip()
                        time.sleep(0.5)
                elif self.drone_count == 3:
                    for i, j in [(1, 0), (0, 1)]:  # Coordinates for 4 surrounding robots
                        pygame.draw.rect(self.screen, RED, (new_pose_x * CELL_SIZE, new_pose_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Single cell robot
                        pygame.draw.rect(self.screen, BLUE, ((self.current_pose_x + i) * CELL_SIZE, (self.current_pose_y + j) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        # pygame.draw.rect(screen, WHITE, ((new_pose_x+ i) * CELL_SIZE, (new_pose_y + j) * CELL_SIZE, CELL_SIZE, CELL_SIZE),1)
                        pygame.display.flip()
                        time.sleep(0.5)
                elif self.drone_count == 2:
                    pygame.draw.rect(self.screen, RED, (new_pose_x * CELL_SIZE, new_pose_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Single cell robot
                    for i, j in [(0, 1)]:  # Coordinates for 4 surrounding robots
                        pygame.draw.rect(self.screen, BLUE, ((self.current_pose_x + i) * CELL_SIZE, (self.current_pose_y + j) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        # pygame.draw.rect(screen, WHITE, ((new_pose_x+ i) * CELL_SIZE, (new_pose_y + j) * CELL_SIZE, CELL_SIZE, CELL_SIZE),1)
                        pygame.display.flip()
                        time.sleep(0.5)
                elif self.drone_count == 1:
                    if (new_pose_x, new_pose_y) not in obstacles:
                        pygame.draw.rect(self.screen, RED, (new_pose_x * CELL_SIZE, new_pose_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        pygame.display.flip()
                        time.sleep(0.5)

                

                self.Path_Data.append(self.current_pose_x)
                self.Path_Data.append(self.current_pose_y)
                
                self.current_pose_x = new_pose_x
                self.current_pose_y = new_pose_y
                if pat[0] == True and pat[1] == True:
                    print(self.current_pose_x,self.current_pose_y)
                    print("door_detected")
                    door_detected = 1
                    if self.drone_count == 5:
                        self.vel_y = 0
                        self.detatch_data[0] = self.current_pose_x
                        self.detatch_data[1] = self.current_pose_y
                        self.detatch_data[-1] = d.door_dist
                        self.detatch("left")
                        self.vel_y = 1
                        self.vel_y = 1
                    elif self.drone_count == 4:
                        self.vel_y = 0
                        self.detatch_data[0] = self.current_pose_x
                        self.detatch_data[1] = self.current_pose_y
                        self.detatch_data[-1] = d.door_dist
                        self.detatch("back")
                        self.vel_y = 1
                        self.vel_y = 1
                    elif self.drone_count == 3:
                        self.vel_y = 0
                        self.detatch_data[0] = self.current_pose_x
                        self.detatch_data[1] = self.current_pose_y
                        self.detatch_data[-1] = d.door_dist
                        self.detatch("front")
                        self.vel_y = 1
                        self.vel_y = 1
                    elif self.drone_count == 2:
                        self.vel_y = 0
                        self.detatch_data[0] = self.current_pose_x
                        self.detatch_data[1] = self.current_pose_y
                        self.detatch_data[-1] = d.door_dist
                        self.detatch("right")
                        self.vel_y = 1
                        self.vel_y = 1
                        # self.Motion_Data["Moving"] = 1
                    print("Detatched",self.drone_count)
                    door_detected = 0

        if self.drone_count == 1:
            self.detatch_data[2] = self.current_pose_x
            self.detatch_data[3] = self.current_pose_y 

            i=0
            self.Detatch_Poses.data = self.detatch_data
            while i < 100:
                self.det_pub_f.publish(self.Detatch_Poses)
                self.det_pub_b.publish(self.Detatch_Poses)
                self.det_pub_r.publish(self.Detatch_Poses)
                self.det_pub_l.publish(self.Detatch_Poses)
                i+=1
                time.sleep(0.25)

        # self.Motion_Data["Moving"] = 0

def main(args=None):
    rclpy.init(args=args)
    pygame.init()

    # Init_pos = [27,27]
    # vel_x = 1
    # vel_y = 1
    
    screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
    pygame.display.set_caption("Grid with Obstacles and Robots")
    print("ive built the screen")
    
    swarm_node = Swarm(init_pos=[27, 27], screen=screen)
    print("ive made the swarm node")
    running = True
    while running:
        print("i am in running and navigating")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        print("now im making screen")
        # Clear the screen
        screen.fill(WHITE)
        for x in range(0, WIDTH * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT * CELL_SIZE))
        for y in range(0, HEIGHT * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(screen, BLACK, (0, y), (WIDTH * CELL_SIZE, y))
        for obstacle in obstacles:
            pygame.draw.rect(screen, BLACK, (obstacle[0] * CELL_SIZE, obstacle[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        pygame.display.update()
        print("ive updated screen")
        cv2.imshow("grid",grid)
        print("ive put cv2 imshow")
        # swarm_node.navigate()
        rclpy.spin(swarm_node)
    
    cv2.waitKey(0)
    
    # Cleanup
    swarm_node.destroy_node()
    rclpy.shutdown()
    pygame.quit()
    

if __name__ == '__main__':
    main()