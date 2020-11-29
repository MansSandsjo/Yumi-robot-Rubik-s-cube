#!/usr/bin/env python3
# -*- coding: utf-8 -*-
/*
main class
*/
from sys import exit as Die
try:
    import solver as sv
    import video as webcam
    from combiner import combine
except ImportError as err:
    Die(err)


class Qbr:

    def __init__(self):
        pass

    def run(self):
        state         = webcam.scan()
        if not state:
            print('\033[0;33m[QBR SCAN ERROR] Op1s, you did not scan in all 6 sides.')
            print('Please try again.\033[0m')
            Die(1)

        unsolvedState = combine.sides(state)
        
        try:
            a = sv.solve(unsolvedState)
            x = list(a.split(" "))
            print (x)
            del x[-1]
            return x
        except Exception as err:
            print('\033[0;33m[QBR SOLVE ERROR] Ops, you did not scan in all 6 sides correctly.')
            print('Please try again.\033[0m')
            Die(1)

        Die(0)

if __name__ == '__main__':
    a = Qbr().run()

