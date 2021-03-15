package com.example.proiect.Controller.Connections;

import com.example.proiect.Model.Pipe;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ConnectionsHandler {
    public ConnectionsHandler() {
    }

    public ArrayList<String> check() {
        Pipe x = Pipe.getInstance();
        ArrayList<String> result = new ArrayList<String>();
        List<String> str = new ArrayList<String>();
        List<String> str2 = new ArrayList<String>();
        str = Arrays.asList(x.getOutput().toString().split("\n"));
        for (int i = 1; i < str.size(); i++) {
            if ((!str.get(i).contains("0.0.0.0")) && (!str.get(i).contains(":::"))) {
                String fanci = str.get(i);
                List<String> listaString = Arrays.asList(fanci.split(" "));
                int number = 0;
                for (int k = 0; k < listaString.size(); k++) {
                    String string = listaString.get(k);
                    if (string != null && !string.isEmpty()) {
                        number += 1;
                        try {
                            if (number == 4 || number == 5 || number == 6)
                                result.add(string.replace("::ffff:", "").split(":")[0]);
                        } catch (Exception ignored) {

                        }
                    }
                }

                System.out.println(result);
                str2.add(String.valueOf(result));
            }
        }
        return result;
    }
}
