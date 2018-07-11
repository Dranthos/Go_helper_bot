#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
import sqlite3
from random import shuffle

archivo = 'db.sqlite'
tabla = 'Users'

#Comprueba que un nombre de usuario ya existe, ya que en POGO los nombres son unicos
def CheckUser(nombre):

    archivo = 'db.sqlite'

    conn = sqlite3.connect(archivo)

    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS 'Users' ( `name` TEXT NOT NULL, `telegram_id` INTEGER NOT NULL, `team` TEXT NOT NULL, `code` TEXT NOT NULL, `verified` INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(`name`,`telegram_id`) )")

    c.execute("SELECT * FROM users WHERE name='%s'" % (nombre))
    existe = c.fetchone()

    if existe:
        return True
    else:
        return False
    conn.close()

#Comprueba si la ID de Telegram ya esta registrada en la bbdd, para evitar multiples cuentas de un mismo usuario
def CheckUserId(numero):
    archivo = 'db.sqlite'

    conn = sqlite3.connect(archivo)

    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS 'Users' ( `name` TEXT NOT NULL, `telegram_id` INTEGER NOT NULL, `team` TEXT NOT NULL, `code` TEXT NOT NULL, `verified` INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(`name`,`telegram_id`) )")

    c.execute("SELECT * FROM users WHERE telegram_id=%s" % (numero))
    existe = c.fetchone()

    if existe:
        return existe
    else:
        return False
    conn.close()

def AddUser(nombre, equipo, id, codigo):

    archivo = 'db.sqlite'

    conn = sqlite3.connect(archivo)
    c = conn.cursor()

    c.execute("INSERT INTO Users (name, telegram_id, team, code, verified) VALUES ('%s',%s,'%s','%s',1)" % (nombre, id, equipo, codigo))

    conn.commit()
    conn.close()

def GrabCodes(numero, equipo, id):

    archivo = 'db.sqlite'

    conn = sqlite3.connect(archivo)
    c = conn.cursor()

    if equipo == 0:
        c.execute("SELECT name, code, team FROM users WHERE telegram_id!=%s" % (id))
    else:
        c.execute("SELECT name, code, team FROM users WHERE team='%s' AND telegram_id!=%s " % (equipo, id))
    lista = c.fetchall()
    shuffle(lista)

    return lista[:int(numero)]