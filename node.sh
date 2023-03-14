#!/bin/bash

IP="10.46.169.64"
PORT=9991

while getopts "s:p:" opt; do
  case ${opt} in
    s )
      IP=$OPTARG
      ;;
    p )
      PORT=$OPTARG
      ;;
    \? )
      echo "Invalid option: -$OPTARG" 1>&2
      exit 1
      ;;
    : )
      echo "Option -$OPTARG requires an argument" 1>&2
      exit 1
      ;;
  esac
done

shift $((OPTIND -1))

ACTION=$1
FILE=$2

function add_file {
  if [ -e "$1" ]; then
    data=$(cat "$1")
    echo "add $1" | nc $IP $PORT
    read msg <&3
    echo "[SERVER]: $msg"
    echo "$data" | nc $IP $PORT
    read msg <&3
    echo "[SERVER]: $msg"
    exec 3<&-
  else
    echo "File not found"
  fi
}

function list_files {
  echo "list $1" | nc $IP $PORT
  read msg <&3
  echo "[SERVER]: $msg"
  exec 3<&-
}

function fetch_file {
  echo "fetch $1" | nc $IP $PORT
  read msg <&3
  if [ "$msg" != "File not found" ]; then
    read directory filename <<<"$msg"
    mkdir -p "$directory"
    echo "Filename received." | nc $IP $PORT
    read data <&3
    echo "[RECV] Receiving the file data."
    echo "$data" > "$directory/$filename"
    echo "File data received" | nc $IP $PORT
  else
    echo "File not found - [$1]"
  fi
  exec 3<&-
}

exec 3<>/dev/tcp/$IP/$PORT

if [ "$ACTION" == "add" ]; then
  add_file "$FILE" 3<>/dev/tcp/$IP/$PORT
elif [ "$ACTION" == "list" ]; then
  list_files "$FILE" 3<>/dev/tcp/$IP/$PORT
elif [ "$ACTION" == "fetch" ]; then
  fetch_file "$FILE" 3<>/dev/tcp/$IP/$PORT
fi

exec 3<&-
