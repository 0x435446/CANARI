package com.example.proiect.View;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.content.DialogInterface;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.GridView;
import android.widget.TextView;

import com.example.proiect.Controller.Pachete.PacheteDB;
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
        check_traffic();
        Button printTraffic = findViewById(R.id.printTraffic);
        printTraffic.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                check_traffic();
            }
        });

        Button deleteDB = findViewById(R.id.deleteDB);
        deleteDB.setOnClickListener(new View.OnClickListener() {
        Pipe x = Pipe.getInstance();
            @Override
            public void onClick(View view) {
                AlertDialog.Builder builder = new AlertDialog.Builder(x.getContext());
                builder.setTitle("Confirm");
                builder.setMessage("Esti sigur ca vrei sa stergi toata baza de date?");
                builder.setPositiveButton("YES", new DialogInterface.OnClickListener() {

                    public void onClick(DialogInterface dialog, int which) {
                        // Do nothing but close the dialog
                        PacheteDB db = PacheteDB.getInstance(getApplicationContext());
                        db.getPacheteDao().nukeTable();
                        dialog.dismiss();
                    }
                });
                builder.setNegativeButton("NO", new DialogInterface.OnClickListener() {

                    @Override
                    public void onClick(DialogInterface dialog, int which) {

                        // Do nothing
                        dialog.dismiss();
                    }
                });
                AlertDialog alert = builder.create();
                alert.show();
            }
        });


    }
}
