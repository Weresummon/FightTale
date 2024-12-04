# monsters.py

from battle_controller import DummyMonster, GoblinMonster

def get_all_monsters():
    return [
        DummyMonster(name="Dummy", health=100),
        GoblinMonster(name="Goblin", health=80)
        # Вы можете добавить других монстров здесь
    ]
