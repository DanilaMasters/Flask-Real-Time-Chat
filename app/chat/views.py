from flask_socketio import join_room, leave_room, send
from chat import app, socketio
from flask import redirect, render_template, request, session, url_for
import uuid

rooms = {}

@app.route('/', methods=['GET', 'POST'])
def home():
    session.clear()
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        create = request.form.get('create', False)
        join = request.form.get('join', False)

        if not name:
            return render_template('home.html', error='No name provided', code=code, name=name, rooms=rooms) 
        if join and not code:
            return render_template('home.html', error='No code provided', code=code, name=name, rooms=rooms)
        
        room = code
        if create != False:
            room = uuid.uuid4().hex[:6].upper()
            rooms[room] = {'members': 0, "messages": []}
        elif code not in rooms:
            return render_template('home.html', error='Room does not exist', code=code, name=name, rooms=rooms)
        
        session['room'] = room
        session['name'] = name
        return redirect(url_for('chat'))

    return render_template('home.html', rooms=rooms)


@app.route('/chat')
def chat():
    room = session.get('room')
    if room is None or session.get('name') is None or room not in rooms:
        return redirect(url_for('home'))
    return render_template('room.html', code=session.get('room'))


@socketio.on('connect')
def connect(auth):
    room = session.get('room')
    name = session.get('name')
    
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send(message={'name':name, 'message':'has entered the room'}, to=room)
    rooms[room]['members'] += 1


@socketio.on('disconnect')
def disconnect():
    room = session.get('room')
    name = session.get('name')

    if room in rooms:
        rooms[room]['members'] -= 1
        if rooms[room]['members'] == 0:
            del rooms[room]

    send(message={'name': name, 'message': 'has left the room'}, to=room)