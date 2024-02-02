# Queue optimizer

This script implements an algorithm to balance the two queues of the chairlift for skiers.

The chairlift has two stops where skiers can board: a bottom station and and intermediate station.

If all the chairs are used by skiers boarding at the bottom station, there is no space for skiers who want to board at the intermediate station. So it is necessary to leave some chairs empty to allow skiers at the intermediate station to board.

The user provides the current queues, the queue rates (skiers per minute) and how many chairs should be left empty at the bottom stop (for example, one empty chair for every three chairs); the goal is to  balance the queues at the two stations.

![Queue optimizer](/doc/sample.png)
