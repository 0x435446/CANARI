package com.example.proiect.Controller.Applications;

import com.example.proiect.Model.Pipe;

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
import java.util.List;
import java.util.Scanner;

public class ApplicationsHandler {
    public ApplicationsHandler() {
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
