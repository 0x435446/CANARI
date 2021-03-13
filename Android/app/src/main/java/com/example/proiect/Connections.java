package com.example.proiect;

import android.widget.ArrayAdapter;
import android.widget.ListView;

import androidx.appcompat.app.AppCompatActivity;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class Connections  implements Runnable  {

    public void run()
    {
        try {
            while(1 == 1) {
                TimeUnit.SECONDS.sleep(1);
                Process process = null;
                process = Runtime.getRuntime().exec("netstat -tulpn");
                BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
                int read;
                char[] buffer = new char[4096];
                StringBuilder output = new StringBuilder();
                while ((read = in.read(buffer)) > 0) {
                    output.append(buffer, 0, read);
                }
                Pipe x=Pipe.getInstance();
                x.setOutput(output.toString());
            }
        }
        catch (Exception e) {
            System.out.println("Exception is caught");
        }
    }
}
