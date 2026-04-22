import os
import pandas as pd
from datetime import datetime
import pytz
import glob

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

bj_tz = pytz.timezone('Asia/Shanghai')
now_bj = datetime.now(bj_tz)
report_date = now_bj.strftime('%Y年%m月%d日')
timestamp_str = now_bj.strftime('%Y%m%d%H%M%S')

existing_reports = glob.glob(os.path.join(OUTPUT_DIR, 'YB_*.html'))
next_num = len(existing_reports) + 1
filename = f"YB_000{next_num}_{timestamp_str}.html"
filepath = os.path.join(OUTPUT_DIR, filename)

df_index = pd.read_csv(os.path.join(OUTPUT_DIR, 'index_data.csv'))
df_stock = pd.read_csv(os.path.join(OUTPUT_DIR, 'stock_data.csv'))
df_cbbc = pd.read_csv(os.path.join(OUTPUT_DIR, 'cbbc_stock_data.csv'))

hsi = 26487.87
hstech = 5061.80
hscei = 9052.34
ndx = 26592.77
spx = 7109.14
dji = 49442.56

def calc_rise(current, target):
    return round((target - current) / current * 100, 2)

def calc_fall(current, target):
    return round((target - current) / current * 100, 2)

index_analysis = [
    {"name": "恒生指数", "code": "HSI", "current": hsi, "trend": "震荡偏强", "high": 28500, "low": 24000,
     "logic": "美伊停火谈判重启带来地缘缓和预期，南向资金持续流入，能源和煤炭板块受益油价上涨领涨，但科网股回调拖累科技指数，市场呈现结构性分化。"},
    {"name": "恒生科技指数", "code": "HSTECH", "current": hstech, "trend": "震荡偏弱", "high": 5800, "low": 4400,
     "logic": "科网股普遍回调（腾讯、阿里、美团下跌），AI概念高位获利回吐，但百度受自动驾驶催化逆势走强，板块内部分化加剧，短期缺乏统一方向。"},
    {"name": "国企指数", "code": "HSCEI", "current": hscei, "trend": "震荡上行", "high": 9800, "low": 8000,
     "logic": "中字头板块受益油价飙升和分红提升预期，能源板块（中海油、中石油、中石化）领涨，银行板块高股息防御属性突出，估值修复逻辑持续。"},
    {"name": "纳斯达克100指数", "code": ".NDX", "current": ndx, "trend": "震荡偏强", "high": 30000, "low": 24000,
     "logic": "纳指13连涨后首日回调0.3%，费半指数逆势14连涨，AI算力需求持续推动半导体板块，但美伊停火到期不确定性压制风险偏好，苹果换帅增添变数。"},
    {"name": "标普500指数", "code": ".SPX", "current": spx, "trend": "震荡偏强", "high": 7800, "low": 6500,
     "logic": "标普500止步五连涨，能源板块受益油价上涨，但科技和消费板块承压，一季报超预期比例近90%支撑盈利端，地缘风险限制估值扩张。"},
    {"name": "道琼斯指数", "code": ".DJI", "current": dji, "trend": "震荡偏强", "high": 53000, "low": 45000,
     "logic": "道指基本持平，传统行业盈利改善与油价成本压力对冲，苹果换帅事件对道指成分股影响有限，金融和能源板块提供底部支撑。"},
]

