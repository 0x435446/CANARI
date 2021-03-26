package com.example.proiect.Controller.Pachete;

import com.example.proiect.Model.Pachete;
import com.example.proiect.Model.Pipe;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.List;

public class PacheteUsage {


    static void addTraffic(String TYPE, String MESSAGE, String RISK, String SURSA, String DESTINATIE, String PAYLOAD, String TIMESTAMP){
        Pipe x = Pipe.getInstance();
        x.setTraffic(TYPE);
        x.setTraffic(MESSAGE);
        x.setTraffic(RISK);
        x.setTraffic(SURSA);
        x.setTraffic(DESTINATIE);
        x.setTraffic(PAYLOAD);
        x.setTraffic(TIMESTAMP);
    }


    public void addPachet(List<Pachete> pachete){
        for(int i=0; i<pachete.size(); i++){
            addTraffic(pachete.get(i).getType(),
                    pachete.get(i).getMessage(),
                    pachete.get(i).getRisk(),
                    pachete.get(i).getSursa(),
                    pachete.get(i).getDestinatie(),
                    pachete.get(i).getPayload(),
                    pachete.get(i).getTimestamp());
        }
    }

}
