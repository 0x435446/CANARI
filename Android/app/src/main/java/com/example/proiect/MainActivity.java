package com.example.proiect;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.IntentFilter;
import android.net.ConnectivityManager;
import android.os.Bundle;
import android.os.StrictMode;
import android.provider.Telephony;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.GridView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.proiect.CheckApps;
import com.example.proiect.Connections;
import com.example.proiect.Metasploit;
import com.example.proiect.Pipe;
import com.example.proiect.R;
import com.example.proiect.See_apps;
import com.example.proiect.Traffic;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;





public class MainActivity extends AppCompatActivity {
    private void check(){
        Pipe x= Pipe.getInstance();
        ArrayList<String> result= new ArrayList<String>();
        List<String> str = new ArrayList<String>();
        List<String> str2 = new ArrayList<String>();
        str= Arrays.asList(x.getOutput().toString().split("\n"));
        for (int i = 1; i < str.size(); i++){
            if ((!str.get(i).contains("0.0.0.0")) && (!str.get(i).contains(":::"))) {
                String fanci = str.get(i);
                List<String> listaString= Arrays.asList(fanci.split(" "));
                int number = 0;
                for (int k=0;k<listaString.size();k++) {
                        String string = listaString.get(k);
                        if (string != null && !string.isEmpty()) {
                            number += 1;
                            try {
                                if (number == 4 || number == 5 || number == 6)
                                    result.add(string.replace("::ffff:", "").split(":")[0]);
                            }
                            catch (Exception ignored){

                            }
                        }
                    }

                System.out.println(result);
                str2.add(String.valueOf(result));
            }
        }
        GridView g = (GridView) findViewById(R.id.gridView);
        ArrayAdapter adapter = new ArrayAdapter(getApplicationContext(),android.R.layout.simple_list_item_1,result);
        g.setAdapter(adapter);
    }



    private void check_metasploit(){
        Pipe x = Pipe.getInstance();
        Toast.makeText(getApplicationContext(),x.getMetasploit(),Toast.LENGTH_LONG).show();
    }



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (android.os.Build.VERSION.SDK_INT > 9)
        {
            StrictMode.ThreadPolicy policy = new
                    StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }
        setContentView(R.layout.activity_main);

        Thread object
                = new Thread(new Connections());
        object.start();

        Thread object2
                = new Thread(new Metasploit());
        object2.start();

        Thread object3
                = new Thread(new CheckApps());
        object3.start();

        Thread object4
                = new Thread(new Traffic());
        object4.start();

        Button Start = findViewById(R.id.startBtn);
        Start.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                check();
            }

        });


        Button Metasploit = findViewById(R.id.startBtn2);
        Metasploit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                check_metasploit();

            }

        });

        Button Traffic = findViewById(R.id.Traffic);
        Traffic.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent it = new Intent(getApplicationContext(), Preview_traffic.class);
                startActivityForResult(it,2);
            }
        });

    }



    public void open_see_apps(View view) {
        Intent it = new Intent(getApplicationContext(), See_apps.class);
        startActivityForResult(it,1);
    }

    /*
    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 1){
            if (resultCode == RESULT_OK){

            }
        }
    }
     */
}

