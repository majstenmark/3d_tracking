# yumivoice_medicalinstruments

Python and RAPID scripts for interacting with Yumi using voice commands on Mac.

The voice commands are captured using Mac OS voice control which triggers Automator scripts.

Each voice command runs a Python script from Automator. The scripts connects to robot_com which in turn sends commands to the robot.

Workflow.
Load rapidmodules into robot and start robot program. Run robot_com.py and activate voice control on mac. Connect the voice controls to the python scripts.
