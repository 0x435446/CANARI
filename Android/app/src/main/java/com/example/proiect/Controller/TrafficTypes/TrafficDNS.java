package com.example.proiect.Controller.TrafficTypes;

import android.os.Build;
import android.widget.Toast;

import com.example.proiect.Controller.DomainWhiteListDB.DomainWhitelistUsage;
import com.example.proiect.Controller.Pachete.PacheteDB;
import com.example.proiect.Model.DomainWhiteListDB.DomainWhilelist;
import com.example.proiect.Model.PacheteDB.Pachete;
import com.example.proiect.Model.Pipe;
import com.example.proiect.Model.DNS;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Base64;
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

public class TrafficDNS implements Runnable{


    public boolean checkDomain(String Domain){
        DomainWhitelistUsage x = new DomainWhitelistUsage();
        List<DomainWhilelist> domains = x.getDomains();
        ArrayList<String> stringdomains = new ArrayList<>();
        for (int i = 0; i < domains.size(); i++) {
            stringdomains.add(domains.get(i).getDomain());
        }
        for (int i = 0; i < stringdomains.size(); i++) {
            if (stringdomains.get(i).replace(" ","").replace("\t","").replace("\n","").equals(Domain.replace(" ","").replace("\t","").replace("\n","")))
                return true;
        }
        return false;
    }

    public String hexToAscii(String hexStr) {
        StringBuilder output = new StringBuilder("");

        for (int i = 0; i < hexStr.length(); i += 2) {
            String str = hexStr.substring(i, i + 2);
            output.append((char) Integer.parseInt(str, 16));
        }

        return output.toString();
    }

