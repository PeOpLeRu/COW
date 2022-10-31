from ilib.interpreter import *

filename = input("Enter namefile for cow: ")

inter = Interpreter()
inter.exec(filename)

print("\n----------- Interpretator finish!-----------")