stock_analysis = [
    {"name": "腾讯控股", "code": "00700.HK", "price": 519.0, "trend": "震荡偏强", "high": 620, "low": 450, "advice": "做多", "position": "持有",
     "events": "微信AI搜索功能上线，游戏版号持续获批，回购计划推进", "logic": "AI赋能核心业务提升变现效率，游戏出海加速，估值仍有修复空间，短期回调提供加仓机会。"},
    {"name": "阿里巴巴", "code": "09988.HK", "price": 136.3, "trend": "震荡偏强", "high": 180, "low": 110, "advice": "做多", "position": "加仓",
     "events": "云业务AI收入快速增长，菜鸟分拆上市推进中", "logic": "电商基本盘稳固，云业务AI转型加速，估值处于历史低位具备安全边际。"},
    {"name": "小米", "code": "01810.HK", "price": 32.4, "trend": "震荡上行", "high": 42, "low": 26, "advice": "做多", "position": "加仓",
     "events": "小米汽车SU7交付量持续攀升，IoT生态扩张", "logic": "汽车业务放量带动估值重估，手机高端化战略见效，生态协同效应增强。"},
    {"name": "快手", "code": "01024.HK", "price": 46.38, "trend": "震荡偏强", "high": 58, "low": 38, "advice": "做多", "position": "持有",
     "events": "短剧和电商GMV增长超预期，海外业务减亏", "logic": "商业化效率持续提升，盈利拐点确认，但需关注用户增长天花板。"},
    {"name": "京东", "code": "09618.HK", "price": 123.0, "trend": "震荡偏弱", "high": 150, "low": 100, "advice": "观望", "position": "平仓",
     "events": "京东物流整合推进，百亿补贴效果待验证", "logic": "电商竞争加剧挤压利润率，物流优势难以完全转化为盈利，短期缺乏催化。"},
    {"name": "美团", "code": "03690.HK", "price": 86.45, "trend": "震荡偏强", "high": 105, "low": 68, "advice": "做多", "position": "持有",
     "events": "即时零售业务扩张，到店业务竞争趋缓", "logic": "本地生活壁垒稳固，新业务减亏趋势明确，盈利能力持续改善。"},
    {"name": "紫金矿业", "code": "02899.HK", "price": 38.2, "trend": "震荡上行", "high": 50, "low": 30, "advice": "做多", "position": "加仓",
     "events": "黄金价格屡创新高，铜矿产能扩张", "logic": "金价受益于地缘避险和降息预期，铜价受AI算力需求拉动，量价齐升逻辑清晰。"},
    {"name": "中芯国际", "code": "00981.HK", "price": 60.1, "trend": "震荡偏强", "high": 75, "low": 48, "advice": "做多", "position": "持有",
     "events": "成熟制程产能利用率回升，国产替代加速", "logic": "半导体国产化长期逻辑不变，成熟制程需求稳健，但先进制程突破仍需时间。"},
    {"name": "华虹半导体", "code": "01347.HK", "price": 95.4, "trend": "震荡偏弱", "high": 115, "low": 75, "advice": "观望", "position": "平仓",
     "events": "功率半导体需求分化，产能利用率恢复缓慢", "logic": "成熟制程竞争加剧，价格压力较大，需等待需求端明确改善信号。"},
    {"name": "泡泡玛特", "code": "09992.HK", "price": 164.4, "trend": "震荡偏强", "high": 200, "low": 130, "advice": "做多", "position": "持有",
     "events": "海外市场快速扩张，新IP持续孵化", "logic": "出海逻辑验证中，IP矩阵丰富度提升，但高估值需要业绩持续超预期支撑。"},
    {"name": "中国神华", "code": "01088.HK", "price": 46.58, "trend": "震荡上行", "high": 55, "low": 38, "advice": "做多", "position": "加仓",
     "events": "煤炭长协价格稳定，分红率维持高位，今日涨超3%领涨蓝筹", "logic": "高股息防御属性突出，煤价中枢上移利好盈利，能源板块整体受益油价上涨。"},
    {"name": "宁德时代", "code": "03750.HK", "price": 736.0, "trend": "震荡上行", "high": 920, "low": 580, "advice": "做多", "position": "加仓",
     "events": "港股股价再创历史新高，今日涨超4%，2026超级科技日将发布全新技术", "logic": "全球动力电池龙头地位稳固，储能业务高增长，超级科技日催化短期情绪。"},
    {"name": "赣锋锂业", "code": "01772.HK", "price": 80.4, "trend": "震荡偏弱", "high": 100, "low": 60, "advice": "观望", "position": "平仓",
     "events": "锂价低位震荡，产能扩张与需求恢复错配", "logic": "锂价底部确认但反弹力度有限，行业供给过剩格局未根本改变。"},
    {"name": "昆仑能源", "code": "00135.HK", "price": 7.74, "trend": "震荡偏强", "high": 9.5, "low": 6.5, "advice": "做多", "position": "持有",
     "events": "天然气销售量增长，管道资产注入预期", "logic": "天然气消费量稳步增长，中石油体系内资源协同优势明显，估值偏低。"},
    {"name": "中国石油化工股份", "code": "00386.HK", "price": 4.6, "trend": "震荡上行", "high": 5.8, "low": 3.8, "advice": "做多", "position": "加仓",
     "events": "油价飙升直接利好上游，炼化盈利改善", "logic": "油价高位利好上游，炼化价差修复，高股息特征在震荡市中具备吸引力。"},
    {"name": "国泰君安国际", "code": "01788.HK", "price": 2.65, "trend": "震荡偏强", "high": 3.3, "low": 2.2, "advice": "做多", "position": "持有",
     "events": "港股成交额回升利好经纪业务，跨境理财通扩容", "logic": "港股市场活跃度提升直接受益，财富管理转型推进，估值处于历史低位。"},
    {"name": "中国宏桥", "code": "01378.HK", "price": 37.12, "trend": "震荡上行", "high": 46, "low": 30, "advice": "做多", "position": "加仓",
     "events": "铝价受地缘冲突支撑上涨，产能优化推进", "logic": "电解铝供给刚性约束，油价推升能源成本但铝价传导顺畅，盈利弹性大。"},
    {"name": "招商银行", "code": "03968.HK", "price": 51.35, "trend": "震荡偏强", "high": 62, "low": 43, "advice": "做多", "position": "持有",
     "events": "零售银行龙头地位稳固，财富管理业务恢复增长", "logic": "资产质量优于同业，零售业务护城河深厚，估值修复空间较大。"},
    {"name": "建设银行", "code": "00939.HK", "price": 8.96, "trend": "震荡偏强", "high": 10.5, "low": 7.5, "advice": "做多", "position": "持有",
     "events": "信贷投放稳健，分红率维持30%以上", "logic": "国有大行估值极低，股息率超7%具备配置价值，但净息差收窄压力持续。"},
    {"name": "中国银行", "code": "03988.HK", "price": 5.25, "trend": "震荡偏强", "high": 6.2, "low": 4.4, "advice": "做多", "position": "持有",
     "events": "国际化业务优势突出，跨境人民币结算量增长", "logic": "外汇业务和跨境金融优势明显，高股息低估值特征突出。"},
    {"name": "汇丰控股", "code": "00005.HK", "price": 143.7, "trend": "震荡偏强", "high": 168, "low": 125, "advice": "做多", "position": "持有",
     "events": "利率维持高位利好净息差，回购计划持续推进", "logic": "高利率环境直接受益，亚洲业务增长强劲，股东回报力度大。"},
    {"name": "信达生物", "code": "01801.HK", "price": 89.85, "trend": "震荡上行", "high": 120, "low": 70, "advice": "做多", "position": "加仓",
     "events": "PD-1海外授权推进，减重药物临床进展积极", "logic": "创新药管线持续兑现，商业化能力提升，GLP-1赛道布局具备想象空间。"},
    {"name": "药明生物", "code": "02269.HK", "price": 35.3, "trend": "震荡偏弱", "high": 45, "low": 25, "advice": "观望", "position": "平仓",
     "events": "美国生物安全法案影响持续，海外订单恢复缓慢", "logic": "地缘政治风险压制估值，短期订单恢复不确定性大，需等待政策面明朗。"},
    {"name": "中国海洋石油", "code": "00883.HK", "price": 26.6, "trend": "震荡上行", "high": 34, "low": 22, "advice": "做多", "position": "加仓",
     "events": "油价飙升直接受益，深海油气勘探突破", "logic": "地缘冲突推升油价，桶油成本行业最低，高股息+高盈利弹性双击。"},
    {"name": "中国石油股份", "code": "00857.HK", "price": 10.44, "trend": "震荡上行", "high": 13.5, "low": 8.5, "advice": "做多", "position": "加仓",
     "events": "油价高位运行利好上游，天然气业务快速增长", "logic": "油价每涨10美元增厚利润约200亿，地缘溢价直接受益，估值仍偏低。"},
    {"name": "工商银行", "code": "01398.HK", "price": 7.26, "trend": "震荡偏强", "high": 8.5, "low": 6.0, "advice": "做多", "position": "持有",
     "events": "信贷规模稳健增长，不良率持续下降", "logic": "宇宙行估值极低，股息率超8%，防御配置价值突出。"},
    {"name": "比亚迪股份", "code": "01211.HK", "price": 109.1, "trend": "震荡上行", "high": 145, "low": 88, "advice": "做多", "position": "加仓",
     "events": "海外市场拓展加速，智能驾驶技术突破", "logic": "新能源车全球销量龙头，海外放量打开第二增长曲线，智能化升级提升产品力。"},
]

