package com.example.proiect;

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
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;

public class Traffic implements Runnable{

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


    





    private String getPayload(String Text,List<String> TLD) throws IOException {
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
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            forReturn.remove(forReturn.size() - 1);
           return String.join(".", forReturn);
        }
        return "Nope";
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
            List<String> TLD = Arrays.asList(getTLD().split("\n"));
            while(1==1) {
                Process process = null;
                process = Runtime.getRuntime().exec(new String[]{"su", "-c", "tcpdump -c1 -l -v -n -t port 53 2>/dev/null"});
                //process = Runtime.getRuntime().exec(new String[]{"su", "-c", "pwd"});
                BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
                int read;
                char[] buffer = new char[8192];
                StringBuilder output = new StringBuilder();
                while ((read = in.read(buffer)) > 0) {
                    output.append(buffer, 0, read);
                }
                Pipe x = Pipe.getInstance();
                x.setTraffic(get_Source(output.toString()));
                String URL = get_URL(output.toString());
                x.setTraffic(URL);
                x.setTraffic(getPayload(URL,TLD));
                x.setTraffic(output.toString());
            }
        }
        catch (Exception e) {
            Pipe x= Pipe.getInstance();
            System.out.println("Exception is caught");
        }

    }
}