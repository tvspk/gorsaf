package cymru.gorsaf.abercastell;

import android.app.Activity;
import android.graphics.Color;
import android.view.View;
import android.view.Window;

/** Colours the status and navigation bars to match the page's look (dark station or light manuscript). */
public class BarsTask implements Runnable {
    private final Activity activity;
    private final boolean light;

    public BarsTask(Activity activity, boolean light) { this.activity = activity; this.light = light; }

    @Override
    public void run() {
        Window w = activity.getWindow();
        int c = light ? Color.rgb(230, 214, 174) : Color.rgb(12, 19, 31);
        w.setStatusBarColor(c);
        w.setNavigationBarColor(c);
        w.getDecorView().setSystemUiVisibility(light
            ? View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR | View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR : 0);
    }
}
