"""Unidad 3: notación postfija con pilas.

Infija:  (1500 + 2500) * 90 / 100     (la que escribimos todos)
Postfija: 1500 2500 + 90 * 100 /      (sin paréntesis: el orden ya dice qué se hace primero)

infija_a_postfija usa una pila de operadores; evaluar_postfija usa una pila de números."""
import re

from estructuras.pila import PilaDinamica

PRECEDENCIA = {"+": 1, "-": 1, "*": 2, "/": 2}


def tokenizar(texto):
    tokens = re.findall(r"\d+\.?\d*|[()+\-*/]", texto)
    if "".join(tokens) != re.sub(r"\s+", "", texto):
        raise ValueError("La cuenta tiene caracteres que no entiendo. Usá números y + - * / ( )")
    return tokens


def infija_a_postfija(texto):
    salida = []
    operadores = PilaDinamica()
    for t in tokenizar(texto):
        if t in PRECEDENCIA:
            while (not operadores.esta_vacia() and operadores.ver_tope() in PRECEDENCIA
                   and PRECEDENCIA[operadores.ver_tope()] >= PRECEDENCIA[t]):
                salida.append(operadores.desapilar())
            operadores.apilar(t)
        elif t == "(":
            operadores.apilar(t)
        elif t == ")":
            while not operadores.esta_vacia() and operadores.ver_tope() != "(":
                salida.append(operadores.desapilar())
            if operadores.esta_vacia():
                raise ValueError("Hay un paréntesis ')' sin su '('")
            operadores.desapilar()
        else:
            salida.append(t)
    while not operadores.esta_vacia():
        op = operadores.desapilar()
        if op == "(":
            raise ValueError("Hay un paréntesis '(' sin cerrar")
        salida.append(op)
    return salida


def evaluar_postfija(tokens):
    numeros = PilaDinamica()
    for t in tokens:
        if t in PRECEDENCIA:
            if len(numeros) < 2:
                raise ValueError("La cuenta está incompleta")
            b = numeros.desapilar()
            a = numeros.desapilar()
            if t == "+":
                numeros.apilar(a + b)
            elif t == "-":
                numeros.apilar(a - b)
            elif t == "*":
                numeros.apilar(a * b)
            else:
                if b == 0:
                    raise ValueError("No se puede dividir por cero")
                numeros.apilar(a / b)
        else:
            numeros.apilar(float(t))
    if len(numeros) != 1:
        raise ValueError("La cuenta está incompleta")
    return numeros.desapilar()


def calcular(texto):
    return evaluar_postfija(infija_a_postfija(texto))
