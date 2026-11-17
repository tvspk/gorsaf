package cymru.gorsaf.abercastell;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.webkit.JavascriptInterface;

/** Lets the page's backup screen copy, paste and share the backup code; app version and download of a new version. */
public class Bridge {
    private final Activity activity;

    public Bridge(Activity activity) { this.activity = activity; }

    @JavascriptInterface
    public void copy(String text) {
        ClipboardManager cm = (ClipboardManager) activity.getSystemService(Context.CLIPBOARD_SERVICE);
        cm.setPrimaryClip(ClipData.newPlainText("Gorsaf Abercastell", text));
    }

    @JavascriptInterface
    public String paste() {
        ClipboardManager cm = (ClipboardManager) activity.getSystemService(Context.CLIPBOARD_SERVICE);
        ClipData clip = cm.getPrimaryClip();
        if (clip == null || clip.getItemCount() == 0) return "";
        CharSequence t = clip.getItemAt(0).coerceToText(activity);
        return t == null ? "" : t.toString();
    }

    /** The page's look changed: match the system bars (dark station or light manuscript). */
    @JavascriptInterface
    public void bars(final boolean light) {
        activity.runOnUiThread(new BarsTask(activity, light));
    }

    /** versionName of the installed app (the page compares it with the latest release on GitHub). */
    @JavascriptInterface
    public String version() {
        try { return activity.getPackageManager().getPackageInfo(activity.getPackageName(), 0).versionName; }
        catch (Exception e) { return ""; }
    }

    /** Opens a release download in the browser: only this project's releases on GitHub. */
    @JavascriptInterface
    public void open(String url) {
        if (url == null || !url.startsWith("https://github.com/tvspk/gorsaf/releases/")) return;
        activity.runOnUiThread(new OpenTask(activity, url));
    }

    @JavascriptInterface
    public void share(String text) {
        activity.runOnUiThread(new ShareTask(activity, text));
    }
}
