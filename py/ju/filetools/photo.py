from watermarker.marker import add_mark

# 需要加水印的图片目录
srcpath = r'C:\Users\PC\Desktop\temp\wjfbk'

# 加水印后保存目录
retpath = r'C:\Users\PC\Desktop\temp\water'

# file：图片文件或图片文件夹路径
	# out：添加水印后的结果保存位置，默认生成到 output 文件夹
	# mark：要添加的水印内容
	# opacity：水印的透明度，默认 0.15
	# angle：水印旋转角度，默认 30 度
	# space：水印直接的间隔, 默认 75 个空格
	# size：水印字体的大小，默认 50
	# color：文字水印颜色设置 16进制
add_mark(file=srcpath + '.jpg', out=retpath, mark="王巨峰", opacity=0.7, angle=35, space=30, size=20,
         color='#FFFFFF')
