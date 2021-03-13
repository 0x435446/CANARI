package com.example.proiect;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.GridView;
import android.widget.ListView;
import android.widget.Toast;

import com.example.proiect.R;

import java.util.Arrays;
import java.util.List;

public class Preview_traffic extends AppCompatActivity {

    private void check_traffic(){
        Pipe x = Pipe.getInstance();
        /*
        ListView g = (ListView) findViewById(R.id.listViewTraffic);
        ArrayAdapter adapter = new ArrayAdapter(getApplicationContext(), android.R.layout.simple_list_item_1,x.getTraffic());
        g.setAdapter(adapter);
         */
        GridView g = (GridView) findViewById(R.id.gridViewTraffic);
        ArrayAdapter adapter = new ArrayAdapter(getApplicationContext(),android.R.layout.simple_list_item_1,x.getTraffic());
        g.setAdapter(adapter);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_preview_traffic);

        Button printTraffic = findViewById(R.id.printTraffic);
        printTraffic.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                check_traffic();
            }
        });
    }
}