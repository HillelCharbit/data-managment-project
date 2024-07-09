import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
// import org.locationtech.jts.geom.Coordinate;

public class CSVReader {
    public double[][] readCSV(String csvFile, int k) {
        List<double[]> dataList = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {
            String line;
            int count = 0;
            while ((line = br.readLine()) != null && count < k) {
                String[] values = line.split(","); // Split by comma or other delimiter

                // Assuming the CSV format is x,y
                if (values.length >= 2) {
                    double x = Double.parseDouble(values[0].trim());
                    double y = Double.parseDouble(values[1].trim());
                    double[] point = { x, y };
                    dataList.add(point);
                }
                count++;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Convert List<double[]> to double[][]
        double[][] data = new double[dataList.size()][2];
        for (int i = 0; i < dataList.size(); i++) {
            data[i] = dataList.get(i);
        }
        normalizeData(data);
        return data;
    }

    public static void normalizeData(double[][] data) {
        if (data.length == 0) {
            return; // Handle empty data case
        }

        // Find min and max values for x and y
        double minX = 41.64467013;
        double maxX = 42.02106425;
        double minY = -87.90687413;
        double maxY = -87.52509414;

        for (int i = 1; i < data.length; i++) {
            if (data[i][0] < minX) {
                minX = data[i][0];
            }
            if (data[i][0] > maxX) {
                maxX = data[i][0];
            }
            if (data[i][1] < minY) {
                minY = data[i][1];
            }
            if (data[i][1] > maxY) {
                maxY = data[i][1];
            }
        }

        // Normalize each point in data
        for (int i = 0; i < data.length; i++) {
            data[i][0] = (data[i][0] - minX) / (maxX - minX); // Normalize x
            data[i][1] = (data[i][1] - minY) / (maxY - minY); // Normalize y
        }
    }
}
