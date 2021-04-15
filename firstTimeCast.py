from utils.querys import getReportSet, firstCastTime
import matplotlib.pyplot as plt
from numpy import arange


def crawlReport(url: str, encounterID: int, abilityID: int):
    response = firstCastTime(url, encounterID, abilityID).get('reportData', {}).get('report', {})
    startTime = response.get('fights', [])
    event = response.get('events', {}).get('data', [])
    if not event or not startTime:
        return -1
    startTime = startTime[0].get('startTime')
    event = event[0].get('timestamp')
    return round((event - startTime) / 1000, 1)


if __name__ == '__main__':
    reportSet = getReportSet(1005, 10)
    dataset = []
    counter = 0
    bins_list = arange(10, 45, 1)
    for report in reportSet:
        dataset.append(crawlReport(report, 714, 26180))
        counter += 1
        print(counter, report)

        if counter % 500 == 0:  # Return histogram after every N reports
            plt.hist(dataset, bins=bins_list)
            plt.show()
