from flask import jsonify, request
from app import app, db
from app.models import Hero, Power, HeroPower
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(hero_list)
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
        }
        return jsonify(hero_data)
    else:
        return jsonify({'error': 'Hero not found'}), 404
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_list)
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        return jsonify(power_data)
    else:
        return jsonify({'error': 'Power not found'}), 404
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()
    if 'description' in data:
        new_description = data['description']
        if len(new_description) >= 20:
            power.description = new_description
            db.session.commit()
            return jsonify({
                'id': power.id,
                'name': power.name,
                'description': power.description
            })
        else:
            return jsonify({'errors': ['Description must be at least 20 characters long']}), 400
    else:
        return jsonify({'errors': ['Invalid request']}), 400

# POST /hero_powers route
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    if 'strength' in data and 'power_id' in data and 'hero_id' in data:
        strength = data['strength']
        power_id = data['power_id']
        hero_id = data['hero_id']
        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if not hero or not power:
            return jsonify({'errors': ['Hero or Power not found']}), 400

        hero_power = HeroPower(strength=strength, hero=hero, power=power)
        db.session.add(hero_power)
        db.session.commit()

        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': p.id, 'name': p.name, 'description': p.description} for p in hero.powers]
        }
        return jsonify(hero_data), 201
    else:
        return jsonify({'errors': ['Invalid request']}), 400

# PATCH /heroes/:id route
@app.route('/heroes/<int:id>', methods=['PATCH'])
def update_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404

    data = request.get_json()
    if 'name' in data:
        hero.name = data['name']
    if 'super_name' in data:
        hero.super_name = data['super_name']
    db.session.commit()
    return jsonify({
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name
    })

# DELETE /heroes/:id route
@app.route('/heroes/<int:id>', methods=['DELETE'])
def delete_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404

    db.session.delete(hero)
    db.session.commit()
    return jsonify({'message': 'Hero deleted successfully'})
@app.route('/powers', methods=['POST'])
def create_power():
    data = request.get_json()
    if 'name' in data and 'description' in data:
        name = data['name']
        description = data['description']
        power = Power(name=name, description=description)
        db.session.add(power)
        db.session.commit()
        return jsonify({
            'id': power.id,
            'name': power.name,
            'description': power.description
        }), 201
    else:
        return jsonify({'errors': ['Invalid request']}), 400