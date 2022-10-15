from app import *
class user:
    def __init__(self, id, name, quest, color):
        self.id = id
        self.name = name
        self.quest = quest
        self.color = color

p1 = user("123","Loretta", "to be a woman", "")

choices = ["{{ url_for('bridge') }}", "{{ url_for('bridgeroobin') }}"]
bridge = choice(choices)
    
