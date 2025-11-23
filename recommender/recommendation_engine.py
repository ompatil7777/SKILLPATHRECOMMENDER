from .models import Career, Skill, LearningPath, PathStep

class RecommendationEngine:
    
    @staticmethod
    def get_matching_careers(domain, user_skills):
        """Find careers matching domain and user skills"""
        careers = Career.objects.filter(domain=domain)
        
        # Score careers based on how many required skills user already has
        career_scores = []
        for career in careers:
            required_skills = set(career.required_skills.all())
            user_skill_set = set(user_skills)
            matching_skills = required_skills.intersection(user_skill_set)
            
            score = len(matching_skills) / len(required_skills) if required_skills else 0
            career_scores.append({
                'career': career,
                'score': score,
                'matching_skills': len(matching_skills),
                'total_required': len(required_skills)
            })
        
        # Sort by score
        career_scores.sort(key=lambda x: x['score'], reverse=True)
        return career_scores
    
    @staticmethod
    def generate_learning_path(user, career):
        """Generate step-by-step learning path for a career"""
        # Get user's current skills
        user_profile = user.userprofile
        current_skills = set(user_profile.current_skills.all())
        
        # Get required skills for career
        required_skills = career.required_skills.all()
        
        # Find skills user needs to learn
        skills_to_learn = [skill for skill in required_skills if skill not in current_skills]
        
        # Sort by difficulty level
        difficulty_order = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
        skills_to_learn.sort(key=lambda x: difficulty_order.get(x.difficulty_level, 2))
        
        # Create learning path
        learning_path = LearningPath.objects.create(
            user=user,
            target_career=career
        )
        
        # Create path steps
        for index, skill in enumerate(skills_to_learn, start=1):
            PathStep.objects.create(
                learning_path=learning_path,
                skill=skill,
                step_order=index,
                status='Not Started'
            )
        
        return learning_path
    
    @staticmethod
    def get_suggested_skills(domain, current_skills):
        """Suggest next skills to learn based on current skills"""
        # Get all skills in the domain
        all_domain_skills = Skill.objects.filter(domain=domain)
        
        # Filter out skills user already has
        current_skill_ids = [skill.id for skill in current_skills]
        suggested = []
        
        for skill in all_domain_skills:
            if skill.id not in current_skill_ids:
                # Check if prerequisites are met
                prerequisites = skill.prerequisites.all()
                if all(prereq in current_skills for prereq in prerequisites):
                    suggested.append(skill)
        
        return suggested[:10]  # Return top 10 suggestions