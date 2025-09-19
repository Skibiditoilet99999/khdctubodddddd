import os
import zipfile

project_name = "TTC_TikBot"

# --- 1. Tạo folder ---
folders = [
    f"{project_name}/app/src/main/java/com/ttctik/phuocan",
    f"{project_name}/app/src/main/res/layout",
    f"{project_name}/app/src/main/res/xml",
    f"{project_name}/app/src/main/res/values"
]
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# --- 2. Nội dung các file ---
files = {
    f"{project_name}/app/src/main/java/com/ttctik/phuocan/MainActivity.java": """package com.ttctik.phuocan;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.*;
import android.view.View;
import android.os.Handler;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import android.content.Intent;
import android.net.Uri;
import android.provider.Settings;
import android.view.WindowManager;
import android.graphics.PixelFormat;
import okhttp3.*;
import org.json.JSONArray;
import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {

    EditText tokenInput, uidInput, delayInput;
    Button startBtn;
    TextView logView;
    ScrollView scrollLog;

    OkHttpClient client = new OkHttpClient();
    ExecutorService executor = Executors.newSingleThreadExecutor();
    Handler handler = new Handler();

    private boolean running = false;
    private View stopButtonView;
    private int jobCount = 0;

    private final String userAgent = "Mozilla/5.0 (Android)";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tokenInput = findViewById(R.id.tokenInput);
        uidInput = findViewById(R.id.uidInput);
        delayInput = findViewById(R.id.delayInput);
        startBtn = findViewById(R.id.startBtn);
        logView = findViewById(R.id.logView);
        scrollLog = findViewById(R.id.scrollLog);

        startBtn.setOnClickListener(v -> {
            String token = tokenInput.getText().toString().trim();
            String uid = uidInput.getText().toString().trim();
            String delayStr = delayInput.getText().toString().trim();
            if(token.isEmpty() || uid.isEmpty() || delayStr.isEmpty()){
                Toast.makeText(this,"Vui lòng nhập đủ thông tin",Toast.LENGTH_SHORT).show();
                return;
            }
            int delaySec;
            try{ delaySec = Integer.parseInt(delayStr); } catch(Exception e){ delaySec = 3; }

            if(!Settings.canDrawOverlays(this)){
                Intent intent = new Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION, Uri.parse("package:" + getPackageName()));
                startActivity(intent);
                Toast.makeText(this,"Cấp quyền overlay trước khi bắt đầu",Toast.LENGTH_LONG).show();
                return;
            }

            if(!isAccessibilityEnabled()){
                Toast.makeText(this,"Vui lòng bật Accessibility cho app",Toast.LENGTH_LONG).show();
                startActivity(new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS));
                return;
            }

            log("Bắt đầu bot...");
            executor.execute(() -> runBot(token, uid, delaySec));
        });
    }

    private boolean isAccessibilityEnabled(){
        String setting = Settings.Secure.getString(getContentResolver(), Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES);
        return setting != null && setting.contains(getPackageName() + "/.TikTokAccessibilityService");
    }

    void log(String msg){
        handler.post(() -> {
            logView.append(msg + "\\n");
            handler.postDelayed(() -> scrollLog.fullScroll(View.FOCUS_DOWN),50);
        });
    }

    private void showStopOverlay(){
        WindowManager wm = (WindowManager)getSystemService(WINDOW_SERVICE);
        stopButtonView = new Button(this);
        ((Button)stopButtonView).setText("STOP");
        stopButtonView.setBackgroundColor(0xFFFF4500);
        stopButtonView.setAlpha(0.8f);

        WindowManager.LayoutParams params = new WindowManager.LayoutParams(
                WindowManager.LayoutParams.WRAP_CONTENT,
                WindowManager.LayoutParams.WRAP_CONTENT,
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
                PixelFormat.TRANSLUCENT
        );
        params.x = 50; params.y = 100;

        stopButtonView.setOnClickListener(v -> stopBot());
        wm.addView(stopButtonView, params);
    }

    private void stopBot(){
        running = false;
        if(stopButtonView != null){
            WindowManager wm = (WindowManager)getSystemService(WINDOW_SERVICE);
            wm.removeView(stopButtonView);
            stopButtonView = null;
        }
        log("Bot đã dừng!");
    }

    private JSONObject postType(String url, String data) {
        try {
            RequestBody body = RequestBody.create(data, MediaType.parse("application/x-www-form-urlencoded; charset=UTF-8"));
            Request request = new Request.Builder()
                    .url(url)
                    .header("User-Agent", userAgent)
                    .header("x-requested-with","XMLHttpRequest")
                    .header("accept","*/*")
                    .header("origin","https://tuongtaccheo.com")
                    .header("referer","https://tuongtaccheo.com/tiktok/kiemtien/subcheo/")
                    .post(body)
                    .build();
            Response res = client.newCall(request).execute();
            if(res.body() != null){
                return new JSONObject(res.body().string());
            }
        } catch(Exception e){}
        return new JSONObject();
    }

    private JSONArray getJobList() {
        try {
            Request request = new Request.Builder()
                    .url("https://tuongtaccheo.com/tiktok/kiemtien/subcheo/getpost.php")
                    .header("User-Agent",userAgent)
                    .header("x-requested-with","XMLHttpRequest")
                    .build();
            Response res = client.newCall(request).execute();
            if(res.body() != null){
                return new JSONArray(res.body().string());
            }
        } catch(Exception e){}
        return new JSONArray();
    }

    private JSONObject configureUID(String uid){
        try {
            RequestBody body = new FormBody.Builder()
                    .add("iddat[]", uid)
                    .add("loai","tt")
                    .build();
            Request request = new Request.Builder()
                    .url("https://tuongtaccheo.com/cauhinh/datnick.php")
                    .header("User-Agent",userAgent)
                    .post(body)
                    .build();
            Response res = client.newCall(request).execute();
            if(res.body()!=null && res.body().string().trim().equals("1")){
                JSONObject ok = new JSONObject();
                ok.put("status","success");
                return ok;
            }
        } catch(Exception e){}
        JSONObject err = new JSONObject();
        try{err.put("status","error");}catch(Exception e){}
        return err;
    }

    private String getXu(){
        try{
            Request req = new Request.Builder()
                    .url("https://tuongtaccheo.com/home.php")
                    .build();
            Response res = client.newCall(req).execute();
            if(res.body()!=null){
                String s = res.body().string();
                if(s.contains("id=\\"soduchinh\\">")){
                    return s.split("id=\\"soduchinh\\">")[1].split("<")[0];
                }
            }
        }catch(Exception e){}
        return "0";
    }

    private void nhanXu(String idp){
        JSONObject nhan = postType("https://tuongtaccheo.com/tiktok/kiemtien/subcheo/nhantien.php","id="+idp);
        String tc = nhan.optString("sodu");
        if(tc!=null && !tc.isEmpty()){
            String xuu = getXu();
            log("✅ Nhận thành công: "+tc+" xu | Tổng xu: "+xuu);
        }else{
            log("⚡ Chưa follow acc nào!");
        }
    }

    private void runBot(String token, String uid, int delaySec){
        running = true;
        showStopOverlay();
        jobCount = 0;
        String idp = "";

        try{
            JSONObject config = configureUID(uid);
            if(!config.optString("status").equals("success")){
                log("Lỗi cấu hình UID");
                stopBot();
                return;
            }else{
                log("Cấu hình UID thành công!");
            }

            while(running){
                JSONArray jobs = getJobList();
                if(jobs.length()==0){
                    log("Chưa có job mới, đợi 5s...");
                    Thread.sleep(5000);
                    continue;
                }

                for(int i=0;i<jobs.length() && running;i++){
                    JSONObject job = jobs.getJSONObject(i);
                    String url = job.getString("url");
                    String jobid = job.getString("id");
                    log("Mở job: "+jobid);
                    log("Đợi "+delaySec+"s trước khi Follow...");
                    Thread.sleep(delaySec*1000);

                    Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    startActivity(intent);

                    Thread.sleep(3000);

                    jobCount++;
                    idp += jobid + ",";

                    log("✅ Job "+jobCount+" hoàn thành");

                    if(jobCount%10==0){
                        nhanXu(idp);
                        idp = "";
                    }
                    Thread.sleep(2000);
                }
            }
        }catch(Exception e){
            log("Lỗi: "+e.getMessage());
        }finally{
            stopBot();
        }
    }
}""",

    f"{project_name}/app/src/main/java/com/ttctik/phuocan/TikTokAccessibilityService.java": """package com.ttctik.phuocan;

import android.accessibilityservice.AccessibilityService;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import android.widget.Toast;

public class TikTokAccessibilityService extends AccessibilityService {
    @Override
    public void onAccessibilityEvent(AccessibilityEvent event){
        AccessibilityNodeInfo root = getRootInActiveWindow();
        if(root == null) return;

        // Tìm nút Follow
        for(int i=0;i<root.getChildCount();i++){
            AccessibilityNodeInfo node = root.getChild(i);
            if(node==null) continue;
            CharSequence desc = node.getContentDescription();
            if(desc!=null && desc.toString().toLowerCase().contains("follow")){
                node.performAction(AccessibilityNodeInfo.ACTION_CLICK);
                Toast.makeText(this,"Đã bấm Follow",Toast.LENGTH_SHORT).show();
            }
        }
    }

    @Override
    public void onInterrupt(){}
}""",

    f"{project_name}/app/src/main/res/layout/activity_main.xml": """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:orientation="vertical"
    android:padding="16dp"
    android:background="#0A0A0A"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <EditText
        android:id="@+id/tokenInput"
        android:hint="Nhập Token"
        android:textColor="#00FFFF"
        android:textColorHint="#00BFFF"
        android:backgroundTint="#00BFFF"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"/>

    <EditText
        android:id="@+id/uidInput"
        android:hint="Nhập UID TikTok"
        android:textColor="#00FFFF"
        android:textColorHint="#00BFFF"
        android:backgroundTint="#00BFFF"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:inputType="text"/>

    <EditText
        android:id="@+id/delayInput"
        android:hint="Delay giữa job (giây)"
        android:textColor="#00FFFF"
        android:textColorHint="#00BFFF"
        android:backgroundTint="#00BFFF"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:inputType="number"/>

    <Button
        android:id="@+id/startBtn"
        android:text="Bắt đầu"
        android:textColor="#FFFFFF"
        android:background="#FF4500"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"/>

    <ScrollView
        android:id="@+id/scrollLog"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:background="#0A0A0A">

        <TextView
            android:id="@+id/logView"
            android:textColor="#00FF00"
            android:padding="8dp"
            android:text="Log sẽ hiển thị ở đây"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"/>
    </ScrollView>
</LinearLayout>""",

    f"{project_name}/app/src/main/res/xml/accessibility_service_config.xml": """<?xml version="1.0" encoding="utf-8"?>
<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:accessibilityEventTypes="typeWindowStateChanged|typeViewClicked"
    android:accessibilityFeedbackType="feedbackGeneric"
    android:notificationTimeout="100"
    android:canRetrieveWindowContent="true"
    android:settingsActivity=""
    android:description="@string/accessibility_service_description"
/>""",

    f"{project_name}/app/src/main/res/values/strings.xml": """<resources>
    <string name="app_name">TTC TikBot</string>
    <string name="accessibility_service_description">Bot auto follow TikTok</string>
</resources>""",

    f"{project_name}/app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest package="com.ttctik.phuocan"
    xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW"/>

    <application
        android:allowBackup="true"
        android:label="@string/app_name"
        android:theme="@style/Theme.AppCompat.DayNight.NoActionBar">

        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>

        <service
            android:name=".TikTokAccessibilityService"
            android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE"
            android:exported="true">
            <meta-data
                android:name="android.accessibilityservice"
                android:resource="@xml/accessibility_service_config"/>
        </service>
    </application>
</manifest>"""
}

# --- 3. Tạo file ---
for path, content in files.items():
    with open(path,"w",encoding="utf-8") as f:
        f.write(content)

# --- 4. Tạo ZIP ---
zip_name = project_name + ".zip"
with zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, filenames in os.walk(project_name):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            zipf.write(filepath, os.path.relpath(filepath, project_name))

print(f"✅ ZIP đã tạo: {zip_name}")
