#!/bin/bash

pdbset xyzin $1 xyzout $2 1>/dev/null <<EOF
renumber 1
EOF
