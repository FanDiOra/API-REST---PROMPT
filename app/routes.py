from flask import Blueprint, jsonify, request
from app import db
from app.models import User, Group, Prompt, Vote, Note
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint('api', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(
        firstname=data['firstname'],
        lastname=data['lastname'],
        login=data['login'],
        password=data['password'],  # Password should be hashed
        role=data['role'],
        group=data['groupe']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(login=data['login']).first()
    if user and user.password == data['password']:  # Password should be verified with hashing
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify({'message': 'Invalid credentials'}), 401

@bp.route('/prompts', methods=['GET'])
def get_prompts():
    prompts = Prompt.query.all()
    return jsonify([prompt.to_dict() for prompt in prompts])

@bp.route('/prompts', methods=['POST'])
@jwt_required()
def create_prompt():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_prompt = Prompt(
        content=data['content'],
        status='en attente',
        user_id=current_user
    )
    db.session.add(new_prompt)
    db.session.commit()
    return jsonify({'message': 'Prompt created successfully'}), 201