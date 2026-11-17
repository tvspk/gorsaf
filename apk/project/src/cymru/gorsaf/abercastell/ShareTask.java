package cymru.gorsaf.abercastell;

import android.app.Activity;
import android.content.Intent;

/** Opens Android's share sheet with the backup code. */
public class ShareTask implements Runnable {
    private final Activity activity;
    private final String text;

    public ShareTask(Activity activity, String text) { this.activity = activity; this.text = text; }

    @Override
    public void run() {
        Intent send = new Intent(Intent.ACTION_SEND);
        send.setType("text/plain");
        send.putExtra(Intent.EXTRA_SUBJECT, "Gorsaf Abercastell backup");
        send.putExtra(Intent.EXTRA_TEXT, text);
        activity.startActivity(Intent.createChooser(send, "Share backup code"));
    }
}
