# SkillPathRecommender/recommender/models.py
from django.db import models
from django.contrib.auth.models import User

class Domain(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    name = models.CharField(max_length=200)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='skills')
    description = models.TextField(blank=True)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Beginner')
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependent_skills')

    def __str__(self):
        return f"{self.name} ({self.domain.name})"

class Career(models.Model):
    title = models.CharField(max_length=200)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='careers')
    required_skills = models.ManyToManyField(Skill, blank=True, related_name='required_for_careers')
    description = models.TextField(blank=True)

    # Accept salary label strings like "$70,000 - $120,000"
    average_salary = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.domain.name}"

class UserProfile(models.Model):
    # IMPORTANT: related_name='profile' so you can access user.profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, null=True, blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name='users_with_skill')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Profile: {self.user.username}"

class LearningPath(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_paths')
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True, blank=True, related_name='learning_paths')
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title or f"{self.user.username}'s path for {self.career.title if self.career else 'custom'}"

class PathStep(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='steps')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    step_order = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started')

    class Meta:
        ordering = ['step_order']
        unique_together = ('learning_path', 'step_order')

    def __str__(self):
        return f"Step {self.step_order}: {self.skill.name}"
