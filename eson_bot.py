#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in imports
from subprocess import PIPE, Popen
import contextlib
import threading
import time

# third-party imports
from pyrogram import Client, filters
import dns.resolver


# initialize pyrogram client
app = Client("EsonhughAgent")


def auto_delete(message):
    time.sleep(8)
    app.delete_messages(message.chat.id, message.message_id)


# hot reload / refresh handler? Unknown bugs
@app.on_message(filters.text & filters.command("reload"))
def reload(client, message):
    if message.from_user["id"] == app.get_me().id:
        message.reply_text("Ok.")
        app.restart(block=False)
    else:
        message.reply_text("Invalid User.")


# dig command
@app.on_message(filters.text & filters.command("dig"))
def dns_solve(client, message):

    try:
        hostname = message.command[1]
        record_type = message.command[2]

        answer = dns.resolver.query(hostname, record_type)
        response = ["Lookup results from {}".format(answer.nameserver)]

        for answer in answer.response.answer:
            response.append(answer.to_text())

    # more dns.resolver errors can be caught here
    except dns.resolver.NXDOMAIN:
        response = ["NXDOMAIN"]

    # this also includes IndexError
    except Exception:
        response = ["command usage: /dig {hostname} {record_type}"]

    # converge list into a single string
    response = "\n".join(response)
    message.reply_text(response)


@app.on_message(filters.text & filters.command("echo"))
def auto_echo(client, message):
    reply = message.reply_text("".join(message.command[1:]))
    threading.Thread(target=auto_delete, args=(reply,)).start()


@app.on_message(filters.text & filters.command("eval"))
def eval(client, message):

    # if the command came from the current user the bot
    # is running as
    if message.from_user["id"] == app.get_me().id:
        result = eval("".join(message.command[1:]))

    # unauthorized third-party
    else:
        result = "Invalid User."

    reply = message.reply_text(result)
    threading.Thread(target=auto_delete, args=(reply,)).start()


@app.on_message(filters.text & filters.command("ping"))
def ping_test(client, message):
    response = "command usage: /ping {hostname} "

    with contextlib.suppress(IndexError):
        command = [
            "/usr/bin/ping",
            message.command[1],
            "-c",
            "2",
        ]

        process = Popen(command, stdout=PIPE, stderr=PIPE)
        response = process.stdout.read().decode()

    reply = message.reply_text(response)
    threading.Thread(target=auto_delete, args=(reply,)).start()


if __name__ == "__main__":
    app.run()
