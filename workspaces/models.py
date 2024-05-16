from django.db import models
from accounts.models import User
from datetime import timedelta
# ************ Here is All the Models of the Workspace *********** #


# * ==================== * This is Member Model * =========================== * #
class roles_choice(models.TextChoices):
    MANAGER = "Manager"
    ASSOCIATE_MANAGER = "Associate Manager"
    TEAM_LEADER = "Team Leader"
    MEMBER = "Member"

class Member(models.Model):
    role = models.CharField(max_length=100, choices=roles_choice.choices, default=roles_choice.MEMBER)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Member name :{self.user.first_name} , Member's User ID: {self.user.id}" 
    


# * ==================== * This is WorkSpeace Model * =========================== * #
class WorkSpace(models.Model):
    name = models.CharField(max_length=250)
    workSpace_manager = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"WorkSpace Name: {self.name}"



# * ==================== * This is TimeLine Model * =========================== * #
class Timeline_Status(models.TextChoices):
    IN_PROGRESS = "In Progress"
    TO_DO = "To Do"
    TESTING = "Testing"
    DONE = "Done"

class Timeline(models.Model):
    workspace_Name =  models.ForeignKey(WorkSpace, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=500)
    details = models.TextField()
    assign = models.ForeignKey(Member, on_delete=models.CASCADE)
    start_Date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_Date = models.DateTimeField(auto_now=False, auto_now_add=False)
    comment = models.TextField(null=True,blank=True)
    duration = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=Timeline_Status.choices, default=Timeline_Status.TO_DO)

    def save(self, *args, **kwargs):
        # Calculate duration only if both start_Date and end_Date are set
        if self.start_Date and self.end_Date:
            duration_timedelta = self.end_Date - self.start_Date
            self.duration = duration_timedelta.days 

        super().save(*args, **kwargs)  # Call the original save method
    
    def __str__(self):
        return f"Timeline Name : {self.name} Team Lead : {self.assign.user}"

# * ==================== * This is Scrum Model * =========================== * #
class Scrum(models.Model):
    timeline_Name = models.OneToOneField(Timeline, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=250)
    details = models.TextField()
    members = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f"Scrum Name: {self.name}"
    

# * ==================== * This is Task Model * =========================== * #
class Task_Status(models.TextChoices):
    IN_PROGRESS = "In Progress"
    TO_DO = "To Do"
    DONE = "Done"
class TaskPriority(models.TextChoices):
    NORMAL = "Normal Priority"
    MID = "MID Priority"
    IMMEDIATE = "Immediate Priority"

class TaskType(models.TextChoices):
    FEATURE = "Feature"
    BUG_FIX = "Bug Fix" 
    CODE_TEST = "Code Test"
    TASK = "Task"  

class Task(models.Model):
    scrum_Name = models.ForeignKey(Scrum, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=250)
    details = models.TextField()
    assign = models.ForeignKey(Member, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=Task_Status.choices, default=Task_Status.TO_DO)
    priority = models.CharField(max_length=100, choices=TaskPriority.choices, default=TaskPriority.NORMAL)
    which_Type = models.CharField(max_length=100, choices=TaskType.choices, default=TaskType.TASK)
    task_Value = models.DecimalField(max_digits=5, decimal_places=0)

    def __str__(self):
        return f"Task Name: {self.name} Task Assign to: {self.assign.user}"


# * ==================== * This is Task Comment Model * =========================== * #
class TaskComment(models.Model):
    task_Name = models.ForeignKey(Task, on_delete=models.CASCADE,null=True)
    comment = models.TextField()
    created = models.DateTimeField(auto_now=False, auto_now_add=False)
    commernter = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Commenter Name: {self.commernter.user}"