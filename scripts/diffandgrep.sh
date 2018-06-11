#!/bin/bash
cd ~/build
logs=()
for i in $(ls /home/travis/build/*.log);
do
        logs+=($i)
done
diff ${logs[0]} ${logs[1]} > /home/travis/diff.txt
cat $logs | grep -n '^\[ERROR\]' > /home/travis/grep_errors.txt
echo "done executing diffandgrep script"
