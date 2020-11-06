import task_manager
import iniparser


from iniparser import parse
from task_manager import _run, check_task_for_cycle
tasks = parse("test.ini")
done = {}
visited = {}
def reset():
    for task in tasks:
        done[task] = False
        visited[task] = False

reset()
assert _run(tasks, "main", done, []) == ['4', '1', '5', '7', '6', '3', '2', 'main']
assert done == {'main': True, '1': True, '2': True, '3': True, '4': True, '5': True, '6': True, '7': True, '8': False, '9': False, '10': False}
reset()
assert _run(tasks, "1", done, []) == ['4', '1']
assert done == {'main': False, '1': True, '2': False, '3': False, '4': True, '5': False, '6': False, '7': False, '8': False, '9': False, '10': False}
reset()
assert _run(tasks, "2", done, []) == ['4', '5', '7', '6', '3', '2']
assert done == {'main': False, '1': False, '2': True, '3': True, '4': True, '5': True, '6': True, '7': True, '8': False, '9': False, '10': False}
reset()
assert check_task_for_cycle(tasks, "main", visited, done, []) == False
reset()
assert check_task_for_cycle(tasks, "2", visited, done, []) == False
reset()
assert check_task_for_cycle(tasks, "8", visited, done, []) == True
reset()
assert check_task_for_cycle(tasks, "10", visited, done, []) == True