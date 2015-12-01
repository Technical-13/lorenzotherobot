from src.lib.queries.connection import *
import time

"""
schema:
CREATE TABLE custom_commands(
   channel VARCHAR(20) NOT NULL,
   command VARCHAR(20) NOT NULL,
   creator VARCHAR(20) NOT NULL,
   user_level VARCHAR(10) NOT NULL,
   time datetime DEFAULT NULL,
   response VARCHAR(200) NOT NULL,
   times_used INT NOT NULL default 0,
   PRIMARY KEY ( command )
);
"""


def get_custom_commands():  # only gets donation_points
    con = get_connection()
    with con:
        cur = con.cursor()
        cur.execute("""SELECT channel, command, creator, user_level,
            time, response, custom_use FROM custom_commands""")
        commands = cur.fetchall()
        return commands


def get_custom_command(command):
    con = get_connection()
    with con:
        cur = con.cursor()
        cur.execute("""SELECT channel, command FROM custom_commands
            WHERE command = %s AND channel = %s""", [
                command, globals.global_channel])
        commands = cur.fetchall()
        return commands


def save_command(command, creator, user_level, response):
    con = get_connection()
    command_fetch = get_custom_command(command)
    if len(command_fetch) > 0:
        # print get_custom_command(command)[0], get_custom_command(command)[1]
        if command_fetch[0][0] == globals.global_channel and command_fetch[0][1] == command:
            return "{0} already exists in {1}'s channel!".format(
                command, globals.global_channel)
    else:
        with con:
            cur = con.cursor()
            cur.execute(
                """INSERT INTO custom_commands (
                    channel, command, creator, user_level, time, response, times_used
                    ) VALUES (%s, %s, %s, %s, %s, %s, 0)""", [
                        globals.global_channel, command, creator, user_level,
                        str(datetime.datetime.now()), response])
            return "{0} successfully added".format(command)


def delete_command(command):
    con = get_connection()
    command_fetch = get_custom_command(command)
    if len(command_fetch) > 0:
        if command_fetch[0][0] != globals.global_channel and command_fetch[0][1] != command:
            return "{0} not found as a command in {1}'s channel!".format(
                command, globals.global_channel)
        else:
            with con:
                cur = con.cursor()
                cur.execute(
                    """DELETE FROM custom_commands
                        WHERE command = %s and channel = %s""", [
                            command, globals.global_channel])
                return "{0} successfully removed".format(command)
    else:
        return "{0} not found as a command in {1}'s channel!".format(
            command, globals.global_channel)
