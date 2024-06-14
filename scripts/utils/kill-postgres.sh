read -p "Enter the port of the process you want to kill:"$'\n> ' port
sudo lsof -i :$port
read -p "Enter process PID:"$'\n> ' pid
read -p "Are you sure you want to kill the process with pid: $pid"$'\n(y/N) > ' -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo kill $pid
fi