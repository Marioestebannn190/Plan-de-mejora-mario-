from flask import Blueprint, request, jsonify
from app.models import db, Course, Module, UserProgress, UserSchema, CourseSchema, ModuleSchema
from functools import wraps

student_bp = Blueprint('student', __name__)

# Decorador para validar rol de estudiante
def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Aquí iría la lógica de autenticación y verificación de rol
        # Por ahora, un placeholder
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/inscribir-curso', methods=['POST'])
@student_required
def inscribir_curso():
    data = request.json
    
    # Validaciones básicas
    if not data or not data.get('course_id'):
        return jsonify({"error": "ID de curso es obligatorio"}), 400
    
    # TODO: Obtener usuario actual autenticado
    usuario_actual_id = 1  # Reemplazar con lógica de autenticación
    
    # Verificar que el curso exista
    curso = Course.query.get(data['course_id'])
    if not curso:
        return jsonify({"error": "Curso no encontrado"}), 404
    
    # Verificar que el estudiante no esté ya inscrito
    if curso.students.filter(UserSchema == usuario_actual_id).first():
        return jsonify({"error": "Ya estás inscrito en este curso"}), 400
    
    # Asociar estudiante al curso
    curso.students.append(usuario_actual_id)
    db.session.commit()
    
    return jsonify({"mensaje": "Inscripción exitosa"}), 201

@student_bp.route('/mis-cursos', methods=['GET'])
@student_required
def mis_cursos():
    # TODO: Obtener el usuario actual autenticado
    usuario_actual_id = 1  # Reemplazar con lógica de autenticación
    
    # Obtener cursos del estudiante
    cursos = Course.query.filter(Course.students.any(id=usuario_actual_id)).all()
    
    # Serializar los cursos
    course_schema = CourseSchema(many=True)
    return jsonify(course_schema.dump(cursos)), 200

@student_bp.route('/modulos-curso/<int:curso_id>', methods=['GET'])
@student_required
def modulos_curso(curso_id):
    # Verificar que el curso exista
    curso = Course.query.get(curso_id)
    if not curso:
        return jsonify({"error": "Curso no encontrado"}), 404
    
    # Obtener módulos del curso
    modulos = Module.query.filter_by(course_id=curso_id).all()
    
    # TODO: Obtener el usuario actual autenticado
    usuario_actual_id = 1  # Reemplazar con lógica de autenticación
    
    # Obtener progreso del estudiante
    modulos_con_progreso = []
    for modulo in modulos:
        progreso = UserProgress.query.filter_by(
            user_id=usuario_actual_id, 
            module_id=modulo.id
        ).first()
        
        modulo_data = ModuleSchema().dump(modulo)
        modulo_data['progreso'] = {
            'completado': progreso.completed if progreso else False,
            'porcentaje': progreso.progress_percentage if progreso else 0
        }
        
        modulos_con_progreso.append(modulo_data)
    
    return jsonify(modulos_con_progreso), 200

@student_bp.route('/actualizar-progreso', methods=['POST'])
@student_required
def actualizar_progreso():
    data = request.json
    
    # Validaciones básicas
    if not data or not data.get('module_id') or 'progress' not in data:
        return jsonify({"error": "Datos incompletos"}), 400
    
    # TODO: Obtener el usuario actual autenticado
    usuario_actual_id = 1  # Reemplazar con lógica de autenticación
    
    # Verificar que el módulo exista
    modulo = Module.query.get(data['module_id'])
    if not modulo:
        return jsonify({"error": "Módulo no encontrado"}), 404
    
    # Buscar o crear registro de progreso
    progreso = UserProgress.query.filter_by(
        user_id=usuario_actual_id, 
        module_id=data['module_id']
    ).first()
    
    if not progreso:
        progreso = UserProgress(
            user_id=usuario_actual_id,
            module_id=data['module_id']
        )
        db.session.add(progreso)
    
    # Actualizar progreso
    progreso.progress_percentage = data['progress']
    progreso.completed = data['progress'] >= 100
    
    db.session.commit()
    
    return jsonify({
        "mensaje": "Progreso actualizado exitosamente",
        "progreso": {
            "porcentaje": progreso.progress_percentage,
            "completado": progreso.completed
        }
    }), 200