package com.example.proiect;

import android.content.Intent;
import android.os.Build;
import android.os.StrictMode;

import androidx.annotation.RequiresApi;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Array;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.stream.Collectors;

public class TrafficDNS implements Runnable{

    private String get_Source(String Text){
        List<String> splited = new ArrayList<String>();
        splited = Arrays.asList(Text.split("\n")[1].split(" "));
        String Source = "NIMIC";
        for (int i=0 ; i<splited.size()-1; i++){
            if (splited.get(i).compareTo(">") ==  0){
                Source = splited.get(i - 1);
                break;
            }
        }
        String[] Thing = Source.split("\\.");
        List<String> list = new ArrayList<String>(Arrays.asList(Thing));
        list.remove(list.size()-1);
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            String joined = String.join(".", list);
            return joined;
        }
        else return "Teapa";
    }


    private String get_URL(String Text){
        String splited = "";
        splited = Text.split("\n")[1].split("\\?")[1].split(" ")[1];
        return splited;
    }

    void removeAll(List<String> list, String element) {
        while (list.contains(element)) {
            list.remove(element);
        }
    }

    public String getTLD() throws IOException {
        URL url = new URL("http://www.hack-it.ro:8000/IANA.txt");
        HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
        try {
            InputStream in = new BufferedInputStream(urlConnection.getInputStream());
            String text = null;
            try (Scanner scanner = new Scanner(in, StandardCharsets.UTF_8.name())) {
                text = scanner.useDelimiter("\\A").next();
            }
            System.out.println(text);
            return text;
        }
        finally {
            urlConnection.disconnect();
        }
    }

    public Map getProbabilitati() throws IOException {
        URL url = new URL("http://www.hack-it.ro:8000/probabilitati.txt");
        HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
        try {
            InputStream in = new BufferedInputStream(urlConnection.getInputStream());
            String text = null;
            try (Scanner scanner = new Scanner(in, StandardCharsets.UTF_8.name())) {
                text = scanner.useDelimiter("\\A").next();
            }
            System.out.println(text);
            Map<String, Integer> map = new HashMap<>();
            List <String> p = Arrays.asList(text.split("\n"));
            for (int i=0; i < p.size(); i++) {
                if(p.get(i).contains(":")) {
                    map.put(p.get(i).split(":")[0], Integer.parseInt(p.get(i).split(":")[1]));
                }
            }
            return map;
        }
        finally {
            urlConnection.disconnect();
        }
    }


    public int checkEncoding(Map p, String Payload){
        float Sum = 0;
        int nr = 0;
        for(int i=0 ;i<Payload.length()-1;i++){
            nr+= 1;
            StringBuilder sb = new StringBuilder();
            sb.append(Payload.charAt(i));
            sb.append(Payload.charAt(i+1));
            if (p.get(sb.toString())==null) {
                Sum+=0;
            }
            else{
                Sum+=Float.parseFloat(p.get(sb.toString()).toString());
            }
        }
        float medie = Sum/nr;
        if (medie < 10)
            return 0;
        return 1;
    }




    private List<String> getPayload(String Text,List<String> TLD) throws IOException {
        List<String> splited = new ArrayList<String>();
        splited = Arrays.asList(Text.split("\\."));
        List<String> forReturn = new ArrayList<String>();
        boolean ok = true;
        for (int i=0; i < splited.size(); i++){
            if (!TLD.contains(splited.get(i).toUpperCase())){
                if(!splited.get(i).equals("www")) {
                    forReturn.add(splited.get(i));
                    ok = false;
                }
            }
        }
        forReturn.remove(forReturn.size() - 1);
        return forReturn;
    }


    private boolean checkPayloadEncoding(String payload, Map probabilitati){
        if (checkEncoding(probabilitati,payload) == 0)
            return true;
        return false;
    }

    private boolean checkPayloadLength(String payload){
        if (payload.length() > 10)
            return true;
        return false;
    }

    private boolean checkPayloadNumberOfSubdomains(List<String> payload){
        if (payload.size() > 3)
            return true;
        return false;
    }


    public boolean checkPayloadNonAscii(String payload){
        for (int i=0;i<payload.length();i++){
            if (payload.charAt(i)<0x21 || payload.charAt(i) >127){
                System.out.println("Teapa");
                if(payload.charAt(i) != 0x0d || payload.charAt(i) != 0x0a)
                    return true;
            }
        }
        return false;
    }



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
    public void run()
    {
        /*
        try {
            Process process = null;
            process = Runtime.getRuntime().exec(new String[]{"su", "-c", "mkdir /data/user/0/com.example.proiect/files"});
            process.waitFor();
            process = Runtime.getRuntime().exec(new String[]{"su", "-c", "wget http://hack-it.ro:8000/tcpdump -O /data/user/0/com.example.proiect/files/tcpdump"});
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
         */
        try {
            Pipe x = Pipe.getInstance();
            x.setTraffic("Type");
            x.setTraffic("Message");
            x.setTraffic("Risk");
            x.setTraffic("Sursa");
            x.setTraffic("Destinatie");
            x.setTraffic("Payload");
            x.setTraffic("Timestamp");
            List<String> TLD = Arrays.asList(getTLD().split("\n"));
            while(1==1) {
                Process process = null;
                process = Runtime.getRuntime().exec(new String[]{"su", "-c", "tcpdump -c1 -l -v -n -t port 53 2>/dev/null"});
                BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
                int read;
                char[] buffer = new char[8192];
                StringBuilder output = new StringBuilder();
                while ((read = in.read(buffer)) > 0) {
                    output.append(buffer, 0, read);
                }
                String URL = get_URL(output.toString());
                Map Probabilitati = getProbabilitati();
                List <String> Payload = getPayload(URL,TLD);
                for(int i=0; i<Payload.size();i++){
                    if(checkPayloadEncoding(Payload.get(i), Probabilitati)){
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                            addTraffic("DNS", "UNKNOWN BASE FOUND!", "HIGH", get_Source(output.toString()), URL, String.join(".", Payload));
                        }

                    }
                    if(checkPayloadLength(Payload.get(i))){
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                            addTraffic("DNS", "SUBDOMAIN EXFILTRATION LENGTH", "HIGH", get_Source(output.toString()), URL, String.join(".", Payload));
                        }
                    }
                    if (checkPayloadNonAscii(Payload.get(i))){
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                            addTraffic("DNS", "NONASCII CHARS", "HIGH", get_Source(output.toString()), URL, String.join(".", Payload));
                        }
                    }
                }
                if(checkPayloadNumberOfSubdomains(Payload)){

                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                        addTraffic("DNS", "MULTIPLE SUBDOMAINS", "HIGH", get_Source(output.toString()), URL, String.join(".", Payload));
                    }


                }
            }
        }
        catch (Exception e) {
            Pipe x= Pipe.getInstance();
            System.out.println("Exception is caught");
        }

    }
}