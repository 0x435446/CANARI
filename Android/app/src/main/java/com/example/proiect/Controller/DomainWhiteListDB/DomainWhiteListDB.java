package com.example.proiect.Controller.DomainWhiteListDB;

import android.content.Context;

import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;

import com.example.proiect.Controller.Pachete.PacheteDB;
import com.example.proiect.Model.DomainWhiteListDB.DomainWhilelist;
import com.example.proiect.Model.DomainWhiteListDB._DomainWhitelist;
import com.example.proiect.Model.PacheteDB.Pachete;
import com.example.proiect.Model.PacheteDB._Pachete;

@Database(entities = {Pachete.class,DomainWhilelist.class}, version = 2, exportSchema = false)
public abstract class DomainWhiteListDB extends RoomDatabase {

    private final static String DB_NAME="licenta.db";
    private static DomainWhiteListDB instance;

    public static DomainWhiteListDB getInstance(Context cnt){
        if (instance==null){
            instance= Room.databaseBuilder(cnt, DomainWhiteListDB.class, DB_NAME)
                    .allowMainThreadQueries()
                    .fallbackToDestructiveMigration()
                    .build();
            }
        return instance;
    }


    public abstract _DomainWhitelist getDomainWhiteListDao();
    public abstract _Pachete getPacheteDao();

}
