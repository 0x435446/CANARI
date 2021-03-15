package com.example.proiect.View;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import com.example.proiect.Controller.Applications.ApplicationsHandler;
import com.example.proiect.Model.Pipe;
import com.example.proiect.R;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class See_apps extends AppCompatActivity {



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_see_apps);
        Button btnPrint = findViewById(R.id.PrintApps);
        btnPrint.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    ApplicationsHandler z = new ApplicationsHandler();
                    ArrayList<ArrayList<String>> forret= new ArrayList<ArrayList<String>>();
                    forret=z.Check_apps();

                    ArrayList<String> forprint = forret.get(0);
                    ArrayList<String> forlongprint =  forret.get(1);
                    ListView g = (ListView) findViewById(R.id.listViewApps);
                    ArrayAdapter adapter = new ArrayAdapter(getApplicationContext(), android.R.layout.simple_list_item_1, forprint);
                    g.setAdapter(adapter);
                    g.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener() {
                        @Override
                        public boolean onItemLongClick(AdapterView<?> adapterView, View view, int i, long l) {
                            Toast.makeText(getApplicationContext(), forlongprint.get(i), Toast.LENGTH_LONG).show();
                            return false;
                        }
                    });
                }
                catch (Exception e){
                    Toast.makeText(getApplicationContext(),"Sorry, you need a rooted device",Toast.LENGTH_LONG).show();
                }
            }
        });
    }

}