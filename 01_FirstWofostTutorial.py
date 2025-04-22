import pcse.start_wofost as start_wofost
import matplotlib.pyplot as plt
import pandas as pd

wofostPP = start_wofost(mode="pp")
wofostPP.run_till_terminate()
output = wofostPP.get_output()
dfPP = pd.DataFrame(output).set_index("day")

fig, axs = plt.subplots(nrows = 1, ncols = 2, figsize=(16,8))
dfPP["LAI"].plot(ax=axs[0], label="LAI", color='k')
dfPP["TAGP"].plot(ax=axs[1], label="Total biomass")
dfPP["TWSO"].plot(ax=axs[1], label="Yield")
axs[0].set_title("Leaf Area Index")
axs[1].set_title("Crop biomass")
r = axs[1].legend()
fig.autofmt_xdate()
plt.show()
print(dfPP.head().to_string())
print("...")
print(dfPP.tail().to_string())