cbbc_stock_analysis = [
    {"name": "新鸿基地产", "code": "00016.HK", "price": 138.4, "trend": "震荡偏弱", "high": 160, "low": 115, "advice": "观望", "position": "平仓",
     "events": "香港楼市成交回暖但价格承压，利率维持高位增加融资成本", "logic": "高利率环境压制地产估值，楼市复苏力度不及预期，短期缺乏催化。"},
    {"name": "恒基地产", "code": "00012.HK", "price": 30.7, "trend": "震荡偏弱", "high": 36, "low": 25, "advice": "观望", "position": "平仓",
     "events": "农地转换进展缓慢，楼市去化压力仍存", "logic": "地产板块整体承压，利率高位增加持有成本，需等待楼市政策进一步放松。"},
    {"name": "新世界发展", "code": "00017.HK", "price": 8.82, "trend": "震荡下行", "high": 10.5, "low": 6.5, "advice": "做空", "position": "根据当前预设，做空无仓位调整建议",
     "events": "债务压力较大，出售资产回笼资金", "logic": "财务杠杆过高，降杠杆过程压制估值，地产业务恢复缓慢。"},
    {"name": "长实集团", "code": "01113.HK", "price": 48.86, "trend": "震荡偏弱", "high": 56, "low": 40, "advice": "观望", "position": "平仓",
     "events": "飞机租赁业务稳健，地产销售承压", "logic": "多元化业务提供一定防御，但地产核心业务仍受高利率压制。"},
    {"name": "香港交易所", "code": "00388.HK", "price": 417.2, "trend": "震荡偏强", "high": 480, "low": 360, "advice": "做多", "position": "持有",
     "events": "港股成交额回升，胜宏科技IPO首日涨超50%", "logic": "市场活跃度提升直接受益，IPO市场回暖，垄断地位不可替代。"},
    {"name": "友邦保险", "code": "01299.HK", "price": 82.8, "trend": "震荡偏强", "high": 98, "low": 70, "advice": "做多", "position": "持有",
     "events": "新业务价值增长稳健，内地访客需求强劲", "logic": "亚太寿险龙头地位稳固，利率高位利好投资收益，估值处于合理区间。"},
    {"name": "中国人寿", "code": "02628.HK", "price": 27.52, "trend": "震荡偏强", "high": 34, "low": 22, "advice": "做多", "position": "持有",
     "events": "保费收入增长，投资收益改善", "logic": "寿险行业景气度回升，权益市场回暖利好投资端，估值修复空间较大。"},
    {"name": "中国平安", "code": "02318.HK", "price": 61.45, "trend": "震荡偏强", "high": 75, "low": 50, "advice": "做多", "position": "持有",
     "events": "综合金融生态协同增强，科技赋能降本增效", "logic": "金融+科技双轮驱动，寿险改革成效显现，估值处于历史低位。"},
    {"name": "中国移动", "code": "00941.HK", "price": 83.7, "trend": "震荡偏强", "high": 95, "low": 70, "advice": "做多", "position": "持有",
     "events": "5G用户渗透率提升，算力网络建设加速，国内首个Pre6G试验网投入运行", "logic": "高股息+稳增长特征突出，AI算力需求拉动云业务增长，6G催化通信板块。"},
    {"name": "中国联通", "code": "00762.HK", "price": 7.4, "trend": "震荡偏强", "high": 8.8, "low": 6.2, "advice": "做多", "position": "持有",
     "events": "产业互联网收入占比提升，大数据业务增长", "logic": "数字化转型加速，产业互联网打开增长空间，估值偏低具备安全边际。"},
    {"name": "中国电信", "code": "00728.HK", "price": 5.05, "trend": "震荡偏强", "high": 6.0, "low": 4.2, "advice": "做多", "position": "持有",
     "events": "天翼云收入高速增长，AI大模型落地应用，Pre6G试验网投入运行", "logic": "云业务增速行业领先，AI+通信融合催化，高股息率具备配置吸引力。"},
    {"name": "网易", "code": "09999.HK", "price": 182.9, "trend": "震荡偏强", "high": 220, "low": 155, "advice": "做多", "position": "持有",
     "events": "新游戏上线表现优异，AI赋能游戏研发提效", "logic": "游戏管线丰富，AI降本增效逻辑清晰，海外市场拓展顺利。"},
    {"name": "百度集团", "code": "09888.HK", "price": 124.6, "trend": "震荡上行", "high": 155, "low": 100, "advice": "做多", "position": "加仓",
     "events": "文心大模型持续迭代，自动驾驶商业化推进，今日逆势涨超1%", "logic": "AI搜索和大模型商业化加速，自动驾驶Robotaxi落地，估值修复空间大。"},
    {"name": "哔哩哔哩", "code": "09626.HK", "price": 189.5, "trend": "震荡偏强", "high": 240, "low": 160, "advice": "做多", "position": "持有",
     "events": "广告和增值服务收入高增长，首次实现季度盈利", "logic": "盈利拐点确认，社区生态变现效率提升，但估值偏高需业绩持续验证。"},
    {"name": "蔚来", "code": "09866.HK", "price": 52.65, "trend": "震荡偏弱", "high": 65, "low": 38, "advice": "观望", "position": "平仓",
     "events": "换电网络扩张，但交付量增长放缓", "logic": "换电模式差异化但资本开支大，销量增速落后竞品，盈利时点不确定。"},
    {"name": "理想汽车", "code": "02015.HK", "price": 73.2, "trend": "震荡偏强", "high": 92, "low": 58, "advice": "做多", "position": "持有",
     "events": "纯电车型上市，智驾技术迭代", "logic": "产品矩阵完善，家庭用车定位精准，但纯电转型效果待验证。"},
    {"name": "小鹏汽车", "code": "09868.HK", "price": 68.3, "trend": "震荡偏强", "high": 88, "low": 52, "advice": "做多", "position": "持有",
     "events": "MONA系列销量超预期，智驾技术领先", "logic": "智驾技术护城河加深，大众合作推进，但盈利能力仍需改善。"},
    {"name": "海尔智家", "code": "06690.HK", "price": 21.36, "trend": "震荡偏强", "high": 26, "low": 18, "advice": "做多", "position": "持有",
     "events": "海外市场盈利改善，高端品牌卡萨帝增长", "logic": "全球化布局成效显现，高端化战略提升盈利能力，估值合理。"},
    {"name": "李宁", "code": "02331.HK", "price": 21.42, "trend": "震荡偏弱", "high": 26, "low": 16, "advice": "观望", "position": "平仓",
     "events": "国潮热度退减，库存去化进行中", "logic": "运动服饰竞争加剧，品牌力边际减弱，需等待渠道改革和产品创新见效。"},
    {"name": "安踏体育", "code": "02020.HK", "price": 86.1, "trend": "震荡偏强", "high": 105, "low": 70, "advice": "做多", "position": "持有",
     "events": "亚玛芬体育整合顺利，多品牌战略成效显著", "logic": "多品牌矩阵覆盖各细分市场，全球化进程加速，经营效率行业领先。"},
]

