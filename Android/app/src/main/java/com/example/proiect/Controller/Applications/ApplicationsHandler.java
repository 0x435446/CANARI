package com.example.proiect.Controller.Applications;

import com.example.proiect.Model.Pipe;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ApplicationsHandler {
    public ApplicationsHandler() {
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
