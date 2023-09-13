#! /usr/bin/env bash
set -euxo nounset
((   $UID ))
if (( $# )) ; then
     M="$*"
else M=update
fi
git pull
git add .
git commit -m "$M" || :
git push             || :

python3 -m build
python3 -m pip install --force-reinstall dist/teamhack_rest-*.*.*-py3-none-any.whl
#pytest
python3 -m teamhack_rest

