import iniparser
import os

from iniparser import parse

def manage(filename: str):
    """
    Manages tasks and passes main to finish() to run

    Args:
        filename: the name of the INI file containing the tasks
    """
    tasks = parse(filename)
    if "main" not in tasks:
        raise NameError("main task not found")
    detect_cycle(tasks)
    run(tasks, "main")

def run(tasks: dict, task_name: str):
    """
    Runs given task

    Args:
        tasks: contains task names as dicts containing commands and dependencies
        task_name: name of the task to be run
    """
    is_done = {}
    for task in tasks:
        is_done[task] = False
    tasks_done = []
    _run(tasks, "main", is_done, tasks_done)

def _run(tasks: dict, task_name: str, is_done: dict, tasks_done: list) -> list:
    """
    Runs given task and returns a list of tasks done in order to finish that task

    Args:
        tasks: contains task names as dicts containing commands and dependencies
        task_name: name of the task to be run
        is_done: dict of which task is done
    Returns:
        list of tasks done in order
    """
    if task_name not in tasks:
        raise NameError("task " + task_name + " not found")
    if is_done[task_name]:
        return tasks_done
    if tasks[task_name]['dependencies'] == "":
        os.system(tasks[task_name]['command'])
        tasks_done.append(task_name)
        is_done[task_name] = True
        return tasks_done
    tasks_needed = tasks[task_name]['dependencies'].split(', ')
    for task in tasks_needed:
        if task not in tasks:
            raise NameError("task " + task + " not found")
        _run(tasks, task, is_done, tasks_done)
    os.system(tasks[task_name]['command'])
    tasks_done.append(task_name)
    is_done[task_name] = True
    return tasks_done

def detect_cycle(tasks: dict):
    """
    Check if their is a cycle in all tasks

    Args:
        tasks: contains task names as dicts containing commands and dependencies
    """
    is_visited = {}
    is_done = {}
    tasks_in_queue = []
    for task in tasks:
        is_visited[task] = False
        is_done[task] = False
    if check_task_for_cycle(tasks, "main", is_visited, is_done, tasks_in_queue):
        print_cycle(tasks_in_queue)

def check_task_for_cycle(tasks: dict, task_name: str, is_visited: dict, is_done: dict, tasks_in_queue: list) -> bool:
    """
    Check if their is a cycle in a task dependencies

    Args:
        tasks: contains task names as dicts containing commands and dependencies
        task_name: the name of the task the function check for cycles
        is_visited: dict of tasks visited once
        is_done: dict of tasks done
        tasks_in_queue: empty list to be filled with tasks that need to be done in order to finish task_name
    Returns:
        True if their is a cycle in the task dependencies and False if their isn't
    """
    if task_name not in tasks:
        raise NameError("task " + task_name + " not found")
    if is_visited[task_name] and is_done[task_name]:
        return False
    if is_visited[task_name]:
        tasks_in_queue.append(task_name)
        return True
    is_visited[task_name] = True
    if task_name not in tasks:
        raise NameError("task " + task_name + " not found")
    if tasks[task_name]['dependencies'] == "":
        is_done[task_name] = True
        return False
    tasks_needed = tasks[task_name]['dependencies'].split(', ')
    for task in tasks_needed:
        if task not in tasks:
            raise NameError("task " + task + " not found")
        if check_task_for_cycle(tasks, task, is_visited, is_done, tasks_in_queue):
            tasks_in_queue.append(task_name)
            return True
    is_done[task_name] = True
    return False

def print_cycle(cycle: list):
    """
    Print name of tasks in cycle

    Args:
        cycle: list of tasks in cycle
    """
    raise Exception("Error: found a cycle in tasks\n" + " ==> ".join(cycle[cycle.index(cycle[0], 1)::-1]))