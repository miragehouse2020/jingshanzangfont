# 导入系统库
import cv2
import os
import numpy as np


def main(): 
    '''
    主函数
    '''
    # 定义参数
    img_list = list()
    img_dir = './ocr' 
    target_width, target_height = 100, 100

    # 获取文件列表
    for file in os.listdir(img_dir):
            if os.path.splitext(file)[1].lower() in '.png|.jpg':
                img_list.append(file)
    print('当前总图片数量： %d' % len(img_list))
    
    # 循环处理图片
    index = 0
    error_index = 0
    for img_path in img_list:
        img = cv2.imread(os.path.join(img_dir,img_path),cv2.IMREAD_COLOR)
        # 图像标准化
        h, w, _=img.shape
        if h != target_height or w != target_width:
            img = cv2.resize(img, dsize=(target_width, target_height))
        '''
        # 去掉上下左右边界线
        image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(image_gray, 170, 220, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 250)
        for line in lines:
            # 获取rho和theta
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), thickness=20)
        '''
        # 提取图形区域
        img = img[1:100,1:100,:]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 精确裁剪
        ret, thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
        coords = np.column_stack(np.where(thresh > 0))
        coords = np.array(coords, dtype=np.float32)
        #min_rect = cv2.minAreaRect(coords)
        
        rect = cv2.boundingRect(coords)
        [y, x, h, w] = rect
        img = img[y:y+h,x:x+w,:]
        
        # 调整为正方形
        h,w,_ = img.shape
        if h>w:
            pad = int((h-w)/2.0)
            img = cv2.copyMakeBorder(img,0,0,pad,pad, cv2.BORDER_CONSTANT,value=[255,255,255])
        elif w>h:
            pad = int((w-h)/2.0)
            img = cv2.copyMakeBorder(img,pad,pad,0,0, cv2.BORDER_CONSTANT,value=[255,255,255])
                    
        # 统一缩放
        img = cv2.resize(img, dsize=(128, 128))

        # 边缘补白
        img = cv2.copyMakeBorder(img,10,10,10,10, cv2.BORDER_CONSTANT,value=[255,255,255])   
        
        # 保存
        code = os.path.splitext(img_path)[0]
        save_path = 'crop/%s.png' % code  
        cv2.imwrite(save_path, img)
        index += 1
        print(img_path)   
        


if __name__ == "__main__":
    '''
    程序入口
    '''
    main()