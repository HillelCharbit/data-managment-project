import javax.swing.*;
import java.awt.*;

public class Hivoro extends JPanel {
    Color backgroundColor, textColor;
    int numPoints, height, width;
    double[][] data;
    Color[] lineColors = new Color[13];
    double[] xCoords = new double[100000];
    double[] yCoords = new double[100000];
    int[] xIntCoords = new int[100000];
    int[] yIntCoords = new int[100000];
    double[] distances = new double[100000];
    double[] bisectorX = new double[100000];
    double[] bisectorY = new double[100000];
    double[] unused = new double[100000];

    public Hivoro(double[][] data) {
        this.data = data;
        backgroundColor = Color.black;
        textColor = Color.yellow;
        lineColors[0] = Color.green;
        lineColors[1] = Color.white;
        // lineColors[2] = Color.black;

        lineColors[2] = new Color(199, 111, 238);
        width = 800;
        height = 600;
        numPoints = data.length;

        for (int k = 0; k < numPoints; k++) {
            xCoords[k] = data[k][0] * (width - 30) + 15;
            yCoords[k] = data[k][1] * (height - 30) + 15;
            xIntCoords[k] = (int) (xCoords[k] + 0.5);
            yIntCoords[k] = (int) (yCoords[k] + 0.5);
            distances[k] = Math.pow(xCoords[k] * xCoords[k] + yCoords[k] * yCoords[k], 0.5);
        }
        heapSort(distances, xCoords, yCoords, numPoints);
    }

    public double power(double base, double exponent) {
        return Math.pow(base, exponent);
    }

