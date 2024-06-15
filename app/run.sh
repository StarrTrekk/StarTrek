#!/bin/bash

# build  imgae docker if not exist and run it
docker build -t startrek .
docker run -p 5000:5000 startrek