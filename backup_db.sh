#!/bin/bash

today=$(date +'%Y-%m-%d')
filename=/var/lib/postgresql/manolo_$today.sql

pg_dump -d manolo > $filename && bzip2 $filename
