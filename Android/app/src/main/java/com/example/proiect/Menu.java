package com.example.proiect;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.drawerlayout.widget.DrawerLayout;

import android.content.Intent;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.MenuItem;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;





import com.example.proiect.Controller.Applications.ApplicationsHandler;
import com.example.proiect.Controller.Applications.CheckApps;
import com.example.proiect.Controller.Connections.Connections;
import com.example.proiect.Controller.Metasploit.Metasploit;
import com.example.proiect.Controller.Pachete.PacheteDB;
import com.example.proiect.Controller.Pachete.PacheteUsage;
import com.example.proiect.Controller.TrafficTypes.TrafficDNS;
import com.example.proiect.Controller.TrafficTypes.TrafficHTTP;
import com.example.proiect.Controller.TrafficTypes.TrafficICMP;
import com.example.proiect.Model.PacheteDB.Pachete;
import com.example.proiect.Model.Pipe;
import com.example.proiect.View.DomainWhiteListView;
import com.example.proiect.View.Preview_Connections;
import com.example.proiect.View.Preview_traffic;
import com.example.proiect.View.See_apps;
import com.google.android.material.navigation.NavigationView;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;


public class Menu extends AppCompatActivity {


    private void check_metasploit() {
        Pipe x = Pipe.getInstance();
        Toast.makeText(getApplicationContext(),x.getMetasploit(),Toast.LENGTH_LONG).show();
    }



