#!/bin/bash

LINK_DIR=era5_links/
mkdir -p ${LINK_DIR}

ERA5_BASE="/global/cfs/cdirs/m3522/cmip6/ERA5"

VARIABLES3D="128_060_pv 128_129_z 128_130_t 128_131_u 128_132_v 128_133_q 128_135_w"
VARIABLEESFC="128_134_sp 128_136_tcw 128_059_cape 128_167_2t"
VARIABLESVINTEG="162_071_viwve 162_072_viwvn"

# error-out on any failure
set -e 

# 3D variables
for var in $VARIABLES3D
do
    echo $var
    ln -s ${ERA5_BASE}/e5.oper.an.pl/*/*${var}*.nc ${LINK_DIR}
done

# surface variables
for var in $VARIABLEESFC
do
    echo $var
    ln -s ${ERA5_BASE}/e5.oper.an.sfc/*/*${var}*.nc ${LINK_DIR}
done

# vertically-integrated variables
for var in $VARIABLESVINTEG
do
    echo $var
    ln -s ${ERA5_BASE}/e5.oper.an.vinteg/*/*${var}*.nc ${LINK_DIR}/
done

# link precipitation, but remove any files in 2022, since other variables only go through 2021
ln -s /global/cfs/cdirs/m3522/cmip6/ERA5/e5.accumulated_tp_1h/e5.accumulated_tp_1h.*.nc ${LINK_DIR}
rm ${LINK_DIR}/e5.accumulated_tp_1h.2022*.nc

