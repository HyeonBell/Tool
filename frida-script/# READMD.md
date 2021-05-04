# frida-script

## Content

1. arg_trace.py
- Trace Arguments of Exception by create application Exception infomation with frida implementation so called 'hooking'
- Causing Exception by using android.util.Log and java.lang.Exception
- There are still a lot of parts that need to be supplemented.
- There are lack of implementation of target Exception binding.
  - Explaination : For example, this program run 3 times in total. I got exception call stack. But if i hooking method of exception i got, all methods are hooked, not just the call stack i want. This is main problem :<

2. full_thread_stack_trace.js
- Trace method call stack you want by exception handling.
- This code used Java.cast(). It's to using for tracing value of return like java.util.HashMap  
