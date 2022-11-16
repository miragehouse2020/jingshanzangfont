# 导入系统库
from time import sleep
import fontforge, os,psMat


def main():
    '''
    主函数
    '''
    # 定义参数
    img_list = list()
    img_dir = 'd:/git/jingshangzangfont/svg' 

    # 获取文件列表
    for file in os.listdir(img_dir):
            if os.path.splitext(file)[1].lower() in '.svg':
                img_list.append(file)
    print('当前总图片数量： %d' % len(img_list))
    
    # 循环处理图片
    index = 0
    
    for img_path in img_list:  
        print('当前处理 '+img_path)
        
        # 获取unicode
        codestr = os.path.splitext(img_path)[0]
        code = int(codestr,16)
        
         # 创建字体
        font = fontforge.font()
        font.encoding = 'UnicodeFull'
        font.version = '1.0'
        font.weight = 'Regular'
        font.fontname = 'uni'+codestr
        font.familyname = 'uni'+codestr
        font.fullname = 'uni'+codestr       
        
        # 创建字符
        glyph = font.createChar(code, "uni"+codestr)
        glyph.importOutlines(os.path.join(img_dir,img_path))
        
        # 位移调整
        base_matrix = psMat.translate(0,0)
        glyph.transform(base_matrix)
        
        # 写入ttf
        font.generate('./ttf/'+codestr+'.ttf')      
        index +=1
        # if index>1:
        #     break
        print('当前处理完 %d 张图片' % index)
        
        # 删除文件
        os.remove(os.path.join(img_dir,img_path))
        
    print('全部处理结束')


if __name__ == "__main__":
    '''
    程序入口
    '''
    main()
