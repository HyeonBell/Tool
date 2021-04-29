function thread_trace(){
    var test = Java.use("java.lang.Thread").currentThread();

    var hashmap = Java.use("java.util.HashMap");
    var cast = Java.cast(test.getAllStackTraces(), hashmap);
    var iter = cast.entrySet().iterator();
    console.log("---------------------------------------------------------------------------------");
    while (iter.hasNext()){
        var entry = Java.cast(iter.next(), Java.use("java.util.HashMap$HashMapEntry"));
        var thread = Java.cast(entry.getKey(), Java.use("java.lang.Thread"));
        console.log("ID : " + thread.getId()+ ", Name : " + thread.getName() + ", Priority : " + thread.getPriority() +  "\nState : " + thread.getState() + ", ThreadGroup : " + thread.getThreadGroup());
        console.log("StackTrace ┐  \n" + thread.getStackTrace().toString().replaceAll(',','\n'));
        console.log("---------------------------------------------------------------------------------");
    }
}

setImmediate(function(){
    Java.perform(function(){
        var runtime = Java.use("java.lang.Runtime"); // Target class you want.
        var imp9 = runtime.getRuntime()['exit'].overload('int'); // Overloading put in data you want as same.

        imp9.implementation = function(param){
            console.log("java.lang.Runtime.getRuntime exit hooked!"); // Code that succeeded hooking
            console.log("exit return value : " + param); // Same.
            thread_trace(); // Trace call stack of whole program scope at time that target class hooked.
            return runtime.getRuntime()['exit'].call(this, param); // Code for normally function executing.
        }
    })
})
