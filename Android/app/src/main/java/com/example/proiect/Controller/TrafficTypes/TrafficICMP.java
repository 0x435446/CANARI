package com.example.proiect.Controller.TrafficTypes;

import android.os.Build;

import com.example.proiect.Controller.Pachete.PacheteDB;
import com.example.proiect.Model.Pachete;
import com.example.proiect.Model.Pipe;
import com.example.proiect.Model.ICMP;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.List;

public class TrafficICMP implements Runnable{


    void addTraffic(String TYPE,String MESSAGE, String RISK, String SURSA, String DESTINATIE, String PAYLOAD){
        Pipe x = Pipe.getInstance();
        x.setTraffic(TYPE);
        x.setTraffic(MESSAGE);
        x.setTraffic(RISK);
        x.setTraffic(SURSA);
        x.setTraffic(DESTINATIE);
        x.setTraffic(PAYLOAD);
        Calendar calendar = Calendar.getInstance();
        SimpleDateFormat formatter = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");
        System.out.println(formatter.format(calendar.getTime()));
        x.setTraffic(formatter.format(calendar.getTime()).toString());
        x.setICMPCount();

        Pachete fordb = new Pachete(TYPE,MESSAGE,RISK,SURSA,DESTINATIE,PAYLOAD,formatter.format(calendar.getTime()).toString());
        PacheteDB db = PacheteDB.getInstance(x.getContext());
        db.getPacheteDao().insert(fordb);
    }



    private boolean checkPayload(String Payload){
        if (Payload.compareTo("101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f3031323334353637")==0)
            return false;
        return true;
    }

    private boolean checkFreq(ArrayList<ICMP> pachete, String Destination){
        for(int i=0;i<pachete.size();i++){
            if(pachete.get(i).getIP().equals(Destination)) {
                if (pachete.get(i).getDate().size() > 3) {
                    if (pachete.get(i).getDate().get(pachete.get(i).getDate().size() - 1) - pachete.get(i).getDate().get(pachete.get(i).getDate().size() - 4) < 60) {
                        return true;
                    }
                }
            }
        }
        return false;
    }


    public void run()
    {
        try {
            ArrayList <ICMP> pachete = new ArrayList<>();
            while(1==1) {
                Process process = null;
                process = Runtime.getRuntime().exec(new String[]{"su", "-c", "tcpdump -x -c1 -l -v icmp[icmptype] == icmp-echo and icmp[icmptype] != icmp-echoreply 2>/dev/null"});
                BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
                int read;
                char[] buffer = new char[8192];
                StringBuilder output = new StringBuilder();
                while ((read = in.read(buffer)) > 0) {
                    output.append(buffer, 0, read);
                }
                List<String> pachet = Arrays.asList(output.toString().split("\n"));
                List <String> search = Arrays.asList(pachet.get(1).split(" "));
                String Destination = "";
                String Source = "";
                for (int i=0;i<search.size()-1;i++){
                    if(search.get(i).compareTo(">") == 0){
                        Source = search.get(i-1);
                        Destination = search.get(i+1);
                    }
                }
                ArrayList<String> hex = new ArrayList<>();
                for ( int i=2; i<pachet.size();i++){
                    hex.add(pachet.get(i).split(":")[1]);
                }
                String Payload = "";
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    Payload=String.join("", hex);
                }
                Payload=Payload.replace(" ","");
                Payload=Payload.replace("\n","");
                Payload=Payload.substring(88,Payload.length());

                boolean ok = true;
                for (int i=0;i<pachete.size();i++){
                    if(pachete.get(i).getIP().equals(Destination)){
                        pachete.get(i).setFreq(pachete.get(i).getFreq()+1);
                        Long currentTimestamp = System.currentTimeMillis()/1000;
                        pachete.get(i).setDate(currentTimestamp);
                        ok=false;
                    }
                }
                if (ok){
                    ICMP x = new ICMP();
                    x.setIP(Destination);
                    x.setFreq(0);
                    Long currentTimestamp = System.currentTimeMillis()/1000;
                    x.setDate(currentTimestamp);
                    pachete.add(x);
                }


                if(checkPayload(Payload))
                    addTraffic("ICMP","PADDING FAILED", "HIGH", Source, Destination, Payload);

                if(checkFreq(pachete,Destination)){
                    addTraffic("ICMP","HIGH FREQUENCY", "HIGH", Source, Destination, Payload);
                }



            }

        }
        catch (Exception e) {
            Pipe x= Pipe.getInstance();
            x.setCheckStatus(2);
            System.out.println("Exception is caught");
        }

    }
}
