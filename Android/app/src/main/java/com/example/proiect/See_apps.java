package com.example.proiect;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Context;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.GridView;
import android.widget.ListView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class See_apps extends AppCompatActivity {


    private void Check_apps(){
        Pipe x = Pipe.getInstance();
        //Toast.makeText(getApplicationContext(),x.getApps(),Toast.LENGTH_LONG).show();
        try {
            ListView g = (ListView) findViewById(R.id.listViewApps);
            List<String> spanac = Arrays.asList(x.getApps().split("\n"));
            ArrayList<String> forprint = new ArrayList<String>();
            ArrayList<String> forlongprint = new ArrayList<String>();
            for (int i=0 ;i <spanac.size();i++){
                try {
                    forprint.add(spanac.get(i).split(" ")[0]);
                    forlongprint.add(spanac.get(i).split(" ")[2].split("/")[3].split("-")[0]);
                }
                catch (Exception e){
                    forprint.add(spanac.get(i).split(" ")[0]);
                }
            }
            ArrayAdapter adapter = new ArrayAdapter(getApplicationContext(), android.R.layout.simple_list_item_1,forprint);
            g.setAdapter(adapter);
            g.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener() {
                @Override
                public boolean onItemLongClick(AdapterView<?> adapterView, View view, int i, long l) {
                    Toast.makeText(getApplicationContext(),forlongprint.get(i),Toast.LENGTH_LONG).show();
                    return false;
                }
            });
        }
        catch (Exception e){
            Toast.makeText(getApplicationContext(),"Sorry, you need a rooted device",Toast.LENGTH_LONG).show();
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_see_apps);
        Button btnPrint = findViewById(R.id.PrintApps);
        btnPrint.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Check_apps();
                //Toast.makeText(getApplicationContext(),getApplicationContext().getApplicationInfo().dataDir,Toast.LENGTH_LONG).show();
            }
        });
    }

}