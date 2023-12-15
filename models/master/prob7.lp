\* RMP *\
Minimize
OBJ: Init_Pat0 + Init_Pat1 + Init_Pat10 + Init_Pat11 + Init_Pat2 + Init_Pat3
 + Init_Pat4 + Init_Pat5 + Init_Pat6 + Init_Pat7 + Init_Pat8 + Init_Pat9
 + Pat12 + Pat13 + Pat14 + Pat15 + Pat16 + Pat17 + Pat18
Subject To
C0: Init_Pat0 + Pat16 >= 17
C1: Init_Pat1 >= 89
C10: Init_Pat10 + 2 Pat12 + Pat13 + Pat17 >= 29
C11: Init_Pat11 >= 93
C2: Init_Pat2 + Pat12 + 3 Pat14 >= 12
C3: Init_Pat3 >= 43
C4: Init_Pat4 + 2 Pat15 >= 79
C5: Init_Pat5 + Pat17 + Pat18 >= 39
C6: Init_Pat6 >= 19
C7: Init_Pat7 >= 57
C8: Init_Pat8 >= 68
C9: Init_Pat9 + 2 Pat13 + Pat16 + Pat18 >= 64
End
