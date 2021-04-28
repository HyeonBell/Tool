setImmediate(function(){
    Java.perform(function(){
        var test = Java.use("java.lang.Thread").currentThread();
        console.log(test);
        //console.log(test.class.getDeclaredMethods())
        console.log(typeof test.getAllStackTraces());
        console.log(test.getAllStackTraces().$className);

        var hashmap = Java.use("java.util.HashMap");
        var cast = Java.cast(test.getAllStackTraces(), hashmap);
        console.log(cast);
        console.log(typeof cast.entrySet());

        // Code for comprehension
        console.log(cast.entrySet().$className);
        console.log(cast.entrySet().iterator());
        console.log(cast.entrySet().iterator().$className);
        // Code for comprehension

        var iter = cast.entrySet().iterator();
        while (iter.hasNext()){
            var entry = Java.cast(iter.next(), Java.use("java.util.HashMap$HashMapEntry"));
            console.log("key : "+entry.getKey() + ", value : " + entry.getValue());
            console.log("key type : " + typeof entry.getKey() + " className : "+ entry.getKey().$className);
            console.log("value type : " + typeof entry.getValue() + " className : " + entry.getValue().$className);
            var thread = Java.cast(entry.getKey(), Java.use("java.lang.Thread"));
            //console.log("method : " + thread.class.getDeclaredMethods());
            console.log(thread.currentThread().getStackTrace());

        }

    });
});