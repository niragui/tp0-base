MSG = "This Is A Test"
SERVER_PORT = "12345"
SERVER_IP = "server"

# RET = (echo "$MSG" | nc -w 1 "$SERVER_IP" "$SERVER_PORT")
RET = "This Is A Test"


if [[ "$MSG" == "$RET" ]]; then
    echo "Everything is Ok ✅"
else
    echo "Error ❌"