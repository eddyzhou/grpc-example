package main

import (
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"time"

	"xmiddleware"

	"grpc.sample/kv"
	"grpc.sample/search"
)

const (
	port        = 50052
	metricsPort = 8899
	sentryDSN   = "http://6ac4e8e7a2de45579d5ee1df1899d4ed:92291760a07b46eaaccf24e46ffcfdcf@10.10.28.2:9000/2"
)

func init() {
	log.SetOutput(io.Writer(os.Stderr))
	log.SetFlags(log.Ldate | log.Lmicroseconds | log.Lshortfile)
}

func main() {
	lis, err := net.Listen("tcp", fmt.Sprintf(":%v", port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
		return
	}

	xmiddleware.StartMetricsServer(metricsPort)
	options := []xmiddleware.XServerOption{xmiddleware.Monitor("sample", port, sentryDSN), xmiddleware.RateLimit(1*time.Second, 10000)}
	//options := []xmiddleware.XServerOption{xmiddleware.Monitor("sample", port, sentryDSN)}
	s := xmiddleware.NewServer(options...)
	kv.RegisterKeyValueServer(s, &KvService{values: make(map[string]string)})
	search.RegisterSearchServiceServer(s, &SearchService{})
	s.Serve(lis)
}
