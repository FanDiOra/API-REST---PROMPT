from flask import Blueprint, jsonify, request
from app import db
from app.models import User, Group, Prompt, Vote, Note
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('api', __name__)

# ----------------------------- Gestion Utilisateur -----------------------------------
# Connexion (création du super admin)
@bp.route('/admin/register', methods=['POST'])
def create_user_without_auth():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(
        firstname=data['firstname'],
        lastname=data['lastname'],
        login=data['login'],
        password=hashed_password,
        role=data['role'],
        groupID=data.get('groupID')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Connexion
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(login=data['login']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.userID)
        return jsonify(access_token=access_token)
    return jsonify({'message': 'Invalid credentials'}), 401


# Créer un utilisateur
@bp.route('/admin/user', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(
        firstname=data['firstname'],
        lastname=data['lastname'],
        login=data['login'],
        password=hashed_password,
        role=data['role'],
        # groupID=data.get('groupID')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Lister les utilisateurs
@bp.route('/admin/users', methods=['GET'])
@jwt_required()
def list_users():
    users = User.query.all()
    return jsonify([{
        'userID': user.userID,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'login': user.login,
        'role': user.role,
        'groupID': user.groupID
    } for user in users])

# Modifier un utilisateur
@bp.route('/admin/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    user.firstname = data['firstname']
    user.lastname = data['lastname']
    user.login = data['login']
    if 'password' in data:
        user.password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    user.role = data['role']
    user.groupID = data.get('groupID')
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

# Supprimer un utilisateur
@bp.route('/admin/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

# ----------------------------- Gestion Groupe -----------------------------------
# Créer un groupe d'utilisateurs
@bp.route('/admin/group', methods=['POST'])
@jwt_required()
def create_group():
    data = request.get_json()
    new_group = Group(name=data['name'])
    db.session.add(new_group)
    db.session.commit()
    
    # Ajouter les utilisateurs au groupe
    if 'user_ids' in data:
        for user_id in data['user_ids']:
            user = User.query.get(user_id)
            if user:
                user.groupID = new_group.groupID
        db.session.commit()
    
    return jsonify({'message': 'Group created successfully'}), 201

# Lister les groupes d'utilisateurs
@bp.route('/admin/groups', methods=['GET'])
@jwt_required()
def list_groups():
    groups = Group.query.all()
    return jsonify([{
        'groupID': group.groupID,
        'name': group.name,
        'users': [{'userID': user.userID, 'firstname': user.firstname, 'lastname': user.lastname} for user in group.users]
    } for group in groups])

# Lister un groupe d'utilisateurs
@bp.route('/admin/group/<int:group_id>', methods=['GET'])
@jwt_required()
def get_group(group_id):
    group = Group.query.get_or_404(group_id)
    return jsonify({
        'groupID': group.groupID,
        'name': group.name,
        'users': [{'userID': user.userID, 'firstname': user.firstname, 'lastname': user.lastname} for user in group.users]
    })


# Modifier un groupe d'utilisateurs
@bp.route('/admin/group/<int:group_id>', methods=['PUT'])
@jwt_required()
def update_group(group_id):
    data = request.get_json()
    group = Group.query.get_or_404(group_id)
    group.name = data['name']
    
    # Mettre à jour les utilisateurs du groupe
    if 'user_ids' in data:
        for user in group.users:
            user.groupID = None  # Retirer tous les utilisateurs du groupe actuel
        db.session.commit()
        
        for user_id in data['user_ids']:
            user = User.query.get(user_id)
            if user:
                user.groupID = group.groupID
        db.session.commit()
    
    return jsonify({'message': 'Group updated successfully'})

# Supprimer un groupe d'utilisateurs
@bp.route('/admin/group/<int:group_id>', methods=['DELETE'])
@jwt_required()
def delete_group(group_id):
    group = Group.query.get_or_404(group_id)
    
    # Supprimer les relations avec les utilisateurs
    for user in group.users:
        user.groupID = None
    db.session.delete(group)
    db.session.commit()
    
    return jsonify({'message': 'Group deleted successfully'})

# ----------------------------- Gestion Prompts -----------------------------------
# Créer un prompt
@bp.route('/prompt', methods=['POST'])
@jwt_required()
def create_prompt():
    data = request.get_json()
    current_user = get_jwt_identity()
    new_prompt = Prompt(
        content=data['content'],
        status='en attente',  # Statut initial
        user_id=current_user
    )
    db.session.add(new_prompt)
    db.session.commit()
    return jsonify({'message': 'Prompt created successfully'}), 201

# Modifier un prompt
@bp.route('/prompt/<int:prompt_id>', methods=['PUT'])
@jwt_required()
def update_prompt(prompt_id):
    data = request.get_json()
    prompt = Prompt.query.get_or_404(prompt_id)
    prompt.content = data['content']
    prompt.status = data['status']
    prompt.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Prompt updated successfully'})

# Supprimer un prompt
@bp.route('/prompt/<int:prompt_id>', methods=['DELETE'])
@jwt_required()
def delete_prompt(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    db.session.delete(prompt)
    db.session.commit()
    return jsonify({'message': 'Prompt deleted successfully'})

# Lister les prompts
@bp.route('/prompts', methods=['GET'])
@jwt_required()
def list_prompts():
    prompts = Prompt.query.all()
    return jsonify([{
        'promptID': prompt.promptID,
        'content': prompt.content,
        'status': prompt.status,
        'price': prompt.price,
        'creation_date': prompt.creation_date,
        'edit_date': prompt.edit_date,
        'user_id': prompt.user_id
    } for prompt in prompts])

# Lister les prompts par utilisateur
@bp.route('/user/<int:user_id>/prompts', methods=['GET'])
@jwt_required()
def list_prompts_by_user(user_id):
    prompts = Prompt.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'promptID': prompt.promptID,
        'content': prompt.content,
        'status': prompt.status,
        'price': prompt.price,
        'creation_date': prompt.creation_date,
        'edit_date': prompt.edit_date,
        'user_id': prompt.user_id
    } for prompt in prompts])
