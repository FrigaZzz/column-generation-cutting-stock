\* RMP *\
Minimize
OBJ: Init_Pat0 + Init_Pat1 + Init_Pat10 + Init_Pat11 + Init_Pat2 + Init_Pat3
 + Init_Pat4 + Init_Pat5 + Init_Pat6 + Init_Pat7 + Init_Pat8 + Init_Pat9
 + Pat12 + Pat13 + Pat14 + Pat15 + Pat16 + Pat17 + Pat18 + Pat19 + Pat20
 + Pat21 + Pat22
Subject To
C0: Init_Pat0 + Pat16 + Pat21 >= 17
C1: Init_Pat1 + Pat19 + Pat20 + Pat22 >= 89
C10: Init_Pat10 + 2 Pat12 + Pat13 + Pat17 + Pat19 >= 29
C11: Init_Pat11 >= 93
C2: Init_Pat2 + Pat12 + 3 Pat14 + Pat22 >= 12
C3: Init_Pat3 >= 43
C4: Init_Pat4 + 2 Pat15 + Pat21 >= 79
C5: Init_Pat5 + Pat17 + Pat18 >= 39
C6: Init_Pat6 >= 19
C7: Init_Pat7 >= 57
C8: Init_Pat8 >= 68
C9: Init_Pat9 + 2 Pat13 + Pat16 + Pat18 + Pat20 >= 64
Bounds
 0 <= Init_Pat0
 0 <= Init_Pat1
 0 <= Init_Pat10
 0 <= Init_Pat11
 0 <= Init_Pat2
 0 <= Init_Pat3
 0 <= Init_Pat4
 0 <= Init_Pat5
 0 <= Init_Pat6
 0 <= Init_Pat7
 0 <= Init_Pat8
 0 <= Init_Pat9
 0 <= Pat12
 0 <= Pat13
 0 <= Pat14
 0 <= Pat15
 0 <= Pat16
 0 <= Pat17
 0 <= Pat18
 0 <= Pat19
 0 <= Pat20
 0 <= Pat21
 0 <= Pat22
Generals
Init_Pat0
Init_Pat1
Init_Pat10
Init_Pat11
Init_Pat2
Init_Pat3
Init_Pat4
Init_Pat5
Init_Pat6
Init_Pat7
Init_Pat8
Init_Pat9
Pat12
Pat13
Pat14
Pat15
Pat16
Pat17
Pat18
Pat19
Pat20
Pat21
Pat22
End
