from flask import Flask, render_template, redirect, request, session
from flask_socketio import SocketIO, send, emit
from decouple import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config('FLASK_SECRET_KEY')
socketio = SocketIO(app)

############################ HOME PAGE ################################

@app.route('/' , methods=["GET" ,"POST"])
def home():
    return render_template("tic-tac-toe.jinja")

########################## SOCKET CONNECTIONS #######################################################

# Create game rooms in a dictionary or add players joining to a game room.
# Rooms will look like the example below. User id of whom created the room will be a key in the dictionary. Second user will be saved with their own id in an array.
# Only two players (element) will be allowed in an array. If a room is inactive for 33 minutes, the key will be deleted from the dictionary. 

# Games = {'8ed9147bba0b44f5948d9a3109d12adf': ['george', 'neil-f415330c93034667925afc981ccaf02f'], 
#           '58141c3efc204af580cb8658113c1b4e': ['lily', 'Susan-23feef494b15455598a665ff1a5baa97'], 
#           '1a6c943d12484fd7973703288e54fd1c': ['Tom', 'Jane-f2f52a9996564e2b84f2e9f844933049']}

games = {}

@socketio.on("game_type")
def game_type(type):
    type = type.split("-")
    user_name = type[1]
    
    if type[0] == "new_game":
        game_id = request.sid
        games[game_id] = [user_name]
        emit('session_id' , game_id , room = game_id)
        
    else:
        game_id = type[0]
        for i in games:
            
            if game_id == i[-10:] and len(games[i]) == 2:
                user_id = request.sid
                emit('session_id' , "full" , room = user_id)
            
            elif game_id == i[-10:]:
                user_id = request.sid
                games[i].append(user_name+'-'+user_id)
                emit('session_id' , game_id , room = user_id)
                
            elif game_id != i[-10:]:
                user_id = request.sid
                emit('session_id' , "none" , room = user_id)
            

# Listenening for the play of 'X' and 'O' then broadcast it to the players in individual rooms

@socketio.on('message')
def receive_message_event(message):
    # Delete disconnected user from the games dictionary.
    if message == "disconnected":
        for i in games:
            if i == request.sid:
                del games[i]
    else:
        for i in games:
            if message == "restart" and (request.sid == i or request.sid == games[i][1].split("-")[1]):
                room_1 = i
                room_2 = games[i][1].split("-")[1]
                socketio.send("restart", room = room_1)
                socketio.send("restart", room = room_2)

            elif request.sid == i:
                room_1 = i
                room_2 = games[i][1].split("-")[1]
                user_name = games[i][0]
                #socketio.send(message, room = room_1)
                socketio.send(message, room = room_2)
                if(message == 'win'):
                    socketio.send(f"{user_name} <br> WINS!!!", room = room_1)
                    socketio.send(f"{user_name} <br> WINS!!!", room = room_2)
                
                elif(message == 'draw'):   
                    socketio.send('draw' , room = room_1)
                    socketio.send('draw' , room = room_2)
                
            elif request.sid == games[i][1].split("-")[1]:
                room_1 = i
                room_2 = games[i][1].split("-")[1]
                user_name = games[i][1].split("-")[0]
                socketio.send(message, room = room_1)
                #socketio.send(message, room = room_2)
                if(message == 'win'):
                    socketio.send(f"{user_name} <br> WINS!!!", room = room_1)
                    socketio.send(f"{user_name} <br> WINS!!!", room = room_2)
                    
                elif(message == 'draw'):  
                    socketio.send('draw' , room = room_1)
                    socketio.send('draw' , room = room_2)
    
# Listening for the chat message and broadcast it to all clients
@socketio.on('chat_message')
def send_chat_message(chat_message):
    for i in games:
        if request.sid == i: 
            user_1 = games[i][0]
            room_1 = i 
            room_2 = games[i][1].split("-")[1]
            socketio.emit('private_chat_message', f"{user_1}: {chat_message}" , room = room_1)
            socketio.emit('private_chat_message', f"{user_1}: {chat_message}" , room = room_2)
        elif request.sid == games[i][1].split("-")[1]:
            user_2 = games[i][1].split("-")[0]
            room_1 = i
            room_2 = games[i][1].split("-")[1]
            socketio.emit('private_chat_message', f"{user_2}: {chat_message}", room = room_1)
            socketio.emit('private_chat_message', f"{user_2}: {chat_message}", room = room_2)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')