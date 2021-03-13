package com.example.proiect;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.GridView;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Preview_Connections extends AppCompatActivity {
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
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_preview_connections);

        Button Start = findViewById(R.id.startBtn3);
        Start.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                check();
            }

        });
    }
}