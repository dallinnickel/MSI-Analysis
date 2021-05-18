import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
import math as math

championsGroup = pd.read_csv("ChampionsPicked.csv")
championsRumble = pd.read_csv("ChampionsPickedRumbleStage.csv")
frames = [championsGroup, championsRumble]
champions = pd.concat(frames)
released = pd.read_csv("ChampionReleaseDate.csv")
picks = champions[champions["Pick/Ban"] == "Pick"]
picks = picks.reset_index(drop=True)
picks = picks.drop(picks.index[range(650, 670)])
bans = champions[(champions["Pick/Ban"] == "Ban") & (champions["Champion"] != "None")]
allRunes = pd.read_csv("ChampionRunes.csv")
allRunes = allRunes.drop(allRunes.index[range(650, 653)])

# get a list of all champs picked
champs_picked = sorted(picks.Champion.unique())
# get a list of all banned champs
champs_banned = sorted(bans.Champion.unique())
# get a list of all champs picked or banned
champs_total = sorted(champions.Champion.unique())
# get a list of all teams
teams = sorted(picks.Team.unique())
# get a list of all runes which have been taken
uniqueRunes1 = sorted(allRunes.Rune1Reverse.unique())
uniqueRunes2 = sorted(allRunes.Rune2Reverse.unique())
uniqueRunes3 = sorted(allRunes.Rune3Reverse.unique())
uniqueRunes4 = sorted(allRunes.Rune4Reverse.unique())
uniqueRunes5 = sorted(allRunes.Rune5Reverse.unique())
uniqueRunesAll = sorted(list(set(uniqueRunes1) | set(uniqueRunes2) | set(uniqueRunes3) | set(uniqueRunes4) | set(uniqueRunes5)))
# get a list of all keystones which have been taken
keystones = sorted(allRunes.KeystoneReverse.unique())

print(champs_picked)

# track each champions win/loss
champWinLoss = OrderedDict()
for i in champs_picked:
    champWinLoss[i] = [0, 0]

for index, row in picks.iterrows():
    if row["GameResult"] == "Win":
        champWinLoss[row["Champion"]][0] += 1
    else:
        champWinLoss[row["Champion"]][1] += 1

# Track each champions win rate
champWinRate = OrderedDict()
for i in champs_picked:
    champWinRate[i] = champWinLoss[i][0] / (champWinLoss[i][0] + champWinLoss[i][1])

# The number of champs released each season
champsPerSeason = OrderedDict()
for i in range(12):
    champsPerSeason[i] = 0
for index, row in released.iterrows():
    champsPerSeason[row["Season"]] += 1

# The percent of total champs that were released each season
champsPercentPerSeason = OrderedDict()
for i in champsPerSeason.keys():
    champsPercentPerSeason[i] = champsPerSeason[i]/len(released.index)

# The number of champs picked per season at MSI
champsPickedPerSeason = OrderedDict()
for i in range(12):
    champsPickedPerSeason[i] = 0
for index, row in champions.iterrows():
    if row["Champion"] != "None":
        champsPickedPerSeason[released.loc[released["Champion"] == row["Champion"], "Season"].item()] += 1

# The percentage of champs picked per season at MSI
champsPercentPickedPerSeason = OrderedDict()
for i in champsPickedPerSeason.keys():
    champsPercentPickedPerSeason[i] = champsPickedPerSeason[i]/len(champions.index)

df = pd.DataFrame({
    "% of Champs Released Per Season": list(champsPercentPerSeason.values()),
    "% of Champs Picked at MSI Per Season": list(champsPercentPickedPerSeason.values())},
    index=range(12)
)
ax = df.plot.bar(title="% of Champs Released VS Picked at MSI per Season")
plt.show()

# The number of champs released each season
champsPerSeasonRework = OrderedDict()
for i in range(12):
    champsPerSeasonRework[i] = 0
for index, row in released.iterrows():
    champsPerSeasonRework[row["SeasonRework"]] += 1

