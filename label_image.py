from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
 
import numpy as np
import os, sys
import time

from time import sleep, strftime
from datetime import datetime

import captureimage

#import tensorflow as tf
import tensorflow.compat.v1 as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


image_path = sys.argv[1]

# Read image_data
image_data = tf.gfile.FastGFile(image_path, 'rb').read()

# Label file
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("retrained_labels.txt")]

# Load Model
with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
    # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    
    predictions = sess.run(softmax_tensor, \
             {'DecodeJpeg/contents:0': image_data})
    
    # Sort to show labels of first prediction in order of confidence
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    
    #i = 0
    f = open('results.txt', 'w')
    f.write('')
    f.close()
    a = []
    for node_id in top_k:
        #i = i + 1
        weather = label_lines[node_id]
        score = predictions[0][node_id]
        print('%s (score = %.5f)' % (weather, score))
        #print(i)
        f = open('results.txt', 'a')
        f.write('%s (score = %.5f)\n' % (weather, score))
        f.close()
        a.append(weather)
        
    print ('Pred. Weather: ' + a[0])
    PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
    PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
    # Create PCF8574 GPIO adapter.
    mcp = PCF8574_GPIO(PCF8574_address)
    lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    lcd.setCursor(0,0)  # set cursor position
    lcd.message( 'Pred. Weather:\n' ) # Title
    lcd.message( a[0] ) # Predicted Weather
    #sleep(1)
        #lcd.clear()
        #lcd.setCursor(0,0)  # set cursor position
        #lcd.message('Pred. Weather \n') # display the visibility
        #lcd.message('%s (score = %.5f)' % (human_string, score))# display the humidity
        #time.sleep(6)
        #lcd.clear()
    #highestscore = float(np.argmax(score))
    #print(highestscore)
    
    #print('The weather today is most likely %.5f' % human_string[highestscore])