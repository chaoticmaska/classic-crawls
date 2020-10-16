from utils.querys import getReportSet, twinEmpEvents
import matplotlib.pyplot as plt
from numpy import arange


def crawlReport(url: str):
    try:
        data = twinEmpEvents(url).get('reportData', {}).get('report', {}).get('events', {}).get('data', [])
    except:
        return []

    if not data:
        return []
    # Leave only one emperor and applybuff events only
    sourceID = data[0].get('sourceID')
    data = list(filter(lambda e: e.get('sourceID') == sourceID and e.get('type') == 'applybuff', data))

    rangeList = []
    for i in range(len(data) - 1):
        tpRange = round((data[i + 1].get('timestamp') - data[i].get('timestamp')) / 1000, 1)
        if tpRange < 25 or tpRange > 50:  # Skip obv wrong values
            continue
        rangeList.append(tpRange)
    return rangeList


if __name__ == '__main__':
    reportSet = getReportSet(1005, 2)
    dataset = []
    counter = 0
    bins_list = arange(28, 45, 0.1)
    for report in reportSet:
        dataset.extend(crawlReport(report))
        counter += 1
        print(counter, report)

        if counter % 1000 == 0:  # Return histogram after every N reports
            plt.hist(dataset, bins=bins_list)
            plt.show()
