import numpy as np
import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------- SKILL LEARNING RESOURCES ----------------
SKILL_RESOURCES = {
    "python": {
        "youtube": "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
        "course": "https://www.coursera.org/specializations/python",
        "docs": "https://docs.python.org/3/"
    },
    "java": {
        "youtube": "https://www.youtube.com/watch?v=eIrMbAQSU34",
        "course": "https://www.udemy.com/course/java-the-complete-java-developer-course/",
        "docs": "https://docs.oracle.com/en/java/"
    },
    "machine learning": {
        "youtube": "https://www.youtube.com/watch?v=GwIo3gDZCVQ",
        "course": "https://www.coursera.org/learn/machine-learning",
        "docs": "https://scikit-learn.org/stable/"
    },
    "sql": {
        "youtube": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
        "course": "https://www.udacity.com/course/sql-for-data-analysis--ud198",
        "docs": "https://dev.mysql.com/doc/"
    },
    "javascript": {
        "youtube": "https://www.youtube.com/watch?v=W6NZfCO5SIk",
        "course": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/",
        "docs": "https://developer.mozilla.org/en-US/docs/Web/JavaScript"
    },
    "react": {
        "youtube": "https://www.youtube.com/watch?v=bMknfKXIFA8",
        "course": "https://react.dev/learn",
        "docs": "https://react.dev/"
    },
    "node.js": {
        "youtube": "https://www.youtube.com/watch?v=TlB_eWDSMt4",
        "course": "https://www.udemy.com/course/the-complete-nodejs-developer-course-2/",
        "docs": "https://nodejs.org/en/docs/"
    },
    "aws": {
        "youtube": "https://www.youtube.com/watch?v=k1RI5locZE4",
        "course": "https://aws.amazon.com/training/",
        "docs": "https://docs.aws.amazon.com/"
    },
    "docker": {
        "youtube": "https://www.youtube.com/watch?v=pTFZFxd4hOI",
        "course": "https://www.docker.com/101-tutorial/",
        "docs": "https://docs.docker.com/"
    },
    "kubernetes": {
        "youtube": "https://www.youtube.com/watch?v=X48VuDVv0do",
        "course": "https://kubernetes.io/training/",
        "docs": "https://kubernetes.io/docs/home/"
    }
}

# ---------------- SKILL MARKET OPPORTUNITIES ----------------
SKILL_OPPORTUNITIES = {
    "python": [
        {"company": "Google India (Entry)", "salary": "₹12 - ₹15 LPA"},
        {"company": "Zomato", "salary": "₹8 - ₹14 LPA"},
        {"company": "Airtel X Labs", "salary": "₹7 - ₹12 LPA"}
    ],
    "java": [
        {"company": "Standard Chartered", "salary": "₹9 - ₹15 LPA"},
        {"company": "ICICI Bank", "salary": "₹6 - ₹11 LPA"},
        {"company": "TCS Digital", "salary": "₹7 - ₹10 LPA"}
    ],
    "javascript": [
        {"company": "Paytm", "salary": "₹10 - ₹15 LPA"},
        {"company": "Flipkart (Associate)", "salary": "₹9 - ₹14 LPA"},
        {"company": "OYO Rooms", "salary": "₹7 - ₹12 LPA"}
    ],
    "react": [
        {"company": "Razorpay", "salary": "₹11 - ₹15 LPA"},
        {"company": "PhonePe", "salary": "₹10 - ₹14 LPA"},
        {"company": "DailyHunt", "salary": "₹6 - ₹11 LPA"}
    ],
    "node.js": [
        {"company": "Postman", "salary": "₹12 - ₹15 LPA"},
        {"company": "Urban Company", "salary": "₹9 - ₹14 LPA"},
        {"company": "Byju's", "salary": "₹6 - ₹11 LPA"}
    ],
    "machine learning": [
        {"company": "Fractal Analytics", "salary": "₹10 - ₹15 LPA"},
        {"company": "Mu Sigma", "salary": "₹7 - ₹12 LPA"},
        {"company": "Tiger Analytics", "salary": "₹8 - ₹13 LPA"}
    ],
    "aws": [
        {"company": "Dell India", "salary": "₹8 - ₹13 LPA"},
        {"company": "Oracle India", "salary": "₹9 - ₹14 LPA"},
        {"company": "Tech Mahindra", "salary": "₹5 - ₹9 LPA"}
    ],
    "sql": [
        {"company": "JP Morgan Chase", "salary": "₹10 - ₹15 LPA"},
        {"company": "Capgemini", "salary": "₹6 - ₹10 LPA"},
        {"company": "Infosys", "salary": "₹4 - ₹8 LPA"}
    ]
}

def get_skill_resources(skill_name):
    skill_key = skill_name.lower().strip()
    return SKILL_RESOURCES.get(skill_key, {
        "youtube": f"https://www.youtube.com/results?search_query={skill_key}+tutorial",
        "course": f"https://www.coursera.org/search?query={skill_key}",
        "docs": f"https://www.google.com/search?q={skill_key}+official+documentation"
    })

