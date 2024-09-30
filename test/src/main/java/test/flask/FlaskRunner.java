package test.flask;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.springframework.stereotype.Component;

@Component
public class FlaskRunner {

    public void startFlaskServer() {
        try {
            ProcessBuilder builder = new ProcessBuilder("python", "start_flask.py");
            // ProcessBuilder builder = new ProcessBuilder("python",
            // "path/to/start_flask.py");
            builder.redirectErrorStream(true);
            Process process = builder.start();

            // 프로세스 출력 확인
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);

                // 특정 로그 메시지를 확인할 수 있습니다.
                if (line.contains("Starting Flask server")) {
                    System.out.println("Flask server is running successfully!");
                }

            }
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
