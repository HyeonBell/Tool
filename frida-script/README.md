# frida-script
-----


1. arg_trace.py
- Trace Arguments of Exception by create application Exception infomation with frida implementation so called 'hooking'
- Causing Exception by using android.util.Log and java.lang.Exception
- There are still a lot of parts that need to be supplemented.
- There are lack of implementation of target Exception binding.
  - Explaination : For example, this program run 3 times in total. I got exception call stack. But if i hooking method of exception i got, all methods are hooked, not just the call stack i want. This is main problem :<

### Main Menu
```
-------------------------------------------------
        Trace exception argument in runtime
-------------------------------------------------


1. Setup
2. Show data
3. Setup to script
4. Run script
5. Overloading Calculate --> Not yet no implement.
6. Exit

```

\1. Setup
```
1. Setup to target
2. Setup to data that have to trace in exception result
 > 1
[INFO] Put Application Info
PACKAGE_NAME > test.test.app
Class Name > example.class
Is method init constructor?(Y/n) --> If this is init meaning 'y', auto setup to '$init' word
[INFO] Targeting Init
[*] Try to connect device with USB connection
[*] Try to spawn app with process id.
[*] Try to attach process for creating session.
[*] Finished setup
[INFO] Target Waiting for %resume. --> Frida agent waiting state for %resume put in
```

\2. Show data
```
> 2
1. Show current JS code
2. Show exception data
 >

```

\3. Setup to script
```
1. Cause error overloading
2. Trace exception
3. Trace argument of exception
```

2. full_thread_stack_trace.js
- Trace method call stack you want by exception handling.
- This code used Java.cast(). It's to using for tracing value of return like java.util.HashMap  
