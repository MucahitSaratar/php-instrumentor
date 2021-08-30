# php instrument tool

| how does work?
- fetching any function name from function_list.txt
- detecting all php file in the directory
- reading files as line by line
- detecting the written function each line 
- if line has the function, php instrumentor program is doing adding trigger before the executes the function
- the path of php file,line of execute the function,name of the function are keeping and trigger is sending the data to server
- server is catching report and show on the main page(and server auto refreshing in 1 second)

| how i can use that?
- you can see parameters with -h flag. but i can tell you paramaters.
- `-h` for help message
- `-d` directory path for root of php files (eg. -d /var/www/html/myproject) (required)
- `--function-list / -l` use if you want another function list. default:function_list.txt (eg. -l myfunction_list.lst)
- `--ip` http server ip adres. default:127.0.0.1
- `--port / -p` http server port. default:65534
- `--only-server / -os` if you used this param, should be value. use for already instrumented project. default:False (eg. --only-server 1)

### [!] warning: php instrumentor chancing files. recommend to backup before

| how i can use full power of php-instrumentor?
- you should edit to params of the function from trigger

![2021-08-31_00-56](https://user-images.githubusercontent.com/29048982/131411656-1f5f37d9-9f6d-4d2b-9f3e-11c85420fbd1.png)