import subprocess

result = subprocess.call('/usr/local/bin/run_failed.sh')
print result
if result == 0:
	print "Build passed!! WOOOHOOOOO!"
elif result == 2:
	print "MAA KI AANKH!"