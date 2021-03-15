package com.example.proiect.Model;

import java.util.ArrayList;

public interface Protocols {
    public ArrayList<Long> getDate();

    public void setDate(Long date);

    public int getFreq();

    public void setFreq(int pings);

    public String getIP();

    public void setIP(String IP);
}