# The percent of total champs that were released each season
champsPercentPerSeasonRework = OrderedDict()
for i in champsPerSeasonRework.keys():
    champsPercentPerSeasonRework[i] = champsPerSeasonRework[i]/len(released.index)

# The number of champs picked per season at MSI
champsPickedPerSeasonRework = OrderedDict()
for i in range(12):
    champsPickedPerSeasonRework[i] = 0
for index, row in champions.iterrows():
    if row["Champion"] != "None":
        champsPickedPerSeasonRework[released.loc[released["Champion"] == row["Champion"], "SeasonRework"].item()] += 1

# The percentage of champs picked per season at MSI
champsPercentPickedPerSeasonRework = OrderedDict()
for i in champsPickedPerSeasonRework.keys():
    champsPercentPickedPerSeasonRework[i] = champsPickedPerSeasonRework[i]/len(champions.index)

df = pd.DataFrame({
    "% of Champs Released/Reworked Per Season": list(champsPercentPerSeasonRework.values()),
    "% of Champs Picked at MSI Per Season Released/Reworked": list(champsPercentPickedPerSeasonRework.values())},
    index=range(12)
)
ax = df.plot.bar(ylim=(0, 0.3))
plt.show("% of Champs Released/Last Reworked VS Picked at MSI per Season")

# Find the win loss of champions per season
champsWinLossPerSeason = OrderedDict()
for i in range(12):
    champsWinLossPerSeason[i] = [0, 0]
for i in champWinLoss.keys():
    champsWinLossPerSeason[released.loc[released["Champion"] == i, "Season"].item()][0] += champWinLoss[i][0]
    champsWinLossPerSeason[released.loc[released["Champion"] == i, "Season"].item()][1] += champWinLoss[i][1]

# Find the winning ratio of champions per season
champsWinRatioPerSeason = OrderedDict()
for i in range(12):
    champsWinRatioPerSeason[i] = 0
for i in range(12):
    try:
        champsWinRatioPerSeason[i] = champsWinLossPerSeason[i][0]/(sum(champsWinLossPerSeason[i]))
    except ZeroDivisionError:
        champsWinRatioPerSeason[i] = champsWinLossPerSeason[i][0]/(sum(champsWinLossPerSeason[i]) + .000000000000001)

# Find the win loss of champions per season with rework
champsWinLossPerSeasonRework = OrderedDict()
for i in range(12):
    champsWinLossPerSeasonRework[i] = [0, 0]
for i in champWinLoss.keys():
    champsWinLossPerSeasonRework[released.loc[released["Champion"] == i, "SeasonRework"].item()][0] += champWinLoss[i][0]
    champsWinLossPerSeasonRework[released.loc[released["Champion"] == i, "SeasonRework"].item()][1] += champWinLoss[i][1]

# Find the winning ratio of champions per season with rework
champsWinRatioPerSeasonRework = OrderedDict()
for i in range(12):
    champsWinRatioPerSeasonRework[i] = 0
for i in range(12):
    try:
        champsWinRatioPerSeasonRework[i] = champsWinLossPerSeasonRework[i][0]/(sum(champsWinLossPerSeasonRework[i]))
    except ZeroDivisionError:
        champsWinRatioPerSeasonRework[i] = champsWinLossPerSeasonRework[i][0]/(sum(champsWinLossPerSeasonRework[i]) + .000000000000001)

df = pd.DataFrame({
    "Champs Per Season Win Rate": list(champsWinRatioPerSeason.values())},
    index=range(12)
)

# Graph
ax = df.plot.bar(title="Champs win rate at MSI per season released")
ax.get_legend().remove()
plt.show()

df = pd.DataFrame({
    "Champs Per Season Win Rate with Rework": list(champsWinRatioPerSeasonRework.values())},
    index=range(12)
)
ax = df.plot.bar(title="Champs win rate at MSI per season released/last reworked")
ax.get_legend().remove()
plt.show()

# Find the costs of champs
costOfChamps = OrderedDict()
costs = sorted(released.BlueEssence.unique())
for i in costs:
    costOfChamps[i] = 0
for index, row in released.iterrows():
    costOfChamps[row["BlueEssence"]] += 1

