package com.example.proiect.Controller.Applications;

import com.example.proiect.Model.Pipe;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.concurrent.TimeUnit;

public class CheckApps implements Runnable{
    public void run()
    {
        boolean yes = true;
        try {
            while(1 == 1) {
                Process process = null;
                process = Runtime.getRuntime().exec(new String[]{"su", "-c", "sha256sum /data/app/*/base.apk"});
                BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
                int read;
                char[] buffer = new char[4096];
                StringBuilder output = new StringBuilder();
                while ((read = in.read(buffer)) > 0) {
                    output.append(buffer, 0, read);
                }
                Pipe x=Pipe.getInstance();
                x.setApps(output.toString());
                x.setCheckStatus(1);
                TimeUnit.SECONDS.sleep(60);
            }
        }
        catch (Exception e) {
            System.out.println("AM AJUNS AICI 22222222222");
            Pipe x = Pipe.getInstance();
            x.setCheckStatus(2);
            System.out.println("Exception is caught");
        }
    }
}