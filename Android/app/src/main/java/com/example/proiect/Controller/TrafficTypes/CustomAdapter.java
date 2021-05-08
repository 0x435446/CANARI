package com.example.proiect.Controller.TrafficTypes;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.example.proiect.R;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;


public class CustomAdapter extends ArrayAdapter<Traffic> {

    private Context cnt;
    private int resurse;
    private ArrayList<Traffic> procList;
    private LayoutInflater layoutInflater;


    public CustomAdapter(@NonNull Context context, int resource, ArrayList<Traffic> list, LayoutInflater layoutxInflater) {
        super(context,resource,list);
        this.cnt=context;
        this.resurse=resource;
        this.layoutInflater=layoutxInflater;
        this.procList= list;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        View view=layoutInflater.inflate(resurse, parent, false);
        Traffic prod =procList.get(position);
        if (prod!=null){
            TextView tv1=view.findViewById(R.id.traffic1);
            tv1.setText(prod.getType());
            TextView tv2=view.findViewById(R.id.traffic2);
            tv2.setText(prod.getMessage());
            TextView tv3=view.findViewById(R.id.traffic3);
            tv3.setText(prod.getRisk());
            TextView tv4=view.findViewById(R.id.traffic4);
            tv4.setText(prod.getSursa());
            TextView tv5=view.findViewById(R.id.traffic5);
            tv5.setText(prod.getDestinatie());
            TextView tv6=view.findViewById(R.id.traffic6);
            try {
                tv6.setText(prod.getPayload().substring(0, 15));
            }
            catch (Exception e){
                tv6.setText(prod.getPayload());
            }
        }
        System.out.println("AICI E"+position);



        return view;

    }
}
