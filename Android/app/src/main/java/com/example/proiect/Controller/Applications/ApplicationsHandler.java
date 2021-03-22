package com.example.proiect.Controller.Applications;

import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.GridView;
import android.widget.ListView;
import android.widget.Toast;

import com.example.proiect.Model.Pipe;
import com.example.proiect.R;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Scanner;

public class ApplicationsHandler {
    public ApplicationsHandler() {
    }



    public ArrayList<String> checkJSON(String JSON, boolean ok) throws JSONException {

        ArrayList<String> Lista = new ArrayList<>();
        Lista.add("API");
        Lista.add("Website");
        Lista.add("Rezultat");
        Lista.add("Risc");
        Lista.add("Application");
        try {
            JSON = JSON.replace("[", "").replace("]", "").replace("\"", "");
            JSONArray jsonarray = new JSONArray("[" + JSON + "]");

            ApplicationsHandler z = new ApplicationsHandler();
            ArrayList<ArrayList<String>> forret = new ArrayList<ArrayList<String>>();
            forret = z.Check_apps();
            ArrayList<String> forlongprint = forret.get(1);

            for (int i = 0; i < jsonarray.length(); i++) {
                JSONObject obj = jsonarray.getJSONObject(i);
                try {
                    JSONObject reader = obj;
                    Iterator<String> keys = reader.getJSONObject("scans").keys();
                    while (keys.hasNext()) {
                        String cheie = keys.next();
                        if (!ok) {
                            Lista.add("VirusTotal");
                            Lista.add(cheie);
                            Lista.add(reader.getJSONObject("scans").getJSONObject(cheie).getString("result"));
                            if (!reader.getJSONObject("scans").getJSONObject(cheie).getString("result").contains("None"))
                                Lista.add("HIGH");
                            else
                                Lista.add("None");
                            Lista.add(forlongprint.get(i));
                        }
                        else{
                            if (reader.getJSONObject("scans").getJSONObject(cheie).getString("detected").equals("true")) {
                                Lista.add("VirusTotal");
                                Lista.add(cheie);
                                Lista.add(reader.getJSONObject("scans").getJSONObject(cheie).getString("result"));
                                if (!reader.getJSONObject("scans").getJSONObject(cheie).getString("result").contains("None"))
                                    Lista.add("HIGH");
                                else
                                    Lista.add("None");
                                Lista.add(forlongprint.get(i));
                            }
                        }
                    }
                } catch (Exception ignored) {

                }
            }
        }
        catch (Exception ignored){
        }

        return Lista;

    }










    public void sendAPK(String forGET) throws IOException {
        URL url = new URL("http://192.168.150.130:5000/checkAndroid?sha="+forGET);
        HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
        try {
            InputStream in = new BufferedInputStream(urlConnection.getInputStream());
            String text = null;
            try (Scanner scanner = new Scanner(in, StandardCharsets.UTF_8.name())) {
                text = scanner.useDelimiter("\\A").next();
            }
        }
        finally {
            urlConnection.disconnect();
        }
    }



    public String getInfo()throws IOException {
        URL url = new URL("http://192.168.150.130:5000/checkHashes");
        HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
        try {
            InputStream in = new BufferedInputStream(urlConnection.getInputStream());
            String text = null;
            try (Scanner scanner = new Scanner(in, StandardCharsets.UTF_8.name())) {
                text = scanner.useDelimiter("\\A").next();
                if (text.equals("None")){
                    return "None";
                }
                else{
                    return text;
                }
            }
        }
        finally {
            urlConnection.disconnect();
        }
    }


    public  ArrayList<ArrayList<String>> Check_apps() {
        Pipe x = Pipe.getInstance();
        List<String> spanac = Arrays.asList(x.getApps().split("\n"));
        ArrayList<String> forprint = new ArrayList<String>();
        ArrayList<String> forlongprint = new ArrayList<String>();
        ArrayList<ArrayList<String>> forret= new ArrayList<ArrayList<String>>();
        for (int i=0 ;i <spanac.size();i++){
            try {
                forprint.add(spanac.get(i).split(" ")[0]);
                forlongprint.add(spanac.get(i).split(" ")[2].split("/")[3].split("-")[0]);
                forret.add(forprint);
                forret.add(forlongprint);
            }
            catch (Exception e){
                forprint.add(spanac.get(i).split(" ")[0]);
                forret.add(forprint);
            }
        }
        return forret;
    }
}
