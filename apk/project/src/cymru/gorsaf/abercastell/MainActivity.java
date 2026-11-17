package cymru.gorsaf.abercastell;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.webkit.WebSettings;
import android.webkit.WebView;

/** Shows the game, a single self-contained page bundled in the app's assets.
 *  Network: only the English app (INTERNET permission added by build_en.sh), only api.github.com for sync and the
 *  new-version check. Camera: only for scanning the sync pairing QR code (CameraClient). */
public class MainActivity extends Activity {
    private static final String HOME = "file:///android_asset/index.html";
    private WebView web;
    private CameraClient camera;
    private final Handler handler = new Handler(Looper.getMainLooper());
    private PauseTask pauser;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        int night = Color.rgb(12, 19, 31);
        getWindow().setStatusBarColor(night);
        getWindow().setNavigationBarColor(night);

        web = new WebView(this);
        web.setBackgroundColor(night);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);   // the game is JavaScript
        s.setDomStorageEnabled(true);   // progress is kept in localStorage, inside the app's private data
        s.setAllowContentAccess(false);
        s.setMediaPlaybackRequiresUserGesture(false); // "Listen to the column" plays sentence after sentence; sound still only starts from a button
        web.addJavascriptInterface(new Bridge(this), "GorsafAndroid");
        web.setWebViewClient(new StayHomeClient());
        camera = new CameraClient(this);
        web.setWebChromeClient(camera);
        pauser = new PauseTask(web);
        setContentView(web);
        web.loadUrl(HOME);
    }

    @Override
    public void onBackPressed() {
        // Back sends the app to the background instead of closing it, so a case in progress is not lost.
        moveTaskToBack(true);
    }

    @Override
    public void onRequestPermissionsResult(int req, String[] perms, int[] results) {
        if (req == CameraClient.REQ_CAMERA && camera != null) camera.permissionResult();
    }

    @Override protected void onPause() {
        // Save the game before Android may stop the app in the background (save() skips unchanged data).
        // Hiding the page (web.onPause) also starts the sync upload, so the JS timers stop only ~20 s later.
        web.evaluateJavascript("try{save()}catch(e){}try{if(window.syMaybe)syMaybe(0)}catch(e){}", null);
        super.onPause(); web.onPause();
        handler.removeCallbacks(pauser);
        handler.postDelayed(pauser, 20000);
    }
    @Override protected void onResume() { super.onResume(); handler.removeCallbacks(pauser); web.onResume(); web.resumeTimers(); }
    @Override protected void onDestroy() { handler.removeCallbacks(pauser); web.destroy(); super.onDestroy(); }
}
