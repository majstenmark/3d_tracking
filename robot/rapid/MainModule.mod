MODULE MainModuleL
	VAR socketdev serversocket;
	VAR socketdev cientsocket;
	CONST string receivestr:="";
	CONST string clientip:="";
	VAR num pincett:=0;
	PERS bool bdiatermi := FALSE;
	VAR num nal:=0;
	VAR num el:=0;
	VAR num nval:=0;
	VAR bool ok:=FALSE;
	VAR string msg:="";
	TASK PERS wobjdata wobjpin:=[FALSE,TRUE,"",[[413.255,-0.131408,-10.9514],[1.0, 0.0, 0.0, 0.0]],[[0,0,0],[1,0,0,0]]];
	TASK PERS wobjdata wobjnal:=[FALSE,TRUE,"",[[413.255,200,-10.9514],[0.999976,-0.0050778,0.00407438,0.0024214]],[[0,0,0],[1,0,0,0]]];
	TASK PERS wobjdata wobjel:=[FALSE,TRUE,"",[[413.255,-200,-10.9514],[0.999976,-0.0050778,0.00407438,0.0024214]],[[0,0,0],[1,0,0,0]]];

	
	VAR robtarget appr:= [[0, 0, 100],[1.0, 0.0, 0.0, 0.0],[-1,1,-2,4],[174.877,9E+09,9E+09,9E+09,9E+09,9E+09]];
		
	VAR robtarget pick:= [[0, 0, 0],[1.0, 0.0, 0.0, 0.0],[-1,1,-2,4],[174.877,9E+09,9E+09,9E+09,9E+09,9E+09]];
	

	PROC main()
		SocketCreate serversocket;
		SocketBind serversocket, "192.168.125.1", 1025;
		SocketListen serversocket;
		SocketAccept serversocket, cientsocket;
		WHILE true DO
			SocketReceive cientsocket\Str:=msg;
			
			TPWrite msg;
			ok:= Strtoval(msg,nval);
			IF nval = 1 THEN
				TPWrite "pincett";
				pinc;
			ENDIF
			IF nval = 2 THEN
				TPWrite "nalforare";
				nalf;
			ENDIF
			IF nval = 3 THEN
				TPWrite "elkniv";
				bdiatermi := TRUE;
				WaitUntil bdiatermi = FALSE;
			ENDIF
			SocketSend cientsocket\Str:="ok";
		ENDWHILE
	ENDPROC
	PROC pinc()
		MoveAbsJ [[-96.9735,-66.9799,35.6313,103.087,92.4393,-165.326],[61.8558,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v1000, z50, tGripper;
		g_GripOut;
		MoveL [[410.32,-4.37,56.29],[0.0261231,-0.712031,0.701619,0.00776269],[-1,1,-2,4],[174.877,9E+09,9E+09,9E+09,9E+09,9E+09]], v200, z5, tGripper;
		MoveL [[414.01,1.96,-6.78],[0.0255418,-0.714431,0.69882,-0.0242314],[-1,2,-2,4],[-174.674,9E+09,9E+09,9E+09,9E+09,9E+09]], v200, fine, tGripper;
		g_GripIn;
		MoveL [[410.32,-4.37,56.29],[0.0261231,-0.712031,0.701619,0.00776269],[-1,1,-2,4],[174.877,9E+09,9E+09,9E+09,9E+09,9E+09]], v200, z5, tGripper;
		MoveAbsJ [[-90.0466,-66.984,27.7456,71.1812,51.9979,-96.1368],[17.6017,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v200, z5, tGripper;
		MoveAbsJ [[-90.0465,-66.984,21.9463,74.4412,41.4957,-96.137],[14.7465,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v200, z5, tGripper;
		MoveAbsJ [[-90.0469,-66.9752,36.5675,66.3006,51.9677,-96.1224],[29.5709,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v200, z5, tGripper;
		MoveL [[410.32,-4.37,56.29],[0.0261231,-0.712031,0.701619,0.00776269],[-1,1,-2,4],[174.877,9E+09,9E+09,9E+09,9E+09,9E+09]], v200, z5, tGripper;
		MoveL [[414.01,1.96,-6.79],[0.025542,-0.71443,0.69882,-0.0242306],[-1,2,-2,4],[-174.674,9E+09,9E+09,9E+09,9E+09,9E+09]], v200, fine, tGripper;
		g_GripOut;
		MoveL [[410.32,-4.37,56.29],[0.0261231,-0.712031,0.701619,0.00776269],[-1,1,-2,4],[174.877,9E+09,9E+09,9E+09,9E+09,9E+09]], v200, z5, tGripper;
	ENDPROC

	PROC pinc2()

		MoveAbsJ [[-96.9735,-66.9799,35.6313,103.087,92.4393,-165.326],[61.8558,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v1000, z50, tGripper;
		g_GripOut;
		MoveL appr, v200, z5, tGripper\WObj:=wobjpinc;
		MoveL pick, v200, fine, tGripper\WObj:=wobjpinc;
		g_GripIn;
		MoveL appr, v200, z5, tGripper\WObj:=wobjpinc;
		MoveAbsJ [[-90.0466,-66.984,27.7456,71.1812,51.9979,-96.1368],[17.6017,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v200, z5, tGripper;
		MoveAbsJ [[-90.0465,-66.984,21.9463,74.4412,41.4957,-96.137],[14.7465,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v200, z5, tGripper;
		MoveAbsJ [[-90.0469,-66.9752,36.5675,66.3006,51.9677,-96.1224],[29.5709,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v200, z5, tGripper\WObj:=wobjpinc;
		MoveL appr, v200, z5, tGripper;
		MoveL pick, v200, fine, tGripper;
		g_GripOut;
		MoveL appr, v200, z5, tGripper\WObj:=wobjpinc;
	ENDPROC


	PROC nalf()
		MoveAbsJ [[-96.9735,-66.9799,35.6313,103.087,92.4393,-165.326],[61.8558,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v1000, z50, tGripper;
		g_GripOut;
		MoveL appr, v200, z5, tGripper\WObj:=wobjnal;
		MoveL pick, v200, fine, tGripper\WObj:=wobjnal;
		g_GripIn;
		MoveL appr, v200, z5, tGripper\WObj:=wobjnal;
		MoveAbsJ [[-90.0466,-66.984,27.7456,71.1812,51.9979,-96.1368],[17.6017,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v200, z5, tGripper;
		MoveAbsJ [[-90.0465,-66.984,21.9463,74.4412,41.4957,-96.137],[14.7465,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v200, z5, tGripper;
		MoveAbsJ [[-90.0469,-66.9752,36.5675,66.3006,51.9677,-96.1224],[29.5709,9E+09,9E+09,9E+09,9E+09,9E+09]]\NoEOffs, v200, z5, tGripper\WObj:=wobjnal;
		MoveL appr, v200, z5, tGripper;
		MoveL pick, v200, fine, tGripper;
		g_GripOut;
		MoveL appr, v200, z5, tGripper\WObj:=wobjnal;
	ENDPROC

ENDMODULE