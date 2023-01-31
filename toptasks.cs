using System.Diagnostics;
using System;
using System.Resources;
using System.Runtime;
using System.Collections;

class Main
{   
    DateTime time_start;
    
    public Main()
    {
        time_start = DateTime.Now;
        Log("started");
        
    }

    private void Log(object o)
    {
        DateTimeOffset time_delta = DateTimeOffset.Now - time_start;
        Debug.WriteLine($"[{time_delta.Hour}:{time_delta.Minute}:{time_delta.Second}]: {o}");
    }
}