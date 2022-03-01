MODULE MainModuleR

	PERS bool bdiatermi := FALSE;

	TASK PERS wobjdata wobjpin:=[FALSE,TRUE,"",[[413.255,-0.131408,-10.9514],[0.999976,-0.0050778,0.00407438,0.0024214]],[[0,0,0],[1,0,0,0]]];
	TASK PERS wobjdata wobjnal:=[FALSE,TRUE,"",[[413.255,200,-10.9514],[0.999976,-0.0050778,0.00407438,0.0024214]],[[0,0,0],[1,0,0,0]]];
	TASK PERS wobjdata wobjel:=[FALSE,TRUE,"",[[413.255,-200,-10.9514],[0.999976,-0.0050778,0.00407438,0.0024214]],[[0,0,0],[1,0,0,0]]];
	
	VAR robtarget appr:= [[0, 0, 100],[1.0, 0.0, 0.0, 0.0],[-1,1,-2,4],[174.877,9E+09,9E+09,9E+09,9E+09,9E+09]];
		
	VAR robtarget pick:= [[0, 0, 0],[1.0, 0.0, 0.0, 0.0],[-1,1,-2,4],[174.877,9E+09,9E+09,9E+09,9E+09,9E+09]];

	PROC main()

		WHILE true DO
			
			WaitUntil bdiatermi = TRUE;
			elk;
            bdiatermi := FALSE;
		ENDWHILE
	ENDPROC

	PROC elk()
		MoveAbsJ [[-96.9735,-66.9799,35.6313,103.087,92.4393,-165.326],[61.8558,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v1000, z50, tGripper;
		g_GripOut;
		MoveL appr, v200, z5, tGripper\WObj:=wobjel;
		MoveL pick, v200, fine, tGripper\WObj:=wobjel;
		g_GripIn;
		MoveL appr, v200, z5, tGripper\WObj:=wobjel;
		MoveAbsJ [[-90.0466,-66.984,27.7456,71.1812,51.9979,-96.1368],[17.6017,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v200, z5, tGripper;
		MoveAbsJ [[-90.0465,-66.984,21.9463,74.4412,41.4957,-96.137],[14.7465,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v200, z5, tGripper;
		MoveAbsJ [[-90.0469,-66.9752,36.5675,66.3006,51.9677,-96.1224],[29.5709,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v200, z5, tGripper\WObj:=wobjel;
		MoveL appr, v200, z5, tGripper;
		MoveL pick, v200, fine, tGripper;
		g_GripOut;
		MoveL appr, v200, z5, tGripper\WObj:=wobjel;
	ENDPROC

ENDMODULE