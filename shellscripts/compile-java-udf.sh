#!/bin/bash

if [ "$1" == "" ]; then
   echo "Usage: $0 <java file>"
   exit 1
fi

CNAME=${1%.java}
JARNAME=$CNAME.jar
JARDIR=/tmp/hive_jars/$CNAME
CLASSPATH=$(ls /home/hadoop/hive/lib/hive-serde-*.jar):$(ls /home/hadoop/hive/lib/hive-exec-*.jar):$(ls /home/hadoop/hadoop-core-*.jar)

function tell {
    echo
    echo "$1 successfully compiled.  In Hive run:"
    echo "$> add jar $JARNAME;"
    echo "$> create temporary function $CNAME as 'com.example.hive.udf.$CNAME';"
    echo
}

mkdir -p $JARDIR
javac -classpath $CLASSPATH -d $JARDIR/ $1 && jar -cf $JARNAME -C $JARDIR/ . && tell $1
