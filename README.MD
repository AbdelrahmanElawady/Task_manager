Task Manager
===========
Task Manager is a python tool to help execute tasks in topological order.

Usage
=====
```python
import task_manager
task_manager.manage('file.ini') # execute the main task and its dependencies in topological order
```
file.ini content:
-----------------
```ini
[main]
command=echo this is last
dependencies=second, third
[first]
command=echo this is first
dependencies=
[second]
command=echo this is second
dependencies=first
[third]
command=echo this is third
dependencies=
[fourth]
command=echo this should not run
dependencies=
```

output:
-------
The order of the tasks should be:

first, second, third, main

The output should be:
```
this is first
this is second
this is third
this is last
```

Specification
=============
* The program runs the task named 'main'.
* The program returns an error if their isn't a task named 'main'.
* The program checks automatically for cycles in tasks order.
* If a cycle is found the program returns an error and prints the cycle.