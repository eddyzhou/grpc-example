"""Runs protoc with the gRPC plugin to generate messages and gRPC stubs."""

from grpc.tools import protoc

protoc.main(
    (
	'',
	'-I../protos',
	'--python_out=./pb',
	'--grpc_python_out=./pb',
        '../protos/search.proto',
    )
)

