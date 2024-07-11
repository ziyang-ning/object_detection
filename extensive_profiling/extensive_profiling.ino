#include "esp_camera.h"
#define CAMERA_MODEL_XIAO_ESP32S3 // Has PSRAM
#include "camera_pins.h"

const uint8_t IMG_WIDTH = 240;   //have to change this var manually
const uint8_t IMG_HIGHT = 240;   //have to change this var manually
const uint8_t THRESH = 0;       //have to change this var manually
const uint8_t min_bright_rows = 5; //The min bright row to return median

uint32_t x_medians [5760];

camera_fb_t *fb;


//exactlly 10% of the image size
uint32_t rand_index [5760];
void rand_gen(){
  for(int i = 0; i < 5760; i++){
    rand_index[i] = random(0, 57600);
  }
}


void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();
  
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  
//-----CHANGE DEPENDING ON NEEDS----------//
//  config.frame_size = FRAMESIZE_QVGA;  // 320x240
  config.frame_size = FRAMESIZE_240X240;
  config.pixel_format = PIXFORMAT_GRAYSCALE;
//-----CHANGE DEPENDING ON NEEDS----------//
  
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 12;
  config.fb_count = 2;
  

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  // Setup LED FLash if LED pin is defined in camera_pins.h
  #if defined(LED_GPIO_NUM)
    setupLedFlash(LED_GPIO_NUM);
  #endif

  rand_gen();

}

//benchmark for accessing all pixels  
void loop() {  
  uint64_t fr_start = esp_timer_get_time();
  fb = esp_camera_fb_get();

  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }
  uint64_t frameloadT = esp_timer_get_time() - fr_start;
  printf("%s, %d\n", "frame loader time:", frameloadT);
  
//  int buff = fb->buf[1];
//  Serial.println(buff);
  uint64_t func_start = esp_timer_get_time();

  //Some slow function
  int x = 0;
  for(int i = 0; i < 57; i++){
    x = random(0, 57600);
  }

  // Random access function
  //A array of random number with length 5760 was generated
  //Make a random start index, to ensure random access
  
//  int rand_start = random(0, 5760);
//  for(int i = 0; i < 5760; i++){
//    if(rand_start == 5760){
//      rand_start = 0;
//    }
//    if(fb->buf[ rand_index[rand_start] ] > THRESH){
//      x_medians[i] = (fb->buf[ rand_index[rand_start] ]);
//    }
//    rand_start++;
//  }

// inorder access function
//  int rand_start = random(0, 5760);
//  for(int i = 0; i < 5760; i++){
//    //Still keeping this if statement for consistency
//    if(rand_start == 5760){
//      rand_start = 0;
//    }
//    
//    if(fb->buf[i] > THRESH){
//      x_medians[i] = (fb->buf[i]);
//    }
//    rand_start++;
//  }

  // Jump 10 with 90% prob and jump 5 with 10% prob
//  int rand_start = random(0, 57600);
//  int index = 0;
//  for(int i = 0; i < 5760; i++){
//    if(rand_start == 57600){
//      rand_start = 0;
//    }
//    if(rand_index[rand_start] > 5760){
//      x_medians[i] = fb->buf[index];
//      index += 10;
//    }else{
//      x_medians[i] = fb->buf[index];
//      index += 5;
//      }
//      rand_start++;
//  }
  
  
  uint64_t funcT = esp_timer_get_time() - func_start;
  printf("%s, %d\n", "function run time:", funcT);

  esp_camera_fb_return(fb);

  uint64_t print_frame_time = esp_timer_get_time() - fr_start;
  Serial.println(print_frame_time);
  Serial.println("___________ONE PICTURE__________");

}
