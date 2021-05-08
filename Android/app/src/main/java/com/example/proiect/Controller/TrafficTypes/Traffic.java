package com.example.proiect.Controller.TrafficTypes;

public class Traffic {
    private String Type;
    private String Message;
    private String Risk;
    private String Sursa;
    private String Destinatie;
    private String Payload;
    private String Timestamp;


    public Traffic() {

    }

    public String getType() {
        return Type;
    }

    public void setType(String type) {
        Type = type;
    }

    public String getMessage() {
        return Message;
    }

    public void setMessage(String message) {
        Message = message;
    }

    public String getRisk() {
        return Risk;
    }

    public void setRisk(String risk) {
        Risk = risk;
    }

    public String getSursa() {
        return Sursa;
    }

    public void setSursa(String sursa) {
        Sursa = sursa;
    }

    public String getDestinatie() {
        return Destinatie;
    }

    public void setDestinatie(String destinatie) {
        Destinatie = destinatie;
    }

    public String getPayload() {
        return Payload;
    }

    public void setPayload(String payload) {
        Payload = payload;
    }

    public String getTimestamp() {
        return Timestamp;
    }

    public void setTimestamp(String timestamp) {
        Timestamp = timestamp;
    }


}
