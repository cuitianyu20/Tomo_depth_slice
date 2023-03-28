import math
import pygmt
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d
from scipy.interpolate import griddata

# 读取地震层析成像结果数据
coor_data = np.loadtxt('model/LLNL_G3Dv3.Interpolated.Coordinates.txt')
model_data = np.loadtxt('model/LLNL_G3Dv3.Interpolated.Layer57_Lower_Mantle_2891km.txt')

# 定义特定地区的深度切片经纬度范围
minlat = 45; maxlat = 70
minlon = -120; maxlon = 160

# 读取数据
lat = coor_data[:,0]
lon = coor_data[:,1]
vp = model_data[:,2]

# 寻找区域的经纬度范围
region_index = np.where(((lat >= minlat) & (lat <= maxlat)) & ((lon <= minlon) | (lon >= maxlon)))

vp_slice = vp[region_index]  # 进行深度和经纬度同时切片
lon_slice = lon[region_index]
lat_slice = lat[region_index]

print("min dlnVp is %f, max dlnVp is %f\n" % (np.min(vp_slice),np.max(vp_slice)))

# 绘制CMB附近的S波速度结构
fig = pygmt.Figure()
pygmt.config(
    FONT_LABEL='10p,Helvetica',
    FONT_TITLE='10p,Helvetica',
    MAP_TITLE_OFFSET = '1p',
)
region = [minlon-(180+minlon)-(180-maxlon),minlon, minlat, maxlat]  # 定义地图范围
projection = 'M5i'  # 定义投影方式，这里选择墨卡托投影
transparency = 0   # 定义图像的透明度
# 进行数据插值
interp_data = pygmt.surface(
    x=lon_slice, 
    y=lat_slice, 
    z=vp_slice,
    region=region,
    spacing = 0.05,
)
# 根据网格文件设置对应的cpt
tomo_cpt = pygmt.grd2cpt(
    grid = interp_data,
    background = True,
    cmap = 'vik',
    reverse=True,
    transparency=transparency,
    continuous = False,
    # series = [math.floor(np.min(vp_slice)),math.ceil(np.max(vp_slice)),0.1],
    series = [-2,2,0.1],
)
# 绘制插值图
fig.grdimage(
    grid=interp_data,
    cmap=tomo_cpt, 
    region = region, 
    transparency=transparency,
    projection = projection
)
fig.coast(
    shorelines=True,
    area_thresh=100,
    region = region,
    projection = projection,
    resolution='i',
    frame=['WSne+t"LLNL-G3Dv3"', "xa10f5", "ya5f2.5"]
)
rectangle = [[-155.2, 59, -145.8, 62]]
fig.plot(data=rectangle, style="r+s", pen="0.5p,black")
with pygmt.config(
    FONT='8p,Helvetica,black',
    MAP_TICK_LENGTH_PRIMARY='2.5p/1.5p', # 一级刻度的主刻度和次刻度的长度 [2.5p/1.5p]
    MAP_FRAME_PEN='0.7p,black', # 一级边框的画笔属性；
    MAP_TICK_PEN_PRIMARY='0.7p,black', # 一级刻度的画笔属性；
):
    fig.colorbar(
        cmap = tomo_cpt,
        region = region,
        projection = projection,
        truncate=[-2,2],
        position = 'jMR+w5c/0.4c+o-1.2c/0c+v+m',
        frame = ['xa1f0.5+l"dlnVp (%)"'],
    )

# 显示图像
# fig.show()
fig.savefig('Tomo_LLNL.png',dpi=600)