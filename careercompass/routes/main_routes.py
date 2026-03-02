from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from careercompass.models import Job
from careercompass.extensions import db
from careercompass.recommendation_engine import recommend_jobs
from . import main_bp



@main_bp.route('/')
def home():
    return render_template('index.html')



@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')



@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        tech_skills = request.form.getlist('tech_skills')
        soft_skills = request.form.get('soft_skills')
        qualification = request.form.get('qualification')
        industry = request.form.get('industry')

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
            analysis_result = analyze_resume(resume_text, job.tech_skills)
            flash('Resume analyzed successfully!', 'success')
        else:
            flash('Invalid file format. Please upload a PDF file.', 'danger')
            return redirect(request.url)
            
    return render_template('resume_analyzer.html', job=job, analysis_result=analysis_result)