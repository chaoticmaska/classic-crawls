from utils.querys import getReportSet, patchwerkHatefulStrike
import matplotlib.pyplot as plt
from numpy import arange


def crawlReport(url: str):
    try:
        data = patchwerkHatefulStrike(url).get('reportData', {}).get('report', {}).get('events', {}).get('data', [])
    except:
        return []

    if not data:
        return []

    for event in data:
        if event.get('hitType', 0) not in (0, 1, 4, 7, 8):
            print(event.get('hitType'))
    '''
    {
        1: 'hit',
        4: 'block',
        7: 'dodge',
        8: 'parry'
    }
    '''
    return


if __name__ == '__main__':
    reportSet = getReportSet(1006, 1)
    dataset = []
    counter = 0
    bins_list = arange(28, 45, 0.1)
    for report in reportSet:
        crawlReport(report)
        '''
        dataset.extend(crawlReport(report))
        counter += 1
        print(counter, report)

        if counter % 1000 == 0:  # Return histogram after every N reports
            plt.hist(dataset, bins=bins_list)
            plt.show()
        '''
