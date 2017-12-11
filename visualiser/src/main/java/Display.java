import java.awt.EventQueue;
import java.awt.Graphics;
import java.awt.Graphics2D;
import javax.swing.JFrame;
import javax.swing.JPanel;

    public class Display extends JFrame {
        public Display(String room) {
            initUI(room);
        }

        private void initUI(String room) {
            add(new Room(room));
            setTitle("Visualiser");
            setSize(1280, 720);
            setLocationRelativeTo(null);
            setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        }

        public static void main(String[] args) {

            EventQueue.invokeLater(new Runnable() {

                @Override
                public void run() {
                    //String filename = "1.txt";
                    //ReadFile read = new ReadFile(filename);
                    //Display ex = new Display(read.getRoom());
                    Display ex = new Display("(0,0), (10,0), (10,10), (0,10)");
                    ex.setVisible(true);
                }
            });
        }
    }