# Find the win loss of champions per season with rework
costOfChampsWinLoss = OrderedDict()
for i in costs:
    costOfChampsWinLoss[i] = [0, 0]
for i in champWinLoss.keys():
    costOfChampsWinLoss[released.loc[released["Champion"] == i, "BlueEssence"].item()][0] += champWinLoss[i][0]
    costOfChampsWinLoss[released.loc[released["Champion"] == i, "BlueEssence"].item()][1] += champWinLoss[i][1]

costOfChampsWinRatio = OrderedDict()
for i in costs:
    costOfChampsWinRatio[i] = 0
for i in costs:
    try:
        costOfChampsWinRatio[i] = costOfChampsWinLoss[i][0]/(sum(costOfChampsWinLoss[i]))
    except ZeroDivisionError:
        costOfChampsWinRatio[i] = costOfChampsWinLoss[i][0]/(sum(costOfChampsWinLoss[i]) + .000000000000001)

costOfChampsPercent = OrderedDict()
for i in costOfChamps.keys():
    costOfChampsPercent[i] = costOfChamps[i]/155

df = pd.DataFrame({
    "Win Rate of Champs per Cost": list(costOfChampsWinRatio.values())},
    index=costs
)
ax = df.plot.bar(ylim=(0, 0.7), title="Win Rate of Champs per Blue Essence Cost")
ax.get_legend().remove()
x_offset = -0.1
y_offset = 0.02
for p in ax.patches:
    b = p.get_bbox()
    val = "{:.2f}".format(b.y1 + b.y0)
    ax.annotate(val, ((b.x0 + b.x1)/2 + x_offset, b.y1 + y_offset), fontsize=8)
plt.show()


totalRunes = OrderedDict()
for i in uniqueRunesAll:
    totalRunes[i] = 0

for index, row in allRunes.iterrows():
    totalRunes[row["Rune1"]] += 1
    totalRunes[row["Rune2"]] += 1
    totalRunes[row["Rune3"]] += 1
    totalRunes[row["Rune4"]] += 1
    totalRunes[row["Rune5"]] += 1

df = pd.DataFrame({
    "Total Picks per rune": list(totalRunes.values())},
    index=uniqueRunesAll
)
ax = df.plot.bar(title="Total picks of each rune")
ax.get_legend().remove()
x_offset = -0.1
y_offset = 0.02
for p in ax.patches:
    b = p.get_bbox()
    val = "{:.2f}".format(b.y1 + b.y0)
    ax.annotate(val, ((b.x0 + b.x1)/2 + x_offset, b.y1 + y_offset), fontsize=8)
plt.show()

totalRunesPercent = OrderedDict()
for i in totalRunes.keys():
    totalRunesPercent[i] = totalRunes[i]/len(allRunes.index)

df = pd.DataFrame({
    "Total Picks per rune": list(totalRunesPercent.values())},
    index=uniqueRunesAll
)
ax = df.plot.bar(title="Total Picks Per Rune")
ax.get_legend().remove()
x_offset = -0.1
y_offset = 0.02
for p in ax.patches:
    b = p.get_bbox()
    val = "{:.2f}".format(b.y1 + b.y0)
    ax.annotate(val, ((b.x0 + b.x1)/2 + x_offset, b.y1 + y_offset), fontsize=8)
plt.show()

picks["Rune1"] = allRunes["Rune1Reverse"]
picks["Rune2"] = allRunes["Rune2Reverse"]
picks["Rune3"] = allRunes["Rune3Reverse"]
picks["Rune4"] = allRunes["Rune4Reverse"]
picks["Rune5"] = allRunes["Rune5Reverse"]

print(picks)

runeWinLoss = OrderedDict()
for i in uniqueRunesAll:
    runeWinLoss[i] = [0, 0]
