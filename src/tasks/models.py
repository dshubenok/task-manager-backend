from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Task(BaseModel):
    class Status(models.TextChoices):
        NOT_STARTED = "NS", "Not started"
        IN_PROGRESS = "IP", "In progress"
        DONE = "DN", "Done"

    class Priority(models.TextChoices):
        LOW = "LW", "Low"
        MEDIUM = "MD", "Medium"
        HIGH = "HG", "High"

    title = models.CharField(max_length=200)
    description = models.TextField(
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owner_tasks",
        blank=True,
        null=True,
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="assignee_tasks",
    )
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.NOT_STARTED.value
    )
    priority = models.CharField(
        max_length=2, choices=Priority.choices, default=Priority.LOW.value
    )
    expired_at = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Task {self.title} by {self.owner}"


class Comment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"
