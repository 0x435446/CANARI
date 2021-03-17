package com.example.proiect.Controller.TrafficTypes;

import android.os.Build;
import android.widget.Toast;

import com.example.proiect.Model.ICMP;
import com.example.proiect.Model.Pipe;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.List;

public class TrafficHTTP implements Runnable {

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
    }

    public TrafficHTTP() {

    }

    private boolean checkUserAgent(String UserAgent){
        return false;
    }

    private boolean checkCookies(String Cookie){
        return false;
    }

    private boolean checkGET(String Cookie){
        return false;
    }

    public void parseRequest(String request){
        String Sursa = "";
        String Destinatia = "";
        String Payload = "";
        String UserAgent = "";
        String Cookie = "";
        List<String> requestList = Arrays.asList(request.split("\n"));
        for (int i=0; i<requestList.size(); i++){
            String bucatica = requestList.get(i);
            List<String> aux = Arrays.asList(bucatica.split(" "));
            if (Sursa.equals("")){
                for (int j = 0; j < aux.size()-1; j++){
                        if(aux.get(j).equals(">")){
                            String[] Thing = aux.get(j-1).split("\\.");
                            List<String> list = new ArrayList<String>(Arrays.asList(Thing));
                            list.remove(list.size()-1);
                            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                                Sursa = String.join(".", list);
                            }
                            break;
                        }
                    }
                }
            else {

                try {
                    if (aux.get(0).contains("User-Agent")) {
                        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                            UserAgent = String.join(" ", aux);
                            UserAgent=UserAgent.replace("User-Agent: ","");
                        }
                    }
                    if (aux.get(0).contains("Host")) {
                        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                            Destinatia = String.join(" ", aux);
                            Destinatia=Destinatia.replace("Host: ","");
                        }
                    }
                    if (aux.get(0).contains("Cookie")) {
                        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                            Cookie = String.join(" ", aux);
                            Cookie=Cookie.replace("Cookie: ","");
                        }
                    }


                }
                catch (Exception ignored){

                }


            }
        }

        addTraffic("HTTP",UserAgent,"HIGH",Sursa,Destinatia,Cookie);

    }

    public void run() {
        try {
            ArrayList<ICMP> pachete = new ArrayList<>();
            while (1 == 1) {
                Process process = null;
                process = Runtime.getRuntime().exec(new String[]{"su", "-c", "tcpdump -v -A -s 0 'tcp dst port http and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)' -c 1 2>/dev/null"});
                BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
                int read;
                char[] buffer = new char[8192];
                StringBuilder output = new StringBuilder();
                while ((read = in.read(buffer)) > 0) {
                    output.append(buffer, 0, read);
                }

                parseRequest(output.toString());

            }
        } catch (Exception e) {
            System.out.println("Exception is caught");
        }
    }
}


