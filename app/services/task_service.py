tasks = []

def get_all_tasks():
    return tasks

def get_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def create_task(title):
    task = {
        "id": len(tasks) + 1,
        "title": title
    }
    tasks.append(task)
    return task

def delete_task(task_id):
    task = get_task(task_id)
    if task:
        tasks.remove(task)
        return True
    return False