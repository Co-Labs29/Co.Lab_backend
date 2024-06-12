from flask import Blueprint, jsonify
from app.models import Notifications, Child, Goal, Chores

notifications = Blueprint('notifications', __name__)

@notifications.route('/notifications/<int:parent_id>', methods=['GET'])
def get_notifications(parent_id):
    
    children = Child.query.filter_by(parent_id=parent_id).all()

    
    notifications_list = []

  
    for child in children:
       
        completed_goals = Goal.query.filter_by(child_id=child.id, complete=True).all()
        completed_chores = Chores.query.filter_by(child_id=child.id, status='completed').all()

       
        for goal in completed_goals:
            notification = {
                'child_name': child.username,
                'type': 'goal',
                'name': goal.name
            }
            notifications_list.append(notification)
        for chore in completed_chores:
            notification = {
                'child_name': child.username,
                'type': 'chore',
                'name': chore.name
            }
            notifications_list.append(notification)

   
    return jsonify(notifications_list)

