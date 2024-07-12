from functions import *

if __name__ == "__main__":
    ticks = fetchTicks()
    ticksNumber = len(ticks)
    print("NUMBER OF TICKS: " + str(ticksNumber))
    interval = selectTimeframe()

    for tick in ticks:
        analyzeCurrency(tick, interval)

    showResults()