for index, row in picks.iterrows():
    if row["GameResult"] == "Win":
        runeWinLoss[row["Rune1"]][0] += 1
        runeWinLoss[row["Rune2"]][0] += 1
        runeWinLoss[row["Rune3"]][0] += 1
        runeWinLoss[row["Rune4"]][0] += 1
        runeWinLoss[row["Rune5"]][0] += 1
    else:
        runeWinLoss[row["Rune1"]][1] += 1
        runeWinLoss[row["Rune2"]][1] += 1
        runeWinLoss[row["Rune3"]][1] += 1
        runeWinLoss[row["Rune4"]][1] += 1
        runeWinLoss[row["Rune5"]][1] += 1

runeWinPercent = OrderedDict()
for i in uniqueRunesAll:
    runeWinPercent[i] = 0
for i in runeWinLoss.keys():
    runeWinPercent[i] = runeWinLoss[i][0]/sum(runeWinLoss[i])

df = pd.DataFrame({
    "Win Rate Per Rune": list(runeWinPercent.values())},
    index=uniqueRunesAll
)
ax = df.plot.bar(title="Win Rates Per Rune")
ax.get_legend().remove()
x_offset = -0.1
y_offset = 0.02
for p in ax.patches:
    b = p.get_bbox()
    val = "{:.2f}".format(b.y1 + b.y0)
    ax.annotate(val, ((b.x0 + b.x1)/2 + x_offset, b.y1 + y_offset), fontsize=8)
plt.show()

runeWinPercent10Games = OrderedDict()
for i in runeWinLoss.keys():
    if sum(runeWinLoss[i]) > 10:
        runeWinPercent10Games[i] = runeWinPercent[i]

print(runeWinLoss)


df = pd.DataFrame({
    "Win Rate Per Rune": list(runeWinPercent10Games.values())},
    index=runeWinPercent10Games.keys()
)
ax = df.plot.bar(title="Win Rates Per Rune with > 10 Games played")
ax.get_legend().remove()
x_offset = -0.1
y_offset = 0.02
for p in ax.patches:
    b = p.get_bbox()
    val = "{:.2f}".format(b.y1 + b.y0)
    ax.annotate(val, ((b.x0 + b.x1)/2 + x_offset, b.y1 + y_offset), fontsize=8)
plt.show()

picks["Keystone"] = allRunes["KeystoneReverse"]

keystoneWinLoss = OrderedDict()
for i in keystones:
    keystoneWinLoss[i] = [0, 0]
for index, row in picks.iterrows():
    if row["GameResult"] == "Win":
        keystoneWinLoss[row["Keystone"]][0] += 1
    else:
        keystoneWinLoss[row["Keystone"]][1] += 1

keystoneWinPercent = OrderedDict()
for i in keystones:
    keystoneWinPercent[i] = 0
for i in keystoneWinLoss.keys():
    keystoneWinPercent[i] = keystoneWinLoss[i][0]/sum(keystoneWinLoss[i])

df = pd.DataFrame({
    "Win Rate Per Rune": list(keystoneWinPercent.values())},
    index=keystoneWinLoss.keys()
)
ax = df.plot.bar(title="Win Rates Per Keystone")
ax.get_legend().remove()
x_offset = -0.1
y_offset = 0.02
for p in ax.patches:
    b = p.get_bbox()
    val = "{:.2f}".format(b.y1 + b.y0)
    ax.annotate(val, ((b.x0 + b.x1)/2 + x_offset, b.y1 + y_offset), fontsize=8)
plt.show()

keystoneWinPercent10Games = OrderedDict()
for i in keystoneWinLoss.keys():
    if sum(keystoneWinLoss[i]) > 10:
        keystoneWinPercent10Games[i] = keystoneWinPercent[i]



df = pd.DataFrame({
    "Win Rate Per Keystone": list(keystoneWinPercent10Games.values())},
    index=keystoneWinPercent10Games.keys()
)
ax = df.plot.bar(title="Win Rates Per Keystone with > 10 Games played")
ax.get_legend().remove()
x_offset = -0.1
y_offset = 0.02
for p in ax.patches:
    b = p.get_bbox()
    val = "{:.2f}".format(b.y1 + b.y0)
    ax.annotate(val, ((b.x0 + b.x1)/2 + x_offset, b.y1 + y_offset), fontsize=8)
plt.show()

print(keystoneWinLoss)
