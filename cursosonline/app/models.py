from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  
    profile_picture = db.Column(db.String(255))
    
    courses_teaching = db.relationship('Course', secondary='course_teachers', back_populates='teachers')
    enrolled_courses = db.relationship('Course', secondary='course_enrollments', back_populates='students')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    modules = db.relationship('Module', back_populates='course', cascade='all, delete-orphan')
    teachers = db.relationship('User', secondary='course_teachers', back_populates='courses_teaching')
    students = db.relationship('User', secondary='course_enrollments', back_populates='enrolled_courses')

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    

    course = db.relationship('Course', back_populates='modules')
    study_materials = db.relationship('StudyMaterial', back_populates='module', cascade='all, delete-orphan')

class StudyMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    file_url = db.Column(db.String(255))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    
    
    module = db.relationship('Module', back_populates='study_materials')

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    progress_percentage = db.Column(db.Float, default=0.0)


course_teachers = db.Table('course_teachers',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

course_enrollments = db.Table('course_enrollments',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password',)

class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        load_instance = True

class ModuleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Module
        load_instance = True