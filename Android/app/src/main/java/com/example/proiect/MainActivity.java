package com.example.proiect;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;


public class MainActivity extends AppCompatActivity {


    private void check_metasploit() {
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
                = new Thread(new TrafficDNS());
        object4.start();


        Button Conn = findViewById(R.id.startBtn);
        Conn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent it = new Intent(getApplicationContext(), Preview_Connections.class);
                startActivityForResult(it,3);
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

}

