package com.example.proiect;

import android.view.View;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class CheckApps implements Runnable{
    public void run()
    {
        boolean yes = true;
        try {
            while(1 == 1) {
                if (yes == true) {
                    TimeUnit.SECONDS.sleep(5);
                    yes = false;
                }
                else{
                    TimeUnit.SECONDS.sleep(60);
                }
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
            }
        }
        catch (Exception e) {
            System.out.println("Exception is caught");
        }
    }
}
