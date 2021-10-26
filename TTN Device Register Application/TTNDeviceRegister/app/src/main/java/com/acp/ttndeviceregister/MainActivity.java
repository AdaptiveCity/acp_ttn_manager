package com.acp.ttndeviceregister;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    Button btnRegisterSingle, btnRegisterMultiple;
    EditText ttnAppNameBox;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initViews();
    }

    private void initViews() {
        btnRegisterSingle = findViewById(R.id.btnRegisterSingle);
        btnRegisterMultiple = findViewById(R.id.btnRegisterMultiple);
        ttnAppNameBox = findViewById(R.id.editBoxAppName);
        btnRegisterSingle.setOnClickListener(this);
        btnRegisterMultiple.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()){
            case R.id.btnRegisterSingle:
                Intent singleRegisterIntent = new Intent(MainActivity.this, RegisterSingleDeviceActivity.class);
                singleRegisterIntent.putExtra("ttnAppName",ttnAppNameBox.getText());
                startActivity(singleRegisterIntent);
                break;
            case R.id.btnRegisterMultiple:
                Intent multiRegisterIntent = new Intent(MainActivity.this, RegisterMultipleDeviceActivity.class);
                multiRegisterIntent.putExtra("ttnAppName",ttnAppNameBox.getText());
                startActivity(multiRegisterIntent);
                break;
        }

    }
}
