import math
import pygmt
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d
from scipy.interpolate import griddata

# 读取地震层析成像结果数据
model_data = np.loadtxt('model/SP12RTS..ES.2891.unfrm.1.latlon.dat')

# 定义特定地区的深度切片经纬度范围
minlat = 45; maxlat = 70
minlon = -120; maxlon = 160

# 读取数据
latitudes = model_data[:,0]
longitudes = model_data[:,1]
dlnvs = model_data[:,2]

# 寻找区域的经纬度范围
region_index = np.where(((latitudes >= minlat) & (latitudes <= maxlat)) & ((longitudes <= minlon) | (longitudes >= maxlon)))

# 提取出该区域的数据 # lat lon dlnVs
region_slice = model_data[region_index,:][0]
lat_slice = region_slice[:,0]
lon_slice = region_slice[:,1]
dlnvs_slice = region_slice[:,2]

# 转换 (lat,lon) -> (lon,lat)
region_slice[:,[0,1]] = region_slice[:,[1,0]]
print("min dlnVs is %f, max dlnVs is %f\n" % (np.min(region_slice[:,2]),np.max(region_slice[:,2])))

fig = pygmt.Figure()
projection = "M5i"
transparency = 0   # 定义图像的透明度
pygmt.config(
        FONT='Helvetica',
        FONT_LABEL='10p,Helvetica,black',
        FONT_TITLE='10p,Helvetica',
        MAP_TITLE_OFFSET = '1p',
    )
region = [minlon-(180+minlon)-(180-maxlon),minlon,minlat,maxlat]
tomo_grd=pygmt.surface(
    data = region_slice,
    region = region,
    spacing = 0.05,
)
tomo_cpt=pygmt.grd2cpt(
    grid = tomo_grd,
    background = True,
    reverse=True,
    transparency=transparency,
    continuous = False,
    cmap = 'vik',
    # series = [math.floor(np.min(region_slice[:,2])),math.ceil(np.max(region_slice[:,2])),0.05],
    series = [-2,2,0.1],
)
fig.grdimage(
    grid = tomo_grd,
    cmap = tomo_cpt,
    region = region,
    transparency=transparency,
    projection = projection,
)
fig.coast(
    shorelines=True,
    area_thresh=100,
    region = region,
    projection = projection,
    resolution='i',
    frame=['WSne+t"SP12RTS"', "xa10f5", "ya5f2.5"]
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
        # truncate=[-2,2],
        position = 'jMR+w5c/0.4c+o-1.2c/0c+v+m',
        frame = ['xa1f0.5+l"dlnVs (%)"'],
    )
fig.savefig("Tomo_SP12RTS.png",dpi=600)

