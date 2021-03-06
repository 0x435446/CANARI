package com.example.proiect.Controller.TrafficTypes;

import android.os.Build;

import com.example.proiect.Controller.DomainWhiteListDB.DomainWhitelistUsage;
import com.example.proiect.Controller.Pachete.PacheteDB;
import com.example.proiect.Model.DomainWhiteListDB.DomainWhilelist;
import com.example.proiect.Model.HTTP;
import com.example.proiect.Model.PacheteDB.Pachete;
import com.example.proiect.Model.Pipe;

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
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

public class TrafficHTTP implements Runnable {


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

    private boolean checkFreqCookies(ArrayList<HTTP> pachete, String Destination){
        for(int i=0;i<pachete.size();i++){
            if(pachete.get(i).getIP().equals(Destination)) {
                if (pachete.get(i).getDate().size() > 2) {
                    if (pachete.get(i).getDate().get(pachete.get(i).getDate().size() - 1) - pachete.get(i).getDate().get(pachete.get(i).getDate().size() - 3) < 60) {
                        return true;
                    }
                }
            }
        }
        return false;
    }



    public Map getProbabilitati() throws IOException {
        URL url = new URL("http://192.168.150.135:5000/AndroidFiles/probabilitati.txt");
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


    private boolean checkPayloadEncoding(String payload, Map probabilitati){
        if (checkEncoding(probabilitati,payload) == 0)
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
        x.setHTTPCount();

        Pachete fordb = new Pachete(TYPE,MESSAGE,RISK,SURSA,DESTINATIE,PAYLOAD,formatter.format(calendar.getTime()).toString());
        PacheteDB db = PacheteDB.getInstance(x.getContext());
        db.getPacheteDao().insert(fordb);
    }

    public TrafficHTTP() {

    }

    private boolean checkUserAgent(String UserAgent){
        return false;
    }

    private boolean checkCookies(String Cookie){
        List<String> Pieces = Arrays.asList(Cookie.split(";"));
        for (int i=0; i<Pieces.size(); i++){

        }
        return false;
    }

    private boolean checkCookie(String Cookie){
        return false;
    }




    private String checkGET(String GET,Map p){
        if (checkEncoding(p,GET) == 0){
            return GET;
        }
        return "NU";
    }


    public HTTP parseRequest(String request, Map Probabilitati){
        HTTP pachet = new HTTP();
        String Sursa = "";
        String Destinatia = "";
        String GET = "";
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
                            UserAgent = UserAgent.replace("User-Agent: ","");
                        }
                    }

                    if (aux.get(0).contains("Host")) {
                        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                            Destinatia = String.join(" ", aux);
                            Destinatia = Destinatia.replace("Host: ","");
                        }
                    }

                    if (aux.get(0).contains("Cookie")) {
                        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                            Cookie = String.join(" ", aux);
                            Cookie = Cookie.replace("Cookie: ","");
                        }
                    }
                }
                catch (Exception ignored){

                }


            }
            List<String> aux2 = Arrays.asList(bucatica.split("/"));
            if (GET.equals("")){
                int remember = 0;
                if(aux2.get(0).contains("GET")) {
                    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                        GET = String.join(" ", aux2);
                        GET = GET.replace("GET  ","");
                        GET = GET.replace("?","");
                        GET = GET.replace("\n","");
                        GET = GET.replace("\r","");
                        GET = GET.split("HTTP")[0];
                    }
                }
            }
        }

        pachet.setCookies(Cookie);
        pachet.setIP(Destinatia);
        pachet.setUserAgent(UserAgent);
        pachet.setGET(GET);
        pachet.setSursa(Sursa);
        List<String> forCheck = Arrays.asList(GET.split("&"));
        for (int k=0; k<forCheck.size(); k++) {
            List<String> Splited = Arrays.asList(forCheck.get(k).split("="));
            String GETresp="";
            String forView="";
            if(Splited.size() == 2) {
                forView=Splited.get(1);
                GETresp = checkGET(forView, Probabilitati);
            }
            else{
                forView=Splited.get(0);
                GETresp = checkGET(forView, Probabilitati);
            }
            if(!checkDomain(Destinatia)) {
                if (!GETresp.equals("NU")) {
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                        addTraffic("HTTP", "UNKNOWN BASE GET", "MEDIUM", Sursa, Destinatia, forView);
                    }
                }
            }
        }

        if(!checkDomain(Destinatia)) {
            if (checkPayloadEncoding(Cookie, Probabilitati)) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    addTraffic("HTTP", "UNKNOWN BASE COOKIE", "LOW", Sursa, Destinatia, Cookie);
                }
            }
        }
        return pachet;

    }

    public void run() {
        try {
            Map Probabilitati = getProbabilitati();

            ArrayList<HTTP> pachete = new ArrayList<>();
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

                HTTP pachet = parseRequest(output.toString(), Probabilitati);
                if (!checkDomain(pachet.getIP())) {
                    boolean ok = true;
                    for (int k = 0; k < pachete.size(); k++) {
                        if (pachete.get(k).getIP().equals(pachet.getIP())) {
                            pachete.get(k).setCookiesNumber(pachete.get(k).getCookiesNumber() + 1);
                            Long currentTimestamp = System.currentTimeMillis() / 1000;
                            pachete.get(k).setDate(currentTimestamp);
                            ok = false;
                        }
                    }
                    if (ok) {
                        pachet.setCookiesNumber(0);
                        Long currentTimestamp = System.currentTimeMillis() / 1000;
                        pachet.setDate(currentTimestamp);
                        pachete.add(pachet);
                    }

                    if (checkFreqCookies(pachete, pachet.getIP())) {
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                            addTraffic("HTTP", "COOKIES FREQUENCY", "MEDIUM", pachet.getSursa(), pachet.getIP(), "-");
                        }
                    }
                }
            }
        } catch (Exception e) {
            Pipe x= Pipe.getInstance();
            x.setCheckStatus(2);
            System.out.println("Exception is caught");
        }
    }
}


