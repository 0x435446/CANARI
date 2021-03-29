package com.example.proiect.Model.PacheteDB;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "pachete")
public class Pachete {

    @PrimaryKey(autoGenerate = true)
    private int id;

    private String type;
    private String message;
    private String risk;
    private String sursa;
    private String destinatie;
    private String payload;
    private String timestamp;

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getRisk() {
        return risk;
    }

    public void setRisk(String risk) {
        this.risk = risk;
    }

    public String getSursa() {
        return sursa;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setSursa(String sursa) {
        this.sursa = sursa;
    }

    public String getDestinatie() {
        return destinatie;
    }

    public void setDestinatie(String destinatie) {
        this.destinatie = destinatie;
    }

    public String getPayload() {
        return payload;
    }

    public void setPayload(String payload) {
        this.payload = payload;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public Pachete(String type, String message, String risk, String sursa, String destinatie, String payload, String timestamp) {
        this.type = type;
        this.message = message;
        this.risk = risk;
        this.sursa = sursa;
        this.destinatie = destinatie;
        this.payload = payload;
        this.timestamp = timestamp;
    }
}
