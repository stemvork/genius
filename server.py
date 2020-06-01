import socket
from _thread import *

import json

from game import Game

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Allows the address to be reused, preventing block by TCP TIME_WAIT.
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server.bind(('', 5555))
except socket.error as e:
    print("BindException: ", e)

server.listen(2)
print("Waiting for a connection.")

# Games
games = {}
# Number of clients
client_count = 0

# Should correspond with Network class
packet_size = 2048
packet_count = 2


def threaded_client(new_conn, new_player_id, new_game_id):
    global client_count
    # Send the client a player_id
    new_conn.send(str.encode(str(new_player_id)))

    # Server/connection loop
    while True:
        try:
            # Receive new data
            data = new_conn.recv(packet_size * packet_count).decode()

            # If the game_id is valid
            if new_game_id in games:
                # Select the game with that id
                game = games[new_game_id]

                # Process request
                if not data:
                    break
                else:
                    # Restart the game
                    if data == "reset":
                        pass
                        # game.resetWent()

                    # If request is ACTIVE
                    elif data != "get":
                        game_dict = json.loads(data)
                        if type(game_dict) is list:
                            game.players[game_dict[0]] = game_dict[1]
                        else:
                            game.__dict__.update(game_dict)

                    # Always send new state to everyone
                    data_json = json.dumps(game.__dict__)
                    new_conn.sendall(str.encode(data_json))
            else:
                break
        except Exception as ex:
            print("exception", ex)

    # Impossible to send data
    print("Lost connection")
    try:
        del games[new_game_id]
        print("Closing Game", new_game_id)
    except Exception as ex:
        print("Closing exception", ex)

    # Closing the connection
    client_count -= 1
    new_conn.close()


# Server loop
while True:
    try:
        # Creating new connection
        conn, addr = server.accept()

        # New client has connected
        client_count += 1
        player_id = 0
        game_id = (client_count - 1) // 2
        if client_count % 2 == 1:
            # Create game object
            games[game_id] = Game(server=True, new_game_id=game_id)
            # print("First client to enter game id: ", game_id)
        else:
            # print("Second client connecting to game id: ", game_id)
            games[game_id].ready = True
            player_id = 1

        start_new_thread(threaded_client, (conn, player_id, game_id))
    except KeyboardInterrupt as e:
        break
