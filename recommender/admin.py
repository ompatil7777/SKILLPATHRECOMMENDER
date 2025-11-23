from django.contrib import admin
from .models import Domain, Skill, Career, UserProfile, LearningPath, PathStep

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain', 'difficulty_level']
    list_filter = ['domain', 'difficulty_level']
    search_fields = ['name']
    filter_horizontal = ['prerequisites']

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ['title', 'domain', 'num_required_skills', 'average_salary']
    list_filter = ['domain']
    search_fields = ['title']
    filter_horizontal = ['required_skills']

    def num_required_skills(self, obj):
        return obj.required_skills.count()
    num_required_skills.short_description = 'Required Skills'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'domain']
    list_filter = ['domain']
    search_fields = ['user__username']
    filter_horizontal = ['skills']

@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ['user', 'career', 'title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'career__title', 'title']

@admin.register(PathStep)
class PathStepAdmin(admin.ModelAdmin):
    list_display = ['learning_path', 'skill', 'step_order', 'status']
    list_filter = ['status']
    ordering = ['learning_path', 'step_order']
