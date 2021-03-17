package com.example.proiect.Model;

import java.util.ArrayList;

public class HTTP implements Protocols{

    private String IP;
    private int freq;
    private ArrayList<Long> date;

    public ArrayList<Long> getDate() {
        return date;
    }

    public void setDate(Long date) {
        this.date.add(date);
    }

    public int getFreq() {
        return freq;
    }

    public void setFreq(int pings) {
        this.freq = pings;
    }

    public String getIP() {
        return IP;
    }

    public void setIP(String IP) {
        this.IP = IP;
    }

    public HTTP() {
        this.IP="";
        this.date = new ArrayList<>();
        this.freq = 0;
    }

}
