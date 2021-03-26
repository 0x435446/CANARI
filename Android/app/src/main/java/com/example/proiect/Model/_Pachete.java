package com.example.proiect.Model;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import java.util.List;

@Dao
public interface _Pachete {
@Insert
void insert(Pachete pachet);

@Query("select*from pachete")
    List<Pachete> getAll();

@Query("DELETE FROM pachete")
    public void nukeTable();

}
