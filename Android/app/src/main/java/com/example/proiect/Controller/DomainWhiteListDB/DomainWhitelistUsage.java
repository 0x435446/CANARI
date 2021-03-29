package com.example.proiect.Controller.DomainWhiteListDB;

import com.example.proiect.Controller.Pachete.PacheteDB;
import com.example.proiect.Model.DomainWhiteListDB.DomainWhilelist;
import com.example.proiect.Model.Pipe;
import com.example.proiect.View.DomainWhiteListView;

import java.util.ArrayList;
import java.util.List;

public class DomainWhitelistUsage {

    public DomainWhitelistUsage() {
    }

    public void addDomain(DomainWhilelist domain){
        Pipe x = Pipe.getInstance();
        x.setDomainlist(domain);
        PacheteDB db = PacheteDB.getInstance(x.getContext());
        db.getDomainWhiteListDao().insert(domain);
    }

    public List<DomainWhilelist> getDomains(){
        Pipe x = Pipe.getInstance();
        PacheteDB db = PacheteDB.getInstance(x.getContext());
        List<DomainWhilelist> lista = db.getDomainWhiteListDao().getAll();
        System.out.println("AICI E LISTA BA:   "+lista);
        return lista;

    }
}
