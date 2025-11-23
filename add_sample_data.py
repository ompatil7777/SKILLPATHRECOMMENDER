import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillpath_project.settings')
django.setup()

from recommender.models import Domain, Skill, Career

def add_sample_data():
    print("Adding sample data...")
    
    # Clear existing data
    Domain.objects.all().delete()
    
    # Create Domains
    web_dev = Domain.objects.create(
        name="Web Development",
        description="Building websites and web applications"
    )
    
    ai_ml = Domain.objects.create(
        name="Artificial Intelligence & Machine Learning",
        description="AI, ML, Deep Learning, and Data Science"
    )
    
    cloud = Domain.objects.create(
        name="Cloud Computing",
        description="Cloud infrastructure, DevOps, and deployment"
    )
    
    mobile = Domain.objects.create(
        name="Mobile Development",
        description="iOS and Android app development"
    )
    
    print("✓ Domains created")
    
    # Create Skills for Web Development
    html = Skill.objects.create(
        name="HTML",
        domain=web_dev,
        difficulty_level="Beginner",
        description="Markup language for creating web pages"
    )
    
    css = Skill.objects.create(
        name="CSS",
        domain=web_dev,
        difficulty_level="Beginner",
        description="Styling language for web pages"
    )
    
    javascript = Skill.objects.create(
        name="JavaScript",
        domain=web_dev,
        difficulty_level="Intermediate",
        description="Programming language for web interactivity"
    )
    javascript.prerequisites.add(html, css)
    
    react = Skill.objects.create(
        name="React.js",
        domain=web_dev,
        difficulty_level="Intermediate",
        description="JavaScript library for building user interfaces"
    )
    react.prerequisites.add(javascript)
    
    nodejs = Skill.objects.create(
        name="Node.js",
        domain=web_dev,
        difficulty_level="Intermediate",
        description="JavaScript runtime for server-side development"
    )
    nodejs.prerequisites.add(javascript)
    
    mongodb = Skill.objects.create(
        name="MongoDB",
        domain=web_dev,
        difficulty_level="Intermediate",
        description="NoSQL database"
    )
    
    fullstack = Skill.objects.create(
        name="Full Stack Development",
        domain=web_dev,
        difficulty_level="Advanced",
        description="End-to-end web development"
    )
    fullstack.prerequisites.add(react, nodejs, mongodb)
    
    print("✓ Web Development skills created")
    
    # Create Skills for AI/ML
    python = Skill.objects.create(
        name="Python Programming",
        domain=ai_ml,
        difficulty_level="Beginner",
        description="High-level programming language"
    )
    
    numpy = Skill.objects.create(
        name="NumPy",
        domain=ai_ml,
        difficulty_level="Beginner",
        description="Library for numerical computing"
    )
    numpy.prerequisites.add(python)
    
    pandas = Skill.objects.create(
        name="Pandas",
        domain=ai_ml,
        difficulty_level="Beginner",
        description="Data manipulation and analysis"
    )
    pandas.prerequisites.add(python, numpy)
    
    ml_basics = Skill.objects.create(
        name="Machine Learning Basics",
        domain=ai_ml,
        difficulty_level="Intermediate",
        description="Fundamentals of ML algorithms"
    )
    ml_basics.prerequisites.add(python, pandas)
    
    deep_learning = Skill.objects.create(
        name="Deep Learning",
        domain=ai_ml,
        difficulty_level="Advanced",
        description="Neural networks and deep learning"
    )
    deep_learning.prerequisites.add(ml_basics)
    
    tensorflow = Skill.objects.create(
        name="TensorFlow",
        domain=ai_ml,
        difficulty_level="Advanced",
        description="Deep learning framework"
    )
    tensorflow.prerequisites.add(deep_learning)
    
    print("✓ AI/ML skills created")
    
    # Create Skills for Cloud Computing
    linux = Skill.objects.create(
        name="Linux Basics",
        domain=cloud,
        difficulty_level="Beginner",
        description="Operating system fundamentals"
    )
    
    docker = Skill.objects.create(
        name="Docker",
        domain=cloud,
        difficulty_level="Intermediate",
        description="Containerization platform"
    )
    docker.prerequisites.add(linux)
    
    kubernetes = Skill.objects.create(
        name="Kubernetes",
        domain=cloud,
        difficulty_level="Advanced",
        description="Container orchestration"
    )
    kubernetes.prerequisites.add(docker)
    
    aws = Skill.objects.create(
        name="AWS",
        domain=cloud,
        difficulty_level="Intermediate",
        description="Amazon Web Services cloud platform"
    )
    aws.prerequisites.add(linux)
    
    print("✓ Cloud Computing skills created")
    
    # Create Skills for Mobile Development
    java = Skill.objects.create(
        name="Java",
        domain=mobile,
        difficulty_level="Beginner",
        description="Object-oriented programming language"
    )
    
    kotlin = Skill.objects.create(
        name="Kotlin",
        domain=mobile,
        difficulty_level="Intermediate",
        description="Modern language for Android development"
    )
    kotlin.prerequisites.add(java)
    
    android = Skill.objects.create(
        name="Android Development",
        domain=mobile,
        difficulty_level="Intermediate",
        description="Building Android apps"
    )
    android.prerequisites.add(kotlin)
    
    swift = Skill.objects.create(
        name="Swift",
        domain=mobile,
        difficulty_level="Intermediate",
        description="Programming language for iOS"
    )
    
    ios = Skill.objects.create(
        name="iOS Development",
        domain=mobile,
        difficulty_level="Advanced",
        description="Building iOS apps"
    )
    ios.prerequisites.add(swift)
    
    print("✓ Mobile Development skills created")
    
    # Create Careers
    frontend_dev = Career.objects.create(
        title="Frontend Developer",
        domain=web_dev,
        average_salary="$70,000 - $120,000",
        description="Build user interfaces for websites and web applications"
    )
    frontend_dev.required_skills.add(html, css, javascript, react)
    
    backend_dev = Career.objects.create(
        title="Backend Developer",
        domain=web_dev,
        average_salary="$80,000 - $130,000",
        description="Build server-side logic and databases"
    )
    backend_dev.required_skills.add(javascript, nodejs, mongodb)
    
    fullstack_dev = Career.objects.create(
        title="Full Stack Developer",
        domain=web_dev,
        average_salary="$90,000 - $150,000",
        description="Build complete web applications from front to back"
    )
    fullstack_dev.required_skills.add(html, css, javascript, react, nodejs, mongodb, fullstack)
    
    data_scientist = Career.objects.create(
        title="Data Scientist",
        domain=ai_ml,
        average_salary="$100,000 - $160,000",
        description="Analyze data and build predictive models"
    )
    data_scientist.required_skills.add(python, numpy, pandas, ml_basics)
    
    ml_engineer = Career.objects.create(
        title="Machine Learning Engineer",
        domain=ai_ml,
        average_salary="$120,000 - $180,000",
        description="Design and implement ML systems"
    )
    ml_engineer.required_skills.add(python, ml_basics, deep_learning, tensorflow)
    
    devops = Career.objects.create(
        title="DevOps Engineer",
        domain=cloud,
        average_salary="$95,000 - $150,000",
        description="Automate and optimize development workflows"
    )
    devops.required_skills.add(linux, docker, kubernetes, aws)
    
    cloud_arch = Career.objects.create(
        title="Cloud Architect",
        domain=cloud,
        average_salary="$130,000 - $200,000",
        description="Design scalable cloud infrastructure"
    )
    cloud_arch.required_skills.add(linux, docker, kubernetes, aws)
    
    android_dev = Career.objects.create(
        title="Android Developer",
        domain=mobile,
        average_salary="$80,000 - $140,000",
        description="Build Android mobile applications"
    )
    android_dev.required_skills.add(java, kotlin, android)
    
    ios_dev = Career.objects.create(
        title="iOS Developer",
        domain=mobile,
        average_salary="$85,000 - $150,000",
        description="Build iOS mobile applications"
    )
    ios_dev.required_skills.add(swift, ios)
    
    print("✓ Careers created")
    print("\n✅ Sample data added successfully!")
    print(f"Total Domains: {Domain.objects.count()}")
    print(f"Total Skills: {Skill.objects.count()}")
    print(f"Total Careers: {Career.objects.count()}")

if __name__ == "__main__":
    add_sample_data()