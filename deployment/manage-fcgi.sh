#!/bin/bash
#
# Manages the startup and shutdown of this projects processes
# as well as runing various tasks.
#
# Uses UNIX sockets for FCGI
#
# Version 2.2

# Project Specific Config
PROJNAME='adlibre_tms'
WEB_USER='wwwpub'

MAXSPARE=2
MINSPARE=2
MAXCHILDREN=10
UMASK=007

CWD=$(cd ${0%/*} && pwd -P)
PROJDIR=$(cd $CWD/../ && pwd -P) # Root of our project
SRCDIR=$(cd $CWD/../${PROJNAME}/ && pwd -P) # Path to manage.py
BINDIR=$(cd $CWD/../bin/ && pwd -P) # Path to activate / virtualenv

############################################

ACTION=$1
SETTINGS=${2-settings}
SOCKET="$PROJDIR/"${3-$(echo "${PROJNAME}")}".sock"
PIDBASE="$PROJDIR/"${3-$(echo "${PROJNAME}")}
WPIDFILE="${PIDBASE}.wsgi.pid"
CPIDFILE="${PIDBASE}.celeryd.pid"


# Functions
function startit {
    echo -n "Starting ${PROJNAME} with ${SETTINGS}: "

    if [ -f "${WPIDFILE}" ]; then
        echo "Error: PIDFILE ${WPIDFILE} exists. Already running?"
        RC=128
    else
        . ${BINDIR}/activate
        python ${SRCDIR}/manage.py runfcgi method=threaded minspare=${MINSPARE} maxspare=${MAXSPARE} maxchildren=${MAXCHILDREN} socket=$SOCKET pidfile=${WPIDFILE} umask=${UMASK} --settings=${SETTINGS}
        RC=$?
        echo "Started."
    fi
}

function stopit {
    echo -n "Stopping ${PROJNAME}: "

    if [ -f "${WPIDFILE}" ]; then
        kill `cat -- ${WPIDFILE}`
        RC=$?
        echo "Process(s) Terminated."
        rm -f -- ${WPIDFILE}
    else
        echo "PIDFILE not found. Killing likely processes."
        kill `pgrep -f "python ${SRCDIR}/manage.py runfcgi method=threaded minspare=${MINSPARE} maxspare=${MAXSPARE} maxchildren=${MAXCHILDREN} socket=$SOCKET pidfile=${WPIDFILE} --settings=${SETTINGS}"`
        RC=$?
        echo "Process(s) Terminated."
    fi
}

function status {
    echo "I don't know how to do that yet"
}

function startCelery {
    echo -n "Starting CeleryD ${PROJNAME} with ${SETTINGS}: "

    if [ -f "${CPIDFILE}" ]; then
        echo "Error: PIDFILE ${CPIDFILE} exists. Already running?"
        RC=128
    else
        . ${BINDIR}/activate
        python ${SRCDIR}/manage.py celeryd_detach --pidfile=${CPIDFILE} --settings=${SETTINGS}
        RC=$?
        echo "Started."
    fi
}

function stopCelery {
    echo -n "Stopping CeleryD ${PROJNAME}: "

    if [ -f "${CPIDFILE}" ]; then
        kill `cat -- ${CPIDFILE}`
        RC=$?
        echo "Process(s) Terminated."
        rm -f -- ${CPIDFILE}
    else
        echo "PIDFILE not found. Killing likely processes."
        kill `pgrep -f "python ${SRCDIR}/manage.py celeryd_detach pidfile=${CPIDFILE} --settings=${SETTINGS}"`
        RC=$?
        echo "Process(s) Terminated."
    fi
}

function rebuildIndex {
    echo -n "Rebuilding ${PROJNAME} search index with ${SETTINGS}: "
    . ${BINDIR}/activate
    python ${SRCDIR}/manage.py update_index --remove --settings=${SETTINGS}
    RC=$?
    echo "Done."
}

function showUsage {
    echo "Usage: manage-fcgi.sh {start|stop|restart|status|rebuildindex|startCelery|stopCelery|restartCelery} <settings_file> <sitename>"
}

# check that we have required parameters
if [ "$ACTION" == "" ]; then
    showUsage
    exit 128
fi

# Sanity check username = $WEB_USER else die with error
if [ ! "`whoami`" == "$WEB_USER" ]; then
    echo "Error: Must run as ${WEB_USER}."
    exit 128
fi

# See how we were called.
case "$ACTION" in
    start)
        startit
	;;
    stop)
        stopit
	;;
    startCelery)
        startCelery
	;;
    stopCelery)
        stopCelery
	;;
	restartCelery)
	    stopCelery
	    startCelery
	;;
    status)
        status
        ;;
    rebuildindex)
        rebuildIndex
        ;;
    restart)
        stopit
        startit
	;;
    *)
	    showUsage
	;;
esac

exit $RC
