#!/bin/bash
cd ~/build
logs=()
for i in $(ls *.log);
do
        logs+=($i)
done
diff ${logs[0]} ${logs[1]} > diff.txt
cat $logs | grep -n '^\[ERROR\]' > grep_errors.txt
echo "done executing script"
