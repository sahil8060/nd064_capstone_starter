#!/bin/bash -eu

set -e

# The commands to generate the gRPC files
python3 -m grpc_tools.protoc -I../../pb --python_out=./ --grpc_python_out=./ demo.proto
