from flask import Blueprint, request, jsonify
from app.models import db, User, Course, Module, UserSchema, CourseSchema
from app.services.auth_service import AuthService
from functools import wraps

admin_bp = Blueprint('admin', __name__)

# Decorador para validar rol de admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Aquí iría la lógica de autenticación y verificación de rol
        # Por ahora, un placeholder
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/crear-administrador', methods=['POST'])
@admin_required
def crear_administrador():
    data = request.json
    
    # Validaciones básicas
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Datos incompletos"}), 400
    
    # Verificar si el usuario ya existe
    existing_user = User.query.filter(
        (User.username == data['username']) | (User.email == data['email'])
    ).first()
    
    if existing_user:
        return jsonify({"error": "Usuario ya existe"}), 400
    
    # Crear nuevo administrador
    nuevo_admin = User(
        username=data['username'],
        email=data['email'],
        password=AuthService.hash_password(data['password']),
        role='admin'
    )
    
    db.session.add(nuevo_admin)
    db.session.commit()
    
    return jsonify({"mensaje": "Administrador creado exitosamente"}), 201

@admin_bp.route('/crear-docente', methods=['POST'])
@admin_required
def crear_docente():
    data = request.json
    
    # Validaciones básicas
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Datos incompletos"}), 400
    
    # Verificar si el usuario ya existe
    existing_user = User.query.filter(
        (User.username == data['username']) | (User.email == data['email'])
    ).first()
    
    if existing_user:
        return jsonify({"error": "Usuario ya existe"}), 400
    
    # Crear nuevo docente
    nuevo_docente = User(
        username=data['username'],
        email=data['email'],
        password=AuthService.hash_password(data['password']),
        role='teacher'
    )
    
    db.session.add(nuevo_docente)
    db.session.commit()
    
    return jsonify({"mensaje": "Docente creado exitosamente"}), 201

@admin_bp.route('/crear-curso', methods=['POST'])
@admin_required
def crear_curso():
    data = request.json
    
    # Validaciones básicas
    if not data or not data.get('title'):
        return jsonify({"error": "Título del curso es obligatorio"}), 400
    
    # Crear nuevo curso
    nuevo_curso = Course(
        title=data['title'],
        description=data.get('description', '')
    )
    
    db.session.add(nuevo_curso)
    db.session.commit()
    
    # Serializar el curso
    course_schema = CourseSchema()
    return jsonify(course_schema.dump(nuevo_curso)), 201

@admin_bp.route('/cursos', methods=['GET'])
@admin_required
def listar_cursos():
    cursos = Course.query.all()
    course_schema = CourseSchema(many=True)
    return jsonify(course_schema.dump(cursos)), 200

@admin_bp.route('/usuarios', methods=['GET'])
@admin_required
def listar_usuarios():
    usuarios = User.query.all()
    user_schema = UserSchema(many=True)
    return jsonify(user_schema.dump(usuarios)), 200