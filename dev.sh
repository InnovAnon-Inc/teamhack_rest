#! /usr/bin/env bash
set -euxo nounset
(( ! $#   ))
((   $UID ))
git pull
git add .
git commit -m update || :
git push             || :

python3 -m build
python3 -m pip install --force-reinstall dist/teamhack-*.*.*-py3-none-any.whl
pytest
python3 -m teamhack_db
#python3 -m teamhack_dns  & pids+=( $! )
#python3 -m teamhack_rest & pids+=( $! )
#wait ${pids[@]}

