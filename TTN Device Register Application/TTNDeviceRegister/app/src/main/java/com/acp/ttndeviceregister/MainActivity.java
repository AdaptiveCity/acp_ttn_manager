package com.acp.ttndeviceregister;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    Button btnRegisterSingle, btnRegisterMultiple;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initViews();
    }

    private void initViews() {
        btnRegisterSingle = findViewById(R.id.btnRegisterSingle);
        btnRegisterMultiple = findViewById(R.id.btnRegisterMultiple);
        btnRegisterSingle.setOnClickListener(this);
        btnRegisterMultiple.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()){
            case R.id.btnRegisterSingle:
                startActivity(new Intent(MainActivity.this, RegisterSingleDeviceActivity.class));
                break;
            case R.id.btnRegisterMultiple:
                startActivity(new Intent(MainActivity.this, RegisterMultipleDeviceActivity.class));
                break;
        }

    }
}
