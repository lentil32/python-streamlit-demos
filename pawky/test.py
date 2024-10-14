from pawky import AWKInterpreter


def run_test(title: str, awk_script: str, input_data: str) -> None:
    print(f"\n=== {title} ===")
    interpreter = AWKInterpreter(awk_script)
    interpreter.set_input(input_data)
    interpreter.run()


def main():
    title_test1 = "Case 1: Filter out lines containing 'NULL'"
    awk_script_test1 = '''
BEGIN {
    FS = ",";
}

{
    defected = 0;
    for (i = 1; i <= NF; ++i) {
        if ($i == "NULL") {
            defected = 1;
            break;
        }
    }
    if (!defected)
        print $0;
}
'''
    input_data_test1 = '''\
a1,a2,a3
b1,b2,b3
c1,c2,c3
d1,NULL,d3
NILL,e2,e3
f1,f2,null\
   '''
    run_test(title_test1, awk_script_test1, input_data_test1)

    title_test2 = "Case 2: Sum fields"
    awk_script_test2 = '''
BEGIN {
    FS = ",";
}

{
    total = 0;
    for (i = 1; i <= NF; ++i) {
        total += $i;
    }
    print total;
}
'''

    input_data_test2 = '''\
1,2,3,4,5
6,7,8,9,10
11,12,13,14,15\
    '''
    run_test(title_test2, awk_script_test2, input_data_test2)

    title_test3 = "Case 3: Handling FS, OFS, RS, ORS"
    awk_script_test3 = '''
    BEGIN {
        FS = "|";
        RS = "&";
        OFS = "*";
        ORS = "_";
    }

    {
        print $1, $2, $3, $4;
    }
    '''
    input_data_test3 = '''\
1|2|3|4&5678|910|11121314|15&1617|181920
212223|2425|26272829\
    '''
    run_test(title_test3, awk_script_test3, input_data_test3)

    title_test4 = "Case 4: Conditional printing"
    awk_script_test4 = '''
    BEGIN {
        FS = ",";
    }

    {
        if ($2 > 5)
            print $1;
    }
    '''
    input_data_test4 = '''\
apple,4,red
banana,6,yellow
cherry,5,red\
    '''
    run_test(title_test4, awk_script_test4, input_data_test4)


if __name__ == '__main__':
    main()
