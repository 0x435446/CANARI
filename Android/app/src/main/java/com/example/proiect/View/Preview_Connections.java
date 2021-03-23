package com.example.proiect.View;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.drawerlayout.widget.DrawerLayout;

import android.content.Intent;
import android.os.Bundle;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.GridView;
import android.widget.Toast;

import com.example.proiect.Controller.Connections.ConnectionsHandler;
import com.example.proiect.Model.Pipe;
import com.example.proiect.R;
import com.google.android.material.navigation.NavigationView;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Preview_Connections extends AppCompatActivity {



    private DrawerLayout dl;
    private ActionBarDrawerToggle abdt;

    private void check_metasploit() {
        Pipe x = Pipe.getInstance();
        Toast.makeText(getApplicationContext(),x.getMetasploit(),Toast.LENGTH_LONG).show();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_preview_connections);

        Button Start = findViewById(R.id.startBtn3);
        Start.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ConnectionsHandler x = new ConnectionsHandler();
                ArrayList<String> result = x.check();
                GridView g = (GridView) findViewById(R.id.gridView);
                ArrayAdapter adapter = new ArrayAdapter(getApplicationContext(),android.R.layout.simple_list_item_1,result);
                g.setAdapter(adapter);
            }

        });


    }


}