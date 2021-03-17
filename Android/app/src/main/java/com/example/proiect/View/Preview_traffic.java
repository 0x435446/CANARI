package com.example.proiect.View;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.GridView;
import android.widget.TextView;

import com.example.proiect.Model.Pipe;
import com.example.proiect.R;

public class Preview_traffic extends AppCompatActivity {

    private void check_traffic(){
        Pipe x = Pipe.getInstance();
        /*
        ListView g = (ListView) findViewById(R.id.listViewTraffic);
        ArrayAdapter adapter = new ArrayAdapter(getApplicationContext(), android.R.layout.simple_list_item_1,x.getTraffic());
        g.setAdapter(adapter);
         */
        TextView t = (TextView)findViewById((R.id.textView));
        t.setText(x.getTraffic().get(x.getTraffic().size()-2).toString());
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