    private DrawerLayout dl;
    private ActionBarDrawerToggle abdt;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);

        Pipe x = Pipe.getInstance();
        x.setTraffic("Type");
        x.setTraffic("Message");
        x.setTraffic("Risk");
        x.setTraffic("Sursa");
        x.setTraffic("Destinatie");
        x.setTraffic("Payload");
        x.setTraffic("Timestamp");
        x.setContext(getApplicationContext());
        if (android.os.Build.VERSION.SDK_INT > 9)
        {
            StrictMode.ThreadPolicy policy = new
                    StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        PacheteDB db = PacheteDB.getInstance(getApplication());
        List<Pachete> pachete = db.getPacheteDao().getAll();
        PacheteUsage p = new PacheteUsage();
        p.addPachet(pachete);


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
                = new Thread(new TrafficDNS());
        object4.start();

        Thread object5
                = new Thread(new TrafficICMP());
        object5.start();

        Thread object6
                = new Thread(new TrafficHTTP());
        object6.start();

        dl = (DrawerLayout)findViewById(R.id.dl);
        abdt = new ActionBarDrawerToggle(this, dl, R.string.Open, R.string.Close);

        dl.addDrawerListener(abdt);
        abdt.syncState();

        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        final NavigationView nav_view = (NavigationView)findViewById(R.id.nav_view);
        nav_view.setNavigationItemSelectedListener(new NavigationView.OnNavigationItemSelectedListener()
        {

            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                int id = item.getItemId();

                if(id==R.id.conexiuni)
                {
                    Intent it = new Intent(getApplicationContext(), Preview_Connections.class);
                    startActivityForResult(it,3);
                }

                if(id==R.id.metasploit)
                {
                    check_metasploit();
                }

                if(id==R.id.traffic)
                {
                    Intent it = new Intent(getApplicationContext(), Preview_traffic.class);
                    startActivityForResult(it,2);
                }
                if(id==R.id.aplicatii)
                {
                    Intent it = new Intent(getApplicationContext(), See_apps.class);
                    startActivityForResult(it,1);
                }
                if(id==R.id.Domains)
                {
                    Intent it = new Intent(getApplicationContext(), DomainWhiteListView.class);
                    startActivityForResult(it,4);
                }
                return true;
            }
        });

        try {
            TimeUnit.SECONDS.sleep(5);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("AICI E STATUSUL: "+x.getCheckStatus());
        if (x.getCheckStatus() == 2){
            Toast.makeText(getApplicationContext(),"You need a rooted device",Toast.LENGTH_LONG).show();
        }
        if(x.getCheckStatus() == 1){

            ApplicationsHandler z = new ApplicationsHandler();
            ArrayList<ArrayList<String>> forret = new ArrayList<ArrayList<String>>();
            forret = z.Check_apps();
            TextView text = (TextView) findViewById(R.id.textStatisticiUnu);
            text.setText("Aplicatii  instalate: "+x.getLengthStatus());
            TextView text2 = (TextView) findViewById(R.id.textStatisticiDoi);
            db = PacheteDB.getInstance(getApplicationContext());
            List<Pachete> a = db.getPacheteDao().getAll();
            int ICMPCount = 0;
            int HTTPCount = 0;
            int DNSCount = 0;

            for (int i = 0; i < a.size(); i++) {
                if (a.get(i).getType().equals("ICMP")) {
                    ICMPCount++;
                } else if (a.get(i).getType().equals("DNS")) {
                    DNSCount++;
                } else if (a.get(i).getType().equals("HTTP")) {
                    HTTPCount++;
                }
            }

            ProgressBar progressBar1;
            progressBar1 = findViewById(R.id.progressBar1);
            progressBar1.setMax(a.size());

            if(ICMPCount<=a.size()/3) {
                progressBar1.setProgressTintList(ColorStateList.valueOf(Color.parseColor("#28a100")));
            }
            else if(ICMPCount>a.size()/3) {
                if (ICMPCount <= (a.size()/3)*2) {
                    progressBar1.setProgressTintList(ColorStateList.valueOf(Color.parseColor("#ff8000")));
                }
                else{
                    progressBar1.setProgressTintList(ColorStateList.valueOf(Color.parseColor("#ff0000")));
                }
            }


            TextView progressICMP = findViewById(R.id.progressICMP);
            progressICMP.setText(ICMPCount+" / "+a.size());

            ProgressBar progressBar2;
            progressBar2 = findViewById(R.id.progressBar2);
            progressBar2.setMax(a.size());

            if(HTTPCount<=a.size()/3) {
                progressBar2.setProgressTintList(ColorStateList.valueOf(Color.parseColor("#28a100")));
            }
            else if(HTTPCount>a.size()/3) {
                if (HTTPCount <= (a.size()/3)*2) {
                    progressBar2.setProgressTintList(ColorStateList.valueOf(Color.parseColor("#ff8000")));
                }
                else{
                    progressBar2.setProgressTintList(ColorStateList.valueOf(Color.parseColor("#ff0000")));
                }
            }

            TextView progressHTTP = findViewById(R.id.progressHTTP);
            progressHTTP.setText(HTTPCount+" / "+a.size());

            ProgressBar progressBar3;
            progressBar3 = findViewById(R.id.progressBar3);
            progressBar3.setMax(a.size());

            if(DNSCount<=a.size()/3) {
                progressBar3.setProgressTintList(ColorStateList.valueOf(Color.parseColor("#28a100")));
            }
            else if(DNSCount>a.size()/3) {
                if (DNSCount <= (a.size()/3)*2) {
                    progressBar3.setProgressTintList(ColorStateList.valueOf(Color.parseColor("#ff8000")));
                }
                else{
                    progressBar3.setProgressTintList(ColorStateList.valueOf(Color.parseColor("#ff0000")));
                }
            }

            TextView progressDNS = findViewById(R.id.progressDNS);
            progressDNS.setText(DNSCount+" / "+a.size());

            progressBar1.setProgress(ICMPCount);
            progressBar2.setProgress(HTTPCount);
            progressBar3.setProgress(DNSCount);
        }
        else{
            Toast.makeText(getApplicationContext(),"You need a rooted device.",Toast.LENGTH_LONG).show();
        }

    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        return abdt.onOptionsItemSelected(item) || super.onOptionsItemSelected(item);
    }


}
