#! /usr/bin/env bash
set -euxo nounset
(( ! $# ))
(( $UID ))

curl -X POST \
     -d '{"host":"bookworm.htb", "type":"A", "inet":"10.10.11.215"}' \
     127.0.0.1:5000/create

