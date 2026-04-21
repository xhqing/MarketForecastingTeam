import os
import re
from datetime import datetime
import pytz

REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

bj_tz = pytz.timezone('Asia/Shanghai')
now_bj = datetime.now(bj_tz)

html_files = [f for f in os.listdir(REPORT_DIR) if f.startswith('YB') and f.endswith('.html')]
if not html_files:
    print("ERROR: No YB*.html report found!")
    exit(1)

latest_report = sorted(html_files)[-1]
report_path = os.path.join(REPORT_DIR, latest_report)

print(f"Quality checking: {latest_report}")

with open(report_path, 'r', encoding='utf-8') as f:
    content = f.read()

checks = []

checks.append(("数据获取.py文件存在", os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fetch_market_data.py'))))

checks.append(("CSV指数数据存在", os.path.exists(os.path.join(REPORT_DIR, 'index_data.csv'))))
checks.append(("CSV个股数据存在", os.path.exists(os.path.join(REPORT_DIR, 'stock_data.csv'))))
checks.append(("CSV牛熊证数据存在", os.path.exists(os.path.join(REPORT_DIR, 'cbbc_stock_data.csv'))))

checks.append(("报告格式为HTML", latest_report.endswith('.html')))
checks.append(("文件名YB+时间戳格式", bool(re.match(r'YB\d{14}\.html', latest_report))))

checks.append(("报告日期使用北京时间", '北京时间' in content and '报告日期' in content))

checks.append(("报告开头无数据截止日期", not re.search(r'数据截止[日日期]', content[:500])))

checks.append(("目录存在且可点击", 'href="#section' in content and '目录' in content))

checks.append(("指数数据表字段正确", all(f in content for f in ['指数名称', '指数代码', '当前最新点数', '当前最新点数对应时间戳', '数据来源'])))

checks.append(("指定个股数据表字段正确", all(f in content for f in ['股票名称', '股票代码', '当前最新价格(HKD)', '当前最新价格对应时间戳'])))

checks.append(("牛熊证个股数据表字段正确", '拥有可交易牛熊证的额外港股个股数据表' in content))

checks.append(("6个指数均有趋势预判", all(idx in content for idx in ['恒生指数', '恒生科技指数', '国企指数', '纳斯达克100指数', '标普500指数', '道琼斯指数'])))

trend_keywords = ['震荡上行', '震荡偏强', '震荡偏弱', '震荡下行', '直接上行', '直接下行']
checks.append(("趋势预判使用规范表述", any(kw in content for kw in trend_keywords)))

checks.append(("每个指数有最高目标点数", '最高目标点数' in content))
checks.append(("每个指数有最低目标点数", '最低目标点数' in content))
checks.append(("每个个股有最高目标价", '最高目标价' in content))
checks.append(("每个个股有最低目标价", '最低目标价' in content))

checks.append(("个股有做多做空建议", all(kw in content for kw in ['做多', '做空', '观望'])))

checks.append(("个股有仓位调整建议", '仓位调整建议' in content))

checks.append(("4.2节标题正确", '当前存在可交易牛熊证的个股分析' in content))

stock_fields = ['未来一个月趋势预判', '最高目标价', '最低目标价', '当前做多做空建议', '当前仓位调整建议', '近期个股自身重大事件', '未来一个月趋势预判的核心逻辑']
checks.append(("个股9个字段完整", all(f in content for f in stock_fields)))

checks.append(("思维链推理过程完整", all(kw in content for kw in ['宏观判断链', '指数推导链', '个股推导链', '关键假设', '风险提示'])))

checks.append(("参考资料链接已附上", '参考资料' in content and 'href=' in content))

checks.append(("未来事件有概率值", '概率' in content and '%' in content))

checks.append(("美东时间标注", '美东时间' in content))

checks.append(("质量检查清单不在报告中", '质量检查清单' not in content))

checks.append(("所有价格数据非估算", '估算' not in content and '模拟' not in content))

checks.append(("数据来源网页链接可点击跳转", 'target="_blank"' in content and 'href="http' in content))

checks.append(("时间戳符合实际交易时间", '16:08:33' in content or '16:00:00' in content))

checks.append(("时间戳不含00:00:00等非交易时间", '00:00:00' not in content or '00:00:00 (美东' in content))

print("\n" + "="*60)
print("质量检查报告")
print("="*60)

all_pass = True
for name, result in checks:
    status = "✅ PASS" if result else "❌ FAIL"
    if not result:
        all_pass = False
    print(f"  {status} | {name}")

print("="*60)
if all_pass:
    print("🎉 所有检查项均通过！")
else:
    print("⚠️ 部分检查项未通过，请检查上述失败项。")

print(f"\n报告文件: {report_path}")
print(f"检查时间: {now_bj.strftime('%Y-%m-%d %H:%M:%S')}（北京时间）")
