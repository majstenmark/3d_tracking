MODULE MainModule
    
    PERS bool running;
    PERS BOOL SQUARE := TRUE;
    PERS wobjdata campos:= [FALSE,TRUE,"",[[500,-100,500],[0,-0.707106781,0.707106781,0]],[[0,0,0],[1,0,0,0]]];
    
    PROC main()
        IF square = TRUE THEN
            square_motion;
        ELSE
            surg_path;
        endif
    ENDPROC
    
    PROC square_motion()
        VAR NUM time;
        VAR robtarget calib1 := [[0, 0, 220], [0, 0.70710678, -0.70710678, 0], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
        VAR clock clock2;
        VAR robtarget calib2 := [[100, 0, 220], [0, 0.70710678, -0.70710678, 0], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
        VAR robtarget calib3 := [[100, 100, 220], [0, 0.70710678, -0.70710678, 0], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
        VAR robtarget calib4 := [[0, 100, 220],[0, 0.70710678, -0.70710678, 0], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
        VAR speeddata speed := v50;
        ConfL\Off;
        SingArea\Wrist;
        !Calibration for the camera
        MoveAbsJ [[-92.4278,-44.3477,23.0081,-55.6876,60.7508,-103.887],[105.882,9E+9,9E+9,9E+9,9E+9,9E+9]]\NoEOffs, v1000, z50, tDie\WObj:=campos;
        Stop;
        FOR i FROM 1 TO 10 do
            MoveL calib1, speed, fine, tDie\WObj:=campos;
            MoveL calib2, speed, fine, tDie\WObj:=campos;
            MoveL calib3, speed, fine, tDie\WObj:=campos;
            MoveL calib4, speed, fine, tDie\WObj:=campos;
        endfor
        MoveAbsJ [[-92.4278,-44.3477,23.0081,-55.6876,60.7508,-103.887],[105.882,9E+9,9E+9,9E+9,9E+9,9E+9]]\NoEOffs, v1000, z50, tDie\WObj:=campos;
        !Stop;
    ENDPROC
    
    PROC surg_path()
        
        VAR NUM time;
        VAR robtarget calib1 := [[0, 0, 220], [0, 0.70710678, -0.70710678, 0], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
        VAR clock clock2;
        VAR robtarget calib2 := [[100, 0, 220], [0, 0.70710678, -0.70710678, 0], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
        VAR robtarget calib3 := [[100, 100, 220], [0, 0.70710678, -0.70710678, 0], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
        VAR robtarget calib4 := [[0, 100, 220],[0, 0.70710678, -0.70710678, 0], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
        
        ConfL\Off;
        SingArea\Wrist;
        !Calibration for the camera
        MoveAbsJ [[-92.4278,-44.3477,23.0081,-55.6876,60.7508,-103.887],[105.882,9E+9,9E+9,9E+9,9E+9,9E+9]]\NoEOffs, v1000, z50, tDie\WObj:=campos;
        MoveL calib1, v100, fine, tDie\WObj:=campos;
        !Stop;
        MoveL calib2, v100, fine, tDie\WObj:=campos;
        !Stop;
        MoveL calib3, v100, fine, tDie\WObj:=campos;
        !Stop;
        MoveL calib4, v100, fine, tDie\WObj:=campos;
        !Stop;
        MoveAbsJ [[-92.4278,-44.3477,23.0081,-55.6876,60.7508,-103.887],[105.882,9E+9,9E+9,9E+9,9E+9,9E+9]]\NoEOffs, v1000, z50, tDie\WObj:=campos;
        !Stop;
        running := TRUE;
        ClkReset clock2;
        ClkStart clock2;
        !surgical_path;
        short;
        !track_path;
        running := FALSE;
        Clkstop clock2;
        time := ClkRead(clock2);
        ErrWrite\I, "Time = " + NumToStr(time, 3), "";
    ENDPROC
    
    PROC short()
    VAR robtarget t0 := [[-8.921, 74.854, 217.136], [0.218153, 0.660044, -0.713956, -0.083769], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget t1 := [[-8.799, 74.490, 215.574], [0.217064, 0.655781, -0.718999, -0.076644], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget t2 := [[-6.959, 77.783, 226.881], [0.247035, 0.647412, -0.707869, -0.136945], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget t3 := [[-8.880, 74.399, 216.175], [0.214833, 0.654887, -0.719729, -0.083424], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget t4 := [[-8.724, 74.355, 214.357], [0.219425, 0.653591, -0.720856, -0.070983], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget t5 := [[-6.964, 77.534, 225.243], [0.252596, 0.644815, -0.710833, -0.122985], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget t6 := [[-6.635, 79.635, 228.501], [0.264144, 0.634757, -0.717566, -0.111399], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget t7 := [[-5.996, 80.184, 228.624], [0.266237, 0.633940, -0.717450, -0.111821], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget t8 := [[-6.883, 75.514, 217.046], [0.222408, 0.657358, -0.713686, -0.095222], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget t9 := [[-7.369, 75.120, 214.511], [0.212467, 0.658133, -0.719321, -0.065544], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]]; 
    VAR robtarget t10 := [[-7.110, 75.384, 216.339], [0.213483, 0.659402, -0.715183, -0.090154], [1,-2,0,0], [163.420,9E+09,9E+09,9E+09,9E+09,9E+09]];
    MoveL t0, v100\V:=100.000, z1, tDie, \WObj:=campos;
	MoveL t1, v100\V:=40.210, z1, tDie, \WObj:=campos;
	MoveL t2, v100\V:=297.997, z1, tDie, \WObj:=campos;
	MoveL t3, v100\V:=284.790, z1, tDie, \WObj:=campos;
	MoveL t4, v100\V:=45.641, z1, tDie, \WObj:=campos;
	MoveL t5, v100\V:=286.922, z1, tDie, \WObj:=campos;
	MoveL t6, v100\V:=97.261, z1, tDie, \WObj:=campos;
	MoveL t7, v100\V:=21.268, z1, tDie, \WObj:=campos;
	MoveL t8, v100\V:=312.885, z1, tDie, \WObj:=campos;
	MoveL t9, v100\V:=65.270, z1, tDie, \WObj:=campos;
	MoveL t10, v100\V:=46.620, z1, tDie, \WObj:=campos;
    ENDPROC
    
ENDMODULE