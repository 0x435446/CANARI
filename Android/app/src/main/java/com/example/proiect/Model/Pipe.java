package com.example.proiect.Model;

import android.content.Context;

import com.example.proiect.Model.DomainWhiteListDB.DomainWhilelist;
import com.example.proiect.View.DomainWhiteListView;

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
    private Context context;
    private int checkStatus;
    private int lengthStatus;
    private int DNSCount;
    private int HTTPCount;
    private int ICMPCount;
    private List<DomainWhilelist> domainlist;

    public List<DomainWhilelist> getDomainlist() {
        return domainlist;
    }

    public void setDomainlist(DomainWhilelist domainlist) {
        this.domainlist.add(domainlist);
    }

    public int getDNSCount() {
        return DNSCount;
    }

    public void setDNSCount() {
        this.DNSCount += 1;
    }

    public int getHTTPCount() {
        return HTTPCount;
    }

    public void setHTTPCount() {
        this.HTTPCount += 1;
    }

    public int getICMPCount() {
        return ICMPCount;
    }

    public void setICMPCount() {
        this.ICMPCount += 1;
    }

    public int getLengthStatus() {
        return lengthStatus;
    }

    public void setLengthStatus(int lengthStatus) {
        this.lengthStatus = lengthStatus;
    }

    public int getCheckStatus() {
        return checkStatus;
    }

    public void setCheckStatus(int checkStatus) {
        this.checkStatus = checkStatus;
    }

    public Context getContext() {
        return context;
    }

    public void setContext(Context context) {
        this.context = context;
    }

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

    private Pipe(){
        this.traffic=new ArrayList<String>();
        this.checkStatus = 0;
    }


    // static method to create instance of Singleton class
    public static Pipe getInstance()
    {
        if (single_instance == null)
            single_instance = new Pipe();

        return single_instance;
    }

}
