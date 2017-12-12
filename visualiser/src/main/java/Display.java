import java.awt.EventQueue;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.util.ArrayList;
import javax.swing.JFrame;
import javax.swing.JPanel;

    public class Display extends JFrame {
        Display(String room, ArrayList<String> shapesInRoom) {
            initUI(room, shapesInRoom);
        }

        private void initUI(String room, ArrayList<String> shapesInRoom) {
            add(new Room(room, shapesInRoom));
            setTitle("Visualiser");
            setSize(1280, 720);
            setLocationRelativeTo(null);
            setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        }

        public static void main(String[] args) {

            EventQueue.invokeLater(new Runnable() {

                @Override
                public void run() {
                    String filename = "src/main/java/1.txt";
                    ReadFile read = new ReadFile(filename);
                    Display ex = new Display(read.getRoom(), read.getShapesInRoom());
                    //Display ex = new Display("(0, 0), (10, 0), (10, 10), (0, 10)");
                    ex.setVisible(true);
                }
            });
        }
    }
