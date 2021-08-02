
import unittest
import csv
import pandas as pd
import re
from graspit_commander.graspit_commander import GraspitCommander
from ast import literal_eval

###################setRobotPose#######################
class Pos:
    def __init__(self, plist):
        self.x = plist[0]
        self.y = plist[1]
        self.z = plist[2]

class Ori:
    def __init__(self, olist):
        self.x = olist[0]
        self.y = olist[1]
        self.z = olist[2]
        self.w = olist[3]

class PoseCo:
    def __init__(self, plist, olist):
        pp = Pos(plist)
        rr = Ori(olist)
        self.position = pp
        self.orientation = rr

###################setBodyPose#######################
class Posb:
    def __init__(self, plist_b):
        self.x = plist_b[0]
        self.y = plist_b[1]
        self.z = plist_b[2]

class Orib:
    def __init__(self, olist_b):
        self.x = olist_b[0]
        self.y = olist_b[1]
        self.z = olist_b[2]
        self.w = olist_b[3]

class BodyCo:
    def __init__(self, plist_b, olist_b):
        pp_b = Posb(plist_b)
        rr_b = Orib(olist_b)
        self.position = pp_b
        self.orientation = rr_b

class GraspingTest(unittest.TestCase):

    def testStaticGraspExecution(self):

        grasps = pd.read_csv('gdataset.csv')
        o_name = grasps['3d_model_name']
        h_position = grasps['hand_position']
        h_orientation = grasps['hand_orientation']
        dofs = grasps["finger_dofs"]
        max_ball_radius = grasps['max_ball_radius']

        obj_index = 19 # index of a specific object stored in o_name

        # Each object may contain several grasps positions and orientations stored as list items
        # grasps_num = 0 indicates the position and orientation of the first grasp for the object
        grasp_num = 0

        obj_name = re.search("^[^_]*", o_name[obj_index]).group(0)

        ## setBodyPose
        GraspitCommander.clearWorld()
        GraspitCommander.importGraspableBody(obj_name, pose=None)

        sbp = BodyCo(plist_b=[0, 0, max_ball_radius[obj_index]/1000 + 0.1], olist_b=[0, 0, 0, 1])
        GraspitCommander.setBodyPose(0,sbp)

        ## load Barrett hand
        GraspitCommander.importRobot("Barrett", pose=None)

        ##  set hand position
        srp = PoseCo(plist=literal_eval(h_position[obj_index])[grasp_num], olist=literal_eval(h_orientation[obj_index])[grasp_num])
        GraspitCommander.setRobotPose(srp)

        GraspitCommander.moveDOFToContacts(literal_eval(dofs[obj_index])[grasp_num], [], 1)
        GraspitCommander.toggleAllCollisions(1)


if __name__ == "__main__":

    GT = unittest.main()
