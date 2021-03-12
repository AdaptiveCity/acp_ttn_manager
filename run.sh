SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $SCRIPT_DIR
pid=$(pgrep -f "python3 api_register.py")
if [ $? -eq 0 ]
then
    echo $(date '+%s') api_register.py already running as PID $pid
    exit 1
else
    echo $(date '+%s') starting api_register.py
    nohup python3 api_register.py >/var/log/acp_prod/api_register.log 2>/var/log/acp_prod/api_register.err </dev/null & disown
    exit 0
fi