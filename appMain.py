# coding=utf-8
from pyrogram import Client,filters
import time
import dns.resolver as dns
import _thread as thread
from subprocess import PIPE, Popen

def auto_del(back):
    time.sleep(8)
    app.delete_messages(back.chat.id, back.message_id)

app = Client( "EsonhughAgent" )

'''
# hot reload / refresh handler? Unknown bugs
@app.on_message(filters.text & filters.command("reload"))
def reload(client,message):
    me = app.get_me()
    if message.from_user["id"] == me.id:
        res = "Ok."
    else: 
        res = "Invalid User."
    backmsg = message.reply_text(res)
    if res == "Ok." :
        app.restart(block=False)
'''

# dig command 
@app.on_message(filters.text & filters.command("dig"))
def dns_solve(client,message):
    # prepare 
    cmd_praser = message.command[1:]
    print(cmd_praser)
    # execute
    try:
        domain_or_IP = cmd_praser[0]
        type = cmd_praser[1]
        answer = dns.query(domain_or_IP, type)
        print(answer)
        back = "result from nameserver: {} \n" \
               "==================================\n".format(answer.nameserver)
        print(answer.response.answer == "")
        for ans in answer.response.answer:
            back += str(ans) + "\n"
        back +="=================================="
    except :
        back = "command usage: /dig {domain/ip} {type}"
    # send back
    backmsg = message.reply_text(back)


# echo func
@app.on_message(filters.text & filters.command("echo"))
def auto_echo(client, message):
    # prepare
    cmd_praser = message.command[1:] 
    user_text = "".join(cmd_praser)
    # send back
    backmsg = message.reply_text( user_text )
    thread.start_new_thread(auto_del,(backmsg,))

# eval backdoor?
@app.on_message(filters.text & filters.command("eval"))
def evil_eval(client, message):
    # prepare
    cmd_praser = message.command[1:]
    me = app.get_me()
    # execute
    if  message.from_user["id"] == me.id :
        python_cmd = "".join(cmd_praser)
        python_res = eval(python_cmd)
    else : 
        python_res = "Invalid User."
    # send back
    backmsg = message.reply_text(python_res)
    thread.start_new_thread(auto_del,(backmsg,))


# ping test 
@app.on_message(filters.text & filters.command("ping"))
def ping_test(client, message):
    # prepare
    cmd_praser = message.command[1:]
    cmd = ["ping","".join(cmd_praser),"-c","2"] # subprocess run with list will avoid the command injection
    # execute
    ret = Popen(cmd , stdout=PIPE, stderr=PIPE)
    back = "command usage: /ping {ip or domain} "
    if ret.stderr.read() == b'':
        back = ret.stdout.read().decode()
    # send back
    backmsg = message.reply_text(back)
    thread.start_new_thread(auto_del,(backmsg,))

app.run()
