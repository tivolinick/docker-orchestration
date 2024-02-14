#!/bin/bash
passwd=$1
echo -n "$passwd" | base64 -i -