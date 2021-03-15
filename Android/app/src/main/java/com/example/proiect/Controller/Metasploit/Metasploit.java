package com.example.proiect.Controller.Metasploit;

import android.os.Build;

import androidx.annotation.RequiresApi;

import com.example.proiect.Model.Pipe;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.TimeUnit;

public class Metasploit implements Runnable  {

    @RequiresApi(api = Build.VERSION_CODES.O)
    public void run()
    {
        boolean ok = true;
        try {
        while(1 == 1) {
                    TimeUnit.SECONDS.sleep(1);
                Pipe x = Pipe.getInstance();
                Path path = Paths.get("/data/user/0/com.metasploit.stage/");
                if (!Files.exists(path)) {
                    if(ok==true) {
                        System.out.println("False");
                        x.setMetasploit("False");
                    }
                } else {
                    System.out.println("True");
                    ok = false;
                    x.setMetasploit("True");
                }
            }
        } catch (InterruptedException e) {
        e.printStackTrace();
    }
    }
}