index_table_csv = df_index.to_html(index=False, classes="data-table", border=0, escape=False)
stock_table_csv = df_stock.to_html(index=False, classes="data-table", border=0, escape=False)
cbbc_table_csv = df_cbbc.to_html(index=False, classes="data-table", border=0, escape=False)

def make_index_row(ia):
    high_rise = calc_rise(ia["current"], ia["high"])
    low_fall = calc_fall(ia["current"], ia["low"])
    return f"""<tr>
<td>{ia['name']}</td><td>{ia['code']}</td><td>{ia['current']:,.2f}</td>
<td>{ia['trend']}</td><td>{ia['high']:,.2f}</td><td>{high_rise}%</td>
<td>{ia['low']:,.2f}</td><td>{low_fall}%</td>
<td>{ia['logic']}</td>
</tr>"""

def make_stock_row(sa):
    high_rise = calc_rise(sa["price"], sa["high"])
    low_fall = calc_fall(sa["price"], sa["low"])
    return f"""<tr>
<td>{sa['name']}</td><td>{sa['code']}</td><td>{sa['price']:.2f}</td>
<td>{sa['trend']}</td><td>{sa['high']:.2f}</td><td>{high_rise}%</td>
<td>{sa['low']:.2f}</td><td>{low_fall}%</td>
<td>{sa['advice']}</td><td>{sa['position']}</td>
<td>{sa['events']}</td><td>{sa['logic']}</td>
</tr>"""

index_rows = "".join(make_index_row(ia) for ia in index_analysis)
stock_rows = "".join(make_stock_row(sa) for sa in stock_analysis)
cbbc_rows = "".join(make_stock_row(ca) for ca in cbbc_stock_analysis)

