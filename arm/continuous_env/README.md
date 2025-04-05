# Simulation build for RL made by OpenAI and adapted by Neil Lin

# Quickstart:

Install poetry: [https://python-poetry.org/docs/](https://python-poetry.org/docs/)

Activate the environment in this directory.

Run the simulation with:

```sh
poetry run python -m continuous_env.robot_obstacles 
```

# Info

Log format is state, action, reward, new_state. Ex:

(3, 4); (LEFT, FORWARD); -40.4; (2, 3); (2, 3); (LEFT, BACKWARDS); +20.2; (1, 4);


