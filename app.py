from data import write_data
from flask import Flask, render_template, redirect, request, session
from flask_socketio import SocketIO, send, emit
from models.database import create_room, add_second_player, delete_game, fetch_all_room_id, fetch_player1, fetch_player2
from decouple import config
from datetime import date, datetime
from time import sleep

app = Flask(__name__)
app.config['SECRET_KEY'] = config('FLASK_SECRET_KEY')
socketio = SocketIO(app)

now = datetime.now()
created_on = now.strftime("%Y-%m-%d %H:%M:%S")

############################ HOME PAGE ################################
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/multiplayer-tic-tac-toe' , methods=["GET" ,"POST"])
def tic_tac_toe():
    return render_template("tic-tac-toe.jinja")

########################## SOCKET CONNECTIONS #######################################################

# Create game rooms in a dictionary or add players joining to a game room.
# Rooms will look like the example below. User id of whom created the room will be a key in the dictionary. Second user will be saved with their own id in an array.
# Only two players (element) will be allowed in an array. If a room is inactive for 33 minutes, the key will be deleted from the dictionary. 

# Games = {'8ed9147bba0b44f5948d9a3109d12adf': ['george', 'neil-f415330c93034667925afc981ccaf02f'], 
#           '58141c3efc204af580cb8658113c1b4e': ['lily', 'Susan-23feef494b15455598a665ff1a5baa97'], 
#           '1a6c943d12484fd7973703288e54fd1c': ['Tom', 'Jane-f2f52a9996564e2b84f2e9f844933049']}games = {}

@socketio.on("game_type")
def game_type(type):
    type = type.split("-")
    user_name = type[1]
    if type[0] == "new_game":
        game_id = request.sid
        create_room(game_id, user_name, created_on)
        emit('session_id' , game_id , room = game_id)
    else:
        game_id = type[0]
        user_id = request.sid
        all_rooms = fetch_all_room_id()
        for rooms in all_rooms:
            if rooms[0][-10:] == game_id and fetch_player2(rooms)[0][0] != None:
                emit('session_id' , "full" , room = user_id)

            elif rooms[0][-10:] == game_id:
                player2 = user_id +" "+ type[1]
                add_second_player(rooms[0], player2)
                emit('session_id' , game_id , room = user_id)
                
            elif game_id != rooms[0][-10:]:
                emit('session_id' , "none" , room = user_id)
    
# Listenening for the play of 'X' and 'O' then broadcast it to the players in individual rooms

@socketio.on('message')
def receive_message_event(message):
    print(message)
    all_rooms = fetch_all_room_id()
    # Delete disconnected user from the games dictionary.
    if message == "disconnected":
        for rooms in all_rooms:
            if rooms[0] == request.sid:
                delete_game(rooms[0])
        print(message)
    else:
        for rooms in all_rooms:
            # if message == "restart" and request.sid == rooms[0] or (fetch_player2(rooms[0])[0][0].split(" "))[0]:
            #     room_1 = rooms[0]
            #     room_2 = (fetch_player2(rooms[0])[0][0].split(" "))[0]
            #     socketio.send("restart", room = room_1)
            #     socketio.send("restart", room = room_2)

            if request.sid == rooms[0]:
                print(message + "received")
                room_1 = rooms[0]
                room_2 = (fetch_player2(rooms[0])[0][0].split(" "))[0]
                user_name = fetch_player1(rooms[0])[0][0]
                print(user_name)
                socketio.send(message, room = room_2)
                sleep(0.1)
                socketio.send(message, room = room_2)
                sleep(0.1)
                socketio.send(message, room = room_2)
                sleep(0.1)
                socketio.send(message, room = room_2)
                sleep(0.1)
                socketio.send(message, room = room_2)
                sleep(0.1)
                socketio.send(message, room = room_2)
                sleep(0.1)
                socketio.send(message, room = room_2)
                sleep(0.1)
                socketio.send(message, room = room_2)
                sleep(0.1)
                socketio.send(message, room = room_2)
                if(message == 'win'):
                    socketio.send(f"{user_name} <br> WINS!!!", room = room_1)
                    socketio.send(f"{user_name} <br> WINS!!!", room = room_2)
                    sleep(0.1)
                    socketio.send(f"{user_name} <br> WINS!!!", room = room_1)
                    socketio.send(f"{user_name} <br> WINS!!!", room = room_2)
                elif(message == 'draw'):   
                    socketio.send('draw' , room = room_1)
                    socketio.send('draw' , room = room_2)
                    sleep(0.1)
                    socketio.send('draw' , room = room_1)
                    socketio.send('draw' , room = room_2)
            # (fetch_player2(rooms[0])[0][0].split(" "))[0] => Id of Player_2
            elif fetch_player2(rooms)[0][0] != None and request.sid == (fetch_player2(rooms[0])[0][0].split(" "))[0]:
                room_1 = rooms[0]
                room_2 = (fetch_player2(rooms[0])[0][0].split(" "))[0]
                user_name = (fetch_player2(rooms[0])[0][0].split(" "))[1]
                print(user_name)
                socketio.send(message, room = room_1)
                sleep(0.1)
                socketio.send(message, room = room_1)
                sleep(0.1)
                socketio.send(message, room = room_1)
                sleep(0.1)
                socketio.send(message, room = room_1)
                sleep(0.1)
                socketio.send(message, room = room_1)
                sleep(0.1)
                socketio.send(message, room = room_1)
                sleep(0.1)
                socketio.send(message, room = room_1)
                sleep(0.1)
                socketio.send(message, room = room_1)
                sleep(0.1)
                socketio.send(message, room = room_1)
                if(message == 'win'):
                    socketio.send(f"{user_name} <br> WINS!!!", room = room_1)
                    socketio.send(f"{user_name} <br> WINS!!!", room = room_2)
                    sleep(0.1)
                    socketio.send(f"{user_name} <br> WINS!!!", room = room_1)
                    socketio.send(f"{user_name} <br> WINS!!!", room = room_2)
                elif(message == 'draw'):  
                    socketio.send('draw' , room = room_1)
                    socketio.send('draw' , room = room_2)
                    sleep(0.1)
                    socketio.send('draw' , room = room_1)
                    socketio.send('draw' , room = room_2)
# Listening for the chat message and broadcast it to all clients
@socketio.on('chat_message')
def send_chat_message(chat_message):
    all_rooms = fetch_all_room_id()
    for rooms in all_rooms:
        if request.sid == rooms[0]: 
            room_1 = rooms[0]
            room_2 = (fetch_player2(rooms[0])[0][0].split(" "))[0]
            user_1 = fetch_player1(rooms[0])[0][0]
            socketio.emit('private_chat_message', f"{user_1}: {chat_message}" , room = room_1)
            socketio.emit('private_chat_message', f"{user_1}: {chat_message}" , room = room_2)
        elif fetch_player2(rooms)[0][0] != None and request.sid == (fetch_player2(rooms[0])[0][0].split(" "))[0]:
            room_1 = rooms[0]
            room_2 = (fetch_player2(rooms[0])[0][0].split(" "))[0]
            user_2 = (fetch_player2(rooms[0])[0][0].split(" "))[1]
            socketio.emit('private_chat_message', f"{user_2}: {chat_message}", room = room_1)
            socketio.emit('private_chat_message', f"{user_2}: {chat_message}", room = room_2)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9000)