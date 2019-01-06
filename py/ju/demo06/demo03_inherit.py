#coding=utf-8
class Parent:
    a = '父亲的a'
    b = '母亲的b'
class Sun(Parent):
    a = '儿子的a'

sun = Sun()
print(sun.a)
print(sun.b)