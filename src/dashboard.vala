using Gtk;

namespace Dashboard {
    public class App: Gtk.Application {
        public App() {
            Object(
                    application_id: "org.fascode.dashboard",
                    flags: ApplicationFlags.FLAGS_NONE
            );
        }

        protected override void activate () {
            var window = new Window(this);
            window.title = "Fascode Dashboard";
            window.show_all();
        }
    }
}

public static int main (string[] args) {
    var application = new Dashboard.App();
    return application.run(args);
}
