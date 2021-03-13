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
import java.util.Map;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;





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
                = new Thread(new Traffic());
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

