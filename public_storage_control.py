import sys,time,re,subprocess

_command_string = sys.argv[1]



#_command_type = sys.argv[1]
#_command_arg1 = sys.argv[2]
#_command_arg2 = sys.argv[3]
#_command_arg3 = sys.argv[4]


#[18:50:46] [Server thread/INFO]: ytshiyugh issued server command: /tp @s Illuyankas0310
_command_args_re = re.compile(r'\[(.{1,2}):(.{1,2}):(.{1,2})\] \[Server thread/INFO\]: (.{1,300}) issued server command: (.{1,200}) (.{1,200}) (.{1,200})')
_result_command_args = _command_args_re.finditer(_command_string)
try:
    for i in _result_command_args:
        _playername = i.group(4)
        _command_type = i.group(5)
        try:
            _command_arg1 = i.group(6)
            _command_arg2 = i.group(7)
        except:
            pass
except:
    sys.exit()

_command_args_re2 = re.compile(r'\[(.{1,2}):(.{1,2}):(.{1,2})\] \[Async_Chat_Thread - #(.{1,10})/INFO\]: <(.{1,300})> (.{1,300})')
_result_command_args2 = _command_args_re2.finditer(_command_string)
try:
    for i in _result_command_args2:
        _playername = i.group(5)
        _issued_command = str(i.group(6))
except:
    pass

try:
    if _command_type == "/pst":
        subprocess.Popen(['python','public_storage_pst.py',_playername,_command_arg1,_command_arg2])
    elif _command_type == "/pstd":
        subprocess.Popen(['python','public_storage_pstd.py',_playername,_command_arg1,_command_arg2])
    elif _command_type == "/pstp":
        subprocess.Popen(['python','public_storage_pstp.py',_playername,_command_arg1,_command_arg2])
    elif _command_type == "/psts":
        subprocess.Popen(['python','public_storage_psts.py',_playername])
    elif _issued_command == "./psts":
        if str(_playername) == "ytshiyugh":
            subprocess.Popen(['python','public_storage_psts.py',_playername])
            
    else:
        pass
except:
    sys.exit()