package com.example.proiect.Model;

import java.util.ArrayList;

public class ICMP {
    private String IP;
    private int pings;
    private ArrayList<Long> date;

    public ArrayList<Long> getDate() {
        return date;
    }

    public void setDate(Long date) {
        this.date.add(date);
    }

    public int getPings() {
        return pings;
    }

    public void setPings(int pings) {
        this.pings = pings;
    }

    public String getIP() {
        return IP;
    }

    public void setIP(String IP) {
        this.IP = IP;
    }

    public ICMP() {
        this.IP="";
        this.date = new ArrayList<>();
        this.pings = 0;
    }
}
