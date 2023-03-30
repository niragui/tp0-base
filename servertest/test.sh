MSG="This Is A Test"
SERVER_PORT="12345"
SERVER_IP="server"

RET=(echo "$MSG" | nc "$SERVER_IP" "$SERVER_PORT")
# RET="This Is A Test Of The Test Should Give Error"


if [ "$MSG" = "$RET" ]; then
    echo "Everything is Ok ✅"
else
    echo "Error ❌"
fi