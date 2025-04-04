from flask import Flask, send_file, jsonify
import numpy as np
import io

from camera import capture_and_save_realsense_frames
from b2 import get_robot_state,control_turn_right,control_move_forward,control_turn_left
host_IP="192.168.91.187"
host_port=5000
app = Flask(__name__)

@app.route("/obs", methods=['GET'])
def get_obs():
    color_image,depth_image=capture_and_save_realsense_frames()
    memfile = io.BytesIO()
    np.savez(memfile, color_sensor_1st_person=color_image, depth_sensor_1st_person=depth_image)
    memfile.seek(0)
    
    return send_file(
        memfile,
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name='arrays.npz'
    )
    
@app.route("/agent_state",methods=['GET'])
def get_agent_state():
    position, quaternion=get_robot_state()
    return jsonify({"position": position, "quaternion": quaternion})

@app.route("/move_forward",method=['GET'])
def move_forward():
    success=control_move_forward()
    return jsonify({"status": success}), 200

@app.route("/turn_left",method=['GET'])
def turn_left():
    success=control_turn_left()
    return jsonify({"status": success}), 200

@app.route("/turn_right",method=['GET'])
def turn_right():
    success=control_turn_right()
    return jsonify({"status": success}), 200

if __name__ == '__main__':
    app.run(host=host_IP, port=host_port)
