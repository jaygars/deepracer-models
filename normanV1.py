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
    bounds=params['track_width']/2
    waypoints=params['waypoints']
    closest_waypoints=params['closest_waypoints']
    heading=params['heading']
    x=params['x']
    y=params['y']
    progress=params['progress']
    reward = 1e-3
    max=len(waypoints)-1
    frontwaypoint=waypoints[indexer(max, closest_waypoints[1]+3)]
    rearwaypoint=waypoints[indexer(max, closest_waypoints[0]-3)]
    if progress ==  100:
        reward+=100
    u=[(frontwaypoint[0]-rearwaypoint[0]),(frontwaypoint[1]-rearwaypoint[1])]
    agent=[(frontwaypoint[0]-x), (frontwaypoint[1]-y)]
    angle=math.atan2(u[1],u[0])
    anglediff=abs(heading-angle)
    if anglediff>60:
        penalty=anglediff/60
        reward+=(2-penalty)
        return reward
    else:
        norm=lenfromlinecalc(u,agent)
        bonus=((bounds-norm)/bounds)
        if norm>bounds:
            bonus=0
        reward+=(1*bonus)
        return reward