    void heapSort(double[] arr1, double[] arr2, double[] arr3, int size) {
        int halfSize, k, i, j, m;
        double temp1, temp2, temp3, compare1, compare2, compare3;
        halfSize = size / 2;
        for (k = halfSize; k >= 1; k--) {
            i = k;
            temp1 = arr1[i - 1];
            temp2 = arr2[i - 1];
            temp3 = arr3[i - 1];
            while (2 * i <= size) {
                j = 2 * i;
                if (j + 1 <= size && arr1[j - 1] < arr1[j]) {
                    j++;
                }
                if (arr1[j - 1] <= temp1) {
                    break;
                }
                arr1[i - 1] = arr1[j - 1];
                arr2[i - 1] = arr2[j - 1];
                arr3[i - 1] = arr3[j - 1];
                i = j;
            }
            arr1[i - 1] = temp1;
            arr2[i - 1] = temp2;
            arr3[i - 1] = temp3;
        }
        for (m = size - 1; m >= 1; m--) {
            compare1 = arr1[m];
            compare2 = arr2[m];
            compare3 = arr3[m];
            arr1[m] = arr1[0];
            arr2[m] = arr2[0];
            arr3[m] = arr3[0];
            i = 1;
            while (2 * i <= m) {
                k = 2 * i;
                if (k + 1 <= m && arr1[k - 1] <= arr1[k]) {
                    k++;
                }
                if (arr1[k - 1] <= compare1) {
                    break;
                }
                arr1[i - 1] = arr1[k - 1];
                arr2[i - 1] = arr2[k - 1];
                arr3[i - 1] = arr3[k - 1];
                i = k;
            }
            arr1[i - 1] = compare1;
            arr2[i - 1] = compare2;
            arr3[i - 1] = compare3;
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        g.setColor(backgroundColor);
        g.fillRect(1, 1, width, height);
        g.setColor(textColor);
        g.drawString("N=" + numPoints, 15, 15);
        for (int k = 0; k < numPoints; k++) {
            g.fillOval(xIntCoords[k] - 2, yIntCoords[k] - 2, 4, 4);
        }
        for (int i = 1; i <= numPoints - 1; i++) {
            for (int j = i + 1; j <= numPoints; j++) {
                double slope1 = (yCoords[i - 1] - yCoords[j - 1]) / (xCoords[i - 1] - xCoords[j - 1]);
                double slope2 = -1 / slope1;
                double midY = (yCoords[i - 1] + yCoords[j - 1]) / 2;
                double midX = (xCoords[i - 1] + xCoords[j - 1]) / 2;
                double yIntercept = midY - midX * slope2;
                double x0, y0, xEnd = 0, yEnd = 0;
                if (yIntercept > 0 && yIntercept < height) {
                    x0 = 0;
                    y0 = yIntercept;
                } else {
                    if (slope2 > 0) {
                        x0 = -yIntercept / slope2;
                        y0 = 0;
                    } else {
                        x0 = (height - yIntercept) / slope2;
                        y0 = height;
                    }
                }
                double yMax = slope2 * width + yIntercept;
                if (yMax > 0 && yMax < height) {
                    xEnd = width;
                    yEnd = yMax;
                } else {
                    if (slope2 > 0) {
                        xEnd = (height - yIntercept) / slope2;
                        yEnd = height;
                    } else {
                        xEnd = -yIntercept / slope2;
                        yEnd = 0;
                    }
                }
                int l = 1;
                bisectorX[l - 1] = x0;
                bisectorY[l - 1] = y0;
                for (int k = 1; k <= numPoints; k++) {
                    if (k != i && k != j) {
                        double slope3 = (yCoords[i - 1] - yCoords[k - 1]) / (xCoords[i - 1] - xCoords[k - 1]);
                        double slope4 = -1 / slope3;
                        double midY3 = (yCoords[i - 1] + yCoords[k - 1]) / 2;
                        double midX3 = (xCoords[i - 1] + xCoords[k - 1]) / 2;
                        double yIntercept3 = midY3 - midX3 * slope4;
                        double yAtX0 = slope4 * x0 + yIntercept3;
                        double yAtXEnd = slope4 * xEnd + yIntercept3;
                        double sign1 = y0 - yAtX0;
                        double sign2 = yEnd - yAtXEnd;
                        if (sign1 * sign2 < 0) {
                            l++;
                            bisectorX[l - 1] = (yIntercept3 - yIntercept) / (slope2 - slope4);
                            bisectorY[l - 1] = slope2 * bisectorX[l - 1] + yIntercept;
                        }
                    }
                }
                l++;
                bisectorX[l - 1] = xEnd;
                bisectorY[l - 1] = yEnd;
                for (int u = 1; u <= l; u++) {
                    unused[u - 1] = 0;
                }
                heapSort(bisectorX, bisectorY, unused, l);
                for (int k = 1; k <= l - 1; k++) {
                    int next = k + 1;
                    double midXBisector = (bisectorX[k - 1] + bisectorX[next - 1]) / 2;
                    double midYBisector = slope2 * midXBisector + yIntercept;
                    double midDistSquared = Math.pow(midXBisector - xCoords[i - 1], 2)
                            + Math.pow(midYBisector - yCoords[i - 1], 2);
                    int closerPointsCount = 0;
                    for (int u = 1; u <= numPoints; u++) {
                        if (u != i && u != j) {
                            double pointDistSquared = Math.pow(midXBisector - xCoords[u - 1], 2)
                                    + Math.pow(midYBisector - yCoords[u - 1], 2);
                            if (pointDistSquared < midDistSquared) {
                                closerPointsCount++;
                            }
                        }
                    }
                    if (closerPointsCount < 3) {
                        int x1Int = (int) (bisectorX[k - 1] + 0.5);
                        int y1Int = (int) (bisectorY[k - 1] + 0.5);
                        int x2Int = (int) (bisectorX[next - 1] + 0.5);
                        int y2Int = (int) (bisectorY[next - 1] + 0.5);
                        g.setColor(lineColors[closerPointsCount]);
                        g.drawLine(x1Int, y1Int, x2Int, y2Int);
                    }
                }
            }
        }
    }

    public static void main(String[] args) {
        CSVReader reader = new CSVReader();
        String csvFile = "C:\\Users\\danie\\Food_Inspections_-_1_1_2010_-_6_30_2018_20240704.csv";
        // String csvFile = "C:\\Users\\ASUS\\Downloads\\Food_Inspections_-_1_1_2010_-_6_30_2018_20240704.csv";

        int k = 10; // Number of lines to read
        double[][] data = reader.readCSV(csvFile, k);

        // Prompt the user for the value of k
        String kStr = JOptionPane.showInputDialog("Enter the value of k:");
        int kValue = Integer.parseInt(kStr);

        // Create UncoveredRegion2D instance and add points from data
        UncoveredRegion2D ur = new UncoveredRegion2D(0.1, kValue);
        for (double[] point : data) {
            ur.addPoint(point[0], point[1]);
        }

        // Create the main JFrame for Voronoi and uncovered regions visualization
        JFrame frame = new JFrame("Hivoro and Uncovered Regions Visualization");

        // Add the Voronoi panel
        long startTime = System.nanoTime();
        Hivoro hivoro = new Hivoro(data);
        long endTime = System.nanoTime();
        long totalTime = (endTime - startTime) / 1000000;
        System.out.println(totalTime);
        frame.add(hivoro);

        // Create and add the uncovered regions visualization panel
        VisualizeUncoveredRegions urPanel = new VisualizeUncoveredRegions(ur);
        frame.add(urPanel);

        frame.setLayout(new GridLayout(1, 2)); // Arrange panels side by side
        frame.setSize(1600, 800); // Adjust the size to accommodate both panels
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
    
}
