package common

import (
	"bufio"
	"fmt"
	"net"

	log "github.com/sirupsen/logrus"
)

// ClientConfig Configuration used by the client
type ClientConfig struct {
	server        string
	agency        string
	name          string
	last_name     string
	document      string
	birthdate     string
	number        string
}

// Client Entity that encapsulates how
type Client struct {
	config ClientConfig
	conn   net.Conn
}

// NewClient Initializes a new client receiving the configuration
// as a parameter
func NewClient(config ClientConfig) *Client {
	client := &Client{
		config: config,
	}
	return client
}

// CreateClientSocket Initializes client socket. In case of
// failure, error is printed in stdout/stderr and exit 1
// is returned
func (c *Client) createClientSocket() error {
	conn, err := net.Dial("tcp", c.config.server)
	if err != nil {
		log.Fatalf(
	        "action: connect | result: fail | client_id: %v | error: %v",
			c.config.document,
			err,
		)
	}
	c.conn = conn
	return nil
}

// StartClientLoop Send messages to the client until some time threshold is met
// func (c *Client) StartClientLoop() {
// 	// autoincremental msgID to identify every message sent
// 	msgID := 1

// loop:
// 	// Send messages if the loopLapse threshold has not been surpassed
// 	for timeout := time.After(c.config.LoopLapse); ; {
// 		select {
// 		case <-timeout:
// 	        log.Infof("action: timeout_detected | result: success | client_id: %v",
//                 c.config.document,
//             )
// 			break loop
// 		default:
// 		}

// 		// Create the connection the server in every loop iteration. Send an
// 		c.createClientSocket()

// 		// TODO: Modify the send to avoid short-write
// 		fmt.Fprintf(
// 			c.conn,
// 			"[CLIENT %v] Message N°%v\n",
// 			c.config.document,
// 			msgID,
// 		)
// 		msg, err := bufio.NewReader(c.conn).ReadString('\n')
// 		msgID++
// 		c.conn.Close()

// 		if err != nil {
// 			log.Errorf("action: receive_message | result: fail | client_id: %v | error: %v",
//                 c.config.document,
// 				err,
// 			)
// 			return
// 		}
// 		log.Infof("action: receive_message | result: success | client_id: %v | msg: %v",
//             c.config.document,
//             msg,
//         )

// 		// Wait a time between sending one message and the next one
// 		time.Sleep(c.config.LoopPeriod)
// 	}

// 	log.Infof("action: loop_finished | result: success | client_id: %v", c.config.document)
// }

// SnedBet Send bet to the server
func (c *Client) SendBet() {
	c.createClientSocket()

	// TODO: Modify the send to avoid short-write
	fmt.Fprintf(
		c.conn,
		"Envio Apuesta",
	)
	msg, err := bufio.NewReader(c.conn).ReadString('\n')
	c.conn.Close()

	if err != nil {
		log.Errorf("action: receive_message | result: fail | client_id: %v | error: %v",
			c.config.document,
			err,
		)
		return
	}
	log.Infof("action: receive_message | result: success | client_id: %v | msg: %v",
		c.config.document,
		msg,
	)

	log.Infof("action: Bet Sent | result: success | client_id: %v", c.config.document)
}
