#!/usr/bin/env bash

TOMCAT_HOME=/software/tomcat_supervisor
Tomcat_Gc_Log=/software/logs/tomcat_gc.log


function shutdown()
{
    date
    echo "Shutting down Tomcat"
    unset CATALINA_PID
    unset LD_LIBRARY_PATH
    unset JAVA_OPTS

    ${TOMCAT_HOME}/bin/catalina.sh stop
}

date
echo "Starting Tomcat"
export CATALINA_PID=/tmp/$$
export JAVA_HOME=/software/jdk1.7.0_79
export LD_LIBRARY_PATH=/usr/local/apr/lib
export JAVA_OPTS="$JAVA_OPTS -server -Dfile.encoding=UTF-8 -Xmx2048m -Xms2048m -XX:PermSize=521m -XX:MaxPermSize=1024m -Xss512k -XX:+UseG1GC
-XX:MaxGCPauseMillis=50 -XX:InitiatingHeapOccupancyPercent=70 -XX:+UseCompressedOops -XX:PretenureSizeThreshold=1m
-XX:+UseCMSCompactAtFullCollection -XX:CMSFullGCsBeforeCompaction=5 -XX:+DisableExplicitGC -verbose:gc
-XX:+PrintGCTimeStamps -XX:+PrintGCDetails -Xloggc:${Tomcat_Gc_Log}
-XX:+PrintFlagsFinal -Djava.security.egd=file:/dev/./urandom"


. ${TOMCAT_HOME}/bin/catalina.sh start


# Allow any signal which would kill a process to stop Tomcat
trap shutdown HUP INT QUIT ABRT KILL ALRM TERM TSTP

echo "Waiting for `cat $CATALINA_PID`"
wait `cat ${CATALINA_PID}`