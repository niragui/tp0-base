MSG="This Is A Test"
SERVER_PORT="12345"
SERVER_IP="server"

RET=$(echo "$MSG" | nc "$SERVER_IP" "$SERVER_PORT")


if [ "$MSG" = "$RET" ]; then
    echo "Everything is Ok ✅"
else
    echo "Error ❌"
fi