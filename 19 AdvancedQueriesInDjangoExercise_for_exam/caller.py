import os
from datetime import date

import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import RealEstateListing, VideoGame, BillingInfo, Invoice, Technology, Project, Programmer, Task



# Now, you can run the defined methods

# 1. Get overdue high-priority tasks
overdue_high_priority = Task.overdue_high_priority_tasks()
print("Overdue High Priority Tasks:")
for task in overdue_high_priority:
    print('- ' + task.title)

# 2. Get completed medium-priority tasks
completed_mid_priority = Task.completed_mid_priority_tasks()
print("Completed Medium Priority Tasks:")
for task in completed_mid_priority:
    print('- ' + task.title)

# 3. Search for tasks based on a query
search_results = Task.search_tasks("Task 3")
print("Search Results:")
for task in search_results:
    print('- ' + task.title)

# 4. Get recent completed tasks
recent_completed = task1.recent_completed_tasks(days=5)
print("Recent Completed Tasks:")
for task in recent_completed:
    print('- ' + task.title)



