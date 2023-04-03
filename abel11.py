{
    "all_wheels_on_track": Boolean,        # flag to indicate if the agent is on the track
    "x": float,                            # agent's x-coordinate in meters
    "y": float,                            # agent's y-coordinate in meters
    "closest_objects": [int, int],         # zero-based indices of the two closest objects to the agent's current position of (x, y).
    "closest_waypoints": [int, int],       # indices of the two nearest waypoints.
    "distance_from_center": float,         # distance in meters from the track center 
    "is_crashed": Boolean,                 # Boolean flag to indicate whether the agent has crashed.
    "is_left_of_center": Boolean,          # Flag to indicate if the agent is on the left side to the track center or not. 
    "is_offtrack": Boolean,                # Boolean flag to indicate whether the agent has gone off track.
    "is_reversed": Boolean,                # flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
    "heading": float,                      # agent's yaw in degrees
    "objects_distance": [float, ],         # list of the objects' distances in meters between 0 and track_length in relation to the starting line.
    "objects_heading": [float, ],          # list of the objects' headings in degrees between -180 and 180.
    "objects_left_of_center": [Boolean, ], # list of Boolean flags indicating whether elements' objects are left of the center (True) or not (False).
    "objects_location": [(float, float),], # list of object locations [(x,y), ...].
    "objects_speed": [float, ],            # list of the objects' speeds in meters per second.
    "progress": float,                     # percentage of track completed
    "speed": float,                        # agent's speed in meters per second (m/s)
    "steering_angle": float,               # agent's steering angle in degrees
    "steps": int,                          # number steps completed
    "track_length": float,                 # track length in meters.
    "track_width": float,                  # width of the track
    "waypoints": [(float, float), ]        # list of (x,y) as milestones along the track center

}

import math

def indexer(max, i):
    if i>max:
        return i-max
    if i<0:
        return max+i
    else:
        return i
def  dotprod(u,v):
    return u[0]*v[0]+u[1]*v[1]
def lenfromlinecalc(u,v):
    n=[0,0]
    a=dotprod(u,v)/dotprod(u,u)
    x=u[0]*a
    y=u[1]*a
    n[0]=v[0]-x
    n[1]=v[1]-y
    return math.hypot(n[0],n[1])

def reward_function(params):
    trackwidth=params['track_width']
    waypoints=params['waypoints']
    closest_waypoints=params['closest_waypoints']
    heading=params['heading']
    x=params['x']
    y=params['y']
    progress=params['progress']
    # speed=params['speed']
    reward = 1e-3
    max=len(waypoints)
    frontwaypoint=waypoints[indexer(max, closest_waypoints[1]+4)]
    rearwaypoint=waypoints[indexer(max, closest_waypoints[0]-4)]
    if progress ==  100:
        reward+=100
    # reward-=(1.2-speed)
    u=[(frontwaypoint[0]-rearwaypoint[0]),(frontwaypoint[1]-rearwaypoint[1])]
    agent=[(frontwaypoint[0]-x), (frontwaypoint[1]-y)]
    angle=math.atan2(u[1],u[0])
    anglediff=abs(heading-angle)
    # if anglediff>45:
    penalty=anglediff/70
    if penalty>1:
        penalty=1
    reward+=(1-penalty)
    # return reward
    # else:
    norm=lenfromlinecalc(u,agent)
    bonus=((trackwidth/2)-norm)
    if norm>(trackwidth/2):
        bonus=0
    reward+=bonus
    return reward
