import java.awt.EventQueue;
import java.awt.Graphics;
import java.awt.Graphics2D;
import javax.swing.JFrame;
import javax.swing.JPanel;

    public class Display extends JFrame {
        public Display() {
            initUI();
        }

        private void initUI() {
            add(new Room());
            setTitle("Visualiser");
            setSize(1280, 720);
            setLocationRelativeTo(null);
            setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        }

        public static void main(String[] args) {

            EventQueue.invokeLater(new Runnable() {

                @Override
                public void run() {
                    Display ex = new Display();
                    ex.setVisible(true);
                }
            });
        }
    }
