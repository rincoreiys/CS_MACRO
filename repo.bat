
echo off
set action=%1

IF "%action%"=="push" (
    git add --all
    git commit -m "PUSH"
    git push
)

IF "%action%"=="pull" (
    git checkout .
    git pull
)



