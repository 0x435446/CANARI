package com.example.proiect.View;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.text.Editable;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import com.example.proiect.Controller.DomainWhiteListDB.DomainWhitelistUsage;
import com.example.proiect.Controller.Pachete.PacheteDB;
import com.example.proiect.Model.DomainWhiteListDB.DomainWhilelist;
import com.example.proiect.Model.PacheteDB.Pachete;
import com.example.proiect.Model.Pipe;
import com.example.proiect.R;

import java.util.ArrayList;
import java.util.List;

public class DomainWhiteListView extends AppCompatActivity {

    private ListView lv;

    private void getfromDomains(){
        DomainWhitelistUsage x = new DomainWhitelistUsage();
        List<DomainWhilelist> domains = x.getDomains();
        ArrayList<String> stringdomains = new ArrayList<>();
        for (int i = 0; i < domains.size(); i++) {
            stringdomains.add(domains.get(i).getDomain());
        }
        ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(
                this,
                android.R.layout.simple_list_item_1,
                stringdomains);
        lv = (ListView) findViewById(R.id.DomainView);
        lv.setAdapter(arrayAdapter);

    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_domain_white_list);

        this.getfromDomains();
        Button btnDomain = findViewById(R.id.buttonDomains);
        btnDomain.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                EditText et = findViewById(R.id.editTextDomains);
                Editable domeniu = et.getText();
                Pipe x = Pipe.getInstance();
                PacheteDB db = PacheteDB.getInstance(getApplicationContext());
                DomainWhilelist fordb = new DomainWhilelist(domeniu.toString());
                Toast.makeText(getApplicationContext(),fordb.getDomain(),Toast.LENGTH_LONG).show();
                db.getDomainWhiteListDao().insert(fordb);
                getfromDomains();
            }
        });
        btnDomain.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View view) {
                EditText et = findViewById(R.id.editTextDomains);
                PacheteDB db = PacheteDB.getInstance(getApplicationContext());
                Editable domeniu = et.getText();
                DomainWhilelist fordb = new DomainWhilelist(domeniu.toString());
                db.getDomainWhiteListDao().deleteDomain(domeniu.toString());
                getfromDomains();
                Toast.makeText(getApplicationContext(),domeniu.toString(),Toast.LENGTH_LONG).show();
                return true;
            }
        });

    }
}