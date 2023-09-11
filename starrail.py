import matplotlib
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file = '星穹铁道跃迁记录_20230907_173443.xlsx'

data = pd.read_excel(file, sheet_name='rawData')

DATE_COLUMN = 'time'
ID_COLUMN = 'id'
GACHA_ID_COLUMN = 'gacha_id'
ITEM_ID_COLUMN = 'item_id'
UID_COLUMN = 'uid'
RANK_TYPE = 'rank_type'
# gacha_id: 1001
# gacha_type: 1:常驻跃迁, 2:新手跃迁, 11:角色活动跃迁, 12:光锥活动跃迁

data_types_dict = {ID_COLUMN: str,
                   GACHA_ID_COLUMN: str,
                   ITEM_ID_COLUMN: str,
                   UID_COLUMN: str}

data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
data = data.astype(data_types_dict)
data['year'] = data[DATE_COLUMN].dt.year.astype(str)
data['month'] = data['year'] + "-" + data[DATE_COLUMN].dt.month.astype(str)

character = data.query("gacha_type == 11")
character['总次数'] = range(1, len(character) + 1)
character_5 = character.query("rank_type ==5")
a = character_5['总次数'].tolist()
c = []
for i in range(len(a) - 1):
    b = a[i + 1] - a[i]
    c.append(b)
c.insert(0, a[0])
character_5['保底内'] = c

st.title('星铁跃迁记录分析')
url = st.text_input('开始分析', '请在此输入url')

col1, col2, col3 = st.columns(3)
col1.metric("UID", f"{data[UID_COLUMN].loc[1]}", "")
col2.metric("总抽数", f"{data.shape[0]}", f"共花费{data.shape[0] * 160}星琼")
mean = f"{round(data.shape[0] / data[data[RANK_TYPE].isin([5])].shape[0])}"
col3.metric("平均出货次数", mean, f"共{data[data[RANK_TYPE].isin([5])].shape[0]}个金")
st.subheader('每月抽卡次数')
chronic_data = pd.pivot_table(data, index='month', columns=RANK_TYPE, values=ID_COLUMN, aggfunc='count')
st.bar_chart(chronic_data)

st.subheader('角色池')

import altair as alt
#
# base = alt.Chart(character_5).encode(
#     x='保底内',
#     y=alt.Y('name').title('name'),
#     color=alt.value('lightgray')
# )
# base.mark_bar() + base.mark_text(align='left', dx=2)

base = alt.Chart(character_5).encode(
    x='保底内',
    y=alt.Y('name:N',sort=None),
    color=alt.value('#e7ba52')
)

bars = base.mark_bar().encode(
    # sort=None
)
text = bars.mark_text(
    align='left',
    baseline='middle',
    dx=3
).encode(
    text='保底内:Q'
)

chart = (bars + text).properties(height=300)

tab1, tab2,tab3,tab4 = st.tabs(["角色池", "光锥池","常驻池","新手池"])

with tab1:
    st.altair_chart(chart, theme="streamlit", use_container_width=True)