html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>跨市场重大事件与港股龙头策略研判 - {report_date}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; line-height: 1.8; color: #2c3e50; background: #f8f9fa; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
.header {{ background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%); color: white; padding: 40px; border-radius: 12px; margin-bottom: 30px; text-align: center; }}
.header h1 {{ font-size: 2em; margin-bottom: 10px; letter-spacing: 2px; }}
.header .date {{ font-size: 1.1em; opacity: 0.9; }}
.toc {{ background: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
.toc h2 {{ color: #1a237e; margin-bottom: 20px; border-bottom: 2px solid #1a237e; padding-bottom: 10px; }}
.toc ul {{ list-style: none; padding-left: 0; }}
.toc li {{ margin: 8px 0; }}
.toc a {{ color: #3949ab; text-decoration: none; font-size: 1.05em; transition: color 0.2s; }}
.toc a:hover {{ color: #1a237e; text-decoration: underline; }}
.toc .sub {{ padding-left: 25px; }}
.toc .sub a {{ font-size: 0.95em; color: #5c6bc0; }}
.section {{ background: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
.section h2 {{ color: #1a237e; margin-bottom: 20px; border-bottom: 2px solid #e8eaf6; padding-bottom: 10px; font-size: 1.5em; }}
.section h3 {{ color: #283593; margin: 20px 0 15px; font-size: 1.2em; }}
.section h4 {{ color: #3949ab; margin: 15px 0 10px; font-size: 1.05em; }}
.data-table {{ width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 0.9em; }}
.data-table th {{ background: #e8eaf6; color: #1a237e; padding: 12px 8px; text-align: center; font-weight: 600; border: 1px solid #c5cae9; }}
.data-table td {{ padding: 10px 8px; text-align: center; border: 1px solid #e0e0e0; }}
.data-table tr:nth-child(even) {{ background: #f5f5f5; }}
.data-table tr:hover {{ background: #e8eaf6; }}
.event-card {{ background: #f8f9fa; border-left: 4px solid #3949ab; padding: 15px 20px; margin: 15px 0; border-radius: 0 8px 8px 0; }}
.event-card h4 {{ color: #1a237e; margin-bottom: 8px; }}
.event-card .time {{ color: #e65100; font-weight: 600; font-size: 0.9em; }}
.scenario {{ display: inline-block; padding: 3px 10px; border-radius: 4px; font-size: 0.85em; margin: 3px; }}
.scenario.base {{ background: #e3f2fd; color: #1565c0; }}
.scenario.optimistic {{ background: #e8f5e9; color: #2e7d32; }}
.scenario.pessimistic {{ background: #fce4ec; color: #c62828; }}
.tag {{ display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 0.8em; margin: 2px; }}
.tag.up {{ background: #e8f5e9; color: #2e7d32; }}
.tag.down {{ background: #fce4ec; color: #c62828; }}
.tag.neutral {{ background: #fff3e0; color: #e65100; }}
.tag.strong {{ background: #e3f2fd; color: #1565c0; }}
.reasoning-chain {{ background: #f3e5f5; padding: 20px; border-radius: 8px; margin: 15px 0; }}
.reasoning-chain h4 {{ color: #6a1b9a; }}
.ref-list {{ font-size: 0.9em; }}
.ref-list li {{ margin: 8px 0; }}
.ref-list a {{ color: #3949ab; }}
.footer {{ text-align: center; color: #9e9e9e; padding: 20px; font-size: 0.85em; }}
.disclaimer {{ background: #fff3e0; padding: 15px; border-radius: 8px; margin: 20px 0; font-size: 0.85em; color: #e65100; }}
</style>
</head>
<body>
<div class="container">

<div class="header">
<h1>跨市场重大事件与港股龙头策略研判</h1>
<div class="date">报告日期：{report_date}（北京时间）</div>
</div>

<div class="toc">
<h2>目录</h2>
<ul>
<li><a href="#section1">一、市场数据</a>
<ul class="sub">
<li><a href="#section1-1">1.1 指数数据表</a></li>
<li><a href="#section1-2">1.2 指定个股数据表</a></li>
<li><a href="#section1-3">1.3 拥有可交易牛熊证的额外港股个股数据表</a></li>
</ul>
</li>
<li><a href="#section2">二、重大事件分析</a>
<ul class="sub">
<li><a href="#section2-1">2.1 近期已发生的重大事件</a></li>
<li><a href="#section2-2">2.2 未来一周将要发生的重大事件</a></li>
<li><a href="#section2-3">2.3 重点关注领域</a></li>
</ul>
</li>
<li><a href="#section3">三、指数研判</a></li>
<li><a href="#section4">四、个股分析</a>
<ul class="sub">
<li><a href="#section4-1">4.1 指定个股分析</a></li>
<li><a href="#section4-2">4.2 当前存在可交易牛熊证的个股分析</a></li>
</ul>
</li>
<li><a href="#section5">五、分析推理过程</a></li>
<li><a href="#section6">六、参考资料</a></li>
</ul>
</div>

<div class="section" id="section1">
<h2>一、市场数据</h2>

<h3 id="section1-1">1.1 指数数据表</h3>
{index_table_csv}

<h3 id="section1-2">1.2 指定个股数据表</h3>
{stock_table_csv}

<h3 id="section1-3">1.3 拥有可交易牛熊证的额外港股个股数据表</h3>
{cbbc_table_csv}
</div>

<div class="section" id="section2">
<h2>二、重大事件分析</h2>

<h3 id="section2-1">2.1 近期已发生的重大事件</h3>

<div class="event-card">
<h4>1. 美伊停火协议即将到期，伊斯兰堡第二轮谈判启动</h4>
<p class="time">发生时间：2026年4月20日-21日</p>
<p><strong>事件概述：</strong>美伊两周临时停火协议将于北京时间4月22日8时（华盛顿时间4月22日晚）正式到期。4月21日，第二轮谈判在巴基斯坦伊斯兰堡启动，美国副总统万斯率团抵达。伊朗议长卡利巴夫带队参会，但明确表示"不接受威胁下的谈判"。特朗普称停火到期后"极不可能"延长，若达不成协议将立即恢复军事打击。</p>
<p><strong>对市场的影响机制：</strong>停火到期不确定性压制全球风险偏好，美股三大指数4月21日小幅收跌（标普500跌0.24%至7109.14点）。但伊朗最高领袖哈梅内伊批准谈判的消息一度刺激A股港股暴力拉升，市场对达成协议仍存期待。</p>
<p><strong>后续进展预期：</strong>4月22日停火到期后三种可能：谈判破裂战火重燃（概率70%）、临时延长停火（概率20%）、达成框架协议（概率10%）。</p>
<p><strong>对市场的持续影响评估：</strong>若冲突升级，油价可能突破130-180美元/桶，全球股市面临大幅回调；若达成协议，地缘溢价快速消退，风险资产将迎来反弹。</p>
</div>

<div class="event-card">
<h4>2. 霍尔木兹海峡"双重封锁"，26艘伊朗商船突破美军封锁</h4>
<p class="time">发生时间：2026年4月20日-21日</p>
<p><strong>事件概述：</strong>美军4月20日在阿曼湾武力扣押伊朗货轮"图斯卡号"，伊朗随即再度军事管控霍尔木兹海峡，海峡陷入"双重封锁"。但4月21日，至少26艘涉伊商船成功突破美军封锁通航，美军未敢开火升级冲突。伊朗革命卫队宣布全面掌控海峡，划定禁航区。</p>
<p><strong>对市场的影响机制：</strong>海峡封锁担忧推升国际油价，WTI原油涨至89.61美元/桶（+6.87%），布伦特原油涨至95.48美元/桶（+5.64%）。但26艘商船突破封锁显示美军封锁效力下降，市场对海峡长期受阻的担忧有所缓解。</p>
<p><strong>后续进展预期：</strong>若美军封锁彻底失效，伊朗石油出口恢复将缓解全球供应紧张；若冲突升级导致海峡长期关闭，全球能源运输将面临严重中断。</p>
<p><strong>对市场的持续影响评估：</strong>油价中枢上移将重塑市场风格，港股能源板块（中海油、中石油、中石化）直接受益，但制造业和消费板块成本压力加大。</p>
</div>

<div class="event-card">
<h4>3. 苹果官宣换帅：库克转任执行董事长，特努斯9月接任CEO</h4>
<p class="time">发生时间：2026年4月20日（美东时间）</p>
<p><strong>事件概述：</strong>苹果公司宣布，现任CEO蒂姆·库克将转任董事会执行董事长，硬件工程高级副总裁约翰·特努斯（John Ternus）将于9月1日接任CEO。库克执掌苹果15年间市值增长24倍，年收入突破4000亿美元。同日，苹果还宣布约翰尼·斯鲁吉的人事变动。</p>
<p><strong>对市场的影响机制：</strong>苹果换帅对全球科技股情绪产生短期扰动，但特努斯作为内部人接班降低不确定性。苹果供应链（港股立讯精密等）需关注新CEO战略方向调整。</p>
<p><strong>后续进展预期：</strong>9月正式交接前为过渡期，预计业务连续性强。特努斯作为硬件负责人，可能更注重产品创新和AI硬件整合。</p>
<p><strong>对市场的持续影响评估：</strong>短期影响有限，但需关注6月WWDC上新CEO的首秀表现，以及苹果AI战略在新领导下的推进节奏。</p>
</div>

<div class="event-card">
<h4>4. 美股三大指数从历史高位小幅回调，费半指数14连涨</h4>
<p class="time">发生时间：2026年4月21日（美东时间）</p>
<p><strong>事件概述：</strong>标普500指数跌0.24%至7109.14点，止步五连涨；纳指跌0.26%至24404.39点；道指基本持平报49442.56点。但费城半导体指数逆势上涨0.5%，录得14连涨（2014年以来最长），英伟达涨0.19%，博通涨2.03%。美满电子涨5.8%至历史新高（谷歌商议开发新AI芯片）。</p>
<p><strong>对市场的影响机制：</strong>美股高位回调对港股形成短期压力，但AI算力需求持续推动半导体板块，港股AI概念（中芯国际、华虹半导体）可能受益于费半强势。</p>
<p><strong>后续进展预期：</strong>本周特斯拉、IBM等重磅财报将决定美股方向，若盈利超预期可能重拾升势。</p>
<p><strong>对市场的持续影响评估：</strong>美股整体仍处高位，对港股情绪支撑仍在，但需警惕地缘风险升级导致的联动下跌。</p>
</div>

<div class="event-card">
<h4>5. 恒指收涨0.48%，宁德时代涨超4%创新高，科网股回调</h4>
<p class="time">发生时间：2026年4月21日</p>
<p><strong>事件概述：</strong>恒生指数收涨0.48%报26487.87点，恒生科技指数跌0.08%报5061.80点。板块分化明显：硬件设备、电气设备、煤炭板块领涨（中国神华涨超3%），宁德时代涨超4%创历史新高；国防军工、医药生物、钢铁板块跌幅居前。胜宏科技IPO首日涨超50%。南向资金净买入37.38亿港元。</p>
<p><strong>对市场的影响机制：</strong>市场呈现"能源强、科技弱"的结构性格局，反映地缘风险偏好下降背景下资金从成长向价值轮动。宁德时代受超级科技日催化逆势走强。</p>
<p><strong>后续进展预期：</strong>若美伊谈判取得进展，科网股有望反弹；若冲突升级，能源板块将继续领涨。</p>
<p><strong>对市场的持续影响评估：</strong>结构性分化可能持续，建议关注能源+高股息防御配置，同时逢低布局AI科技主线。</p>
</div>

<div class="event-card">
<h4>6. 国内油价4月21日24时迎来2026年首次下调</h4>
<p class="time">发生时间：2026年4月21日24时</p>
<p><strong>事件概述：</strong>尽管国际油价大涨（WTI 89.61美元/桶、布伦特95.48美元/桶），但国内成品油价因前期统计周期内原油变化率达-7.81%，预计下调820元/吨，折合每升下调0.62-0.74元，为2026年首次下跌。</p>
<p><strong>对市场的影响机制：</strong>国内油价下调利好消费和制造业成本端，对航空、物流等用油行业形成正面催化，但国际油价高位对港股能源板块构成利好。</p>
<p><strong>后续进展预期：</strong>下一轮油价调整窗口需关注中东局势演变，若地缘冲突升级，国内油价可能重回上涨通道。</p>
<p><strong>对市场的持续影响评估：</strong>短期国内油价下调缓解通胀压力，但国际油价高位运行的传导效应将在后续调整中体现。</p>
</div>

<h3 id="section2-2">2.2 未来一周将要发生的重大事件</h3>

<div class="event-card">
<h4>1. 美伊停火协议到期（4月22日北京时间早8点）</h4>
<p class="time">预计时间：2026年4月22日08:00（北京时间）/ 4月22日晚（华盛顿时间）</p>
<p><strong>事件概述：</strong>美伊两周临时停火协议到期，伊斯兰堡第二轮谈判结果将决定战和走向。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario pessimistic">悲观情景（概率70%）：谈判破裂，战火重燃，美军恢复空袭，伊朗封锁霍尔木兹海峡，油价突破130-180美元/桶，全球股市大幅回调</span></p>
<p><span class="scenario base">基准情景（概率20%）：双方短暂延长停火2-3天继续谈判，但核心分歧仍在，市场震荡加剧</span></p>
<p><span class="scenario optimistic">乐观情景（概率10%）：伊朗做出重大让步达成框架协议，地缘溢价快速消退，油价回落至80美元以下，全球风险资产反弹</span></p>
</div>

<div class="event-card">
<h4>2. 美联储发布经济状况褐皮书（4月23日）</h4>
<p class="time">预计时间：2026年4月23日（美东时间）</p>
<p><strong>事件概述：</strong>美联储将发布经济状况褐皮书，揭示关税政策和地缘冲突对地区经济的实际影响，制造业投入价格指数尤其值得关注。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率50%）：经济温和增长，通胀压力持续但不恶化，市场反应有限</span></p>
<p><span class="scenario optimistic">乐观情景（概率20%）：经济韧性超预期，通胀回落迹象明显，降息预期升温</span></p>
<p><span class="scenario pessimistic">悲观情景（概率30%）：滞胀风险上升，高油价传导至核心通胀，美联储鹰派立场强化</span></p>
</div>

<div class="event-card">
<h4>3. Google Cloud Next大会（4月22日-24日）</h4>
<p class="time">预计时间：2026年4月22日-24日</p>
<p><strong>事件概述：</strong>谷歌将举办Google Cloud Next大会，预计发布新一代TPU架构。美满电子已因谷歌商议开发新AI芯片消息涨5.8%，大会可能进一步催化AI算力产业链。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率45%）：TPU架构迭代符合预期，AI算力需求叙事延续，相关个股温和上涨</span></p>
<p><span class="scenario optimistic">乐观情景（概率35%）：新一代TPU性能大幅提升，AI算力投资加速，港股AI概念股大涨</span></p>
<p><span class="scenario pessimistic">悲观情景（概率20%）：发布内容不及预期，AI投资增速放缓担忧升温，科技股回调</span></p>
</div>

<div class="event-card">
<h4>4. 特斯拉、IBM等一季报披露</h4>
<p class="time">预计时间：2026年4月22日-25日</p>
<p><strong>事件概述：</strong>特斯拉、IBM、洛克希德·马丁等公司将披露一季报。目前标普500已公布业绩的公司中近90%利润超预期。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率45%）：特斯拉业绩符合预期，市场反应中性</span></p>
<p><span class="scenario optimistic">乐观情景（概率25%）：特斯拉交付量超预期+AI进展，新能源板块联动上涨</span></p>
<p><span class="scenario pessimistic">悲观情景（概率30%）：特斯拉利润率下滑，新能源车板块承压</span></p>
</div>

<div class="event-card">
<h4>5. 宁德时代2026超级科技日（4月21日已举办）后续催化</h4>
<p class="time">预计时间：2026年4月22日-25日</p>
<p><strong>事件概述：</strong>宁德时代4月21日举办"超级科技日"发布会，称"公司成立以来技术密度最高的一场"，将推出全新技术、产品和生态。港股股价当日涨超4%创新高。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率40%）：技术发布符合预期，股价高位震荡消化涨幅</span></p>
<p><span class="scenario optimistic">乐观情景（概率35%）：固态电池等突破性技术超预期，产业链（赣锋锂业等）联动上涨</span></p>
<p><span class="scenario pessimistic">悲观情景（概率25%）：技术发布不及市场高预期，获利回吐导致回调</span></p>
</div>

<h3 id="section2-3">2.3 重点关注领域</h3>

<h4>⭐⭐⭐ 美联储货币政策</h4>
<div class="event-card">
<p><strong>最新立场：</strong>3月FOMC会议维持利率3.5%-3.75%不变。4月28-29日将召开下一次议息会议，维持利率不变概率高达99.5%。</p>
<p><strong>利率路径预期：</strong>德银预计2026年全年维持利率不变。CME数据显示6月降息概率仅4.5%。芝加哥联储主席古尔斯比称若油价长期高企，美联储可能需等到2027年才会降息。圣路易斯联储主席穆萨莱姆称高油价可能使基本通胀率比2%目标高出近一个百分点。</p>
<p><strong>缩表节奏：</strong>缩表仍在持续但节奏已放缓，市场流动性边际改善但整体仍偏紧。</p>
</div>

<h4>⭐⭐⭐ 中东地缘政治危机</h4>
<div class="event-card">
<p><strong>冲突最新动态：</strong>美伊停火协议4月22日北京时间早8点到期，伊斯兰堡第二轮谈判已启动。美军扣押伊朗货轮"图斯卡号"，伊朗再度管控霍尔木兹海峡。26艘伊朗商船突破美军封锁。三支美军航母编队压境。</p>
<p><strong>对油价影响：</strong>WTI原油89.61美元/桶（+6.87%），布伦特95.48美元/桶（+5.64%）。若冲突升级，油价可能突破130-180美元/桶。</p>
<p><strong>避险情绪传导：</strong>全球避险情绪升温，资金从成长向价值轮动，港股能源+高股息板块受益，科网股承压。</p>
<p><strong>供应链风险：</strong>霍尔木兹海峡承担全球约30%石油海运，"双重封锁"格局下全球能源运输面临严重中断风险。</p>
</div>
</div>

<div class="section" id="section3">
<h2>三、指数研判</h2>

<table class="data-table">
<thead>
<tr>
<th>指数名称</th><th>指数代码</th><th>当前最新点数</th>
<th>未来一个月趋势预判</th>
<th>截止2026年12月31日最高目标点数</th><th>最高目标点数相对当前涨幅</th>
<th>截止2026年12月31日最低目标点数</th><th>最低目标点数相对当前跌幅</th>
<th>未来一个月趋势预判的核心逻辑</th>
</tr>
</thead>
<tbody>
{index_rows}
</tbody>
</table>
</div>

<div class="section" id="section4">
<h2>四、个股分析</h2>

<h3 id="section4-1">4.1 指定个股分析</h3>

<table class="data-table">
<thead>
<tr>
<th>股票名称</th><th>股票代码</th><th>当前最新价格(HKD)</th>
<th>未来一个月趋势预判</th>
<th>截止2026年12月31日最高目标价</th><th>最高目标价相对最新价格涨幅</th>
<th>截止2026年12月31日最低目标价</th><th>最低目标价相对最新价格跌幅</th>
<th>当前做多做空建议</th><th>当前仓位调整建议</th>
<th>近期个股自身重大事件</th><th>未来一个月趋势预判的核心逻辑</th>
</tr>
</thead>
<tbody>
{stock_rows}
</tbody>
</table>

<h3 id="section4-2">4.2 当前存在可交易牛熊证的个股分析</h3>

<table class="data-table">
<thead>
<tr>
<th>股票名称</th><th>股票代码</th><th>当前最新价格(HKD)</th>
<th>未来一个月趋势预判</th>
<th>截止2026年12月31日最高目标价</th><th>最高目标价相对最新价格涨幅</th>
<th>截止2026年12月31日最低目标价</th><th>最低目标价相对最新价格跌幅</th>
<th>当前做多做空建议</th><th>当前仓位调整建议</th>
<th>近期个股自身重大事件</th><th>未来一个月趋势预判的核心逻辑</th>
</tr>
</thead>
<tbody>
{cbbc_rows}
</tbody>
</table>
</div>

<div class="section" id="section5">
<h2>五、分析推理过程</h2>

<div class="reasoning-chain">
<h4>1. 宏观判断链</h4>
<p><strong>重大事件 → 宏观环境影响 → 市场整体方向</strong></p>
<p>美伊停火协议4月22日到期，伊斯兰堡谈判分歧巨大（核问题、海峡管理、制裁解除三大死结无进展），冲突升级概率70%。美军海上封锁遭26艘伊朗商船突破，封锁效力下降但冲突风险上升。油价飙升（WTI 89.61、布伦特95.48美元/桶）推升全球通胀预期，美联储降息推迟至2027年。苹果换帅增添科技股不确定性。国内油价下调820元/吨缓解消费端压力。港股呈现"能源强、科技弱"结构性格局，南向资金净买入37.38亿港元提供底部支撑。</p>
</div>

<div class="reasoning-chain">
<h4>2. 指数推导链</h4>
<p><strong>宏观判断 → 各指数差异化表现</strong></p>
<p>恒生指数：能源+煤炭板块受益油价领涨，南向资金持续流入支撑底部，但科网股回调拖累，整体震荡偏强。</p>
<p>恒生科技指数：科网股普遍回调（腾讯、阿里、美团下跌），AI概念高位获利回吐，仅百度逆势走强，板块内部分化加剧，震荡偏弱。</p>
<p>国企指数：中字头能源板块领涨（中海油、中石油、中石化），银行高股息防御属性突出，震荡上行。</p>
<p>美股三大指数：从历史高位小幅回调，费半14连涨显示AI算力需求仍强，但地缘风险压制风险偏好，震荡偏强。</p>
</div>

<div class="reasoning-chain">
<h4>3. 个股推导链</h4>
<p><strong>宏观+行业+个股事件 → 个股趋势判断</strong></p>
<p>能源板块（中海油、中石油、中石化、紫金矿业、中国神华）：油价飙升+地缘风险直接受益，量价齐升逻辑最清晰，目标价上行空间最大。</p>
<p>AI科技板块（腾讯、百度、中芯国际）：AI催化持续但内部分化，百度受自动驾驶催化逆势走强，腾讯和阿里短期回调提供布局机会。</p>
<p>新能源板块（宁德时代、比亚迪）：宁德时代超级科技日催化创新高，比亚迪海外拓展加速，龙头优势明显。</p>
<p>银行板块（招行、建行、工行、中行）：高股息防御属性突出，但净息差收窄限制上行空间。</p>
<p>地产板块（新鸿基、恒基、新世界）：高利率环境持续压制，短期缺乏催化，建议观望或做空。</p>
<p>创新药板块（信达生物、药明生物）：分化明显，信达管线兑现+GLP-1催化看多，药明受地缘风险压制观望。</p>
</div>

<div class="reasoning-chain">
<h4>4. 关键假设</h4>
<p>① 中东冲突不会演变为全面战争，霍尔木兹海峡不会长期完全关闭（不确定性：高）</p>
<p>② 美联储2026年维持利率3.5%-3.75%不变（不确定性：中）</p>
<p>③ 中国经济温和复苏，GDP增速4.5%-5.0%（不确定性：中）</p>
<p>④ AI产业资本开支维持30%以上增速（不确定性：低）</p>
<p>⑤ 南向资金日均净流入维持30亿港元以上（不确定性：中）</p>
</div>

<div class="reasoning-chain">
<h4>5. 风险提示</h4>
<p>① <strong>地缘风险超预期升级</strong>：若美伊谈判破裂冲突全面升级，油价可能突破130-180美元/桶，全球股市将面临10%-20%回调。</p>
<p>② <strong>美联储鹰派超预期</strong>：若通胀因油价飙升再度加速，美联储可能重启加息，全球风险资产将大幅承压。</p>
<p>③ <strong>中国经济复苏不及预期</strong>：若内需持续疲弱，港股盈利端将面临下修压力。</p>
<p>④ <strong>AI投资增速放缓</strong>：若科技巨头削减AI资本开支，港股科技板块估值将面临回调。</p>
<p>⑤ <strong>苹果换帅不确定性</strong>：新CEO战略方向调整可能影响全球科技供应链格局。</p>
</div>
</div>

<div class="section" id="section6">
<h2>六、参考资料</h2>

<h3>宏观政策类</h3>
<ul class="ref-list">
<li><a href="https://36kr.com/newsflashes/3774347781095940" target="_blank">美联储4月维持利率不变的概率为99.5%</a> — CME美联储观察数据，36氪 (36kr.com)</li>
<li><a href="http://m.toutiao.com/group/7629628119799824911/" target="_blank">德银调整预期：美联储2026年料按兵不动</a> — 德意志银行最新预测，财联社 (toutiao.com)</li>
<li><a href="https://finance.eastmoney.com/a/202604203710365193.html" target="_blank">央行圆桌汇：前景不确定性限制美联储利率指引</a> — 东方财富网 (eastmoney.com)</li>
</ul>

<h3>地缘政治类</h3>
<ul class="ref-list">
<li><a href="http://m.toutiao.com/group/7631029959393329714/" target="_blank">中东：美伊谈判生死局，停火明日到期</a> — 美伊谈判三大死结分析，今日头条 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7630969760498401833/" target="_blank">停火倒计时：美伊战云密布，多维博弈全面升级</a> — 海峡双重封锁与经济绞杀，今日头条 (toutiao.com)</li>
<li><a href="https://m.weibo.cn/detail/5290127752694855" target="_blank">26艘涉伊航运船只突破美军海上封锁</a> — 微博实时战况 (weibo.cn)</li>
<li><a href="http://m.toutiao.com/group/7631106927552807474/" target="_blank">美伊谈判突传利好，股市暴力拉升</a> — 哈梅内伊批准谈判消息，今日头条 (toutiao.com)</li>
</ul>

<h3>行业/公司类</h3>
<ul class="ref-list">
<li><a href="https://36kr.com/newsflashes/3776300212732674" target="_blank">恒指收涨0.48%，宁德时代涨超4%</a> — 港股4月21日收盘数据，36氪 (36kr.com)</li>
<li><a href="http://m.toutiao.com/group/7631118151052165682/" target="_blank">2026年4月21日收盘小结</a> — A股港股收盘总结，今日头条 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7631093319287800356/" target="_blank">宁德时代港股股价创新高，A股第四大股东拟转让1.27%股份</a> — 界面新闻 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7631057703687537203/" target="_blank">库克将卸任苹果公司CEO，特努斯9月接任</a> — 环球网 (toutiao.com)</li>
<li><a href="https://m.36kr.com/p/3775791350268675" target="_blank">苹果官宣换帅：库克卸任CEO，特努斯接任</a> — 36氪 (36kr.com)</li>
<li><a href="https://indexes.nasdaq.com/Index/Breakdown/NDX" target="_blank">NASDAQ-100指数数据</a> — 纳斯达克100指数官方数据，Nasdaq (nasdaq.com)</li>
</ul>

<h3>油价/大宗商品类</h3>
<ul class="ref-list">
<li><a href="http://m.toutiao.com/group/7631020092872016418/" target="_blank">国际油价涨超5.64%，4月21日24时油价或跌820元/吨</a> — 国内油价调整分析，今日头条 (toutiao.com)</li>
<li><a href="https://m.cngold.org/energy/xw10455515.html" target="_blank">今日布伦特原油期货价格最新行情走势</a> — 金投网 (cngold.org)</li>
</ul>

<h3>技术分析类</h3>
<ul class="ref-list">
<li><a href="http://m.toutiao.com/group/7630958481935204874/" target="_blank">美股收盘：三大指数小幅收跌 市场聚焦美伊紧张局势</a> — 财联社4月21日收盘分析 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7630959552531366450/" target="_blank">标普500指数止步五连涨 美伊和谈前景成疑</a> — 新浪财经 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7631100825183502854/" target="_blank">恒生指数4月21日盘中走势分析</a> — 今日头条 (toutiao.com)</li>
</ul>
</div>

<div class="disclaimer">
<strong>免责声明：</strong>本报告仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。报告中的观点和预测基于当前市场信息和分析师判断，可能随市场变化而调整。过往业绩不代表未来表现。
</div>

<div class="footer">
<p>跨市场重大事件与港股龙头策略研判 | 报告生成时间：{now_bj.strftime('%Y-%m-%d %H:%M:%S')}（北京时间）</p>
<p>数据来源：Longport API、36氪、财联社、新浪财经、东方财富网、Nasdaq官网等</p>
</div>

</div>
</body>
</html>"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Report generated: {filepath}")
print(f"Filename: {filename}")
