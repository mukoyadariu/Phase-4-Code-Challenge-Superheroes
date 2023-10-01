from app import db
from app.models import Hero, Power, HeroPower
import random

def seed_powers():
    with app.app_context():
        powers = [
            {"name": "super strength", "description": "gives the wielder super-human strengths"},
            {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
            {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
            {"name": "elasticity", "description": "can stretch the human body to extreme lengths"},
        ]

        for power_data in powers:
            power = Power(**power_data)
            db.session.add(power)
    
        db.session.commit()

def seed_heroes():
    with app.app_context():
        heroes = [
            {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
            {"name": "Doreen Green", "super_name": "Squirrel Girl"},
            {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
            {"name": "Janet Van Dyne", "super_name": "The Wasp"},
            {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
            {"name": "Carol Danvers", "super_name": "Captain Marvel"},
            {"name": "Jean Grey", "super_name": "Dark Phoenix"},
            {"name": "Ororo Munroe", "super_name": "Storm"},
            {"name": "Kitty Pryde", "super_name": "Shadowcat"},
            {"name": "Elektra Natchios", "super_name": "Elektra"},
        ]

        for hero_data in heroes:
            hero = Hero(**hero_data)
            db.session.add(hero)
    
        db.session.commit()

def seed_hero_powers():
    with app.app_context():
        strengths = ["Strong", "Weak", "Average"]

        heroes = Hero.query.all()
        powers = Power.query.all()

        for hero in heroes:
            for _ in range(random.randint(1, 3)):
                power = random.choice(powers)
                strength = random.choice(strengths)

                hero_power = HeroPower(hero=hero, power=power, strength=strength)
                db.session.add(hero_power)
    
        db.session.commit()

def main():
    print("🦸‍♀️ Seeding powers...")
    seed_powers()
    print("🦸‍♀️ Seeding heroes...")
    seed_heroes()
    print("🦸‍♀️ Adding powers to heroes...")
    seed_hero_powers()
    print("🦸‍♀️ Done seeding!")

if __name__ == '__main__':
    from app import app
    with app.app_context():
        main()
