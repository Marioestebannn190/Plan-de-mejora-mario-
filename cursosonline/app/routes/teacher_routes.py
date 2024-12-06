from flask import Blueprint, request, jsonify
from app.models import db, Course, Module, StudyMaterial, ModuleSchema
from functools import wraps

teacher_bp = Blueprint('teacher', __name__)

# Decorador para validar rol de docente
def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Aquí iría la lógica de autenticación y verificación de rol
        # Por ahora, un placeholder
        return f(*args, **kwargs)
    return decorated_function

@teacher_bp.route('/crear-modulo', methods=['POST'])
@teacher_required
def crear_modulo():
    data = request.json
    
    # Validaciones básicas
    if not data or not data.get('course_id') or not data.get('title'):
        return jsonify({"error": "Datos incompletos"}), 400
    
    # Verificar que el curso exista
    curso = Course.query.get(data['course_id'])
    if not curso:
        return jsonify({"error": "Curso no encontrado"}), 404
    
    # Crear nuevo módulo
    nuevo_modulo = Module(
        title=data['title'],
        description=data.get('description', ''),
        course_id=data['course_id']
    )
    
    db.session.add(nuevo_modulo)
    db.session.commit()
    
    # Serializar el módulo
    module_schema = ModuleSchema()
    return jsonify(module_schema.dump(nuevo_modulo)), 201

@teacher_bp.route('/agregar-material-estudio', methods=['POST'])
@teacher_required
def agregar_material_estudio():
    data = request.json
    
    # Validaciones básicas
    if not data or not data.get('module_id') or not data.get('title'):
        return jsonify({"error": "Datos incompletos"}), 400
    
    # Verificar que el módulo exista
    modulo = Module.query.get(data['module_id'])
    if not modulo:
        return jsonify({"error": "Módulo no encontrado"}), 404
    
    # Crear nuevo material de estudio
    nuevo_material = StudyMaterial(
        title=data['title'],
        file_url=data.get('file_url', ''),
        module_id=data['module_id']
    )
    
    db.session.add(nuevo_material)
    db.session.commit()
    
    return jsonify({
        "mensaje": "Material de estudio agregado exitosamente",
        "material_id": nuevo_material.id
    }), 201

@teacher_bp.route('/mis-cursos', methods=['GET'])
@teacher_required
def mis_cursos():
    # TODO: Obtener el usuario actual autenticado
    # Por ahora, un placeholder
    usuario_actual_id = 1  # Reemplazar con lógica de autenticación
    
    # Obtener cursos del docente
    cursos = Course.query.filter(Course.teachers.any(id=usuario_actual_id)).all()
    
    # Serializar los cursos
    course_schema = course_schema(many=True)
    return jsonify(course_schema.dump(cursos)), 200

@teacher_bp.route('/modulos-curso/<int:curso_id>', methods=['GET'])
@teacher_required
def modulos_por_curso(curso_id):
    # Verificar que el curso exista
    curso = Course.query.get(curso_id)
    if not curso:
        return jsonify({"error": "Curso no encontrado"}), 404
    
    # Obtener módulos del curso
    modulos = Module.query.filter_by(course_id=curso_id).all()
    
    # Serializar los módulos
    module_schema = ModuleSchema(many=True)
    return jsonify(module_schema.dump(modulos)), 200