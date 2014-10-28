all: test.bin

test.bin: test.txt
	xxd -c 6 -g1 -r test.txt > test.bin