def get_skill_opportunities(skill_name):
    skill_key = skill_name.lower().strip()
    return SKILL_OPPORTUNITIES.get(skill_key, [
        {"company": "Global Analytics", "salary": "₹7 - ₹12 LPA"},
        {"company": "Tech Startup", "salary": "₹5 - ₹10 LPA"}
    ])

# ---------------- SIMPLE STATIC RECOMMENDATION (Optional) ----------------
def get_recommendations(user):
    return [
        "Data Scientist",
        "AI Engineer",
        "Cloud Engineer",
        "Full Stack Developer"
    ]


# ---------------- PREPROCESS USER / JOB SKILLS ----------------
def preprocess_skills(skills_string):
    """
    Normalize skills:
    - Lowercase
    - Remove extra spaces
    - Remove duplicates
    - Convert comma-separated string into space-separated string
    """
    if not skills_string:
        return ""

    skills_list = [skill.strip().lower() for skill in skills_string.split(',')]

    # Remove duplicates while keeping order
    unique_skills = []
    for skill in skills_list:
        if skill and skill not in unique_skills:
            unique_skills.append(skill)

    return " ".join(unique_skills)


# ---------------- SKILL GAP ANALYSIS ----------------
def calculate_skill_gap(user_skills_list, job_skills_list):
    """
    Returns skills required for the job
    but missing from user profile.
    """
    return [
        skill for skill in job_skills_list
        if skill not in user_skills_list and skill
    ]


# ---------------- MAIN RECOMMENDATION FUNCTION ----------------
def recommend_jobs(user, all_jobs):
    """
    AI-based Job Recommendation using Cosine Similarity.

    Steps:
    1. Preprocess user skills
    2. Preprocess job skills
    3. Convert skills into binary vectors (CountVectorizer)
    4. Compute cosine similarity
    5. Perform skill gap analysis
    6. Rank jobs
    7. Return top 5
    """

    if not all_jobs or not user.tech_skills:
        return []

    # ---------- 1. Prepare User Skills ----------
    user_skills_str = preprocess_skills(user.tech_skills)
    user_skills_list = user_skills_str.split()

    # ---------- 2. Prepare Job Skills ----------
    job_data_list = []

    for job in all_jobs:
        processed_skills = preprocess_skills(job.tech_skills)

        job_data_list.append({
            "job": job,
            "processed_skills": processed_skills,
            "raw_skills_list": [
                s.strip().lower()
                for s in job.tech_skills.split(',')
                if s.strip()
            ]
        })

    # ---------- 3. Combine User + Job Skills ----------
    all_texts = [user_skills_str] + [
        jd["processed_skills"] for jd in job_data_list
    ]

    # ---------- 4. Vectorization ----------
    vectorizer = CountVectorizer(
        binary=True,
        token_pattern=r"(?u)\b[\w\.\+]+\b"
    )

    try:
        matrix = vectorizer.fit_transform(all_texts)
        vectors = matrix.toarray()
    except ValueError:
        # Happens if vocabulary is empty
        return []

    user_vector = vectors[0].reshape(1, -1)
    job_vectors = vectors[1:]

    # ---------- 5. Cosine Similarity ----------
    similarities = cosine_similarity(user_vector, job_vectors)[0]

    # ---------- 6. Build Recommendation List ----------
    recommendations = []

    for i, job_data in enumerate(job_data_list):
        similarity_score = round(similarities[i] * 100, 2)

        missing_skills = calculate_skill_gap(
            user_skills_list,
            job_data["raw_skills_list"]
        )

        missing_skills_with_resources = []
        for ms in missing_skills:
            missing_skills_with_resources.append({
                "skill": ms,
                "resources": get_skill_resources(ms),
                "opportunities": get_skill_opportunities(ms)
            })

        user_skills_with_ops = []
        for us in user_skills_list:
            user_skills_with_ops.append({
                "skill": us,
                "opportunities": get_skill_opportunities(us)
            })

        recommendations.append({
            "job": job_data["job"],
            "similarity_score": similarity_score,
            "missing_skills": missing_skills,
            "missing_skills_resources": missing_skills_with_resources,
            "user_skills_opportunities": user_skills_with_ops
        })

    # ---------- 7. Sort by Highest Match ----------
    recommendations.sort(
        key=lambda x: x["similarity_score"],
        reverse=True
    )

    return recommendations[:5]