    public String AsciiToBase64(String Text){
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            return Base64.getEncoder().encodeToString(Text.getBytes());
        }
        return "";
    }

    public boolean checkBase64(List<String> signatures,String Text){
        try {
            for(int i=0; i<signatures.size(); i++) {
                String Raw = hexToAscii(signatures.get(i).substring(0, signatures.get(i).length() - 1));
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                    String encodedString = Base64.getEncoder().encodeToString(Raw.getBytes());
                    if (Text.equals(encodedString)) {
                        return true;
                    }
                }
            }
        }
        catch (Exception ignored){

        }
        return false;
    }

    public List<String> loadSignatures() throws IOException {
        //URL url = new URL("http://hack-it.ro:8000/signatures.txt");
        URL url = new URL("http://10.10.15.32:8080/Android/signatures.txt");
        HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
        try {
            InputStream in = new BufferedInputStream(urlConnection.getInputStream());
            String text = null;
            try (Scanner scanner = new Scanner(in, StandardCharsets.UTF_8.name())) {
                text = scanner.useDelimiter("\\A").next();
            }
            List <String> signatures = Arrays.asList(text.split("\n"));
            return signatures;
        }
        finally {
            urlConnection.disconnect();
        }
    }

    public boolean checkSignature(String Payload,List<String> signatures) throws IOException {
        for(int i=0; i<signatures.size(); i++) {
            if (Payload.contains(signatures.get(i).substring(0, signatures.get(i).length() - 1))) {
                return true;
            }
        }
        return false;
    }


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
        URL url = new URL("http://10.10.15.32:8080/Android/IANA.txt");
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
        URL url = new URL("http://10.10.15.32:8080/Android/probabilitati.txt");
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
                if(payload.charAt(i) != 0x0d || payload.charAt(i) != 0x0a)
                    return true;
            }
        }
        return false;
    }

    private boolean checkForTXTRecord(String payload){
        if (payload.contains("TXT"))
            return true;
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
        x.setDNSCount();

        Pachete fordb = new Pachete(TYPE,MESSAGE,RISK,SURSA,DESTINATIE,PAYLOAD,formatter.format(calendar.getTime()).toString());
        PacheteDB db = PacheteDB.getInstance(x.getContext());
        db.getPacheteDao().insert(fordb);
    }

    private boolean checkFreq(ArrayList<DNS> pachete, String URL){
        for(int i=0;i<pachete.size();i++){
            if(pachete.get(i).getIP().equals(URL)){
                if(pachete.get(i).getFreq()>399) {
                    if (pachete.get(i).getDate().get(pachete.get(i).getDate().size() - 1) - pachete.get(i).getDate().get(pachete.get(i).getDate().size() - 400) < 3600) {
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
            ArrayList <DNS> pachete = new ArrayList<>();
            List<String> TLD = Arrays.asList(getTLD().split("\n"));
            List<String> Signatures = loadSignatures();
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
                if(URL.endsWith(".")) {
                    URL= URL.substring(0, URL.length() - 1);
                }
                Map Probabilitati = getProbabilitati();
                List<String> Payload = getPayload(URL, TLD);
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    URL = URL.replaceFirst(String.join(".", Payload), "");
                    if (URL.charAt(0) == '.')
                        URL = URL.replaceFirst("\\.", "");
                }
                if (!checkDomain(URL)) {
                    for (int i = 0; i < Payload.size(); i++) {



                        if (checkPayloadEncoding(Payload.get(i), Probabilitati)) {
                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                                addTraffic("DNS", "UNKNOWN BASE FOUND", "HIGH", get_Source(output.toString()), URL, String.join(".", Payload));
                            }

                        }
                        if (checkPayloadLength(Payload.get(i))) {
                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                                addTraffic("DNS", "SUBDOMAIN EXFILTRATION LENGTH", "HIGH", get_Source(output.toString()), URL, String.join(".", Payload));
                            }
                        }
                        if (checkPayloadNonAscii(Payload.get(i))) {
                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                                addTraffic("DNS", "NONASCII CHARS", "HIGH", get_Source(output.toString()), URL, String.join(".", Payload));
                            }
                        }
                        if (checkSignature(Payload.get(i), Signatures)) {
                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                                addTraffic("DNS", "SIGNATURE FOUND - HEX", "HIGH", get_Source(output.toString()), URL, String.join(".", Payload));
                            }
                        }
                        if (checkBase64(Signatures, Payload.get(i))) {
                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                                addTraffic("DNS", "SIGNATURE FOUND - Base64", "HIGH", get_Source(output.toString()), URL, String.join(".", Payload));
                            }
                        }
                    }
                    if (checkPayloadNumberOfSubdomains(Payload)) {
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                            addTraffic("DNS", "MULTIPLE SUBDOMAINS", "HIGH", get_Source(output.toString()), URL, String.join(".", Payload));
                        }
                    }
                    if (checkForTXTRecord(output.toString())) {
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                            addTraffic("DNS", "TXT RECORD", "MEDIUM", get_Source(output.toString()), URL, String.join(".", Payload));
                        }
                    }
                    boolean ok = true;
                    for (int i = 0; i < pachete.size(); i++) {
                        if (pachete.get(i).getIP().equals(URL)) {
                            pachete.get(i).setFreq(pachete.get(i).getFreq() + 1);
                            Long currentTimestamp = System.currentTimeMillis() / 1000;
                            pachete.get(i).setDate(currentTimestamp);
                            ok = false;
                            break;
                        }
                    }

                    if (ok) {
                        DNS z = new DNS();
                        z.setIP(URL);
                        z.setFreq(1);
                        Long currentTimestamp = System.currentTimeMillis() / 1000;
                        z.setDate(currentTimestamp);
                        pachete.add(z);
                    }
                    if (checkFreq(pachete, URL)) {
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                            addTraffic("DNS", "HIGH FREQUENCY", "HIGH", get_Source(output.toString()), URL, String.join(".", Payload));
                        }
                    }
                }
            }
        }
        catch (Exception e) {
            Pipe y= Pipe.getInstance();
            y.setCheckStatus(2);
            System.out.println("Exception is caught");
        }

    }
}