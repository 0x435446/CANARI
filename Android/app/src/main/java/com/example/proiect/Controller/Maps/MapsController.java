package com.example.proiect.Controller.Maps;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class MapsController {

    public String findLocation(String IP) throws IOException {
        //URL url = new URL("http://hack-it.ro:8000/signatures.txt");
        URL url = new URL("http://api.ipstack.com/"+IP+"?access_key=9abe92f65e5577a6838f483bedce2c6e");
        HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
        try {
            InputStream in = new BufferedInputStream(urlConnection.getInputStream());
            String text = null;
            try (Scanner scanner = new Scanner(in, StandardCharsets.UTF_8.name())) {
                text = scanner.useDelimiter("\\A").next();
            }
            return text;
        }
        finally {
            urlConnection.disconnect();
        }
    }

    public MapsController() throws IOException {
    }

}
