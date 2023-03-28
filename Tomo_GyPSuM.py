import math
import pygmt
import numpy as np
import netCDF4 as nc

# 打开NetCDF文件
data = nc.Dataset('model/GYPSUM_percent.nc', 'r')

# 获取变量
lat = data.variables['latitude'][:]
lon = data.variables['longitude'][:]
depth = data.variables['depth'][:]
vs = data.variables['dvs'][:]
vp = data.variables['dvp'][:]

# 进行深度切片
depth_index = np.where(depth == 2900)[0][0]  # 选择深度为2900km的位置
vs_slice = vs[depth_index, :, :]  # 进行深度切片
# 进行深度和经纬度同时切片
lat_min, lat_max = 45.0, 70.0  # 纬度的范围
lon_min, lon_max = -120.0, 160.0  # 经度的范围
lat_index = np.where((lat >= lat_min) & (lat <= lat_max))[0]
lon_index = np.where((lon <= lon_min) | (lon >= lon_max))[0]
vs_slice = vs[depth_index, lat_index, :][:, lon_index]  # 进行深度和经纬度同时切片
vp_slice = vp[depth_index, lat_index, :][:, lon_index]  # 进行深度和经纬度同时切片

print("min dlnVs is %f, max dlnVs is %f\n" % (np.min(vs_slice),np.max(vs_slice)))
print("min dlnVp is %f, max dlnVp is %f\n" % (np.min(vp_slice),np.max(vp_slice)))

# 关闭NetCDF文件
data.close()

# 将截取到的数据二维数组展平成一维数组
vs_slice_flat = vs_slice.T.flatten()
vp_slice_flat = vp_slice.T.flatten()
lon_slice_index =  np.repeat(lon[lon_index], len(lat[lat_index]))
lat_slice_index =  np.tile(lat[lat_index], len(lon[lon_index]))

# 绘制CMB附近的S波速度结构
fig = pygmt.Figure()
pygmt.config(
    FONT_LABEL='10p',
    FONT_TITLE='10p,Helvetica',
    MAP_TITLE_OFFSET = '1p',
)
region = [-200, -120, lat_min, lat_max]  # 定义地图范围
projection = 'M5i'  # 定义投影方式，这里选择墨卡托投影
transparency = 10   # 定义图像的透明度
# 进行数据插值
interp_data = pygmt.surface(
    x=lon_slice_index, 
    y=lat_slice_index, 
    z=vs_slice_flat,
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
    series = [math.floor(np.min(vs_slice)),math.ceil(np.max(vs_slice)),0.1],
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
    frame=['WSne+t"GyPSuM-S"', "xa10f5", "ya5f2.5"]
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
# 显示图像
# fig.show()
fig.savefig('Tomo_GyPSuM_S.png',dpi=600)


# 绘制CMB附近的S波速度结构
fig = pygmt.Figure()
pygmt.config(
    FONT_LABEL='10p,Helvetica',
    FONT_TITLE='10p,Helvetica',
    MAP_TITLE_OFFSET = '1p',
)
region = [-200, -120, lat_min, lat_max]  # 定义地图范围
projection = 'M5i'  # 定义投影方式，这里选择墨卡托投影
transparency = 0   # 定义图像的透明度
# 进行数据插值
interp_data = pygmt.surface(
    x=lon_slice_index, 
    y=lat_slice_index, 
    z=vp_slice_flat,
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
    frame=['WSne+t"GyPSuM-P"', "xa10f5", "ya5f2.5"]
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
        frame = ['xa1f0.5+l"dlnVp (%)"'],
    )
# 显示图像
# fig.show()
fig.savefig('Tomo_GyPSuM_P.png',dpi=600)