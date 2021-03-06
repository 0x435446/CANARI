package com.example.proiect.Controller.Pachete;


import android.content.Context;

import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;

import com.example.proiect.Model.DomainWhiteListDB.DomainWhilelist;
import com.example.proiect.Model.DomainWhiteListDB._DomainWhitelist;
import com.example.proiect.Model.PacheteDB.Pachete;
import com.example.proiect.Model.PacheteDB._Pachete;

@Database(entities = {Pachete.class,DomainWhilelist.class}, version = 1, exportSchema = false)
public abstract class PacheteDB extends RoomDatabase {

    private final static String DB_NAME="licenta.db";
    private static PacheteDB instance;

    public static PacheteDB getInstance(Context cnt){
        if (instance==null){
            instance= Room.databaseBuilder(cnt, PacheteDB.class, DB_NAME)
                    .allowMainThreadQueries()
                    .fallbackToDestructiveMigration()
                    .build();
        }
        return instance;
    }


    public abstract _Pachete getPacheteDao();
    public abstract _DomainWhitelist getDomainWhiteListDao();

}
