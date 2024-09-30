package test.flask;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.bind.annotation.GetMapping;

@RestController
public class flaskController {

    @GetMapping("path")
    public String callFlask() {
        RestTemplate restTemplate = new RestTemplate();
        String flaskUrl = "http://localhost:8080";
        String response = restTemplate.postForObject(flaskUrl, null, String.class);
        return response;
    }

}
