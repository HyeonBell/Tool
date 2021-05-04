# frida-script
-----


1. arg_trace.py
- Trace Arguments of Exception by create application Exception infomation with frida implementation so called 'hooking'
- Causing Exception by using android.util.Log and java.lang.Exception
- There are still a lot of parts that need to be supplemented.
- There are lack of implementation of target Exception binding.
  - Explaination : For example, this program run 3 times in total. I got exception call stack. But if i hooking method of exception i got, all methods are hooked, not just the call stack i want. This is main problem :<

### For example code
```
java.lang.Exception
	at java.lang.Runtime.exec(Native Method)
	at java.lang.reflect.Method.invoke(Native Method)
	at test.tes.write(Unknown Source)
	at test.test2.see.write(Unknown Source)
	at test.pp.read(Unknown Source)
	at test.pp.parsing(Unknown Source)
	at test.pp.codecode(Unknown Source)
	at test.abcdef.run(Unknown Source)
	at test.run(Unknown Source)
	at test.sr.run(Unknown Source)
	at test.sr.call(Unknown Source)
	at java.util.concurrent.FutureTask.run(FutureTask.java:237)
	at java.util.concurrent.ScheduledThreppoolExecutor$ScheduledFutureTask.run(ScheduledThreppoolExecutor.java:272)
	at java.util.concurrent.ThreppoolExecutor.runWorker(ThreppoolExecutor.java:1133)
	at java.util.concurrent.ThreppoolExecutor$Worker.run(ThreppoolExecutor.java:607)
	at java.lang.Thread.run(Thread.java:761)

```


2. full_thread_stack_trace.js
- Trace method call stack you want by exception handling.
- This code used Java.cast(). It's to using for tracing value of return like java.util.HashMap  
