package com.example.proiect.Model.PacheteDB;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;

import com.example.proiect.Model.DomainWhiteListDB.DomainWhilelist;

import java.util.List;

@Dao
public interface _Pachete {
    @Insert
    void insert(Pachete pachet);

    @Query("select*from pachete")
        List<Pachete> getAll();

    @Query("DELETE FROM pachete")
        public void nukeTable();

    @Query("SELECT * FROM pachete ORDER BY CASE WHEN :isAsc = 1 THEN ID END ASC, CASE WHEN :isAsc = 0 THEN ID END DESC")
    List<Pachete> getAllDesc(boolean isAsc);

    @Query("select*from pachete  WHERE type =:type")
    List<Pachete> getSpecific(String type);

}
