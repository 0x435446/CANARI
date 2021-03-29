package com.example.proiect.Model.DomainWhiteListDB;


import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;

import com.example.proiect.Model.PacheteDB.Pachete;

import java.util.List;

@Dao
public interface _DomainWhitelist {
    @Insert
    void insert(DomainWhilelist domain);

    @Query("select*from DomainWhitelist")
    List<DomainWhilelist> getAll();

    @Query("DELETE FROM DomainWhitelist")
    public void nukeTable();

    @Query("DELETE FROM DomainWhitelist WHERE domain =:domeniu")
    void deleteDomain(String domeniu);
}
