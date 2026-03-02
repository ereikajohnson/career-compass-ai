from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from careercompass.extensions import db
from careercompass.models.job import Job

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['GET'])
@login_required
def admin_dashboard():
    
    jobs = Job.query.all()
    return render_template('admin.html', jobs=jobs)

@admin_bp.route('/job/add', methods=['POST'])
@login_required
def add_job():
    title = request.form.get('title')
    company = request.form.get('company')
    tech_skills = request.form.get('tech_skills')
    soft_skills = request.form.get('soft_skills')
    min_qualification = request.form.get('min_qualification')
    description = request.form.get('description')
    industry = request.form.get('industry')
    availability = request.form.get('availability')
    salary_package = request.form.get('salary_package')
    
    new_job = Job(
        title=title,
        company=company,
        tech_skills=tech_skills,
        soft_skills=soft_skills,
        min_qualification=min_qualification,
        description=description,
        industry=industry,
        availability=availability,
        salary_package=salary_package
    )
    
    db.session.add(new_job)
    db.session.commit()
    flash('New job added successfully.', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/job/delete/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully.', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/job/edit/<int:job_id>', methods=['POST'])
@login_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    job.title = request.form.get('title')
    job.company = request.form.get('company')
    job.tech_skills = request.form.get('tech_skills')
    job.soft_skills = request.form.get('soft_skills')
    job.min_qualification = request.form.get('min_qualification')
    job.description = request.form.get('description')
    job.industry = request.form.get('industry')
    job.availability = request.form.get('availability')
    job.salary_package = request.form.get('salary_package')
    
    db.session.commit()
    flash('Job updated successfully.', 'success')
    return redirect(url_for('admin.admin_dashboard'))
