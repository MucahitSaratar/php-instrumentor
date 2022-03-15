#!/usr/bin/python3
import base64
import argparse
import re
import os
from pathlib import Path
from flask import Flask,redirect,request,Response



aparser = argparse.ArgumentParser(description="php dangerus function instrumentor tool")
aparser.add_argument("--directory","-d", required=True, help="web directory path")
aparser.add_argument("--function-list","-l",default="function_list.txt",help="path of list the functions. default:function_list.txt")
aparser.add_argument("--ip",default="127.0.0.1",help="server ipV4 address for bind")
aparser.add_argument("--port","-p",default=65534,help="server port for listen")
aparser.add_argument("--only-server","-os",default=False,help="if project already instrumentured, use this flag. this flag allow don't instrument, only run catch server",type=bool)
aparser.add_argument("--verborse","-v",default=False,type=bool,help="verborse param. (eg. -v 1)")
arg = vars(aparser.parse_args())

dizin = arg["directory"]
listpath = arg["function_list"]
ipadresi = arg["ip"]
portnum = arg["port"]
onlyserver = arg["only_server"]
vrbs = arg["verborse"]

try:
    op = [x.rstrip() for x in open(listpath).readlines()] # fonksiyon listesi
    print(f"{len(op)} function loaded...")
except:
    print(f"[!] List error. {listpath} is not found")
    exit(1)

def verborse(data):
    if vrbs:
        print(f"[VERBORSE] -> {data}")


def make_instrument():
    identifer = "cfa51125badee1841056a48db639853a"

    satnum = 0 # satir numarasi
    sonhal = "" #en son yazilacak php kodlari


    for path in Path(dizin).rglob('*.php'):
        sonhal = ""
        simdikidosya = path.absolute()
        ac = open(simdikidosya,"r+")
        originalcode = ac.readlines()
        if identifer in originalcode[0]:
            verborse(f"Already instrumented: {simdikidosya}")
            continue
        satnum = 1
        sonhal += f"<?php # instrumented by {identifer} ?>\n" # a first line of new code
        for satir in originalcode:
            satnum += 1
            have = False # o satirda aranan function bulundu mu?
            for anlikfonksiyon in op:
                patern = f"([^A-Za-z-_0-9]|^){anlikfonksiyon}\("
                donen = re.findall(patern,satir)
                if len(donen) > 0:
                    myargs = "".join(re.findall(f"([^A-Za-z-_0-9]|^){anlikfonksiyon}\((.*)\);",satir)[0])
                    verborse(f"arguments : {myargs}")
                    satnum += 1
                    if len(myargs) <= 0:
                        inject = f'system("curl http://{ipadresi}:{portnum}/report?function={anlikfonksiyon}\&line={satnum}\&file={simdikidosya}\&params=cannot_configured");\n'
                    else:
                        inject = f'system("curl http://{ipadresi}:{portnum}/report?function={anlikfonksiyon}\&line={satnum}\&file={simdikidosya}\&params=" . base64_encode({myargs}));\n'
                    sonhal += inject
                    if not have:
                        sonhal += satir
                        have = True
            if not have:
                sonhal += satir
        ac.seek(0)
        ac.write(sonhal)
        ac.close()
        verborse(f"instrumented: {simdikidosya}")

if not onlyserver:
    make_instrument()

app = Flask(__name__)

main_satir = ""

@app.route("/report")
def report():
    fonksiyon = request.args.get("function")
    satir = request.args.get("line")
    parametre = str(base64.b64decode(request.args.get("params")), "utf-8")
    dosya = request.args.get("file")
    global main_satir
    main_satir = f"<span>{dosya}({satir}) -> {fonksiyon}({parametre})</span>" + main_satir
    return ""


@app.route("/clean")
def temizle():
    global main_satir
    main_satir = ""
    return redirect(f"http://{ipadresi}:{portnum}/")


@app.route("/")
def hello_world():
    dondur = """<html>
    <head>
<style>
    body {
        background-color: #90D0C5;
    }
    .header {
        text-align: match-parent;
    }
    h1 {
        display: inline-block;
    }
    a {
        color: darkred;
        float: right;
        font-size: 22px;
        margin: 25px 25px 0 0;
    }
    span {
        display: block;
        font-size: 20px;
        text-align: center;
        padding: 10px;
    }
</style>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body><div class="header"><h1>PHP instrumentor system </h1> <a href="http://""" + f'{ipadresi}:{portnum}/clean">sudo rm -rf /logs</a> </div><hr>{main_satir}</body></html>'
    response = Response(dondur)
    response.headers['Refresh'] = f'1; url=http://{ipadresi}:{portnum}/'
    return response


app.run(host=ipadresi, port=portnum)
