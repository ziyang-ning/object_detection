#include "esp_camera.h"
#define CAMERA_MODEL_XIAO_ESP32S3 // Has PSRAM
#include "camera_pins.h"

const uint8_t IMG_WIDTH = 240;   //have to change this var manually
const uint8_t IMG_HIGHT = 240;   //have to change this var manually
const uint8_t THRESH = 210;       //have to change this var manually
const uint8_t min_bright_rows = 5; //The min bright row to return median

camera_fb_t *fb;

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

//  rand_gen();
}

//exactlly 10% of the image size
uint32_t rand_index [5760];
void rand_gen(){
  for(int i = 0; i < 5760; i++){
    rand_index[i] = random(0, 57600);
  }
}

/*
void loop() {
  uint64_t fr_start = esp_timer_get_time();
  fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }
  uint64_t frameloadT = esp_timer_get_time() - fr_start;
  printf("%s, %d\n", "frame loader time:", frameloadT);
   
  char x; 
  // set = p for printing image buf value printing
  if(Serial.available() > 0) {  
    x = Serial.read();
  }

  uint64_t median_start = esp_timer_get_time();

  //Default median = 0 
  uint8_t x_median_final = 0;
  uint8_t y_median_final = 0;
  
  uint32_t pixcount = 0;
  uint16_t x_medians_real_length = 0;
  uint16_t x_medians[IMG_HIGHT];
  uint16_t y_vals_of_x_medians[IMG_HIGHT];

  // fam2p2 additional vars
  uint32_t numpixvisited = 0;
  bool detected = 0;
  uint16_t blob_start_index = -1;
  uint16_t num_conseq_black_rows = 0;
  bool last_row_black = 0;


  // for(uint16_t j = 0; j < IMG_HIGHT; j++){
  uint16_t j = 0;
  while(j < IMG_HIGHT){

    
    uint16_t all_x_gt_thresh [IMG_WIDTH];
    uint16_t all_x_gt_thresh_real_length = 0;

    uint16_t i = 0;
    // for uint16 -1 is 65535
    if(blob_start_index != 65535 && blob_start_index - 20 > 0){
      i = blob_start_index - 20;
      pixcount = pixcount + i;
    }

    // uint64_t innerloop = esp_timer_get_time();
    // for(uint16_t i = 0; i < IMG_WIDTH; i++){
    
  while(i < IMG_WIDTH && pixcount < (IMG_WIDTH * IMG_HIGHT)){
    
    
    //--------For Printing---------------//
//    if(x == 'p'){
//      Serial.printf("%d\n",fb->buf[pixcount]);
//      Serial.printf("%d, %d\n", i, j);
//    }
    //--------For Printing---------------//
    
    // IF there is no 3 whites in a row
    if(fb->buf[pixcount] <= THRESH || fb->buf[pixcount+1] <= THRESH || 
    fb->buf[pixcount+2] <= THRESH){
      
            
      if(i + 10 < IMG_WIDTH){
        i += 10;
        pixcount += 10;
        numpixvisited += 1; //This is not exact, but a good approx
        // This is because the first one is most likely black
      }else{
        pixcount = pixcount + IMG_WIDTH - i;
        i = IMG_WIDTH;
        numpixvisited += 1;
      }
    }else{  // if there is 3 whites in a row
      detected = 1;
      if(i - 20 < 0){
        blob_start_index = 0;
      }else{
        blob_start_index = i;
      }
        all_x_gt_thresh[all_x_gt_thresh_real_length] = i;
        all_x_gt_thresh[all_x_gt_thresh_real_length+1] = i+1;
        all_x_gt_thresh[all_x_gt_thresh_real_length+2] = i+2;
        all_x_gt_thresh_real_length += 3;
        i += 3;
        pixcount += 3;
        numpixvisited += 3;

        //Start searching to the right
        while(fb->buf[pixcount] > THRESH && i < IMG_WIDTH){
          all_x_gt_thresh[all_x_gt_thresh_real_length] = i;
          all_x_gt_thresh_real_length += 1;

          if(i + 5 < IMG_WIDTH){
            i += 5;
            pixcount += 5;
            numpixvisited += 1; //This is not exact, but a good approx
          // This is because the first one is most likely black
          }else{
            pixcount = pixcount + IMG_WIDTH - i;
            i = IMG_WIDTH;
            numpixvisited += 1;
          }
        }

        //current pixcount is already checked and it's not white
        // this was != before, trying to make it more robust? 
        if(i != IMG_WIDTH < IMG_WIDTH){
          i += 1;
          pixcount += 1;
          numpixvisited += 1;
        }

        //since already reaching black, object ends, go to the next row
        pixcount = pixcount + IMG_WIDTH - i;
        i = i + IMG_WIDTH;   //Go striaght to the next row
    }

  }
    // uint64_t innerlooptime = esp_timer_get_time() - innerloop;
    // Serial.println(innerlooptime);
    
    // MEDIAN FUNCTION (not real median, can be off by 1)
    if(all_x_gt_thresh_real_length != 0){
      // This should be already a floor division? because they are integers?
      x_medians[x_medians_real_length] = all_x_gt_thresh[all_x_gt_thresh_real_length/2];
      y_vals_of_x_medians[x_medians_real_length] = j;
      x_medians_real_length += 1;

      last_row_black = 0;
      num_conseq_black_rows = 0;
    }else{
      num_conseq_black_rows += 1;
      last_row_black = 1;
    }

      if(all_x_gt_thresh_real_length == 0 && blob_start_index != -1 && detected){
        break;
      }

      if(num_conseq_black_rows > 2 && last_row_black && j+3 < IMG_WIDTH){
        j = j + 2;
        pixcount = pixcount + 2 * IMG_WIDTH;
      }

      j = j + 2;
      pixcount = pixcount + IMG_WIDTH;

      //visualize all content in the all_x_gt_thresh
      //this is basically all the pixels that are accounted by the algo
      //----- for printing --------------
      if(x == 'p'){
        Serial.println("********i am trying to print here*************");
        Serial.println(all_x_gt_thresh_real_length);
        for(int m = 0; m < all_x_gt_thresh_real_length; m++){
          Serial.printf("%d, %d\n", all_x_gt_thresh[m], j);
        }
      }
      
  }
  // This should be already a floor division? because they are integers?
  //-------CONDITION WHERE BASICALLY EVERYTHING IS DARK ----------------
  if(x_medians_real_length >= min_bright_rows){
    x_median_final = x_medians[x_medians_real_length/2];
    y_median_final = y_vals_of_x_medians[x_medians_real_length/2];
    }

  uint64_t medianT = esp_timer_get_time() - median_start;
  printf("%s, %d\n", "Median algo time: ", medianT);

  Serial.printf("%d, %d\n",x_median_final, y_median_final);
  Serial.printf("%s, %d\n", "numpixvisited: ", numpixvisited);

  esp_camera_fb_return(fb);

  uint64_t print_frame_time = esp_timer_get_time() - fr_start;
  Serial.println("___________ONE PICTURE__________");
  Serial.println(print_frame_time);
}
*/

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

  printf("%s, %d\n", "rand num:", rand_index[1]);

  uint64_t accssT_start = esp_timer_get_time();
  uint32_t pixcount = 0;
  uint16_t x_medians[IMG_HIGHT];


  // TEST FOR INORDER ACCECSS
  for(uint16_t j = 0; j < IMG_HIGHT; j++){
    for(uint16_t i = 0; i < IMG_WIDTH; i++){
      if(fb->buf[pixcount] > THRESH){
        x_medians[i] = fb->buf[pixcount];
//        Serial.println("I am acually doing stuff");
      }
      pixcount++;
    }
  }

// TEST for out of order access
//  for(int i = 0; i < 5760; i++){
//    if(fb->buf[ rand_index[i] ] > THRESH){
//      x_medians[2] = fb->buf[ rand_index[i] ];
//    }
//  }
  
  uint64_t accssT = esp_timer_get_time() - accssT_start;
  printf("%s, %d\n", "img access time:", accssT);

  esp_camera_fb_return(fb);

  uint64_t print_frame_time = esp_timer_get_time() - fr_start;
  Serial.println("___________ONE PICTURE__________");
  Serial.println(print_frame_time);

  rand_gen();
}
