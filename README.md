# CourseDesign_FaceRecognition
Python课程设计，人脸识别考勤系统  

**!!!项目路径不能有中文和空格!!!**  

# release  
windows下运行 [main.py](https://github.com/2891954521/CourseDesign_FaceRecognition/blob/master/release/main.py)  
树莓派下运行 [pi.py](https://github.com/2891954521/CourseDesign_FaceRecognition/blob/master/release/pi.py)  

## Server 服务器端
服务器端可自行部署，使用时去掉System里注释掉的代码

## FaceRecognition模块

参数解析：  
path 当前路径，用于储存人脸识别模型和人脸信息  
root  为显示该组件的窗口  
x, y, w, h 为组件大小  
cameraWidth, cameraHeight 为摄像头拍摄大小，树莓派上设置不合理会导致无法正常录像  
threshold 人脸识别阈值，0为完全匹配，值越大阈值越低  
fps 拍摄帧率