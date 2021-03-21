package com.example.proiect.View;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import com.example.proiect.Controller.Applications.ApplicationsHandler;
import com.example.proiect.R;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;

public class See_apps extends AppCompatActivity {

    private void checkJSON(String JSON) throws JSONException {


        JSON=JSON.replace("[","").replace("]","").replace("\"","");
        JSONArray jsonarray = new JSONArray("["+JSON+"]");
        ArrayList<String> Lista = new ArrayList<>();
        Lista.add("API\tWebsite\tRezultat\tRisc\tApplication");

        ApplicationsHandler z = new ApplicationsHandler();
        ArrayList<ArrayList<String>> forret= new ArrayList<ArrayList<String>>();
        forret=z.Check_apps();
        ArrayList<String> forlongprint =  forret.get(1);

        for(int i=0; i<jsonarray.length(); i++){
            JSONObject obj = jsonarray.getJSONObject(i);
            try {
                JSONObject reader = obj;
                Iterator<String> keys = reader.getJSONObject("scans").keys();
                while(keys.hasNext()) {
                    String cheie = keys.next();
                    if (reader.getJSONObject("scans").getJSONObject(cheie).getString("detected").equals("false")){
                        Lista.add("VirusTotal"+" "+cheie+ " "+ reader.getJSONObject("scans").getJSONObject(cheie).getString("result")+" HIGH " + forlongprint.get(i));
                    }
                }
            }
            catch (Exception ignored){

            }
        }


        ListView g = (ListView) findViewById(R.id.listViewApps);
        ArrayAdapter adapter = new ArrayAdapter(getApplicationContext(), android.R.layout.simple_list_item_1, Lista);
        g.setAdapter(adapter);



    }

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

        btnPrint.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                ApplicationsHandler z = new ApplicationsHandler();
                ArrayList<ArrayList<String>> forret= new ArrayList<ArrayList<String>>();
                forret=z.Check_apps();
                ArrayList<String> forprint = forret.get(0);
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    try {
                        z.sendAPK(String.join("|", forprint));
                        Toast.makeText(getApplicationContext(),"REQUEST SENT",Toast.LENGTH_LONG).show();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
                return false;
            }
        });


        Button btnMalware = findViewById(R.id.GetVuln);
        btnMalware.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ApplicationsHandler z = new ApplicationsHandler();
                try {
                    String JSON=z.getInfo();
                    checkJSON(JSON);
                    if (!JSON.equals("None")){
                    }
                } catch (IOException | JSONException e) {
                    Toast.makeText(getApplicationContext(),"TEAPAAAAA",Toast.LENGTH_LONG).show();
                    e.printStackTrace();
                }

            }
        });
    }

}