# ---------------- AI CAREER ROADMAP GENERATOR ----------------
def generate_roadmap(job_skills_str):
    """
    Dynamically generates a career roadmap based on job skills.
    Spits out 3 phases, projects, certifications, and timeline.
    """
    if not job_skills_str:
        return {}

    skills_list = [s.strip().title() for s in job_skills_str.split(',') if s.strip()]
    
    # We will distribute the skills roughly across 3 phases
    total_skills = len(skills_list)
    phase1_skills = skills_list[:max(1, total_skills // 3)]
    phase2_skills = skills_list[len(phase1_skills):len(phase1_skills) + max(1, total_skills // 3)]
    phase3_skills = skills_list[len(phase1_skills) + len(phase2_skills):]
    
    if not phase3_skills and len(phase2_skills) > 1:
        phase3_skills = [phase2_skills.pop()]
    
    # Fallback if there are very few skills
    if not phase2_skills:
        phase2_skills = ["Advanced Tools & Frameworks"]
    if not phase3_skills:
        phase3_skills = ["System Design & Optimization"]

    primary_skill = skills_list[0] if skills_list else "Technology"

    roadmap = {
        "Phase 1: Foundation Skills": {
            "duration": "Weeks 1-4",
            "description": "Master the core concepts and basic syntax.",
            "skills": phase1_skills
        },
        "Phase 2: Intermediate Skills": {
            "duration": "Weeks 5-8",
            "description": "Learn framework/domain-specific tools and best practices.",
            "skills": phase2_skills
        },
        "Phase 3: Advanced Skills": {
            "duration": "Weeks 9-12",
            "description": "Focus on architecture, deployment, and optimization.",
            "skills": phase3_skills
        },
        "Suggested Projects": [
            f"Build a basic REST API using {primary_skill}",
            "Develop a full-stack portfolio project",
            f"Contribute to an open-source {primary_skill} repository"
        ],
        "Certifications": [
            f"Certified {primary_skill} Developer",
            "AWS Certified Cloud Practitioner (Optional)",
            "Industry standard agile certification"
        ],
        "Estimated Timeline": "12 Weeks (approx. 10-15 hrs/week)"
    }
    
    return roadmap

# ---------------- RESUME ANALYZER ----------------
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + " "
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def analyze_resume(resume_text, job_skills_str, job_soft_skills_str=""):
    """
    Compares resume text to job skills using cosine similarity.
    Returns match percentage, found skills (strengths),
    missing skills, soft skill matches, and improvement suggestions.
    """
    if not job_skills_str or not resume_text:
        return {
            "match_percentage": 0, 
            "strengths": [], 
            "missing": [], 
            "soft_skills": [],
            "suggestions": "Job has no specific skills or resume is empty."
        }

    # Preprocess job skills
    processed_job_skills = preprocess_skills(job_skills_str)
    raw_job_skills = [s.strip() for s in job_skills_str.split(',') if s.strip()]
    job_skills_lower = [s.lower() for s in raw_job_skills]

    # Preprocess resume text
    resume_text_lower = resume_text.lower()

    # Vectorization
    vectorizer = CountVectorizer(
        binary=True,
        token_pattern=r"(?u)\b[\w\.\+]+\b"
    )
    
    try:
        matrix = vectorizer.fit_transform([resume_text_lower, processed_job_skills])
        vectors = matrix.toarray()
        
        resume_vector = vectors[0].reshape(1, -1)
        job_vector = vectors[1].reshape(1, -1)
        
        similarity = cosine_similarity(resume_vector, job_vector)[0][0]
        match_percentage = int(round(similarity * 100, 0))
    except ValueError:
        match_percentage = 0
        
    # Analyze exactly which skills are present
    strengths = []
    missing = []
    
    for i, skill in enumerate(job_skills_lower):
        if skill in resume_text_lower:
            strengths.append(raw_job_skills[i])
        else:
            missing.append(raw_job_skills[i])
            
    # Soft skills analysis
    soft_skills_found = []
    if job_soft_skills_str:
        raw_soft_skills = [s.strip() for s in job_soft_skills_str.split(',') if s.strip()]
        for skill in raw_soft_skills:
            if skill.lower() in resume_text_lower:
                soft_skills_found.append(skill)
            
    # Refine match percentage based on exact hits weighting
    if len(job_skills_lower) > 0:
        exact_match_ratio = len(strengths) / len(job_skills_lower)
        
        # Combining cosine similarity (40%) and exact keyword match (60%)
        match_percentage = int((match_percentage * 0.4) + (exact_match_ratio * 100 * 0.6))
        
        # Adding a small bonus for soft skills matches (up to 5%)
        if job_soft_skills_str:
            raw_soft_skills = [s.strip() for s in job_soft_skills_str.split(',') if s.strip()]
            if raw_soft_skills:
                soft_bonus = (len(soft_skills_found) / len(raw_soft_skills)) * 5
                match_percentage += int(soft_bonus)
        
        # Final adjustment
        match_percentage = min(max(match_percentage, 0), 100)


    suggestions = ""
    if match_percentage >= 80:
        suggestions = "Your resume is highly optimized for this role! Consider tailoring your summary to highlight these key skills."
    elif match_percentage >= 50:
        suggestions = "Solid foundation, but you are missing some key requirements. Consider adding or learning the missing skills."
    else:
        suggestions = "Significant skill gap detected. We recommend focusing on learning the missing core skills before applying."
        
    return {
        "match_percentage": match_percentage,
        "strengths": strengths,
        "missing": missing,
        "soft_skills": soft_skills_found,
        "suggestions": suggestions
    }
