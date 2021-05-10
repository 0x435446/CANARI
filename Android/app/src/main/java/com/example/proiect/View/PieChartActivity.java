package com.example.proiect.View;
import androidx.appcompat.app.AppCompatActivity;
import android.graphics.Color;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.Toast;

import org.eazegraph.lib.charts.PieChart;
import org.eazegraph.lib.models.PieModel;

import com.example.proiect.Controller.Pachete.PacheteDB;
import com.example.proiect.Model.DomainWhiteListDB.DomainWhilelist;
import com.example.proiect.Model.PacheteDB.Pachete;
import com.example.proiect.Model.Pipe;
import com.example.proiect.R;

import java.util.List;

public class PieChartActivity extends AppCompatActivity {

    TextView tICMP, tHTTP, tDNS, tvJava;
    PieChart pieChart;
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pie_chart);
        tICMP = findViewById(R.id.tICMP);
        tHTTP = findViewById(R.id.tHTTP);
        tDNS = findViewById(R.id.tDNS);
        pieChart = findViewById(R.id.piechart);
        setData();
    }

    private void setData()
    {
        PacheteDB db = PacheteDB.getInstance(getApplication());
        db = PacheteDB.getInstance(getApplicationContext());
        List<Pachete> ICMP = db.getPacheteDao().getSpecific("ICMP");
        List<Pachete> DNS = db.getPacheteDao().getSpecific("DNS");
        List<Pachete> HTTP = db.getPacheteDao().getSpecific("HTTP");
        tICMP.setText(Integer.toString(ICMP.size()));
        tHTTP.setText(Integer.toString(HTTP.size()));
        tDNS.setText(Integer.toString(DNS.size()));
        pieChart.addPieSlice(
                new PieModel(
                        "ICMP",
                        Integer.parseInt(tICMP.getText().toString()),
                        Color.parseColor("#FFA726")));
        pieChart.addPieSlice(
                new PieModel(
                        "HTTP",
                        Integer.parseInt(tHTTP.getText().toString()),
                        Color.parseColor("#66BB6A")));
        pieChart.addPieSlice(
                new PieModel(
                        "DNS",
                        Integer.parseInt(tDNS.getText().toString()),
                        Color.parseColor("#EF5350")));
        pieChart.startAnimation();
    }
}