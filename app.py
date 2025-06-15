from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from faker import Faker
import random

# Инициализация приложения и базы данных
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hr.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
fake = Faker('ru_RU')  # Инициализация Faker здесь

# Модели
class Position(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False)

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    
    position = db.relationship('Position', backref='employees')
    manager = db.relationship('Employee', remote_side=[id], backref='subordinates')

def seed_database():
    """Функция для заполнения базы данных тестовыми данными"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Создаем должности
        positions = [
            Position(title='Генеральный директор', level=1),
            Position(title='Директор департамента', level=2),
            Position(title='Руководитель отдела', level=3),
            Position(title='Менеджер', level=4),
            Position(title='Специалист', level=5)
        ]
        db.session.add_all(positions)
        db.session.commit()
        
        # Создаем сотрудников
        employees = []
        ceo = Employee(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            position_id=1,
            hire_date=datetime.now(),
            salary=300000,
            manager_id=None
        )
        employees.append(ceo)

        for _ in range(100):
            level = random.choices([2,3,4,5], weights=[0.1,0.2,0.3,0.4])[0]
            
            possible_managers = [
                e.id for e in employees 
                if e.position and e.position.level < level
            ]
            
            emp = Employee(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                position_id=level,
                hire_date=fake.date_between(start_date='-5y'),
                salary=random.randint(30000, 200000),
                manager_id=random.choice(possible_managers) if possible_managers else None
            )
            employees.append(emp)
        
        db.session.add_all(employees)
        db.session.commit()
        print("Database seeded with test data")

# API Endpoints
@app.route('/api/employees', methods=['GET'])
def get_employees():
    try:
        query = Employee.query.join(Position)
        
        # Поиск
        if search := request.args.get('search'):
            query = query.filter(db.or_(
                Employee.first_name.ilike(f'%{search}%'),
                Employee.last_name.ilike(f'%{search}%')
            ))
        
        # Сортировка
        sort_field = request.args.get('sort', 'id')
        if hasattr(Employee, sort_field):
            order = request.args.get('order', 'asc')
            query = query.order_by(getattr(Employee, sort_field).desc() if order == 'desc' else getattr(Employee, sort_field).asc())
        
        employees = query.all()
        
        return jsonify([{
            'id': e.id,
            'first_name': e.first_name,
            'last_name': e.last_name,
            'position': e.position.title,
            'hire_date': e.hire_date.strftime('%Y-%m-%d'),
            'salary': e.salary,
            'manager': f"{e.manager.first_name} {e.manager.last_name}" if e.manager else None
        } for e in employees])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees/<int:id>/manager', methods=['PUT'])
def update_manager(id):
    try:
        data = request.get_json()
        if not data or 'manager_id' not in data:
            return jsonify({'error': 'Manager ID required'}), 400
            
        employee = Employee.query.get_or_404(id)
        if data['manager_id'] == employee.id:
            return jsonify({'error': 'Employee cannot be their own manager'}), 400
            
        if data['manager_id']:
            manager = Employee.query.get_or_404(data['manager_id'])
        employee.manager_id = data['manager_id']
        db.session.commit()
        
        return jsonify({'message': 'Manager updated successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    seed_database()
    app.run(host='0.0.0.0', port=5000, debug=True)

