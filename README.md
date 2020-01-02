# MDP
Finite Horizon Risk Sensitive MDP and Linear Programming

## github repo
https://github.com/Shar-pei-bear/MDP

## Dependency 
CVXOPT with GLPK is required, install instruction can be found here:
https://scaron.info/blog/linear-programming-in-python-with-cvxopt.html

## Project discription
The project currently supports two types of tasks: sequential tasks and disjunction tasks. Targets path and task type need to be specified before we can run the girdworld simulation. Static targets are treated as a special of dynamic targets, by specifying targets path compsed of same coordinates. Look at test.py for a specific example.

## Generate heat map
Simply run analysis_regret.py
