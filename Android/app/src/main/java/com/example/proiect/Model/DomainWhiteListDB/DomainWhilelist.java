package com.example.proiect.Model.DomainWhiteListDB;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "DomainWhitelist")
public class DomainWhilelist {

    @PrimaryKey(autoGenerate = true)
    private int id;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    private String domain;

    public DomainWhilelist(String domain) {
        this.domain = domain;
    }

    public String getDomain() {
        return domain;
    }

    public void setDomain(String domain) {
        this.domain = domain;
    }
}
