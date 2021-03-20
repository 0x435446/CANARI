package com.example.proiect.Model;

import java.util.ArrayList;
import java.util.List;

public class HTTP implements Protocols{

    private String IP;
    private int freq;
    private ArrayList<Long> date;
    private List<String> Cookies;
    private int CookiesNumber;
    private String UserAgent;
    private String GET;

    public String getGET() {
        return GET;
    }

    public void setGET(String GET) {
        this.GET = GET;
    }

    private int Malitios;

    public int getMalitios() {
        return Malitios;
    }

    public void setMalitios(int malitios) {
        Malitios = malitios;
    }

    public String getUserAgent() {
        return UserAgent;
    }

    public void setUserAgent(String userAgent) {
        UserAgent = userAgent;
    }

    public List<String> getCookies() {
        return Cookies;
    }

    public void setCookies(String cookies) {
        Cookies.add(cookies);
    }

    public int getCookiesNumber() {
        return CookiesNumber;
    }

    public void setCookiesNumber() {
        CookiesNumber = CookiesNumber + 1;
    }

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
        this.Cookies=new ArrayList<String>();
        this.CookiesNumber=0;
        this.Malitios = 0;
        this.UserAgent = "";
    }

}
