from django.db import models
from django.contrib.auth.models import User, Group
from PIL import Image
from django.utils import timezone


# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField()
    members = models.ManyToManyField(User, through="TeamMember", related_name="teams")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="team_created"
    )
    projects = models.ManyToManyField("Project", related_name="teams")

    class Meta:
        permissions = [
            ("can_manage_team", "can manage team"),
            ("can_manage_tasks", "can manage tasks"),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)

        owner_team_member, created = TeamMember.objects.get_or_create(
            user=self.owner, team=self, role="Owner"
        )
        owner_team_member.is_manager = True
        owner_team_member.save()

        super().save(*args, **kwargs)


class CustomTeam(Group):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class UserCreate(models.Model):
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, related_name="profile"
    )
    name = models.CharField(max_length=30, null=True)
    profile_picture = models.ImageField(
        default="default.jpg", upload_to="profile_images", blank=True
    )
    current_team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.name if self.name else self.user.username

    def save(self, *args, **kwargs):
        super(UserCreate, self).save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)


class TeamMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=100)
    responsibilities = models.TextField(blank=True)
    is_manager = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    user_profile = models.OneToOneField(
        UserCreate, on_delete=models.CASCADE, null=True, default=None
    )

    def __str__(self):
        if self.user_profile:
            return self.user_profile.name
        else:
            return self.user.username

    @property
    def profile_picture(self):
        if self.user_profile:
            return self.user_profile.profile_picture
        else:
            return "default.jpg"

    def save(self, *args, **kwargs):
        if not self.user_profile:
            try:
                self.user_profile = UserCreate.objects.get(user=self.user)
            except UserCreate.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        if self.team and self.user_profile:
            self.user_profile.current_team = self.team
            self.user_profile.save()


class Priority(models.Model):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    CRITICAL = "Critical"
    BLOCKER = "Blocker"

    PRIORITY_CHOICES = [
        (HIGH, "High Priority"),
        (MEDIUM, "Medium Priority"),
        (LOW, "Low Priority"),
        (CRITICAL, "Critical Priority"),
        (BLOCKER, "Blocker Priority"),
    ]
    name = models.CharField(max_length=20, choices=PRIORITY_CHOICES, unique=True)
    color = models.CharField(
        max_length=7,
        choices=[
            ("#FF0000", "Red"),
            ("#FFA500", "Orange"),
            ("#FFFF00", "Yellow"),
            ("#800000", "Dark Red"),
            ("#000000", "Black"),
        ],
        default="#FFFFFF",  # (white)
    )

    def __str__(self):
        return self.name

    def get_color(self):
        return self.color

    class Meta:
        verbose_name_plural = "Priorities"


class Project(models.Model):
    STATUS_CHOICES = [
        ("Planning", "Planning"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2400)
    leader = models.ForeignKey(
        TeamMember,
        on_delete=models.SET_NULL,
        null=True,
        related_name="leading_projects",
        limit_choices_to={"is_manager": True},
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Planning")
    team = models.ManyToManyField(Team, related_name="project")
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def update_status_to_in_progress(self):
        if self.status != "In Progress":
            self.status = "In Progress"
            self.save()

    def calculate_overall_progress(self):
        try:
            total_tasks = self.task_set.count()
            total_progress = 0

            for task in self.task_set.all():
                if task.status == "Completed":
                    total_progress += 100
                elif task.status == "In Progress":
                    total_progress += 50

            if total_tasks == 0:
                return 0
            else:
                overall_progress = round((total_progress / (total_tasks * 100)) * 100)

                if overall_progress == 100 and self.status != "Completed":
                    self.status = "Completed"
                    self.save()

                return overall_progress
        except Project.DoesNotExist:
            return None


class Task(models.Model):
    STATUS_CHOICES = [
        ("Not Started", "Not Started"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2400)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(TeamMember, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    start = models.DateTimeField()
    team = models.ManyToManyField(Team, related_name="task")
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Not Started"
    )
    attachments = models.ManyToManyField(
        "Attachment", related_name="tasks", blank=True, null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
        self.project.update_status_to_in_progress()


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(TeamMember, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Comment by {self.user.user.username} on {self.timestamp}"


class Attachment(models.Model):
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="attachments")
    uploaded_by = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class TeamInvitation(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_invitations"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_invitations"
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Team Invitation from {self.sender.username} to {self.receiver.username} for {self.team.name}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    team_invitation = models.ForeignKey(
        TeamInvitation, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"


class Activity(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    task = models.ForeignKey("Task", on_delete=models.CASCADE, null=True, blank=True)
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE)
    description = models.TextField()
