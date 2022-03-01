MODULE MainModule
	VAR socketdev serversocket;
	VAR socketdev cientsocket;
	CONST string receivestr:="";
	CONST string clientip:="";
	VAR num nal:=0;
	VAR num el:=0;
	VAR num nval:=0;
	VAR bool ok:=FALSE;
	VAR string msg:="";
	
    PERS tooldata tDie;
    PERS wobjdata campos;

	PROC main()
        VAR robtarget currpos;
        VAR string recmsg;
		VAR string sendmsg;
        SocketCreate serversocket;
		SocketBind serversocket, "192.168.125.1", 1025;
        !SocketBind serversocket, "127.0.0.1", 1025;
		
		SocketListen serversocket;
		SocketAccept serversocket, cientsocket;
		WHILE true DO
			SocketReceive cientsocket\Str:=recmsg;
			
			ok:= Strtoval(recmsg,nval);
			IF nval = 1 THEN
				
                currpos := CRobT(\TaskName:="T_ROB_L"\Tool:=tDie\WObj:=campos);
                sendmsg := NumToStr(currpos.trans.x,3) + " " +  NumToStr(currpos.trans.y,3) + " "+  NumToStr(currpos.trans.z,3) + " " + NumToStr(currpos.rot.q1,3) + " "+ NumToStr(currpos.rot.q2,3) + " "+ NumToStr(currpos.rot.q3,3) + " "+ NumToStr(currpos.rot.q4,3);
                
			    SocketSend cientsocket\Str:=sendmsg;
			ENDIF
			
		ENDWHILE
	ENDPROC
	
ENDMODULE