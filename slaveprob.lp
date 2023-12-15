\* Slave_solver *\
Minimize
OBJ: - 0.5 S0 - S1 - S11 - S3 - 0.5 S4 - S5 - S6 - S7 - S8
Subject To
_C1: 13 S0 + 16 S1 + 7 S10 + 21 S11 + 8 S2 + 18 S3 + 11 S4 + 15 S5 + 19 S6
 + 17 S7 + 22 S8 + 9 S9 <= 25
Bounds
 0 <= S0
 0 <= S1
 0 <= S10
 0 <= S11
 0 <= S2
 0 <= S3
 0 <= S4
 0 <= S5
 0 <= S6
 0 <= S7
 0 <= S8
 0 <= S9
Generals
S0
S1
S10
S11
S2
S3
S4
S5
S6
S7
S8
S9
End
