import os
import secrets
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from careercompass.models import Job, User
from careercompass.extensions import db
from careercompass.recommendation_engine import recommend_jobs
from . import main_bp


def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    # Save to the actual static folder configured in the app
    picture_path = os.path.join(current_app.static_folder, 'profile_pics', picture_fn)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    
    form_picture.save(picture_path)
    return picture_fn

@main_bp.route('/')
def home():
    return render_template('index.html')



@main_bp.route('/dashboard')
@login_required
def dashboard():
    from careercompass.recommendation_engine import get_skill_opportunities
    
    skill_ops = []
    if current_user.tech_skills:
        skills = [s.strip() for s in current_user.tech_skills.split(',') if s.strip()]
        for s in skills[:4]: # Limit to top 4 for dashboard
            skill_ops.append({
                "skill": s,
                "opportunities": get_skill_opportunities(s)
            })
            
    return render_template('dashboard.html', skill_opportunities=skill_ops)



@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_username = request.form.get('username')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        dob_str = request.form.get('dob')
        gender = request.form.get('gender')
        
        # Social links
        linkedin = request.form.get('linkedin')
        github = request.form.get('github')
        twitter = request.form.get('twitter')
        website = request.form.get('website')
        
        tech_skills = request.form.getlist('tech_skills')
        soft_skills = request.form.get('soft_skills')
        qualification = request.form.get('qualification')
        industry = request.form.get('industry')

        # Handle Profile Picture
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename != '':
                picture_file = save_profile_picture(file)
                current_user.profile_pic = picture_file

        # Username update logic
        if new_username and new_username != current_user.username:
            user_exists = User.query.filter_by(username=new_username).first()
            if user_exists:
                flash('Username already taken. Please choose another.', 'danger')
                return redirect(url_for('main.profile'))
            current_user.username = new_username

        current_user.full_name = full_name
        current_user.email = email
        current_user.phone = phone
        current_user.address = address
        current_user.gender = gender
        
        # Update socials
        current_user.linkedin = linkedin
        current_user.github = github
        current_user.twitter = twitter
        current_user.website = website
        
        if dob_str:
            try:
                current_user.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        current_user.tech_skills = ",".join(tech_skills) if tech_skills else ""
        current_user.soft_skills = soft_skills
        current_user.qualification = qualification
        current_user.industry = industry

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))

    return render_template('profile.html')



@main_bp.route('/recommendations')
@login_required
def recommendations():

    if not current_user.tech_skills:
        flash('Please update your profile with technical skills to get recommendations.', 'warning')
        return redirect(url_for('main.profile'))

    jobs = Job.query.all()

    if not jobs:
        flash('No jobs available in the database.', 'info')
        return render_template('recommendations.html', recommendations=[])

    recommendations_data = recommend_jobs(current_user, jobs)

    return render_template(
        'recommendations.html',
        recommendations=recommendations_data
    )


@main_bp.route('/roadmap/<int:job_id>')
@login_required
def roadmap(job_id):
    job = Job.query.get_or_404(job_id)
    
    from careercompass.recommendation_engine import generate_roadmap
    roadmap_data = generate_roadmap(job.tech_skills)
    
    return render_template('roadmap.html', job=job, roadmap=roadmap_data)


@main_bp.route('/resume-analyzer/<int:job_id>', methods=['GET', 'POST'])
@login_required
def resume_analyzer(job_id):
    job = Job.query.get_or_404(job_id)
    analysis_result = None
    
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file uploaded. Please upload a PDF.', 'danger')
            return redirect(request.url)
            
        file = request.files['resume']
        if file.filename == '':
            flash('No selected file. Please select a PDF.', 'danger')
            return redirect(request.url)
            
        if file and file.filename.endswith('.pdf'):
            from careercompass.recommendation_engine import extract_text_from_pdf, analyze_resume
            resume_text = extract_text_from_pdf(file)
            analysis_result = analyze_resume(resume_text, job.tech_skills, job.soft_skills)
            flash('Resume analyzed successfully!', 'success')
        else:
            flash('Invalid file format. Please upload a PDF file.', 'danger')
            return redirect(request.url)
            
    return render_template('resume_analyzer.html', job=job, analysis_result=analysis_result)