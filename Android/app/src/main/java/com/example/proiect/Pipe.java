package com.example.proiect;

import java.util.ArrayList;
import java.util.List;

public class Pipe {

    // static variable single_instance of type Singleton
    private static Pipe single_instance = null;

    // variable of type String
    public String s;
    private String output;
    private String metasploit;
    private String apps;
    private ArrayList<String> traffic;

    public ArrayList<String> getTraffic() {
        return traffic;
    }

    public void setTraffic(String traffic) {
        this.traffic.add(traffic);
    }

    public String getMetasploit() {
        return metasploit;
    }

    public void setMetasploit(String metasploit) {
        this.metasploit = metasploit;
    }

    public String getOutput() {
        return output;
    }

    public void setOutput(String output) {
        this.output = output;
    }

    public String getApps() {
        return apps;
    }

    public void setApps(String apps) {
        this.apps = apps;
    }

    // private constructor restricted to this class itself
    private Pipe(){
        this.traffic=new ArrayList<String>();
    }


    // static method to create instance of Singleton class
    public static Pipe getInstance()
    {
        if (single_instance == null)
            single_instance = new Pipe();

        return single_instance;
    }


}
