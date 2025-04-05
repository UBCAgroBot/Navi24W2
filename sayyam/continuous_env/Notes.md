# Reward Function

Getting only the reward returned by `RobotObstacles.step` is bad because it only returns the reward for the terminal states. But for training we want to take into account the internal reward of the robot. This will probably involve making some function to export it.