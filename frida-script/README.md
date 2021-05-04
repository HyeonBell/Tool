# frida-script


1. arg_trace.py
- Trace Arguments of Exception by create application Exception infomation with frida implementation so called 'hooking'.
- Causing Exception by using android.util.Log and java.lang.Exception.
- If you run at first, There are selectable overloading method.
- Then select overloading method, Insert code causing exception at second running.
- Save exception infomation, then It's using for Tracing to argument of exception.
- There are still a lot of parts that need to be supplemented.
- There are lack of implementation of target Exception binding.
  - Explaination : For example, this program run 3 times in total. I got exception call stack. But if i hooking method of exception i got, all methods are hooked, not just the call stack i want. This is main problem :<

### Main Menu
```
-------------------------------------------------
        Trace exception argument in runtime
-------------------------------------------------
[*] Status : SESSION : Session(pid=27306), TARGET : test.test.app

1. Setup
2. Show data
3. Setup to script
4. Run script
5. Overloading Calculate --> Not yet no implement.
6. Exit


>
```


Setup
```
 > 1
1. Setup to target -> It is needed for each run.
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


Show data
```
> 2
1. Show current JS code
2. Show exception data
```


Setup to script
```
> 3
1. Cause error overloading -> first running
2. Trace exception -> second running
3. Trace argument of exception -> last running
```

For Example : select exception
```
2. Setup to data that have to trace in exception result
 > 2
1. <__main__.ClassFrida.ClassExceptionData object at 0x0000015FECF43E50>
 > 1
<__main__.ClassFrida.ClassExceptionData object at 0x0000015FECF43E50>
1. Show argument
2. Exit
 > 1
1. argument : test.etes, event, common, [object Object],  2021-05-03T18:03:
58.274+09:00,  #sig_argend
2. argument : test.test, test, common, [object Object], :
03:58.373+09:00, etstetse, 5.4.0, , APP #sig_argend
3. argument : test.test, state, common, [object Object], -3663-44c2-a93a-, -05-
Which one choices?
 > 2
 java.lang.Exception
         at test.test<init>(Native Method)
         at test.test<init>(Unknown Source)
         at app.test.test(Unknown Source)
         at app.retainAll.Vicon(Unknown Source)
         at app.addAll.read(Unknown Source)
         at app.addAll.testexample(Unknown Source)
         at app.previousIndex.read(Unknown Source)
         at app.previousIndex.methodexample(Unknown Source)
         at app.test.read(Unknown Source)
         at android.app.Instrumentation.callActivityOnResume(Instrumentation.java:1269)
         at android.app.Activity.performResume(Activity.java:6796)
         at android.app.ActivityThread.performResumeActivity(ActivityThread.java:3409)
         at android.app.ActivityThread.handleResumeActivity(ActivityThread.java:3472)
         at android.app.ActivityThread.handleLaunchActivity(ActivityThread.java:2735)
         at android.app.ActivityThread.-wrap12(ActivityThread.java)
         at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1480)
         at android.os.Handler.dispatchMessage(Handler.java:102)
         at android.os.Looper.loop(Looper.java:154)
         at android.app.ActivityThread.main(ActivityThread.java:6198)
         at java.lang.reflect.Method.invoke(Native Method)
         at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:891)
         at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:781)

```

-----

2. full_thread_stack_trace.js
- Trace method call stack you want by exception handling.
- This code used Java.cast(). It's to using for tracing value of return like java.util.HashMap  

Usage
```
> frida -U -f test.test.app -l full_thread_stack_trace.js --no-pause
```
