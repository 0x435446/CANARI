package com.example.proiect.View;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.GridView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.proiect.Controller.Maps.MapsController;
import com.example.proiect.Controller.Pachete.PacheteDB;
import com.example.proiect.Controller.TrafficTypes.CustomAdapter;
import com.example.proiect.Controller.TrafficTypes.Traffic;
import com.example.proiect.Model.Pipe;
import com.example.proiect.R;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Preview_traffic extends AppCompatActivity {

    private ListView listView;

    private ArrayList<Traffic> parseTraffic(){
        ArrayList<Traffic> traffic = new ArrayList<>();
        Pipe x = Pipe.getInstance();
        ArrayList<String> a = x.getTraffic();
        for(int i=0; i< a.size();i+=7){
            Traffic z = new Traffic();
            z.setType(a.get(i));
            z.setMessage(a.get(i+1));
            z.setRisk(a.get(i+2));
            z.setSursa(a.get(i+3));
            z.setDestinatie(a.get(i+4));
            z.setPayload(a.get(i+5));
            z.setTimestamp(a.get(i+6));
            traffic.add(z);
        }
        return traffic;
    }

    private void check_traffic(){
        Pipe x = Pipe.getInstance();
        TextView t = (TextView)findViewById((R.id.textView));
        t.setText(x.getTraffic().get(x.getTraffic().size()-2).toString());
        GridView g = (GridView) findViewById(R.id.gridViewTraffic);

        ArrayAdapter adapter = new ArrayAdapter(getApplicationContext(),android.R.layout.simple_list_item_1,x.getTraffic());
        g.setAdapter(adapter);

        listView=findViewById(R.id.listviewprocesoare);
        System.out.println("DA");
        CustomAdapter adapter2=new CustomAdapter(getApplicationContext(), R.layout.elemlistview, parseTraffic(), getLayoutInflater()) {
            @NonNull
            @Override
            public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
                View view = super.getView(position, convertView, parent);
                TextView traffic1 = view.findViewById(R.id.traffic1);
                TextView traffic2 = view.findViewById(R.id.traffic2);
                TextView traffic3 = view.findViewById(R.id.traffic3);
                TextView traffic4 = view.findViewById(R.id.traffic4);
                TextView traffic5 = view.findViewById(R.id.traffic5);
                TextView traffic6 = view.findViewById(R.id.traffic6);
                if (position%2 == 0) {
                    traffic1.setBackgroundColor(Color.LTGRAY);
                    traffic2.setBackgroundColor(Color.LTGRAY);
                    traffic3.setBackgroundColor(Color.LTGRAY);
                    traffic4.setBackgroundColor(Color.LTGRAY);
                    traffic5.setBackgroundColor(Color.LTGRAY);
                    traffic6.setBackgroundColor(Color.LTGRAY);
                }
                else{
                    traffic1.setBackgroundColor(Color.WHITE);
                    traffic2.setBackgroundColor(Color.WHITE);
                    traffic3.setBackgroundColor(Color.WHITE);
                    traffic4.setBackgroundColor(Color.WHITE);
                    traffic5.setBackgroundColor(Color.WHITE);
                    traffic6.setBackgroundColor(Color.WHITE);
                }
                return view;
            }
        };
        listView.setAdapter(adapter2);

        listView.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener() {
            @Override
            public boolean onItemLongClick(AdapterView<?> parent, View view, int position, long id) {
                Traffic aux = (Traffic)parent.getItemAtPosition(position);
                try {
                    MapsController maps = new MapsController();
                    String location = maps.findLocation("hack-it.ro");
                    Toast.makeText(getApplicationContext(),location,Toast.LENGTH_LONG).show();
                    JSONObject json = new JSONObject(location);
                    String lat = json.getString("latitude");
                    String lon = json.getString("longitude");
                    String city = json.getString("city");

                    Intent it = new Intent(getApplicationContext(), MapsActivity.class);
                    it.putExtra("lat",lat);
                    it.putExtra("lon",lon);
                    it.putExtra("city",city);
                    startActivityForResult(it,7);

                    Toast.makeText(getApplicationContext(), lat, Toast.LENGTH_LONG).show();
                } catch (IOException | JSONException e) {
                    e.printStackTrace();
                }

                return true;
            }
        });


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


        /*
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

         */


    }



}
